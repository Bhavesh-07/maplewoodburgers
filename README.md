# 🍔 Maplewood Burgers — Website & Management System

A full-stack web application and content management system for **Maplewood Burgers**, featuring dynamic menus, customer loyalty program, job application portal with resume processing, customer reviews, blog publishing system, and a comprehensive administrative dashboard.

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Architecture](#-project-architecture)
- [Prerequisites](#-prerequisites)
- [Quick Start Guide](#-quick-start-guide)
  - [1. Clone Repository](#1-clone-repository)
  - [2. Set Up Virtual Environment](#2-set-up-virtual-environment)
  - [3. Install Dependencies](#3-install-dependencies)
  - [4. Configure Environment Variables](#4-configure-environment-variables)
  - [5. Initialize Database](#5-initialize-database)
  - [6. Run the Application](#6-run-the-application)
- [Admin Access & Panel](#-admin-access--panel)
- [Database Utilities & Scripts](#-database-utilities--scripts)
- [Environment Configuration](#-environment-configuration)
- [Production Deployment](#-production-deployment)
- [Contributing & Maintenance](#-contributing--maintenance)

---

## ✨ Features

### 🌐 Customer-Facing Website
- **Interactive Menu**: Full menu showcase with categorization (Breakfast, Burgers, Sides, Drinks, Kid's Menu, Catering).
- **Location Pages**: Dedicated landing pages for locations (Lake Charles, Sulphur, Moss Bluff).
- **Loyalty Program**: Customer signup portal with automatic welcome email dispatch.
- **Career & Job Applications**: Online job application form supporting resume uploads (`.pdf`, `.doc`, `.docx`) with automated notification emails.
- **Reviews & Testimonials**: Live customer review showcase with dynamic star rating filters.
- **Blog & News**: Dynamic blog CMS with SEO-friendly slugs and rich formatting.
- **Anti-Spam Security**: In-house mathematical captcha verification on user submissions.

### 🛡️ Administrative Control Panel (`/access-panel`)
- **Authentication**: Secure admin login with password hashing (`scrypt` / `werkzeug.security`) and token-based password reset via email.
- **Job Applications Management**: Review applicant details, download uploaded resumes, filter, and batch delete applications.
- **Loyalty Signups Management**: View and export subscriber lists.
- **Blog CMS**: Full CRUD interface for creating, editing, and publishing articles with custom image URLs and SEO meta tags.
- **Settings & SMTP Configuration**: Manage live chat widget IDs and SMTP server credentials directly from the UI.
- **Menu Sync**: One-click menu synchronization with external ordering platforms.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.10+ / Flask 3.x
- **Database**: MySQL 8.0+ / MariaDB (`mysql-connector-python`)
- **Frontend / Templating**: Jinja2, HTML5, Vanilla CSS3, JavaScript
- **Security & Forms**: Flask-WTF, WTForms, Werkzeug Security, python-dotenv
- **Mailing**: SMTP (`smtplib`, `email.mime`) with SSL/TLS support

---

## 📁 Project Architecture

```plaintext
maplewood-git/
├── app.py                     # Main Flask application & route controllers
├── init_db.py                 # Database initialization & migration script
├── check_db.py                # Database connection check & health monitor
├── seed_applications.py       # Seed script for generating sample job applications
├── test_db_conn.py            # Quick database connection test
├── inject_widget.py           # Helper script for injecting custom chat widget
├── requirements.txt           # Python package dependencies
├── .env.example               # Example environment variable file
├── .gitignore                 # Git ignore rules (logs, venv, secrets, cache)
├── menu_data.json             # Static/cached menu items data
├── database_backup.sql        # Database schema and backup dump
│
├── templates/                 # Jinja2 HTML templates
│   ├── index.html             # Homepage
│   ├── full-menu.html         # Complete menu page
│   ├── application.html      # Job application form
│   ├── blogs.html             # Blog listing
│   ├── blog_detail.html       # Single blog post
│   ├── admin.html             # Admin dashboard (applications)
│   ├── blogs_admin.html       # Admin blog management
│   ├── loyalty_admin.html     # Admin loyalty club management
│   ├── settings.html          # Admin settings & SMTP config
│   ├── login.html             # Admin login page
│   ├── forgot_password.html   # Password recovery request
│   ├── reset_password.html    # Password reset form
│   └── 404.html               # Custom 404 error page
│
├── static/                    # Static assets
│   ├── css/                   # Stylesheets (app.css, admin-style.css, inner.css)
│   ├── js/                    # JavaScript files (app.js)
│   ├── img/                   # Images, logos, and vector assets
│   ├── fonts/                 # Webfonts & Google fonts
│   └── pdf/                   # PDF catering menus and documentation
│
└── uploads/                   # Upload directory for applicant resumes (auto-created)
```

---

## 📦 Prerequisites

Before running the project, ensure you have the following installed on your machine:
- **Python 3.10+** (Python 3.12 recommended) — [Download Python](https://www.python.org/downloads/)
- **MySQL Server 8.0+** or **MariaDB** (e.g., via XAMPP, WampServer, or standalone MySQL)
- **Git** — [Download Git](https://git-scm.com/)

---

## 🚀 Quick Start Guide

### 1. Clone Repository
```bash
git clone https://github.com/Bhavesh-07/maplewoodburgers.git
cd maplewoodburgers
```

### 2. Set Up Virtual Environment

#### On Windows (PowerShell):
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```
*(If PowerShell restricts scripts, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` first)*

#### On macOS / Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

### 4. Configure Environment Variables

Create a `.env` file in the root directory by copying `.env.example`:

```bash
# On Windows
copy .env.example .env

# On macOS / Linux
cp .env.example .env
```

Open `.env` and set your MySQL database credentials:
```ini
DB_HOST=127.0.0.1
DB_USER=root
DB_PASS=your_mysql_password
DB_NAME=maplewood_db
SECRET_KEY=your_random_secret_key_here
PORT=5000
FLASK_DEBUG=True
```

---

### 5. Initialize Database

Make sure your MySQL server is running, then execute the initialization script:

```bash
python init_db.py
```

This script will automatically:
- Create the `maplewood_db` database if it doesn't already exist.
- Create all required tables (`applications`, `users`, `settings`, `blogs`, `loyalty_signups`).
- Seed default system settings and sample blog post.
- Create the default administrator account.

*(Optional)* If you prefer to import the SQL backup directly:
```bash
mysql -u root -p maplewood_db < database_backup.sql
```

---

### 6. Run the Application

Start the Flask development server:

```bash
python app.py
```

Open your browser and visit:
- **Public Site**: [http://localhost:5000](http://localhost:5000)
- **Admin Panel**: [http://localhost:5000/access-panel](http://localhost:5000/access-panel)

---

## 🔐 Admin Access & Panel

| Field | Default Value |
| :--- | :--- |
| **Admin URL** | `http://localhost:5000/access-panel` (or `/login`) |
| **Default Username** | `admin` |
| **Default Password** | `admin123` |
| **Default Email** | `sanjayrathod885@gmail.com` |

> [!IMPORTANT]
> Change the default admin password and email immediately after logging in by visiting **Settings** (`/access-panel/settings`).

---

## ⚙️ Environment Configuration

| Variable | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `DB_HOST` | `string` | `127.0.0.1` | MySQL server host address |
| `DB_USER` | `string` | `root` | MySQL database username |
| `DB_PASS` | `string` | *empty* | MySQL database password |
| `DB_NAME` | `string` | `maplewood_db` | MySQL database name |
| `SECRET_KEY` | `string` | `maplewood_secret_key_fixed` | Flask session secret key |
| `PORT` | `integer` | `5000` | Port for the web server |
| `FLASK_DEBUG` | `boolean` | `False` | Enable/disable Flask debug mode |

---

## 🧰 Database Utilities & Scripts

- **`python check_db.py`**: Validates MySQL connection and prints record counts.
- **`python seed_applications.py`**: Populates the database with sample job applications for testing.
- **`python init_db.py`**: Runs idempotent schema migrations, repairs missing columns, and ensures hashed passwords.

---

## 🌐 Production Deployment

For production deployments (e.g., Ubuntu/Debian server with Nginx and Gunicorn/Waitress):

1. **Install a production WSGI server**:
   ```bash
   pip install gunicorn
   ```
2. **Run using Gunicorn**:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```
3. **Configure Nginx Reverse Proxy**:
   Forward requests from port 80/443 to `http://127.0.0.1:5000`.
4. **Ensure File Permissions**:
   Make sure the `uploads/` directory has appropriate write permissions for the web user (`www-data`).
5. **Set Environment**:
   Set `FLASK_DEBUG=False` and assign a secure, cryptographically random `SECRET_KEY`.

---

## 📄 License & Maintainer

- **Project**: Maplewood Burgers
- **Repository**: [Bhavesh-07/maplewoodburgers](https://github.com/Bhavesh-07/maplewoodburgers)