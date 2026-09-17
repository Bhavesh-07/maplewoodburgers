import os
import mysql.connector
from mysql.connector import errorcode

def init_db():
    try:
        from werkzeug.security import generate_password_hash
    except ImportError:
        print("\n" + "="*80)
        print("ERROR: 'werkzeug' module was not found.")
        print("Please activate your virtual environment (e.g., 'source venv/bin/activate')")
        print("and make sure your requirements are installed ('pip install -r requirements.txt')")
        print("before running this script.")
        print("="*80 + "\n")
        return
    # Load .env manually if it exists to retrieve correct database credentials
    env_host = '127.0.0.1'
    env_port = 3306
    env_user = 'root'
    env_pass = ''
    
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' in line:
                    key, val = line.split('=', 1)
                    key = key.strip()
                    val = val.strip().strip("'").strip('"')
                    if key == 'DB_HOST': env_host = val
                    elif key == 'DB_PORT': env_port = int(val)
                    elif key == 'DB_USER': env_user = val
                    elif key == 'DB_PASS': env_pass = val

    config = {
        'user': env_user,
        'password': env_pass,
        'host': env_host,
        'port': env_port,
    }

    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        
        # Create database
        cursor.execute("CREATE DATABASE IF NOT EXISTS maplewood_db")
        cursor.execute("USE maplewood_db")
        
        # Create applications table
        create_applications_table = """
        CREATE TABLE IF NOT EXISTS applications (
            id INT AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100) NOT NULL,
            contact_number VARCHAR(20) NOT NULL,
            email VARCHAR(100),
            experience TEXT,
            location VARCHAR(255),
            position VARCHAR(255),
            resume_path VARCHAR(255),
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        cursor.execute(create_applications_table)

        # Create users table for auth
        create_users_table = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            email VARCHAR(100) DEFAULT NULL,
            reset_token VARCHAR(255) DEFAULT NULL,
            reset_token_expiry BIGINT DEFAULT NULL
        )
        """
        cursor.execute(create_users_table)

        # Migration check: verify and dynamically add recovery columns to an existing table
        cursor.execute("SHOW COLUMNS FROM users")
        existing_columns = [col[0] for col in cursor.fetchall()]
        
        if 'email' not in existing_columns:
            cursor.execute("ALTER TABLE users ADD COLUMN email VARCHAR(100) DEFAULT NULL")
            print("  [MIGRATE] Added 'email' column to 'users' table.")
            
        if 'reset_token' not in existing_columns:
            cursor.execute("ALTER TABLE users ADD COLUMN reset_token VARCHAR(255) DEFAULT NULL")
            print("  [MIGRATE] Added 'reset_token' column to 'users' table.")
            
        if 'reset_token_expiry' not in existing_columns:
            cursor.execute("ALTER TABLE users ADD COLUMN reset_token_expiry BIGINT DEFAULT NULL")
            print("  [MIGRATE] Added 'reset_token_expiry' column to 'users' table.")
        
        # Create settings table
        create_settings_table = """
        CREATE TABLE IF NOT EXISTS settings (
            id INT AUTO_INCREMENT PRIMARY KEY,
            setting_key VARCHAR(50) UNIQUE NOT NULL,
            setting_value TEXT
        )
        """
        cursor.execute(create_settings_table)

        # Create blogs table
        create_blogs_table = """
        CREATE TABLE IF NOT EXISTS blogs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            slug VARCHAR(191) UNIQUE NOT NULL,
            excerpt TEXT,
            content TEXT,
            image_url VARCHAR(255),
            meta_description VARCHAR(255),
            published_date VARCHAR(50) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        cursor.execute(create_blogs_table)

        # Create loyalty_signups table
        create_loyalty_table = """
        CREATE TABLE IF NOT EXISTS loyalty_signups (
            id INT AUTO_INCREMENT PRIMARY KEY,
            fullname VARCHAR(255) NOT NULL,
            phonenumber VARCHAR(20) NOT NULL,
            email VARCHAR(255) NOT NULL,
            birthdate VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        cursor.execute(create_loyalty_table)
        
        # Insert default settings if not exists
        default_settings = [
            ('chat_widget_key', ''),
            ('smtp_host', 'smtp.gmail.com'),
            ('smtp_port', '587'),
            ('smtp_user', ''),
            ('smtp_password', ''),
            ('smtp_from_email', '')
        ]
        
        for key, value in default_settings:
            cursor.execute("INSERT IGNORE INTO settings (setting_key, setting_value) VALUES (%s, %s)", (key, value))
        
        # Insert default admin if not exists (hashed password and default email)
        hashed_default = generate_password_hash('admin123')
        cursor.execute("""
            INSERT INTO users (username, password, email) 
            VALUES ('admin', %s, 'sanjayrathod885@gmail.com')
            ON DUPLICATE KEY UPDATE email = COALESCE(email, 'sanjayrathod885@gmail.com')
        """, (hashed_default,))

        # Auto-migrate any existing plain-text passwords to hashed versions
        cursor.execute("SELECT id, password FROM users")
        all_users = cursor.fetchall()
        for uid, pwd in all_users:
            # werkzeug hashes start with a method prefix like 'scrypt:', 'pbkdf2:', etc.
            if not pwd.startswith(('scrypt:', 'pbkdf2:', 'sha256$', 'sha512$')):
                hashed_pwd = generate_password_hash(pwd)
                cursor.execute("UPDATE users SET password = %s WHERE id = %s", (hashed_pwd, uid))
                print(f"  [MIGRATE] Hashed plain-text password for user id={uid}")
        conn.commit()
        # Seed default blog if not exists
        cursor.execute("SELECT COUNT(*) FROM blogs WHERE slug = 'will-you-be-my-bogo'")
        if cursor.fetchone()[0] == 0:
            seed_blog = {
                'title': 'Will You Be My BOGO?',
                'slug': 'will-you-be-my-bogo',
                'excerpt': 'What’s Valentine’s Day without a little label confusion? Whether it’s love, a situationship, or just good company, we’ve got you covered. From Tuesday, 2/11, through Monday, 2/17...',
                'content': '<p>What’s Valentine’s Day without a little label confusion? Whether it’s love, a situationship, or just good company, we’ve got you covered.</p><p>From Tuesday, 2/11, through Monday, 2/17, Maplewood is serving up a <strong>Maplewood BOGO*</strong> you don’t want to miss. No need to define what you are—just grab your bestie, your boo, or <em>whoever</em> and enjoy this fiery favorite with code <strong>BEMINE</strong>.</p>',
                'image_url': 'inc/assets/img/The-Hangover-Burger.webp',
                'meta_description': 'What’s Valentine’s Day without a little label confusion? Whether it’s love, a situationship, or just good company, we’ve got you covered.',
                'published_date': 'February 4, 2025'
            }
            cursor.execute("""
                INSERT INTO blogs (title, slug, excerpt, content, image_url, meta_description, published_date)
                VALUES (%(title)s, %(slug)s, %(excerpt)s, %(content)s, %(image_url)s, %(meta_description)s, %(published_date)s)
            """, seed_blog)
        
        print("Database, tables, default user, and blogs initialized/seeded successfully.")
        
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

if __name__ == "__main__":
    init_db()
