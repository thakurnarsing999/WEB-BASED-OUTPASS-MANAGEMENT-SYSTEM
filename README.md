# Web-Based Out Pass Management System

A digital outpass management platform built with **Python (Flask)** and **PostgreSQL (Supabase)**, featuring a modern glassmorphic interface, role-based workflows, and automated gate verification logs.

---

## 🌐 Live Demo

* **Web Application**: [https://web-based-outpass-management-system.vercel.app/](https://web-based-outpass-management-system.vercel.app/)

---

## ✨ Features & User Roles

* **👨‍🎓 Student Portal**:
  * Apply for outpass with departure details, reason, and parent contact.
  * Live status tracking (`Pending`, `Approved`, `Rejected`, `Exited`).
  * Auto-generated OTP visibility upon mentor approval.

* **👩‍🏫 Mentor Portal**:
  * Review, approve, or reject student requests with custom remarks.
  * Real-time metrics for pending, approved, and total applications.

* **🛡️ Security Guard Terminal**:
  * Verify student Request ID, departure date, and OTP at the campus gate.
  * Automatically log departure timestamps and prevent pass re-use.

* **⚙️ Administrator Center**:
  * Registered student registry oversight.
  * System-wide audit log of all outpasses and exits.

---

## 💻 Tech Stack

* **Frontend**: HTML5, CSS3 (Glassmorphism, Responsive Tables), Vanilla JavaScript (ES6)
* **Backend**: Python 3, Flask, Werkzeug Security (Scrypt password hashing)
* **Database**: PostgreSQL (Supabase) via `psycopg2`
* **Deployment**: Vercel (Web Server), Supabase (Cloud Database)

---

## 🚀 Local Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/thakurnarsing999/WEB-BASED-OUTPASS-MANAGEMENT-SYSTEM.git
   cd WEB-BASED-OUTPASS-MANAGEMENT-SYSTEM
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Environment Variables:**
   Create a `.env` file in the root folder:
   ```env
   DATABASE_URL=your_postgresql_connection_string
   SECRET_KEY=your_secret_key
   ```

4. **Run the application:**
   ```bash
   python app.py
   ```
   Open `http://127.0.0.1:5000` in your browser.

---

## 📂 Project Structure

```text
├── app.py                  # Core application routes & backend logic
├── database.sql            # PostgreSQL database schema & initial seed
├── requirements.txt        # Python package dependencies
├── static/
│   ├── style.css           # Glassmorphism styling and responsive layout
│   └── script.js           # Client-side validation scripts
└── templates/              # Jinja2 HTML templates
    ├── base.html           # Master layout & role-based navbar
    ├── home.html           # Unified login & register portal
    ├── apply_outpass.html  # Student outpass application form
    ├── view_status.html    # Student request status history
    ├── mentor_dashboard.html   # Mentor approval dashboard
    ├── security_dashboard.html # Security gate terminal
    └── admin_dashboard.html    # Admin management center
```
