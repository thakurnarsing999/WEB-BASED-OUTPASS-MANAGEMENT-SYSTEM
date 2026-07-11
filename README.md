# Web-Based Out Pass Management System

A digital outpass management portal featuring a premium glassmorphic interface, dynamic role-based routes, and secure database integrations.

---

## 🌐 Live Deployments

* **Live Website URL**: [https://web-based-outpass-management-system.vercel.app/](https://web-based-outpass-management-system.vercel.app/)
* **Cloud Database Host**: `tokaido.proxy.rlwy.net` (Port: `16493`)

---

## 🔑 Pre-Seeded Accounts & Authorization Keys

To register or log in as a staff member (Admin, Mentor, or Security Guard), you must provide the role's corresponding **Security Authorization Key**.

### 1. Global Role Authorization Keys
* **Admin Key**: `adminpass123`
* **Security Key**: `securitypass123`
* **Mentor Key**: `mentorpass123`

### 2. Seeded Login Accounts (For Instant Testing)
* **Root Administrator**:
  * **Email ID**: `admin@outpass.com`
  * **Password**: `admin123`
  * **Security Key**: `adminpass123`
* **Default Mentor**:
  * **Email ID**: `mentor@outpass.com`
  * **Password**: `mentor123`
  * **Security Key**: `mentorpass123`
* **Default Security Guard**:
  * **Email ID**: `security@outpass.com`
  * **Password**: `security123`
  * **Security Key**: `securitypass123`

---

## 💻 Tech Stack & Features

* **Backend**: Python 3 / Flask Micro-framework
* **Security**: `werkzeug.security` (salted scrypt password hashing and validation)
* **Database**: MySQL (hosted on Railway)
* **Session Handling**: Role-appropriate dynamic Flask sessions with encrypted cookie state
* **Frontend**: HTML5, CSS3 Custom Theme (obsidian dark mode, frosted backdrop blurs, responsive tables, single-line data grids), client-side dynamic JavaScript form toggles.
* **Hosting**: Vercel (web hosting), Railway (database hosting)

---

## 📂 Project Structure
* `app.py` - Core application logic and API routes.
* `database.sql` - Complete database schema DDL and seed values.
* `static/style.css` - Custom styling theme.
* `static/script.js` - Client-side verification popups.
* `templates/` - HTML layout views for base structure, forms, and dashboards.
