import os
import time
import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, session, jsonify, abort
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from dotenv import load_dotenv
import logging
import ssl
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import json
import random
import requests

# Load environment variables from .env file if it exists
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'maplewood_secret_key_fixed')

# Setup Logging
logging.basicConfig(
    filename='app.log',
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s: %(message)s'
)
logging.info("--- Server Starting ---")

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Database connection helper
def get_db_connection():
    return mysql.connector.connect(
        host=os.environ.get('DB_HOST', '127.0.0.1'),
        user=os.environ.get('DB_USER', 'root'),
        password=os.environ.get('DB_PASS', ''),
        database=os.environ.get('DB_NAME', 'maplewood_db')
    )

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- Context Processor for Global Settings ---
@app.context_processor
def inject_settings():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT setting_key, setting_value FROM settings")
        db_settings = cursor.fetchall()
        cursor.close()
        conn.close()
        
        settings_dict = {s['setting_key']: s['setting_value'] for s in db_settings}
        return dict(settings=settings_dict)
    except:
        return dict(settings={})

def render_stars(rating):
    full_stars = int(rating)
    half_star = 1 if (rating - full_stars) >= 0.5 else 0
    empty_stars = 5 - full_stars - half_star
    return {'full': full_stars, 'half': half_star, 'empty': empty_stars}

def time_ago(timestamp):
    import time
    diff = int(time.time()) - int(timestamp)
    if diff < 60: return 'Just now'
    if diff < 3600: return f'{diff // 60}m ago'
    if diff < 86400: return f'{diff // 3600}h ago'
    if diff < 2592000: return f'{diff // 86400}d ago'
    import datetime
    return datetime.datetime.fromtimestamp(timestamp).strftime('%b %j, %Y')

def nl2br(value):
    from markupsafe import Markup, escape
    if not value: return ''
    return Markup(str(escape(value)).replace('\n', '<br>\n'))

app.jinja_env.filters['stars'] = render_stars
app.jinja_env.filters['timeago'] = time_ago
app.jinja_env.filters['nl2br'] = nl2br

# --- Auth Middleware ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('admin_dashboard'))
        return f(*args, **kwargs)
    return decorated_function

# --- Frontend Routes ---
def sync_menu_from_json():
    local_path = os.path.join(BASE_DIR, 'menu_data.json')
    old_windows_path = r'/root/maplewoodburgers/'
    
    SCRAP_FILE = os.environ.get('MENU_DATA_PATH', local_path if os.path.exists(local_path) else old_windows_path)
    if not os.path.exists(SCRAP_FILE):
        return False, f"Scrap file not found at: {SCRAP_FILE}"

    with open(SCRAP_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if 'result' not in data or 'pageContext' not in data['result']:
        return False, "Invalid JSON structure"

    menu_data = data['result']['pageContext']['menuData']
    business_id = data['result']['pageContext']['business']['id']
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        for cat in menu_data:
            cursor.execute("""
                INSERT INTO menu_categories (id, name, description, display_order)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE name=%s, description=%s, display_order=%s
            """, (cat['id'], cat['name'], cat.get('description', ''), cat.get('index', 0), 
                  cat['name'], cat.get('description', ''), cat.get('index', 0)))
            
            for item in cat.get('items', []):
                price = item.get('price', 0)
                try:
                    if isinstance(price, str):
                        price = float(price.replace('$', '').replace(',', ''))
                except: price = 0
                    
                image_url = None
                if item.get('imageKey'):
                    image_url = f"http://d2jv14lidw8y7p.cloudfront.net/getMenuItemImage/businessId={business_id}&menuItemId={item['id']}"
                    
                cursor.execute("""
                    INSERT INTO menu_items (id, category_id, name, description, price, image_url, json_data)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE 
                        category_id=%s, name=%s, description=%s, price=%s, image_url=%s, json_data=%s
                """, (item['id'], cat['id'], item['name'], item.get('description', ''), price, image_url, json.dumps(item),
                      cat['id'], item['name'], item.get('description', ''), price, image_url, json.dumps(item)))
        
        conn.commit()
        cursor.close()
        conn.close()
        return True, "Menu synced successfully"
    except Exception as e:
        return False, str(e)

@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/reviews')
@app.route('/reviews.html')
def reviews_page():
    try:
        # Use main database configuration
        conn = mysql.connector.connect(
            host=os.environ.get('DB_HOST', '127.0.0.1'),
            user=os.environ.get('DB_USER', 'root'),
            password=os.environ.get('DB_PASS', ''),
            database=os.environ.get('DB_NAME', 'maplewood_db')
        )
        cursor = conn.cursor(dictionary=True)
        
        locations = {'sulphur': 'Sulphur', 'lake-charles': 'Lake Charles', 'moss-bluff': 'Moss Bluff'}
        location_data = {}

        for slug, name in locations.items():
            cursor.execute("SELECT * FROM mpl_grp_google_place WHERE name LIKE %s", (f'%{name}%',))
            place = cursor.fetchone()
            if place:
                cursor.execute("SELECT * FROM mpl_grp_google_review WHERE google_place_id = %s AND hide != '1' ORDER BY time DESC LIMIT 10", (place['id'],))
                location_data[slug] = {'place': place, 'reviews': cursor.fetchall()}
            else:
                location_data[slug] = {'place': None, 'reviews': []}
        
        cursor.close()
        conn.close()
        return render_template('reviews.html', location_data=location_data)
    except Exception as e:
        return f"Database Error: {str(e)}"

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'inc', 'assets', 'img'),
                               'Maplewood-Burgers-Logo-Horiz.svg', mimetype='image/svg+xml')

