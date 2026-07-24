from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
import random
import os
import datetime
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "outpass_secret_key")


def send_otp_email(recipient_email, otp_code, recipient_name="User"):
    smtp_server = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.environ.get("SMTP_PORT", 587))
    smtp_email = os.environ.get("SMTP_EMAIL", "")
    smtp_password = os.environ.get("SMTP_PASSWORD", "")

    if not smtp_email or not smtp_password:
        print(f"\n[SECURITY OTP NOTICE] SMTP credentials not set in env. OTP for {recipient_email} is: {otp_code}\n")
        return False, "SMTP credentials not configured."

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"Your Outpass Security Verification Code: {otp_code}"
        msg["From"] = f"Outpass Management System <{smtp_email}>"
        msg["To"] = recipient_email

        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #0f172a; color: #f8fafc; padding: 20px;">
            <div style="max-width: 500px; margin: 0 auto; background: #1e293b; border-radius: 12px; padding: 30px; border: 1px solid #334155;">
                <h2 style="color: #818cf8; margin-top: 0;">Email Verification Required</h2>
                <p>Hello <strong>{recipient_name}</strong>,</p>
                <p>Thank you for registering on the <strong>Web-Based Out Pass Management System</strong>. Please enter the 6-digit verification code below to verify your email address and complete registration:</p>
                <div style="background: #0f172a; border: 1px dashed #6366f1; padding: 15px; text-align: center; border-radius: 8px; margin: 20px 0;">
                    <span style="font-size: 32px; font-weight: bold; letter-spacing: 8px; color: #38bdf8; font-family: monospace;">{otp_code}</span>
                </div>
                <p style="font-size: 13px; color: #94a3b8;">This code will expire in 10 minutes. If you did not request this registration, please ignore this email.</p>
            </div>
        </body>
        </html>
        """
        msg.attach(MIMEText(html_content, "html"))

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_email, smtp_password)
        server.sendmail(smtp_email, recipient_email, msg.as_string())
        server.quit()
        return True, "OTP sent successfully."
    except Exception as e:
        print(f"\n[SMTP ERROR] Failed to send OTP email: {e}")
        print(f"[SECURITY OTP FALLBACK] Generated OTP for {recipient_email} is: {otp_code}\n")
        return False, str(e)


DB_CONFIG = {
    "host": os.environ.get("MYSQLHOST", "127.0.0.1"),  # localhost
    "user": os.environ.get("MYSQLUSER", "root"),
    "password": os.environ.get("MYSQLPASSWORD", "N@rs1ng#967!"),
    "database": os.environ.get("MYSQLDATABASE", "outpass_system"),
    "port": int(os.environ.get("MYSQLPORT", 3306))
}

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)


@app.route("/")
def home():
    return render_template("home.html")


# ---------------- STUDENT MODULE ----------------

@app.route("/register", methods=["POST"])
def register():
    role = request.form["role"]
    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]
    confirm_password = request.form.get("confirm_password")
    phone_no = request.form["phone_no"]

    if confirm_password and password != confirm_password:
        flash("Passwords do not match. Please re-enter your password.", "error")
        return redirect(url_for("home"))

    # Security check for Admin, Security, & Mentor registration
    if role == "Admin":
        auth_code = request.form.get("auth_code")
        if auth_code != "adminpass123":
            flash("Invalid security authorization key.", "error")
            return redirect(url_for("home"))
    elif role == "Security":
        auth_code = request.form.get("auth_code")
        if auth_code != "securitypass123":
            flash("Invalid security authorization key.", "error")
            return redirect(url_for("home"))
    elif role == "Mentor":
        auth_code = request.form.get("auth_code")
        if auth_code != "mentorpass123":
            flash("Invalid security authorization key.", "error")
            return redirect(url_for("home"))

    # Pre-check if email or unique ID already exists in DB
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        if role == "Student":
            roll_no = request.form.get("roll_no", "")
            cursor.execute("SELECT student_id FROM students WHERE email = %s OR roll_no = %s", (email, roll_no))
            if cursor.fetchone():
                flash("Email or Roll Number is already registered.", "error")
                return redirect(url_for("home"))
        elif role == "Mentor":
            staff_id = request.form.get("staff_id", "")
            cursor.execute("SELECT mentor_id FROM mentors WHERE email = %s OR staff_id = %s", (email, staff_id))
            if cursor.fetchone():
                flash("Email or Staff ID is already registered.", "error")
                return redirect(url_for("home"))
        elif role == "Security":
            cursor.execute("SELECT security_id FROM security_users WHERE email = %s", (email,))
            if cursor.fetchone():
                flash("Email is already registered.", "error")
                return redirect(url_for("home"))
        elif role == "Admin":
            cursor.execute("SELECT admin_id FROM admins WHERE email = %s", (email,))
            if cursor.fetchone():
                flash("Email is already registered.", "error")
                return redirect(url_for("home"))
    except Exception as e:
        flash(f"Database error: {e}", "error")
        return redirect(url_for("home"))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    # Generate 6-digit OTP and store pending registration state in session
    otp_code = str(random.randint(100000, 999999))
    session["pending_registration"] = {
        "role": role,
        "name": name,
        "email": email,
        "password": password,
        "phone_no": phone_no,
        "roll_no": request.form.get("roll_no", ""),
        "department": request.form.get("department", "CSE"),
        "year": request.form.get("year", "1st Year"),
        "staff_id": request.form.get("staff_id", ""),
        "otp": otp_code,
        "expires_at": time.time() + 600
    }

    send_otp_email(email, otp_code, name)
    flash(f"A 6-digit OTP verification code has been sent to {email}.", "info")
    return redirect(url_for("verify_otp"))


@app.route("/verify_otp", methods=["GET", "POST"])
def verify_otp():
    pending = session.get("pending_registration")
    if not pending:
        flash("No pending registration session found. Please register.", "error")
        return redirect(url_for("home"))

    if request.method == "POST":
        user_otp = request.form.get("otp_code", "").strip()

        if time.time() > pending.get("expires_at", 0):
            flash("OTP code has expired. Please request a new code.", "error")
            return render_template("verify_otp.html", pending_email=pending["email"], pending_role=pending["role"])

        if user_otp != pending.get("otp"):
            flash("Invalid OTP code. Please check your email and try again.", "error")
            return render_template("verify_otp.html", pending_email=pending["email"], pending_role=pending["role"])

        # OTP is verified! Insert user into database
        role = pending["role"]
        name = pending["name"]
        email = pending["email"]
        hashed_password = generate_password_hash(pending["password"])
        phone_no = pending["phone_no"]

        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            if role == "Student":
                query = """
                    INSERT INTO students (name, roll_no, email, password, phone_no, department, year)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (name, pending["roll_no"], email, hashed_password, phone_no, pending["department"], pending["year"]))
            elif role == "Mentor":
                query = """
                    INSERT INTO mentors (name, email, password, staff_id, phone_no)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(query, (name, email, hashed_password, pending["staff_id"], phone_no))
            elif role == "Security":
                query = """
                    INSERT INTO security_users (name, email, password, phone_no)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(query, (name, email, hashed_password, phone_no))
            elif role == "Admin":
                query = """
                    INSERT INTO admins (name, email, password, phone_no)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(query, (name, email, hashed_password, phone_no))

            conn.commit()
            session.pop("pending_registration", None)
            flash(f"{role} registration successful! Email verified. Please sign in.", "success")
            return redirect(url_for("home"))
        except mysql.connector.IntegrityError:
            session.pop("pending_registration", None)
            flash("Email, Roll No, or Staff ID already exists.", "error")
            return redirect(url_for("home"))
        except Exception as e:
            flash(f"Database error: {e}", "error")
            return render_template("verify_otp.html", pending_email=pending["email"], pending_role=pending["role"])
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    return render_template("verify_otp.html", pending_email=pending["email"], pending_role=pending["role"])


@app.route("/resend_otp", methods=["POST"])
def resend_otp():
    pending = session.get("pending_registration")
    if not pending:
        flash("No pending registration session found.", "error")
        return redirect(url_for("home"))

    new_otp = str(random.randint(100000, 999999))
    pending["otp"] = new_otp
    pending["expires_at"] = time.time() + 600
    session["pending_registration"] = pending

    send_otp_email(pending["email"], new_otp, pending["name"])
    flash(f"A new 6-digit OTP code has been sent to {pending['email']}.", "info")
    return redirect(url_for("verify_otp"))


@app.route("/cancel_registration", methods=["POST"])
def cancel_registration():
    session.pop("pending_registration", None)
    flash("Registration cancelled.", "info")
    return redirect(url_for("home"))


@app.route("/login", methods=["POST"])
def login():
    role = request.form["role"]
    email = request.form["email"]
    password = request.form["password"]

    # Authorization code check for Admin, Security, & Mentor login
    if role == "Admin":
        auth_code = request.form.get("auth_code")
        if auth_code != "adminpass123":
            flash("Invalid security authorization key.", "error")
            return redirect(url_for("home"))
    elif role == "Security":
        auth_code = request.form.get("auth_code")
        if auth_code != "securitypass123":
            flash("Invalid security authorization key.", "error")
            return redirect(url_for("home"))
    elif role == "Mentor":
        auth_code = request.form.get("auth_code")
        if auth_code != "mentorpass123":
            flash("Invalid security authorization key.", "error")
            return redirect(url_for("home"))

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        if role == "Student":
            query = "SELECT * FROM students WHERE email = %s OR roll_no = %s"
            cursor.execute(query, (email, email))
            user = cursor.fetchone()
            if not user:
                flash("No student account found with this email or roll number.", "error")
                return redirect(url_for("home"))
            if not check_password_hash(user["password"], password):
                flash("Incorrect password for this student account.", "error")
                return redirect(url_for("home"))

            session.clear()
            session["student_id"] = user["student_id"]
            session["student_name"] = user["name"]
            session["phone_no"] = user["phone_no"]
            session["student_phone"] = user["phone_no"]
            flash("Student login successful.", "success")
            return redirect(url_for("student_dashboard"))
                
        elif role == "Mentor":
            query = "SELECT * FROM mentors WHERE email = %s OR staff_id = %s"
            cursor.execute(query, (email, email))
            user = cursor.fetchone()
            if not user:
                flash("No mentor account found with this email or staff ID.", "error")
                return redirect(url_for("home"))
            if not check_password_hash(user["password"], password):
                flash("Incorrect password for this mentor account.", "error")
                return redirect(url_for("home"))

            session.clear()
            session["mentor_id"] = user["mentor_id"]
            session["mentor_username"] = user["name"]
            session["phone_no"] = user["phone_no"]
            session["mentor_phone"] = user["phone_no"]
            session["security_key"] = auth_code
            flash("Mentor login successful.", "success")
            return redirect(url_for("mentor_dashboard"))
                
        elif role == "Security":
            query = "SELECT * FROM security_users WHERE email = %s"
            cursor.execute(query, (email,))
            user = cursor.fetchone()
            if not user:
                flash("No security guard account found with this email address.", "error")
                return redirect(url_for("home"))
            if not check_password_hash(user["password"], password):
                flash("Incorrect password for this security account.", "error")
                return redirect(url_for("home"))

            session.clear()
            session["security_id"] = user["security_id"]
            session["security_username"] = user["name"]
            session["phone_no"] = user["phone_no"]
            session["security_phone"] = user["phone_no"]
            session["security_key"] = auth_code
            flash("Security login successful.", "success")
            return redirect(url_for("security_dashboard"))
                
        elif role == "Admin":
            query = "SELECT * FROM admins WHERE email = %s"
            cursor.execute(query, (email,))
            user = cursor.fetchone()
            if not user:
                flash("No admin account found with this email address.", "error")
                return redirect(url_for("home"))
            if not check_password_hash(user["password"], password):
                flash("Incorrect password for this admin account.", "error")
                return redirect(url_for("home"))

            session.clear()
            session["admin_id"] = user["admin_id"]
            session["admin_username"] = user["name"]
            session["phone_no"] = user["phone_no"]
            session["admin_phone"] = user["phone_no"]
            session["security_key"] = auth_code
            flash("Admin login successful.", "success")
            return redirect(url_for("admin_dashboard"))

    except Exception as e:
        flash(f"Database error: {e}", "error")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return redirect(url_for("home"))


@app.route("/student_login")
@app.route("/student_register")
def legacy_student_auth():
    return redirect(url_for("home"))


@app.route("/student_dashboard")
def student_dashboard():
    if "student_id" not in session:
        flash("Please login first.", "error")
        return redirect(url_for("home"))

    return render_template("student_dashboard.html")


@app.route("/apply_outpass", methods=["GET", "POST"])
def apply_outpass():
    if "student_id" not in session:
        flash("Please login first.", "error")
        return redirect(url_for("home"))

    if request.method == "POST":
        student_id = session["student_id"]
        reason = request.form["reason"]
        out_date = request.form["out_date"]
        out_time = request.form["out_time"]
        parent_contact = request.form["parent_contact"]

        try:
            out_date_obj = datetime.datetime.strptime(out_date, "%Y-%m-%d").date()
            if out_date_obj < datetime.date.today():
                flash("Out date cannot be in the past.", "error")
                return redirect(url_for("apply_outpass"))
        except ValueError:
            flash("Invalid date format.", "error")
            return redirect(url_for("apply_outpass"))

        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            query = """
                INSERT INTO outpass_requests 
                (student_id, reason, out_date, out_time, parent_contact, status)
                VALUES (%s, %s, %s, %s, %s, 'Pending')
            """
            values = (student_id, reason, out_date, out_time, parent_contact)

            cursor.execute(query, values)
            conn.commit()

            flash("Out pass request submitted successfully.", "success")
            return redirect(url_for("view_status"))
        except Exception as e:
            flash(f"Database error: {e}", "error")
            return redirect(url_for("apply_outpass"))
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    return render_template("apply_outpass.html")


@app.route("/view_status")
def view_status():
    if "student_id" not in session:
        flash("Please login first.", "error")
        return redirect(url_for("home"))

    student_id = session["student_id"]

    conn = None
    cursor = None
    requests_data = []
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT * FROM outpass_requests
            WHERE student_id = %s
            ORDER BY request_id ASC
        """
        cursor.execute(query, (student_id,))
        requests_data = cursor.fetchall()
    except Exception as e:
        flash(f"Database error: {e}", "error")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return render_template("view_status.html", requests_data=requests_data)


