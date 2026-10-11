from flask import Flask, render_template, request, redirect, url_for, session, flash
import psycopg2
from psycopg2.extras import RealDictCursor
import psycopg2.errors
from werkzeug.security import generate_password_hash, check_password_hash
import random
import os
import datetime

# Safe load of local environment variables (if python-dotenv is present)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "outpass_secret_key")


def get_db_connection():
    db_url = os.environ.get("DATABASE_URL") or os.environ.get("POSTGRES_URL") or os.environ.get("SUPABASE_DB_URL")
    if db_url:
        return psycopg2.connect(db_url)

    return psycopg2.connect(
        host=os.environ.get("PGHOST") or os.environ.get("SUPABASE_HOST", "127.0.0.1"),
        user=os.environ.get("PGUSER") or os.environ.get("SUPABASE_USER", "postgres"),
        password=os.environ.get("PGPASSWORD") or os.environ.get("SUPABASE_PASSWORD", ""),
        database=os.environ.get("PGDATABASE") or os.environ.get("SUPABASE_DATABASE", "postgres"),
        port=int(os.environ.get("PGPORT") or os.environ.get("SUPABASE_PORT", 5432))
    )



ADMIN_AUTH_KEY = os.environ.get("ADMIN_AUTH_KEY", "adminpass@123")
MENTOR_AUTH_KEY = os.environ.get("MENTOR_AUTH_KEY", "mentorpass123")
SECURITY_AUTH_KEY = os.environ.get("SECURITY_AUTH_KEY", "securitypass123")


@app.route("/")
@app.route("/app.py")
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
    hashed_password = generate_password_hash(password)

    if role == "Admin":
        flash("Administrator accounts cannot be created via public registration.", "error")
        return redirect(url_for("home"))

    if confirm_password and password != confirm_password:
        flash("Passwords do not match. Please re-enter your password.", "error")
        return redirect(url_for("home"))

    # Security check for Security & Mentor registration
    if role == "Security":
        auth_code = request.form.get("auth_code")
        if auth_code != SECURITY_AUTH_KEY:
            flash("Invalid security authorization key.", "error")
            return redirect(url_for("home"))
    elif role == "Mentor":
        auth_code = request.form.get("auth_code")
        if auth_code != MENTOR_AUTH_KEY:
            flash("Invalid security authorization key.", "error")
            return redirect(url_for("home"))

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        if role == "Student":
            roll_no = request.form["roll_no"]
            department = request.form.get("department", "CSE")
            year = request.form.get("year", "1st Year")
            query = """
                INSERT INTO students (name, roll_no, email, password, phone_no, department, year)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (name, roll_no, email, hashed_password, phone_no, department, year))
            conn.commit()
            flash("Student registration successful. Please login.", "success")

        elif role == "Mentor":
            staff_id = request.form["staff_id"]
            query = """
                INSERT INTO mentors (name, email, password, staff_id, phone_no)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (name, email, hashed_password, staff_id, phone_no))
            conn.commit()
            flash("Mentor registration successful. Please login.", "success")

        elif role == "Security":
            query = """
                INSERT INTO security_users (name, email, password, phone_no)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (name, email, hashed_password, phone_no))
            conn.commit()
            flash("Security guard registration successful. Please login.", "success")

        elif role == "Admin":
            query = """
                INSERT INTO admins (name, email, password, phone_no)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (name, email, hashed_password, phone_no))
            conn.commit()
            flash("Admin registration successful. Please login.", "success")

    except psycopg2.IntegrityError:
        flash("Email, Roll No, or Staff ID already exists.", "error")
    except Exception as e:
        flash(f"Database error: {e}", "error")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return redirect(url_for("home"))


@app.route("/login", methods=["POST"])
def login():
    role = request.form["role"]
    email = request.form["email"]
    password = request.form["password"]

    # Authorization code check for Admin, Security, & Mentor login
    if role == "Admin":
        auth_code = request.form.get("auth_code")
        if auth_code != ADMIN_AUTH_KEY:
            flash("Invalid security authorization key.", "error")
            return redirect(url_for("home"))
    elif role == "Security":
        auth_code = request.form.get("auth_code")
        if auth_code != SECURITY_AUTH_KEY:
            flash("Invalid security authorization key.", "error")
            return redirect(url_for("home"))
    elif role == "Mentor":
        auth_code = request.form.get("auth_code")
        if auth_code != MENTOR_AUTH_KEY:
            flash("Invalid security authorization key.", "error")
            return redirect(url_for("home"))

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

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

            cursor.execute("UPDATE students SET last_login = NOW() WHERE student_id = %s", (user["student_id"],))
            conn.commit()

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

            cursor.execute("UPDATE mentors SET last_login = NOW() WHERE mentor_id = %s", (user["mentor_id"],))
            conn.commit()

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

            cursor.execute("UPDATE security_users SET last_login = NOW() WHERE security_id = %s", (user["security_id"],))
            conn.commit()

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

            cursor.execute("UPDATE admins SET last_login = NOW() WHERE admin_id = %s", (user["admin_id"],))
            conn.commit()

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

    conn = None
    cursor = None
    mentors_count = 0
    requests_count = 0
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        cursor.execute("SELECT COUNT(*) AS count FROM mentors")
        res = cursor.fetchone()
        if res:
            mentors_count = res["count"]

        cursor.execute("SELECT COUNT(*) AS count FROM outpass_requests WHERE student_id = %s", (session["student_id"],))
        res2 = cursor.fetchone()
        if res2:
            requests_count = res2["count"]
    except Exception as e:
        flash(f"Database error: {e}", "error")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return render_template("student_dashboard.html", mentors_count=mentors_count, requests_count=requests_count)