@app.route('/inc/<path:filename>')
def serve_inc(filename):
    return send_from_directory(os.path.join(app.root_path, 'inc'), filename)

# Serving Uploaded Files Publicly
@app.route('/uploads/<path:filename>')
def serve_uploads(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'svg'}
def allowed_image(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS
@app.route('/full-menu')
@app.route('/full-menu.html')
def full_menu_page():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM menu_categories ORDER BY display_order")
        categories = cursor.fetchall()
        for cat in categories:
            cursor.execute("SELECT * FROM menu_items WHERE category_id = %s", (cat['id'],))
            cat['menu_items'] = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('full-menu.html', categories=categories)
    except Exception as e:
        app.logger.error(f"Error serving full-menu: {str(e)}")
        return f"Menu Error: {str(e)}", 500

@app.route('/blogs')
@app.route('/blogs.html')
def blogs_page():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM blogs ORDER BY created_at DESC")
        blogs = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('blogs.html', blogs=blogs)
    except Exception as e:
        app.logger.error(f"Error loading blogs listing: {e}")
        return render_template('blogs.html', blogs=[])

@app.route('/<page>')
def serve_page(page):
    clean_slug = page[:-5] if page.endswith('.html') else page
    
    # Block direct static loading of administrative and login templates
    prohibited_pages = {
        'admin', 'admin-backup', 'blogs_admin', 'blog_form',
        'loyalty_admin', 'reviews_admin', 'settings', 'login'
    }
    if clean_slug in prohibited_pages:
        abort(404)
        
    # Check for dynamic blog post slug first
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM blogs WHERE slug = %s", (clean_slug,))
        blog = cursor.fetchone()
        cursor.close()
        conn.close()
        if blog:
            return render_template('blog_detail.html', blog=blog)
    except Exception as e:
        app.logger.error(f"Error looking up dynamic blog post '{clean_slug}': {e}")

    # Fallback to static template
    if not page.endswith('.html'):
        page += '.html'
    
    from jinja2.exceptions import TemplateNotFound
    try:
        return render_template(page)
    except TemplateNotFound:
        abort(404)
    except Exception as e:
        app.logger.error(f"Template rendering error for '{page}': {e}")
        # Re-raise standard rendering errors to display a 500 error instead of masking as a 404
        raise e

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# --- API / Form Routes ---

@app.route('/api/captcha', methods=['GET'])
def generate_captcha():
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    session['captcha_answer'] = str(num1 + num2)
    response = jsonify({"question": f"What is {num1} + {num2}?"})
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/loyalty-signup', methods=['POST'])
def loyalty_signup():
    try:
        fullname = request.form.get('fullname')
        phonenumber = request.form.get('phonenumber')
        email = request.form.get('email')
        birthdate = request.form.get('birthdate')
        captcha_answer = request.form.get('captcha_answer')
        
        app.logger.debug(f"Loyalty Signup POST received: fullname='{fullname}', phonenumber='{phonenumber}', email='{email}', birthdate='{birthdate}'")
        
        # CAPTCHA validation
        if 'captcha_answer' not in session or not captcha_answer or session['captcha_answer'] != str(captcha_answer).strip():
            return jsonify({"status": "error", "message": "Incorrect math CAPTCHA answer. Please try again."}), 400
        # Clear captcha to prevent replay
        session.pop('captcha_answer', None)
        
        # Simple validation
        if not fullname or not phonenumber or not email:
            app.logger.debug("Validation failed: Missing required fields")
            return jsonify({"status": "error", "message": "Missing required fields"}), 400
            
        # Backend Phone Validation (extract digits only, must be 10 digits)
        import re
        clean_phone = re.sub(r'[^0-9]', '', phonenumber)
        if len(clean_phone) != 10:
            app.logger.debug(f"Validation failed: Phone number '{phonenumber}' (clean: '{clean_phone}') is not 10 digits")
            return jsonify({"status": "error", "message": "Phone number must be exactly 10 digits."}), 400
            
        # Backend Email Validation
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            app.logger.debug(f"Validation failed: Email '{email}' does not match regex")
            return jsonify({"status": "error", "message": "Please enter a valid email address."}), 400
            
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
        INSERT INTO loyalty_signups (fullname, phonenumber, email, birthdate)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (fullname, clean_phone, email, birthdate if birthdate else None))
        conn.commit()
        cursor.close()
        conn.close()
        
        app.logger.info(f"Loyalty signup saved successfully for '{fullname}'")
        return jsonify({"status": "success", "message": "Saved locally successfully"})
    except Exception as e:
        app.logger.error(f"Error saving loyalty signup: {str(e)}")
        print(f"Error saving loyalty signup: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/apply', methods=['POST'])
def apply():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    contact_number = request.form.get('contact_number')
    email = request.form.get('email')
    experience = request.form.get('experience')
    captcha_answer = request.form.get('captcha_answer')
    
    # CAPTCHA validation
    if 'captcha_answer' not in session or not captcha_answer or session['captcha_answer'] != str(captcha_answer).strip():
        return jsonify({"status": "error", "message": "Incorrect math CAPTCHA answer. Please try again."}), 400
    # Clear captcha to prevent replay
    session.pop('captcha_answer', None)
    
    # Backend Validation
    import re
    if not first_name or not last_name or not contact_number or not email:
        return jsonify({"status": "error", "message": "First name, last name, contact number, and email are required."}), 400

    if not re.match(r'^[a-zA-Z\s]+$', first_name):
        return jsonify({"status": "error", "message": "First name should only contain letters."}), 400

    if not re.match(r'^[a-zA-Z\s]+$', last_name):
        return jsonify({"status": "error", "message": "Last name should only contain letters."}), 400

    if not re.match(r'^\d+$', contact_number):
        return jsonify({"status": "error", "message": "Contact number should only contain numbers."}), 400

    if len(contact_number) != 10:
        return jsonify({"status": "error", "message": "Contact number must be exactly 10 digits."}), 400

    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, email):
        return jsonify({"status": "error", "message": "Please enter a valid email address."}), 400

    clean_phone = contact_number
    formatted_phone = f"({clean_phone[:3]}) {clean_phone[3:6]}-{clean_phone[6:]}"
    
    locations = request.form.getlist('location')
    positions = request.form.getlist('position')
    
    location_str = ", ".join(locations)
    position_str = ", ".join(positions)
    
    resume_path = ""
    if 'resume' in request.files:
        file = request.files['resume']
        if file and file.filename != '' and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = f"{int(time.time())}_{filename}"
            try:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                resume_path = filename
            except Exception as e:
                return jsonify({"status": "error", "message": f"Upload Error: {str(e)}"}), 500

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
        INSERT INTO applications (first_name, last_name, contact_number, email, experience, location, position, resume_path)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (first_name, last_name, clean_phone, email, experience, location_str, position_str, resume_path))
        conn.commit()
        logging.info(f"New application saved to DB: {first_name} {last_name}")

        # Send Email Notification
        email_debug_log = []
        try:
            # Fetch SMTP settings
            cursor.execute("SELECT setting_key, setting_value FROM settings WHERE setting_key LIKE 'smtp_%'")
            smtp_settings = {s[0]: s[1] for s in cursor.fetchall()}
            
            if smtp_settings.get('smtp_user') and smtp_settings.get('smtp_password'):
                email_debug_log.append("STEP: SMTP Settings retrieved.")
                logging.debug("SMTP settings loaded from DB.")
                msg = MIMEMultipart()
                msg['From'] = f"Maplewood Burgers <{smtp_settings.get('smtp_from_email')}>"
                msg['To'] = smtp_settings.get('smtp_to_email', 'sanjayconfido@gmail.com')
                msg['Reply-To'] = smtp_settings.get('smtp_reply_to', 'confidosoftsolutionpvtltd@gmail.com')
                msg['Subject'] = f"New Job Application: {first_name} {last_name}"

                template = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <style>
                        .container {{ font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; max-width: 600px; margin: 0 auto; border: 1px solid #e0e0e0; border-radius: 8px; overflow: hidden; }}
                        .header {{ background-color: #c92f2f; color: #ffffff; padding: 25px; text-align: center; }}
                        .content {{ padding: 30px; line-height: 1.6; color: #333; }}
                        .field {{ margin-bottom: 15px; border-bottom: 1px solid #f0f0f0; padding-bottom: 8px; }}
                        .label {{ font-weight: bold; color: #c92f2f; display: inline-block; width: 140px; }}
                        .footer {{ background-color: #f9f9f9; color: #777; padding: 15px; text-align: center; font-size: 12px; }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <div class="header">
                            <h2 style="margin:0;">New Candidate Application</h2>
                        </div>
                        <div class="content">
                            <div class="field"><span class="label">Full Name:</span> {first_name} {last_name}</div>
                            <div class="field"><span class="label">Phone:</span> {formatted_phone}</div>
                            <div class="field"><span class="label">Email:</span> {email if email else 'N/A'}</div>
                            <div class="field"><span class="label">Position(s):</span> {position_str}</div>
                            <div class="field"><span class="label">Location(s):</span> {location_str}</div>
                            <div class="field" style="border:none;">
                                <span class="label" style="display:block; margin-bottom:10px;">Experience Summary:</span>
                                <div style="background:#fcfcfc; padding:15px; border-radius:5px; border-left:4px solid #c92f2f;">{experience}</div>
                            </div>
                        </div>
                        <div class="footer">
                            This is an automated notification from the Maplewood Burgers Careers Portal.
                        </div>
                    </div>
                </body>
                </html>
                """
                msg.attach(MIMEText(template, 'html'))
                
                # Attach Resume if exists
                if resume_path:
                    try:
                        file_path = os.path.join(app.config['UPLOAD_FOLDER'], resume_path)
                        email_debug_log.append(f"STEP: Attaching resume from {file_path}")
                        with open(file_path, "rb") as attachment:
                            part = MIMEBase("application", "octet-stream")
                            part.set_payload(attachment.read())
                            encoders.encode_base64(part)
                            part.add_header("Content-Disposition", f"attachment; filename={resume_path}")
                            msg.attach(part)
                            email_debug_log.append("STEP: Resume attached successfully.")
                    except Exception as e:
                        email_debug_log.append(f"WARNING: Failed to attach resume: {e}")
                        logging.error(f"Attachment Error: {e}")

                # Send via SMTP
                # NOTE: Switching to Port 465 (SSL) to avoid [Errno 5] I/O errors on Windows
                host = smtp_settings.get('smtp_host', 'smtp.gmail.com')
                port = 465 # Forcing 465 for SSL stability
                user = smtp_settings.get('smtp_user')
                pwd = smtp_settings.get('smtp_password')

                email_debug_log.append(f"STEP: Connecting via SSL to {host}:{port}")
                logging.info(f"Attempting SMTP_SSL connection to {host}:{port} with explicit context")
                
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(host, port, context=context, timeout=15) as server:
                    email_debug_log.append("STEP: SSL Handshake successful. Logging in...")
                    logging.debug("SMTP_SSL established with context.")
                    server.login(user, pwd)
                    email_debug_log.append("STEP: Login successful. Sending message...")
                    logging.info("SMTP login successful. Sending email...")
                    server.send_message(msg)
                    email_debug_log.append("STEP: EMAIL SENT SUCCESSFULLY.")
                    logging.info(f"Email sent successfully to sanjayconfido@gmail.com")
                    email_status = "sent"
            else:
                email_debug_log.append("ERROR: SMTP User/Pass missing in settings.")
                email_status = "missing_settings"

        except Exception as email_err:
            email_status = "failed"
            err_msg = str(email_err)
            email_debug_log.append(f"CRITICAL SMTP ERROR: {err_msg}")
            logging.error(f"SMTP FAILURE: {err_msg}")
            import traceback
            logging.error(traceback.format_exc())

        cursor.close()
        conn.close()
        
        response_msg = "Application submitted successfully!"

        return jsonify({
            "status": "success" if email_status == "sent" else "partial_success", 
            "message": response_msg,
            "email_debug": email_debug_log
        })
    except Exception as e:
        import traceback
        print(f"CRITICAL ERROR in /apply: {traceback.format_exc()}")
        return jsonify({"status": "error", "message": f"Application Error: {str(e)}"}), 500

# --- Admin Auth Routes ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Public /login route disabled and returned 404
    abort(404)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('admin_dashboard'))

# --- Admin Routes ---

@app.route('/access-panel', methods=['GET', 'POST'])
def admin_dashboard():
    # Handle authentication locally to serve login template on same URL /access-panel
    if 'logged_in' not in session:
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            
            try:
                conn = get_db_connection()
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
                user = cursor.fetchone()
                cursor.close()
                conn.close()
                
                if user and check_password_hash(user['password'], password):
                    session['logged_in'] = True
                    session['username'] = user['username']
                    return redirect(url_for('admin_dashboard'))
                else:
                    return render_template('login.html', error="Invalid username or password")
            except Exception as e:
                return f"An error occurred: {str(e)}"
        
        # Render the login template on the current /access-panel URL for GET requests
        return render_template('login.html')
    try:
        # Pagination Settings
        page = request.args.get('page', 1, type=int)
        per_page = 10
        offset = (page - 1) * per_page

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Get total count for pagination
        cursor.execute("SELECT COUNT(*) as count FROM applications")
        total_apps = cursor.fetchone()['count']
        total_pages = (total_apps + per_page - 1) // per_page

        # Get paginated applications
        query = "SELECT * FROM applications ORDER BY submitted_at DESC LIMIT %s OFFSET %s"
        cursor.execute(query, (per_page, offset))
        applications = cursor.fetchall()
        
        # Stats
        cursor.execute("SELECT COUNT(*) as count FROM applications WHERE DATE(submitted_at) = CURDATE()")
        today_apps = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM loyalty_signups")
        total_loyalty = cursor.fetchone()['count']
        
        cursor.execute("SELECT * FROM settings")
        current_settings = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return render_template('admin.html', 
                               applications=applications, 
                               total_apps=total_apps, 
                               today_apps=today_apps,
                               total_loyalty=total_loyalty,
                               current_settings=current_settings,
                               current_page=page,
                               total_pages=total_pages)
    except Exception as e:
        import traceback
        logging.error(f"Admin Dashboard Error: {traceback.format_exc()}")
        return f"An error occurred: {str(e)}"

@app.route('/access-panel/blogs')
@login_required
def admin_blogs():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM blogs ORDER BY created_at DESC")
        blogs = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('blogs_admin.html', blogs=blogs)
    except Exception as e:
        app.logger.error(f"Error displaying admin blogs: {e}")
        return f"Database Error: {str(e)}"

@app.route('/access-panel/blogs/new', methods=['GET', 'POST'])
@login_required
def admin_blog_new():
    import datetime
    today_str = datetime.datetime.now().strftime('%B %d, %Y')
    
    if request.method == 'POST':
        title = request.form.get('title')
        slug = request.form.get('slug')
        published_date = request.form.get('published_date', today_str)
        excerpt = request.form.get('excerpt')
        meta_description = request.form.get('meta_description')
        content = request.form.get('content')
        
        # Handle image file upload
        image_url = 'inc/assets/img/The-Hangover-Burger.webp'
        if 'image_file' in request.files:
            file = request.files['image_file']
            if file and file.filename != '':
                if allowed_image(file.filename):
                    filename = secure_filename(file.filename)
                    filename = f"{int(time.time())}_{filename}"
                    try:
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                        image_url = f"uploads/{filename}"
                    except Exception as e:
                        flash(f"Upload Error: {str(e)}", "danger")
                        return render_template('blog_form.html', is_edit=False, today_str=today_str, blog=request.form)
                else:
                    flash("Invalid image file format. Allowed formats: PNG, JPG, JPEG, GIF, WEBP, SVG.", "danger")
                    return render_template('blog_form.html', is_edit=False, today_str=today_str, blog=request.form)
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO blogs (title, slug, published_date, image_url, excerpt, meta_description, content)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (title, slug, published_date, image_url, excerpt, meta_description, content))
            conn.commit()
            cursor.close()
            conn.close()
            flash("Blog post created successfully!", "success")
            return redirect(url_for('admin_blogs'))
        except Exception as e:
            flash(f"Error creating blog post: {str(e)}", "danger")
            return render_template('blog_form.html', is_edit=False, today_str=today_str, blog=request.form)
            
    return render_template('blog_form.html', is_edit=False, today_str=today_str, blog=None)

@app.route('/access-panel/blogs/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_blog_edit(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM blogs WHERE id = %s", (id,))
        blog = cursor.fetchone()
        cursor.close()
        conn.close()
    except Exception as e:
        flash(f"Error fetching blog post: {str(e)}", "danger")
        return redirect(url_for('admin_blogs'))
        
    if not blog:
        flash("Blog post not found.", "danger")
        return redirect(url_for('admin_blogs'))
        
    if request.method == 'POST':
        title = request.form.get('title')
        slug = request.form.get('slug')
        published_date = request.form.get('published_date')
        excerpt = request.form.get('excerpt')
        meta_description = request.form.get('meta_description')
        content = request.form.get('content')
        
        # Handle image file upload
        image_url = request.form.get('existing_image_url')
        if 'image_file' in request.files:
            file = request.files['image_file']
            if file and file.filename != '':
                if allowed_image(file.filename):
                    filename = secure_filename(file.filename)
                    filename = f"{int(time.time())}_{filename}"
                    try:
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                        image_url = f"uploads/{filename}"
                    except Exception as e:
                        flash(f"Upload Error: {str(e)}", "danger")
                        return render_template('blog_form.html', is_edit=True, blog=request.form)
                else:
                    flash("Invalid image file format. Allowed formats: PNG, JPG, JPEG, GIF, WEBP, SVG.", "danger")
                    return render_template('blog_form.html', is_edit=True, blog=request.form)
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE blogs 
                SET title = %s, slug = %s, published_date = %s, image_url = %s, excerpt = %s, meta_description = %s, content = %s
                WHERE id = %s
            """, (title, slug, published_date, image_url, excerpt, meta_description, content, id))
            conn.commit()
            cursor.close()
            conn.close()
            flash("Blog post updated successfully!", "success")
            return redirect(url_for('admin_blogs'))
        except Exception as e:
            flash(f"Error updating blog post: {str(e)}", "danger")
            return render_template('blog_form.html', is_edit=True, blog=request.form)
            
    return render_template('blog_form.html', is_edit=True, blog=blog)

@app.route('/access-panel/blogs/delete/<int:id>', methods=['POST'])
@login_required
def admin_blog_delete(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM blogs WHERE id = %s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        flash("Blog post deleted successfully!", "success")
    except Exception as e:
        flash(f"Error deleting blog post: {str(e)}", "danger")
        
    return redirect(url_for('admin_blogs'))

@app.route('/access-panel/loyalty')
@login_required
def admin_loyalty():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM loyalty_signups ORDER BY created_at DESC")
        signups = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('loyalty_admin.html', signups=signups)
    except Exception as e:
        return f"An error occurred: {str(e)}"

@app.route('/access-panel/loyalty/delete/<int:id>', methods=['POST'])
@login_required
def admin_delete_loyalty(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM loyalty_signups WHERE id = %s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        flash("Loyalty signup deleted successfully!", "success")
    except Exception as e:
        flash(f"Error deleting loyalty signup: {str(e)}", "danger")
    return redirect(url_for('admin_loyalty'))

@app.route('/access-panel/settings', methods=['GET', 'POST'])
@login_required
def admin_settings():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        if request.method == 'POST':
            for key, value in request.form.items():
                query = "UPDATE settings SET setting_value = %s WHERE setting_key = %s"
                cursor.execute(query, (value, key))
            conn.commit()
            flash("Settings updated successfully!")
            return redirect(url_for('admin_settings'))
            
        cursor.execute("SELECT * FROM settings")
        current_settings = cursor.fetchall()
        
        # Fetch the current admin email to render in recovery settings
        cursor.execute("SELECT email FROM users WHERE username = %s", (session['username'],))
        user_data = cursor.fetchone()
        admin_email = user_data['email'] if user_data and user_data['email'] else ''
        
        cursor.close()
        conn.close()
        return render_template('settings.html', current_settings=current_settings, admin_email=admin_email)
    except Exception as e:
        return f"An error occurred: {str(e)}"

@app.route('/access-panel/change-password', methods=['POST'])
@login_required
def admin_change_password():
    current_password = request.form.get('current_password', '')
    new_password = request.form.get('new_password', '')
    confirm_password = request.form.get('confirm_password', '')
    
    if not current_password or not new_password or not confirm_password:
        flash("All password fields are required.", "danger")
        return redirect(url_for('admin_settings'))
    
    if new_password != confirm_password:
        flash("New password and confirmation do not match.", "danger")
        return redirect(url_for('admin_settings'))
    
    if len(new_password) < 6:
        flash("New password must be at least 6 characters long.", "danger")
        return redirect(url_for('admin_settings'))
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (session['username'],))
        user = cursor.fetchone()
        
        if not user or not check_password_hash(user['password'], current_password):
            cursor.close()
            conn.close()
            flash("Current password is incorrect.", "danger")
            return redirect(url_for('admin_settings'))
        
        hashed_new = generate_password_hash(new_password)
        cursor.execute("UPDATE users SET password = %s WHERE username = %s", (hashed_new, session['username']))
        conn.commit()
        cursor.close()
        conn.close()
        
        flash("Password updated successfully!", "success")
    except Exception as e:
        logging.error(f"Change password error: {str(e)}")
        flash(f"Error changing password: {str(e)}", "danger")
    
    return redirect(url_for('admin_settings'))

@app.route('/access-panel/change-email', methods=['POST'])
@login_required
def admin_change_email():
    new_email = request.form.get('admin_email', '').strip()
    if not new_email:
        flash("Email field is required.", "danger")
        return redirect(url_for('admin_settings'))
        
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET email = %s WHERE username = %s", (new_email, session['username']))
        conn.commit()
        cursor.close()
        conn.close()
        flash("Admin email updated successfully!", "success")
    except Exception as e:
        logging.error(f"Change email error: {str(e)}")
        flash(f"Error changing email: {str(e)}", "danger")
        
    return redirect(url_for('admin_settings'))

@app.route('/access-panel/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('recovery_email', '').strip()
        if not email:
            return render_template('forgot_password.html', error="Email field is required.")
            
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            
            if user:
                import secrets
                import time
                
                # Generate time-limited reset token
                token = secrets.token_urlsafe(32)
                expiry = int(time.time()) + 3600  # Token valid for 1 hour
                
                cursor.execute("UPDATE users SET reset_token = %s, reset_token_expiry = %s WHERE id = %s",
                               (token, expiry, user['id']))
                conn.commit()
                
                # Retrieve SMTP settings
                cursor.execute("SELECT setting_key, setting_value FROM settings WHERE setting_key LIKE 'smtp_%'")
                smtp_settings = {s['setting_key']: s['setting_value'] for s in cursor.fetchall()}
                
                cursor.close()
                conn.close()
                
                if smtp_settings.get('smtp_user') and smtp_settings.get('smtp_password'):
                    host = smtp_settings.get('smtp_host', 'smtp.gmail.com')
                    port = 465
                    user_login = smtp_settings.get('smtp_user')
                    pwd = smtp_settings.get('smtp_password')

                    msg = MIMEMultipart('alternative')  # Use alternative structure for both plain-text & HTML
                    msg['From'] = f"Maplewood Burgers <{smtp_settings.get('smtp_from_email')}>"
                    msg['To'] = email
                    msg['Subject'] = "Reset your Maplewood Burgers password"
                    
                    # Generate standard headers required by modern spam filters (Gmail SPF/DKIM validation)
                    from email.utils import make_msgid, formatdate
                    msg["Date"] = formatdate(localtime=True)
                    msg["Message-ID"] = make_msgid(domain=host.split('.')[-2:] if '.' in host else 'maplewoodburgers.com')
                    
                    # Determine correct base URL for links (handling reverse proxy and local development)
                    base_url = request.url_root.rstrip('/')
                    
                    # 1. Allow absolute override via environment variable (best practice for production)
                    env_base_url = os.environ.get('SITE_BASE_URL')
                    if env_base_url:
                        base_url = env_base_url.rstrip('/')
                    else:
                        # 2. Auto-detect standard reverse proxy headers (Nginx/Apache/Cloudflare)
                        forwarded_host = request.headers.get('X-Forwarded-Host')
                        forwarded_proto = request.headers.get('X-Forwarded-Proto', 'https')
                        if forwarded_host:
                            base_url = f"{forwarded_proto}://{forwarded_host}"
                        else:
                            # 3. Fallback to Host header if request was routed externally
                            http_host = request.headers.get('Host')
                            if http_host and '127.0.0.1' not in http_host and 'localhost' not in http_host:
                                # Standard live website should use HTTPS
                                base_url = f"https://{http_host}"
                    
                    reset_link = f"{base_url}/access-panel/reset-password?token={token}"
                    
                    # 1. Plain-text alternative body
                    text_body = f"""
Maplewood Burgers - Administrative Password Reset

We received a request to reset your administrative password.
Please copy and paste the secure link below into your browser to reset your password:

{reset_link}

This link is secure and will expire in 1 hour. If you did not make this request, you can safely ignore this email.
"""
                    
                    # 2. Premium, clean HTML body
                    html_body = f"""<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #eeeeee; border-radius: 8px; }}
        .header {{ background-color: #aa1e2d; color: #ffffff; padding: 15px; text-align: center; border-radius: 6px 6px 0 0; }}
        .content {{ padding: 20px; }}
        .button {{ display: inline-block; background-color: #aa1e2d; color: #ffffff !important; padding: 12px 30px; text-decoration: none; border-radius: 30px; font-weight: bold; margin: 20px 0; }}
        .footer {{ font-size: 12px; color: #777777; margin-top: 25px; border-top: 1px solid #eeeeee; padding-top: 10px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h3 style="margin: 0; text-transform: uppercase;">Password Reset Request</h3>
        </div>
        <div class="content">
            <p>Hello,</p>
            <p>We received a request to reset your administrative password for the Maplewood Burgers Portal.</p>
            <p>Click the button below to configure your new login password:</p>
            <p style="text-align: center;">
                <a href="{reset_link}" class="button">Reset Password Now</a>
            </p>
            <p style="font-size: 13px; color: #666666;">If the button does not work, please copy and paste this URL into your browser:</p>
            <p style="font-size: 13px; color: #aa1e2d; word-break: break-all;">{reset_link}</p>
            <p>This secure link will expire in 1 hour. If you did not request a password reset, you can safely ignore this email.</p>
        </div>
        <div class="footer">
            This is an automated security notification from the Maplewood Burgers Careers Portal.
        </div>
    </div>
</body>
</html>"""

                    # Attach both versions (plain text must go first)
                    msg.attach(MIMEText(text_body, 'plain'))
                    msg.attach(MIMEText(html_body, 'html'))
                    
                    # Send via SMTP Port 465 (SSL)
                    context = ssl.create_default_context()
                    with smtplib.SMTP_SSL(host, port, context=context, timeout=15) as server:
                        server.login(user_login, pwd)
                        server.send_message(msg)
                        
                    return render_template('forgot_password.html', success="A secure password reset link has been emailed to you!")
                else:
                    return render_template('forgot_password.html', error="SMTP server is not configured in settings. Cannot send emails.")
            else:
                # Return standard ambiguous success to prevent username enumeration
                return render_template('forgot_password.html', success="If this email is registered, a password reset link has been sent.")
                
        except Exception as err:
            logging.error(f"Forgot password error: {str(err)}")
            return render_template('forgot_password.html', error=f"An error occurred: {str(err)}")
            
    return render_template('forgot_password.html')

@app.route('/access-panel/reset-password', methods=['GET', 'POST'])
def reset_password():
    token = request.args.get('token') if request.method == 'GET' else request.form.get('token')
    if not token:
        flash("Reset token is missing.", "danger")
        return redirect(url_for('admin_dashboard'))
        
    try:
        import time
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE reset_token = %s AND reset_token_expiry > %s", (token, int(time.time())))
        user = cursor.fetchone()
        
        if not user:
            cursor.close()
            conn.close()
            flash("The reset link is invalid or has expired.", "danger")
            return redirect(url_for('admin_dashboard'))
            
        if request.method == 'POST':
            new_password = request.form.get('new_password', '')
            confirm_password = request.form.get('confirm_password', '')
            
            if new_password != confirm_password:
                cursor.close()
                conn.close()
                return render_template('reset_password.html', token=token, error="Passwords do not match.")
                
            if len(new_password) < 6:
                cursor.close()
                conn.close()
                return render_template('reset_password.html', token=token, error="Password must be at least 6 characters.")
                
            hashed_new = generate_password_hash(new_password)
            cursor.execute("UPDATE users SET password = %s, reset_token = NULL, reset_token_expiry = NULL WHERE id = %s",
                           (hashed_new, user['id']))
            conn.commit()
            cursor.close()
            conn.close()
            flash("Your password has been successfully reset! You can now log in.", "success")
            return redirect(url_for('admin_dashboard'))
            
        cursor.close()
        conn.close()
        return render_template('reset_password.html', token=token)
        
    except Exception as err:
        logging.error(f"Reset password error: {str(err)}")
        flash(f"An error occurred: {str(err)}", "danger")
        return redirect(url_for('admin_dashboard'))

@app.route('/access-panel/download/<filename>')
@login_required
def download_resume(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/access-panel/delete-application/<int:id>', methods=['POST'])
@login_required
def delete_application(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Get resume path to delete file
        cursor.execute("SELECT resume_path FROM applications WHERE id = %s", (id,))
        app_data = cursor.fetchone()
        
        if app_data and app_data['resume_path']:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], app_data['resume_path'])
            if os.path.exists(file_path):
                os.remove(file_path)
        
        # Delete from database
        cursor.execute("DELETE FROM applications WHERE id = %s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        
        flash("Application deleted successfully!", "success")
    except Exception as e:
        flash(f"Error deleting application: {str(e)}", "danger")
        
    return redirect(url_for('admin_dashboard'))

@app.route('/access-panel/delete-multiple', methods=['POST'])
@login_required
def delete_multiple_applications():
    try:
        app_ids = request.form.getlist('app_ids[]')
        if not app_ids:
            flash("No applications selected.", "warning")
            return redirect(url_for('admin_dashboard'))

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Format for IN clause
        format_strings = ','.join(['%s'] * len(app_ids))
        
        # Get resume paths to delete files
        cursor.execute(f"SELECT resume_path FROM applications WHERE id IN ({format_strings})", tuple(app_ids))
        apps_to_delete = cursor.fetchall()
        
        for app_data in apps_to_delete:
            if app_data['resume_path']:
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], app_data['resume_path'])
                if os.path.exists(file_path):
                    try: os.remove(file_path)
                    except: pass
        
        # Delete from database
        cursor.execute(f"DELETE FROM applications WHERE id IN ({format_strings})", tuple(app_ids))
        conn.commit()
        cursor.close()
        conn.close()
        
        flash(f"Successfully deleted {len(app_ids)} applications.", "success")
    except Exception as e:
        flash(f"Error in bulk deletion: {str(e)}", "danger")
        
    return redirect(url_for('admin_dashboard'))



@app.route('/test-email')
def test_email_diagnostic():
    import smtplib
    from email.mime.text import MIMEText
    try:
        host = "smtp.gmail.com"
        port = 465
        user = "confidosoftsolutionpvtltd@gmail.com"
        pwd = "fkiijlgzgjomeqyf"
        
        msg = MIMEText("This is a direct test from the Flask application using the simple terminal logic.")
        msg["Subject"] = "Flask Terminal-Logic Test"
        msg["From"] = user
        msg["To"] = "sanjayconfido@gmail.com"
        
        print(f"DEBUG TEST: Connecting to {host}:{port}...")
        with smtplib.SMTP_SSL(host, port, timeout=15) as server:
            print("DEBUG TEST: Connection successful. Logging in...")
            server.login(user, pwd)
            print("DEBUG TEST: Sending...")
            server.send_message(msg)
            print("DEBUG TEST: SUCCESS!")
            
        return jsonify({"status": "success", "message": "Test email sent successfully using terminal logic!"})
    except Exception as e:
        import traceback
        err = traceback.format_exc()
        print(f"DEBUG TEST FAILURE: {err}")
        return jsonify({"status": "error", "message": str(e), "traceback": err})
@app.route('/access-panel/sync-menu')
@login_required
def admin_sync_menu():
    success, message = sync_menu_from_json()
    if success:
        flash(message, "success")
    else:
        flash(f"Sync failed: {message}", "danger")
    return redirect(url_for('admin_dashboard'))

@app.route('/proxy')
def proxy():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "No URL provided"}), 400
    
    if not url.startswith('https://maplewoodburgers.appfront.app/'):
        return jsonify({"error": "Forbidden domain"}), 403
        
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        return response.content, response.status_code, {'Content-Type': 'application/json'}
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('FLASK_DEBUG', 'False').lower() == 'true')
