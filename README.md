# Web-Based Out Pass Management System

A digital outpass management platform built with **Python (Flask)** and **PostgreSQL (Supabase)**, featuring a modern glassmorphic interface, role-based workflows, and automated gate verification logs.

---

## 🌐 Live Deployment

* **Live Web Application**: [https://web-based-outpass-management-system.vercel.app/](https://web-based-outpass-management-system.vercel.app/)
* **Cloud Database Infrastructure**: Hosted on **Supabase** (PostgreSQL)

---

## ✨ System Features & User Roles

The platform provides dedicated, role-segregated portals:

* **👨‍🎓 Student Portal**:
  * Submit digital outpass requests with reasons, parent contact, and departure schedule.
  * Real-time status tracking (Pending / Approved / Rejected / Exited).
  * Auto-generated OTP visibility upon mentor approval.

* **👩‍🏫 Mentor / Faculty Portal**:
  * Review, approve, or reject student outpasses with custom remarks.
  * Live metrics for pending, approved, and total department applications.

* **🛡️ Security Guard Terminal**:
  * Secure gate-pass validation terminal.
  * Validates OTP & departure date in real-time before allowing campus exit.
  * Automatic exit logging with timestamps.

* **⚙️ Administrator Command Center**:
  * Global student registry oversight.
  * System-wide audit log and movement analytics.

---

## 💻 Tech Stack

* **Backend**: Python 3, Flask Micro-framework, Werkzeug Security (Scrypt password encryption)
* **Database**: PostgreSQL (Supabase) via `psycopg2-binary`
* **Frontend**: HTML5, CSS3 (Obsidian Dark Glassmorphism, Responsive Tables), Vanilla JavaScript (ES6)
* **Hosting & CI/CD**: Vercel (Web Hosting), Supabase (Database), GitHub (Version Control)

---

## 🚀 Local Development Setup

### 1. Clone the Repository:
```bash
git clone https://github.com/thakurnarsing999/WEB-BASED-OUTPASS-MANAGEMENT-SYSTEM.git
cd WEB-BASED-OUTPASS-MANAGEMENT-SYSTEM
```

### 2. Install Dependencies:
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables:
Create a `.env` file in the root directory (this file is ignored by git for security):
```env
DATABASE_URL=postgresql://postgres.[YOUR_PROJECT_REF]:[YOUR_PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres
SECRET_KEY=your_custom_secret_key
ADMIN_AUTH_KEY=your_admin_secret_key
MENTOR_AUTH_KEY=your_mentor_secret_key
SECURITY_AUTH_KEY=your_security_secret_key
```

### 4. Run the Application:
```bash
python app.py
```
Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

---

## 🔄 Deployment Workflow

Whenever updates are made locally:
```bash
git add .
git commit -m "Describe your changes"
git push origin main
```
*Vercel automatically detects commits pushed to `main` and rebuilds the production application within 60 seconds.*

---

## 📂 Project Structure

```text
├── app.py                  # Application routes, authentication & business logic
├── database.sql            # PostgreSQL schema definition and migrations
├── requirements.txt        # Python package dependencies
├── static/
│   ├── style.css           # Glassmorphism styling and responsive layout
│   └── script.js           # Client-side validation & confirmation popups
└── templates/              # HTML layout views
    ├── base.html           # Master navigation & container layout
    ├── home.html           # Unified login & registration portal
    ├── apply_outpass.html  # Outpass application form
    ├── view_status.html    # Student request status history
    ├── mentor_dashboard.html # Mentor approval dashboard
    ├── security_dashboard.html # Gate verification terminal
    └── admin_dashboard.html # Administrator registry & audit log
```