@app.route("/student_mentors")
def student_mentors():
    if "student_id" not in session:
        flash("Please login first.", "error")
        return redirect(url_for("home"))

    conn = None
    cursor = None
    mentors = []
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT mentor_id, name, staff_id, email, phone_no, last_login FROM mentors ORDER BY mentor_id ASC")
        mentors = cursor.fetchall()
    except Exception as e:
        flash(f"Database error: {e}", "error")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return render_template("student_mentors.html", mentors=mentors)


@app.route("/apply_outpass", methods=["GET", "POST"])
def apply_outpass():
    if "student_id" not in session:
        flash("Please login first.", "error")
        return redirect(url_for("home"))

    conn = None
    cursor = None
    mentors = []

    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT mentor_id, name, staff_id FROM mentors ORDER BY name ASC")
        mentors = cursor.fetchall()

        if request.method == "POST":
            student_id = session["student_id"]
            mentor_id = request.form.get("mentor_id")
            if not mentor_id or mentor_id == "all" or mentor_id == "None":
                mentor_id = None
            else:
                mentor_id = int(mentor_id)

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

            query = """
                INSERT INTO outpass_requests 
                (student_id, mentor_id, reason, out_date, out_time, parent_contact, status)
                VALUES (%s, %s, %s, %s, %s, %s, 'Pending')
            """
            values = (student_id, mentor_id, reason, out_date, out_time, parent_contact)

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

    return render_template("apply_outpass.html", mentors=mentors)


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
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        query = """
            SELECT r.*, m.name AS mentor_name 
            FROM outpass_requests r
            LEFT JOIN mentors m ON r.mentor_id = m.mentor_id
            WHERE r.student_id = %s
            ORDER BY r.request_id DESC
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
    student_count = 0
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

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
                r.mentor_remarks,
                r.mentor_id,
                m.name AS mentor_name
            FROM outpass_requests r
            JOIN students s ON r.student_id = s.student_id
            LEFT JOIN mentors m ON r.mentor_id = m.mentor_id
            ORDER BY r.request_id DESC
        """
        cursor.execute(query)
        requests_data = cursor.fetchall()

        cursor.execute("SELECT COUNT(*) AS count FROM students")
        res = cursor.fetchone()
        if res:
            student_count = res["count"]
    except Exception as e:
        flash(f"Database error: {e}", "error")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return render_template("mentor_dashboard.html", requests_data=requests_data, student_count=student_count)


@app.route("/mentor_students")
def mentor_students():
    if "mentor_id" not in session:
        flash("Please login as mentor first.", "error")
        return redirect(url_for("home"))

    conn = None
    cursor = None
    students = []
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        cursor.execute("""
            SELECT student_id, name, roll_no, department, year, email, phone_no, last_login 
            FROM students 
            ORDER BY student_id ASC
        """)
        students = cursor.fetchall()
    except Exception as e:
        flash(f"Database error: {e}", "error")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return render_template("mentor_students.html", students=students)


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
    student_count = 0
    mentor_count = 0
    security_count = 0
    request_count = 0
    pending_count = 0
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        cursor.execute("SELECT COUNT(*) AS count FROM students")
        student_count = cursor.fetchone()["count"]

        cursor.execute("SELECT COUNT(*) AS count FROM mentors")
        mentor_count = cursor.fetchone()["count"]

        cursor.execute("SELECT COUNT(*) AS count FROM security_users")
        security_count = cursor.fetchone()["count"]

        cursor.execute("SELECT COUNT(*) AS count FROM outpass_requests")
        request_count = cursor.fetchone()["count"]

        cursor.execute("SELECT COUNT(*) AS count FROM outpass_requests WHERE status = 'Pending'")
        pending_count = cursor.fetchone()["count"]
    except Exception as e:
        flash(f"Database error: {e}", "error")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return render_template(
        "admin_dashboard.html",
        student_count=student_count,
        mentor_count=mentor_count,
        security_count=security_count,
        request_count=request_count,
        pending_count=pending_count
    )


