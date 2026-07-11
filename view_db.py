import mysql.connector

def view_live_database_records():
    try:
        # Connect to your live Railway cloud database
        conn = mysql.connector.connect(
            host="tokaido.proxy.rlwy.net",
            user="root",
            password="MwqKirqHVafXeICEDzsaYMzrzhmcUHMZ",
            port=16493,
            database="outpass_system"
        )
        cursor = conn.cursor(dictionary=True)

        print("\n==================================================")
        print("          LIVE SYSTEM AUDIT RECORDS               ")
        print("==================================================")

        # 1. Fetch and print registered students
        print("\n--- REGISTERED STUDENTS ---")
        cursor.execute("SELECT name, email, roll_no, phone_no, department, year FROM students ORDER BY student_id ASC")
        students = cursor.fetchall()
        if not students:
            print("No students registered yet.")
        for student in students:
            print(f"[{student['roll_no']}] {student['name']} | Email: {student['email']} | Dept: {student['department']} ({student['year']}) | Phone: {student['phone_no']}")

        # 2. Fetch and print registered mentors
        print("\n--- REGISTERED MENTORS ---")
        cursor.execute("SELECT name, email, staff_id, phone_no FROM mentors ORDER BY mentor_id ASC")
        mentors = cursor.fetchall()
        if not mentors:
            print("No mentors registered yet.")
        for mentor in mentors:
            print(f"[{mentor['staff_id']}] {mentor['name']} | Email: {mentor['email']} | Phone: {mentor['phone_no']}")

        # 3. Fetch and print registered security guards
        print("\n--- REGISTERED SECURITY GUARDS ---")
        cursor.execute("SELECT name, email, phone_no FROM security_users ORDER BY security_id ASC")
        security_guards = cursor.fetchall()
        if not security_guards:
            print("No security guards registered yet.")
        for guard in security_guards:
            print(f"{guard['name']} | Email: {guard['email']} | Phone: {guard['phone_no']}")

        # 4. Fetch and print outpass requests
        print("\n--- LIVE OUTPASS REQUESTS & STATUS ---")
        cursor.execute("""
            SELECT r.request_id, s.name as student_name, s.roll_no, r.reason, r.out_date, r.out_time, r.status, r.otp, r.mentor_remarks
            FROM outpass_requests r
            JOIN students s ON r.student_id = s.student_id
            ORDER BY r.request_id ASC
        """)
        requests = cursor.fetchall()
        if not requests:
            print("No outpass requests submitted yet.")
        for req in requests:
            print(f"Pass #{req['request_id']} | Student: {req['student_name']} ({req['roll_no']})")
            print(f"  Reason: {req['reason']}")
            print(f"  Schedule: {req['out_date']} at {req['out_time']} | Status: {req['status']}")
            print(f"  OTP: {req['otp'] or '-'} | Remarks: {req['mentor_remarks'] or '-'}")
            print("-" * 50)

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Failed to connect to cloud database: {e}")

if __name__ == "__main__":
    view_live_database_records()