# ---------------- MENTOR MODULE ----------------

@app.route("/mentor_register")
@app.route("/mentor_login")
def legacy_mentor_auth():
    return redirect(url_for("home"))


@app.route("/mentor_dashboard")
def mentor_dashboard():
    if "mentor_id" not in session:
        flash("Please login as mentor first.", "error")
        return redirect(url_for("home"))

    conn = None
    cursor = None
    requests_data = []
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT 
                r.request_id,
                s.name,
                s.roll_no,
                s.department,
                s.year,
                r.reason,
                r.out_date,
                r.out_time,
                r.parent_contact,
                r.status,
                r.otp,
                r.mentor_remarks
            FROM outpass_requests r
            JOIN students s ON r.student_id = s.student_id
            ORDER BY r.request_id ASC
        """
        cursor.execute(query)
        requests_data = cursor.fetchall()
    except Exception as e:
        flash(f"Database error: {e}", "error")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return render_template("mentor_dashboard.html", requests_data=requests_data)


@app.route("/approve_request/<int:request_id>", methods=["POST"])
def approve_request(request_id):
    if "mentor_id" not in session:
        flash("Please login as mentor first.", "error")
        return redirect(url_for("mentor_login"))

    otp = str(random.randint(1000, 9999))

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
            UPDATE outpass_requests
            SET status = 'Approved',
                otp = %s,
                mentor_remarks = 'Approved by mentor',
                approved_at = NOW()
            WHERE request_id = %s
        """
        cursor.execute(query, (otp, request_id))
        conn.commit()
        flash(f"Request approved successfully. OTP generated: {otp}", "success")
    except Exception as e:
        flash(f"Database error: {e}", "error")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return redirect(url_for("mentor_dashboard"))