@app.route("/admin_accounts")
def admin_accounts():
    if "admin_id" not in session:
        flash("Please login as admin first.", "error")
        return redirect(url_for("home"))

    conn = None
    cursor = None
    students = []
    mentors = []
    security_users = []
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        cursor.execute("""
            SELECT student_id, name, roll_no, email, department, year, phone_no, last_login 
            FROM students 
            ORDER BY student_id ASC
        """)
        students = cursor.fetchall()

        cursor.execute("""
            SELECT mentor_id, name, staff_id, email, phone_no, last_login 
            FROM mentors 
            ORDER BY mentor_id ASC
        """)
        mentors = cursor.fetchall()

        cursor.execute("""
            SELECT security_id, name, email, phone_no, last_login 
            FROM security_users 
            ORDER BY security_id ASC
        """)
        security_users = cursor.fetchall()
    except Exception as e:
        flash(f"Database error: {e}", "error")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return render_template(
        "admin_accounts.html",
        students=students,
        mentors=mentors,
        security_users=security_users
    )


@app.route("/admin_outpasses")
def admin_outpasses():
    if "admin_id" not in session:
        flash("Please login as admin first.", "error")
        return redirect(url_for("home"))

    conn = None
    cursor = None
    requests_data = []
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

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
                r.mentor_remarks,
                m.name AS mentor_name
            FROM outpass_requests r
            JOIN students s ON r.student_id = s.student_id
            LEFT JOIN mentors m ON r.mentor_id = m.mentor_id
            ORDER BY r.request_id DESC
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

    return render_template("admin_outpasses.html", requests_data=requests_data)


# ---------------- SECURITY MODULE ----------------

@app.route("/security_register")
@app.route("/security_login")
def legacy_security_auth():
    return redirect(url_for("home"))


@app.route("/security_dashboard", methods=["GET", "POST"])
def security_dashboard():
    if "security_id" not in session:
        flash("Please login as security first.", "error")
        return redirect(url_for("home"))

    result = None
    result_type = None
    history_count = 0

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        if request.method == "POST":
            request_id = request.form["request_id"]
            otp = request.form["otp"]

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
                result = "Invalid Request ID. No outpass record found."
                result_type = "error"

            elif outpass["status"] != "Approved":
                result = f"Pass not approved for exit. Current status is '{outpass['status']}'."
                result_type = "error"

            elif outpass["out_date"] != datetime.date.today():
                result = f"Date mismatch: Pass is scheduled for {outpass['out_date']}. Today is {datetime.date.today()}."
                result_type = "error"

            elif str(outpass["otp"]) != str(otp):
                result = "Invalid verification OTP code. Gate exit denied."
                result_type = "error"

            else:
                insert_query = """
                    INSERT INTO security_logs 
                    (request_id, otp, verification_status, exit_time)
                    VALUES (%s, %s, 'Exited', NOW())
                """
                cursor.execute(insert_query, (request_id, otp))

                update_query = """
                    UPDATE outpass_requests 
                    SET status = 'Exited' 
                    WHERE request_id = %s
                """
                cursor.execute(update_query, (request_id,))
                conn.commit()

                result = (
                    f"Pass Validated. Exit Authorized for {outpass['name']} (Roll: {outpass['roll_no']})."
                )
                result_type = "success"

        cursor.execute("SELECT COUNT(*) AS count FROM security_logs")
        res = cursor.fetchone()
        if res:
            history_count = res["count"]

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
        result_type=result_type,
        history_count=history_count
    )


@app.route("/security_history")
def security_history():
    if "security_id" not in session:
        flash("Please login as security first.", "error")
        return redirect(url_for("home"))

    conn = None
    cursor = None
    history_logs = []
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        history_query = """
            SELECT 
                l.log_id,
                l.request_id,
                l.otp,
                l.verification_status,
                l.exit_time,
                s.name,
                s.roll_no,
                s.department,
                r.out_date,
                r.out_time,
                r.reason
            FROM security_logs l
            JOIN outpass_requests r ON l.request_id = r.request_id
            JOIN students s ON r.student_id = s.student_id
            ORDER BY l.log_id DESC
        """
        cursor.execute(history_query)
        history_logs = cursor.fetchall()
    except Exception as e:
        flash(f"Database error: {e}", "error")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return render_template("security_history.html", history_logs=history_logs)


# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.", "success")
    return redirect(url_for("home"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)