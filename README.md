# Web-Based Out Pass Management System

A digital outpass management portal featuring a premium glassmorphic interface, dynamic role-based routes, and secure database integrations.

---

## 🌐 Live Deployments

* **Live Website URL**: [https://web-based-outpass-management-system.vercel.app/](https://web-based-outpass-management-system.vercel.app/)
* **Cloud Database**: Hosted on **Supabase** (PostgreSQL)

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

## ⚡ Supabase Database Setup & Configuration

This project uses **PostgreSQL** hosted on **Supabase**.

### 1. Create Tables in Supabase:
1. Open your project on **[Supabase.com](https://supabase.com)**.
2. In the left sidebar, click on **SQL Editor**.
3. Open the file [`database.sql`](database.sql) in this repository, copy all contents, paste them into the Supabase SQL editor, and click **Run**.

### 2. Connect Your App (Environment Variables):
Under **Project Settings** -> **Database** in Supabase, copy your connection string or URI.
Add the variable in **Vercel** (or in your local `.env`):
* `DATABASE_URL`: `postgresql://postgres.[project-ref]:[password]@aws-0-[region].pooler.supabase.com:6543/postgres` (or Direct Connection URI)

*(Alternatively, you can provide separate variables: `PGHOST`, `PGPORT`, `PGUSER`, `PGPASSWORD`, `PGDATABASE`).*

---

## 🔄 How to Make & Deploy Changes

Whenever you want to modify your website, update a feature, or change any style in the future, follow this simple 4-step workflow:

### Step 1: Make your changes locally
Open your project in **VS Code** and edit the files:
* **Layout / HTML Text**: Edit the files inside the `templates/` folder.
* **Colors / Spacing / Styles**: Edit `static/style.css`.
* **Python Routes / Logic**: Edit `app.py`.

### Step 2: Test your changes locally on your PC
Before pushing to the internet, make sure there are no errors on your local machine:
1. Open Command Prompt inside your project folder.
2. Start the local server:
   ```cmd
   python app.py
   ```
3. Open `http://127.0.0.1:5000/` in your browser and verify that everything looks and functions correctly.
4. Press `Ctrl + C` in the command prompt to stop the server when you are done testing.

### Step 3: Commit your changes to Git
Once your changes are working perfectly on your local machine, save them to your local Git history. Open your terminal and run:
```bash
git add .
git commit -m "Write a short summary of the changes you made"
```

### Step 4: Push to GitHub (This updates Vercel)
Upload your committed code to the cloud:
```bash
git push origin main
```
*Note: Vercel will automatically detect the push, rebuild your application, and update the live website within 60 seconds.*

### ⚠️ Special Step: If you modified the Database (SQL)
If you made changes that affect your database structure (like adding a new table or column in `database.sql`):
* Open the **SQL Editor** in your Supabase dashboard and execute the matching `ALTER` or `CREATE` SQL query so the cloud database has the new fields.

---

## 🔮 Future Roadmap & Potential Updates

Here are some features you can build next to improve the system:

1. **QR Code Scanning**: Generate a unique QR code for approved outpasses. The security guard can scan it using a camera to mark the student "Exited" automatically.
2. **Notifications System**: Set up automated Email/SMS messages to parents when an outpass is approved or when the student exits the campus.
3. **Return Gate Tracking**: Track return timestamps to measure the exact duration a student has been outside campus.
4. **Interactive Analytics**: Use a library like `Chart.js` on the Admin Dashboard to visualize outpass trends, department metrics, and peak hours.
5. **Self-Service Reset**: Allow students and mentors to reset their passwords and update their profile details securely.

---

## 💻 Tech Stack & Features

* **Backend**: Python 3 / Flask Micro-framework
* **Security**: `werkzeug.security` (salted scrypt password hashing and validation)
* **Database**: PostgreSQL (hosted on Supabase) via `psycopg2-binary`
* **Session Handling**: Role-appropriate dynamic Flask sessions with encrypted cookie state
* **Frontend**: HTML5, CSS3 Custom Theme (obsidian dark mode, frosted backdrop blurs, responsive tables, single-line data grids), client-side dynamic JavaScript form toggles.
* **Hosting**: Vercel (web hosting), Supabase (PostgreSQL database hosting)

---

## 📂 Project Structure
* `app.py` - Core application logic and API routes.
* `database.sql` - Complete PostgreSQL database schema DDL and seed values.
* `static/style.css` - Custom styling theme.
* `static/script.js` - Client-side verification popups.
* `templates/` - HTML layout views for base structure, forms, and dashboards.