@app.route("/reject_request/<int:request_id>", methods=["POST"])
def reject_request(request_id):
    if "mentor_id" not in session:
        flash("Please login as mentor first.", "error")
        return redirect(url_for("mentor_login"))

    remarks = request.form.get("remarks", "Rejected by mentor")

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
            UPDATE outpass_requests
            SET status = 'Rejected',
                otp = NULL,
                mentor_remarks = %s
            WHERE request_id = %s
        """
        cursor.execute(query, (remarks, request_id))
        conn.commit()
        flash("Request rejected successfully.", "success")
    except Exception as e:
        flash(f"Database error: {e}", "error")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return redirect(url_for("mentor_dashboard"))


# ---------------- ADMIN MODULE ----------------

@app.route("/admin_register")
@app.route("/admin_login")
def legacy_admin_auth():
    return redirect(url_for("home"))


@app.route("/admin_dashboard")
def admin_dashboard():
    if "admin_id" not in session:
        flash("Please login as admin first.", "error")
        return redirect(url_for("home"))

    conn = None
    cursor = None
    students = []
    requests_data = []
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM students ORDER BY student_id ASC")
        students = cursor.fetchall()

        query = """
            SELECT 
                r.request_id,
                s.name,
                s.roll_no,
                r.reason,
                r.out_date,
                r.out_time,
                r.status,
                r.otp,
                r.mentor_remarks
            FROM outpass_requests r
            JOIN students s ON r.student_id = s.student_id
            ORDER BY r.request_id ASC
        """
        cursor.execute(query)
        requests_data = cursor.fetchall()
    except Exception as e:
        flash(f"Database error: {e}", "error")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return render_template(
        "admin_dashboard.html",
        students=students,
        requests_data=requests_data
    )


# ---------------- SECURITY MODULE ----------------

@app.route("/security_register")
@app.route("/security_login")
def legacy_security_auth():
    return redirect(url_for("home"))


@app.route("/security_dashboard", methods=["GET", "POST"])
def security_dashboard():
    if "security_id" not in session:
        flash("Please login as security first.", "error")
        return redirect(url_for("security_login"))

    result = None
    result_type = None

    if request.method == "POST":
        request_id = request.form["request_id"]
        otp = request.form["otp"]

        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            query = """
                SELECT 
                    r.request_id,
                    r.status,
                    r.otp,
                    s.name,
                    s.roll_no,
                    r.reason,
                    r.out_date,
                    r.out_time
                FROM outpass_requests r
                JOIN students s ON r.student_id = s.student_id
                WHERE r.request_id = %s
            """
            cursor.execute(query, (request_id,))
            outpass = cursor.fetchone()

            if outpass is None:
                result = "Invalid Request ID. No out-pass found."
                result_type = "error"

            elif outpass["status"] != "Approved":
                result = f"Pass not approved. Current status is {outpass['status']}."
                result_type = "error"

            elif outpass["out_date"] != datetime.date.today():
                result = f"Pass is for a different date: {outpass['out_date']}. Today is {datetime.date.today()}."
                result_type = "error"

            elif str(outpass["otp"]) != str(otp):
                result = "Invalid OTP. Please check Request ID and OTP."
                result_type = "error"

            else:
                insert_query = """
                    INSERT INTO security_logs 
                    (request_id, otp, verification_status)
                    VALUES (%s, %s, 'Exited')
                """
                cursor.execute(insert_query, (request_id, otp))
                
                # Update status of outpass request so it cannot be used again
                update_query = """
                    UPDATE outpass_requests 
                    SET status = 'Exited' 
                    WHERE request_id = %s
                """
                cursor.execute(update_query, (request_id,))
                
                conn.commit()

                result = (
                    f"Pass valid. Student allowed to exit. "
                    f"Name: {outpass['name']}, Roll No: {outpass['roll_no']}"
                )
                result_type = "success"

        except Exception as e:
            result = f"Database error: {e}"
            result_type = "error"
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    return render_template(
        "security_dashboard.html",
        result=result,
        result_type=result_type
    )


# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.", "success")
    return redirect(url_for("home"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)