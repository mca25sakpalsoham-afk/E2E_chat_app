import base64
import time
from flask import jsonify
from crypto.crypto_utils import AES_KEY, decrypt_message
from flask import request
from flask import Flask, render_template, request, redirect, session, url_for
from flask_socketio import SocketIO, send
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_db_connection
from crypto.crypto_utils import encrypt_message
from flask import session
from db import get_db_connection
import smtplib
import os
from flask_socketio import SocketIO, emit, join_room
from email.message import EmailMessage
from dotenv import load_dotenv
from collections import defaultdict
from datetime import datetime
from flask import abort
import csv
from flask import send_file
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import StringIO, BytesIO



from datetime import datetime, timedelta

from security_tests import run_encryption_integrity_check
load_dotenv()

# 🚫 Brute-force protection storage

failed_by_minute = defaultdict(int)

def encryption_integrity_test():
    start = time.time()

    test_message = "SECURITY_TEST_PAYLOAD"

    try:
        encrypted = encrypt_message(test_message)
        decrypted = decrypt_message(encrypted)

        if decrypted != test_message:
            return {
                "status": "FAIL",
                "details": "Decrypted text does not match original",
                "time": round((time.time() - start) * 1000, 2)
            }

        return {
            "status": "PASS",
            "details": "AES encryption, MAC, and decryption verified",
            "time": round((time.time() - start) * 1000, 2)
        }

    except Exception as e:
        return {
            "status": "FAIL",
            "details": f"Exception: {str(e)}",
            "time": round((time.time() - start) * 1000, 2)
        }

def tampering_attack_test():
    start = time.time()

    try:
        original = "ATTACK_SIMULATION"
        encrypted = encrypt_message(original)

        raw = bytearray(base64.b64decode(encrypted))
        raw[-1] ^= 0x01  # flip last bit (tamper)
        tampered = base64.b64encode(raw).decode()

        try:
            decrypt_message(tampered)
            return {
                "status": "FAIL",
                "details": "Tampered message was decrypted (SECURITY RISK)",
                "time": round((time.time() - start) * 1000, 2)
            }
        except:
            return {
                "status": "PASS",
                "details": "Tampering detected: MAC verification failed",
                "time": round((time.time() - start) * 1000, 2)
            }

    except Exception as e:
        return {
            "status": "FAIL",
            "details": str(e),
            "time": round((time.time() - start) * 1000, 2)
        }

    
def security_log(event):
    with open("security.log", "a") as f:
        f.write(f"[{datetime.now()}] {event}\n")

def send_admin_registration_alert(username, ip):
    try:
        msg = EmailMessage()
        msg["Subject"] = "🆕 New User Registration Alert"
        msg["From"] = os.getenv("SMTP_EMAIL")
        msg["To"] = os.getenv("ADMIN_EMAIL")

        msg.set_content(f"""
NEW USER REGISTRATION ALERT 🚨

A new user has registered on the system.

Username   : {username}
IP Address : {ip}
Time       : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Please review if this registration is authorized.
        """)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(
                os.getenv("SMTP_EMAIL"),
                os.getenv("SMTP_PASSWORD")
            )
            server.send_message(msg)

    except Exception as e:
        security_log(f"EMAIL REGISTRATION ALERT FAILED - error={str(e)}")


app = Flask(__name__)
app.secret_key = "supersecretkey"

socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode="eventlet"
)

security_log("SECURE HTTP HEADERS CONFIGURED")

ADMIN_USERS = ["admin"]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    message = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hashed_password = generate_password_hash(password)

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (%s, %s)",
                (username, hashed_password)
            )
            conn.commit()
            conn.close()
            message = "Registration successful!"
            send_admin_registration_alert(username, request.remote_addr)

        except Exception:
            message = "Username already exists!"

    return render_template("register.html", message=message)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        ip = request.remote_addr

        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)

        cur.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cur.fetchone()

        # 🚫 User does not exist
        if not user:
            conn.close()
            security_log(f"LOGIN FAILED - user={username} - ip={ip}")
            return render_template("login.html", message="Invalid username or password")

        # 🚫 Account locked
        if user["is_locked"]:
            conn.close()
            security_log(f"LOCKED ACCOUNT LOGIN ATTEMPT - user={username} - ip={ip}")
            return render_template("login.html", message="Account locked. Contact admin.")

        # ✅ Correct password
        if check_password_hash(user["password"], password):
            session.clear()
            session["user"] = username

            cur.execute("""
                UPDATE users
                SET failed_attempts = 0,
                    last_login = NOW(),
                    login_count = login_count + 1
                WHERE username = %s
            """, (username,))
            conn.commit()
            conn.close()

            security_log(f"LOGIN SUCCESS - user={username} - ip={ip}")
            return redirect("/chats")

        # ❌ Wrong password
        cur.execute("""
            UPDATE users
            SET failed_attempts = failed_attempts + 1
            WHERE username = %s
        """, (username,))
        conn.commit()

        cur.execute("SELECT failed_attempts FROM users WHERE username=%s", (username,))
        attempts = cur.fetchone()

        if attempts and attempts["failed_attempts"] >= 5:
            cur.execute("UPDATE users SET is_locked = TRUE WHERE username=%s", (username,))
            conn.commit()
            conn.close()

            security_log(f"ACCOUNT LOCKED - user={username} - ip={ip}")
            return render_template(
                "login.html",
                message="Account locked due to multiple failed attempts."
            )

        conn.close()
        security_log(f"LOGIN FAILED - user={username} - ip={ip}")
        return render_template("login.html", message="Invalid username or password")

    return render_template("login.html")

@app.route("/chats")
def chat_list():
    if "user" not in session:
        return redirect("/login")

    current_user = session["user"]

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT 
            u.username,
            COUNT(m.id) AS unread
        FROM users u
        LEFT JOIN messages m
            ON m.sender = u.username
            AND m.receiver = %s
            AND m.is_read = FALSE
        WHERE u.username != %s
        GROUP BY u.username
    """, (current_user, current_user))

    users = cur.fetchall()
    conn.close()

    return render_template("chat_list.html", users=users)



@app.route("/chat/<chat_user>")
def private_chat(chat_user):
    if "user" not in session:
        return redirect("/login")

    current_user = session["user"]

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    # ✅ MARK MESSAGES AS READ (THIS WAS MISSING)
    cur.execute("""
        UPDATE messages
        SET is_read = TRUE
        WHERE sender = %s AND receiver = %s
    """, (chat_user, current_user))
    conn.commit()

    # Load messages
    cur.execute("""
        SELECT sender, encrypted_message, timestamp
        FROM messages
        WHERE (sender=%s AND receiver=%s)
           OR (sender=%s AND receiver=%s)
        ORDER BY timestamp
    """, (current_user, chat_user, chat_user, current_user))

    messages = cur.fetchall()
    conn.close()

    for msg in messages:
        try:
            msg["decrypted_message"] = decrypt_message(msg["encrypted_message"])
        except Exception:
            msg["decrypted_message"] = "🔒 Unable to decrypt message"

    return render_template(
        "private_chat.html",
        chat_user=chat_user,
        messages=messages
    )



@app.route("/chat")
def chat():
    if "user" not in session:
        return redirect("/login")
    return render_template("chat.html", username=session["user"])

@app.route("/admin")
def admin_home():
    # Admin already logged in
    if session.get("admin"):
        return redirect("/admin/dashboard")

    # Normal user trying to access admin
    if session.get("user"):
        security_log(
            f"UNAUTHORIZED ADMIN PAGE ACCESS - user={session.get('user')} - ip={request.remote_addr}"
        )
        abort(403)  # Forbidden

    # Not logged in at all
    return redirect("/admin/login")


@app.route("/admin/dashboard")
def admin_dashboard():
    if not session.get("admin"):
        security_log(f"UNAUTHORIZED ADMIN ACCESS - ip={request.remote_addr}")
        return redirect("/admin/login")

    # -------------------------
    # DATABASE METRICS
    # -------------------------
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    # Total users
    cur.execute("SELECT COUNT(*) AS total FROM users")
    total_users = cur.fetchone()["total"]

    # Registrations today
    cur.execute("""
        SELECT COUNT(*) AS today
        FROM users
        WHERE DATE(created_at) = CURDATE()
    """)
    today_users = cur.fetchone()["today"]

    # Total successful logins (CORRECT SOURCE)
    cur.execute("SELECT SUM(login_count) AS total FROM users")
    success_logins = cur.fetchone()["total"] or 0

    conn.close()

    # -------------------------
    # LOG-BASED METRICS
    # -------------------------
    failed_logins = 0
    last_login = "N/A"
    recent_events = []
    failed_by_minute.clear()

    try:
        with open("security.log", "r") as f:
            logs = f.readlines()

        for line in logs:
            if "LOGIN FAILED" in line:
                failed_logins += 1

                try:
                    ts = line.split("]")[0].replace("[", "")
                    minute = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S.%f")
                    minute_key = minute.strftime("%H:%M")
                    failed_by_minute[minute_key] += 1
                except:
                    pass

            if "LOGIN SUCCESS" in line:
                last_login = line.split("]")[0].replace("[", "")

        recent_events = logs[-10:][::-1]

    except Exception as e:
        print("Log read error:", e)

    failed_times = list(failed_by_minute.keys())[-10:]
    failed_counts = list(failed_by_minute.values())[-10:]

    # -------------------------
    # LOGIN SPIKE ALERT
    # -------------------------
    alert_level = None
    alert_message = None

    if failed_logins >= 20:
        alert_level = "critical"
        alert_message = f"🚨 CRITICAL: {failed_logins} failed login attempts detected"
        security_log(f"LOGIN SPIKE CRITICAL - failed={failed_logins}")
    elif failed_logins >= 10:
        alert_level = "warning"
        alert_message = f"⚠️ WARNING: {failed_logins} failed login attempts detected"
        security_log(f"LOGIN SPIKE WARNING - failed={failed_logins}")

    return render_template(
        "admin_dashboard.html",
        total_users=total_users,
        today_users=today_users,
        failed_logins=failed_logins,
        success_logins=success_logins,
        last_login=last_login,
        recent_events=recent_events,
        alert_level=alert_level,
        alert_message=alert_message,
        failed_times=failed_times,
        failed_counts=failed_counts
    )



@app.route("/admin/logs")
def admin_logs():
    admin = session.get("admin")

    if not admin:
        security_log(f"UNAUTHORIZED LOG ACCESS - ip={request.remote_addr}")
        return redirect("/admin/login")

    page = int(request.args.get("page", 1))
    per_page = 20
    offset = (page - 1) * per_page

    with open("security.log", "r") as f:
        logs = f.readlines()

    logs = logs[::-1]  # latest first
    total = len(logs)
    page_logs = logs[offset: offset + per_page]
    total_pages = (total + per_page - 1) // per_page

    return render_template(
        "admin_logs.html",
        logs=page_logs,
        page=page,
        total_pages=total_pages
    )


@app.route("/admin/export/csv")
def export_logs_csv():
    if not session.get("admin"):
        return redirect("/admin/login")

    # Step 1: Write CSV to StringIO (TEXT)
    text_stream = StringIO()
    writer = csv.writer(text_stream)

    writer.writerow(["Timestamp", "Event"])

    with open("security.log", "r") as f:
        for line in f:
            if "] " in line:
                timestamp, event = line.split("] ", 1)
                writer.writerow([
                    timestamp.replace("[", ""),
                    event.strip()
                ])

    # Step 2: Convert text → bytes
    byte_stream = BytesIO()
    byte_stream.write(text_stream.getvalue().encode("utf-8"))
    byte_stream.seek(0)

    return send_file(
        byte_stream,
        mimetype="text/csv",
        as_attachment=True,
        download_name="security_logs.csv"
    )


@app.route("/admin/export/pdf")
def export_logs_pdf():
    if not session.get("admin"):
        return redirect("/admin/login")

    filename = "security_logs.pdf"
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    y = height - 40
    c.setFont("Helvetica", 9)

    c.drawString(40, y, "Security Logs Report")
    y -= 20
    c.drawString(40, y, f"Generated on: {datetime.now()}")
    y -= 30

    with open("security.log", "r") as f:
        for line in f:
            if y < 40:
                c.showPage()
                c.setFont("Helvetica", 9)
                y = height - 40

            c.drawString(40, y, line.strip())
            y -= 12

    c.save()

    return send_file(filename, as_attachment=True)

@app.route("/logout")
def logout():
    user = session.get("user", "unknown")
    ip = request.remote_addr

    security_log(f"LOGOUT - user={user} - ip={ip}")

    session.clear()
    return redirect("/login")

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM admins WHERE username=%s", (username,))
        admin = cur.fetchone()
        conn.close()

        if admin and check_password_hash(admin["password_hash"], password):
            session.clear()
            session["admin"] = username
            security_log(f"ADMIN LOGIN SUCCESS - admin={username} - ip={request.remote_addr}")
            return redirect("/admin/dashboard")

        security_log(f"ADMIN LOGIN FAILED - admin={username} - ip={request.remote_addr}")
        return render_template("admin_login.html", message="Invalid admin credentials")

    return render_template("admin_login.html")

@app.route("/admin/users")
def admin_users():
    if not session.get("admin"):
        return redirect("/admin/login")

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT id, username, failed_attempts, is_locked, last_login
        FROM users
    """)
    users = cur.fetchall()
    conn.close()

    return render_template("admin_users.html", users=users)

@app.route("/admin/users/toggle/<int:user_id>")
def toggle_user(user_id):
    if not session.get("admin"):
        return redirect("/admin/login")

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE users
        SET is_locked = NOT is_locked,
            failed_attempts = 0
        WHERE id = %s
    """, (user_id,))
    conn.commit()
    conn.close()

    security_log(f"ADMIN TOGGLED USER STATUS - user_id={user_id}")

    return redirect("/admin/users")

@app.route("/admin/testing")
def admin_testing():
    if not session.get("admin"):
        abort(403)

    return render_template("admin_testing.html")


TEST_LOG = []

@app.route("/admin/testing/encryption")
def run_encryption_test():
    if not session.get("admin"):
        abort(403)

    result = encryption_integrity_test()

    log_entry = {
        "time": datetime.now().strftime("%H:%M:%S"),
        "status": result["status"],
        "ms": result["time"]
    }
    TEST_LOG.append(log_entry)

    return jsonify(result)


@app.route("/admin/testing/history")
def encryption_history():
    if not session.get("admin"):
        abort(403)
    return jsonify(TEST_LOG[-10:])

@app.route("/admin/testing/tamper")
def run_tamper_test():
    if not session.get("admin"):
        abort(403)

    result = tampering_attack_test()

    TEST_LOG.append({
        "time": datetime.now().strftime("%H:%M:%S"),
        "status": result["status"],
        "ms": result["time"]
    })

    return jsonify(result)

@app.route("/admin/testing/key-strength")
def key_strength_test():
    if not session.get("admin"):
        abort(403)

    key_len = len(AES_KEY)

    if key_len == 16:
        strength = "MEDIUM"
        score = 6
    elif key_len == 24:
        strength = "STRONG"
        score = 8
    elif key_len == 32:
        strength = "VERY STRONG"
        score = 10
    else:
        strength = "INVALID"
        score = 0

    return jsonify({
        "status": "PASS",
        "key_length": key_len * 8,
        "strength": strength,
        "score": score
    })



from crypto.crypto_utils import encrypt_message, decrypt_message

from crypto.crypto_utils import encrypt_message, decrypt_message
from flask import session
from db import get_db_connection


@socketio.on("typing")
def handle_typing(username):
    socketio.emit("typing", username)

@socketio.on("stop_typing")
def handle_stop_typing():
    socketio.emit("stop_typing")

@socketio.on("join")
def handle_join(data):
    username = data.get("username")
    if not username:
        return

    join_room(username)


@socketio.on("send_message")
def handle_send_message(data):
    sender = session.get("user")          #secure
    receiver = data.get("receiver")
    message = data.get("message")

    if not sender or not receiver or not message:
        return

    encrypted = encrypt_message(message)

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO messages (sender, receiver, encrypted_message, is_read)
        VALUES (%s, %s, %s, FALSE)
    """, (sender, receiver, encrypted))
    conn.commit()
    conn.close()

    payload = {
        "sender": sender,
        "receiver": receiver,
        "message": message,
        "time": datetime.now().strftime("%H:%M")
    }

    # Send to both users
    socketio.emit("new_message", payload, room=sender)
    socketio.emit("new_message", payload, room=receiver)

@socketio.on("mark_read")
def mark_read(data):
    sender = data["sender"]
    receiver = data["receiver"]

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE messages
        SET is_read = TRUE
        WHERE sender=%s AND receiver=%s
    """, (sender, receiver))
    conn.commit()
    conn.close()

    # 🔕 tell UI to remove badge
    socketio.emit("badge_clear", {
        "from": sender
    }, room=receiver)



@app.route("/security-logs")
def security_logs():
    # Access control
    if "user" not in session:
        return redirect("/login")

    logs = []
    try:
        with open("security.log", "r") as f:
            logs = f.readlines()
    except FileNotFoundError:
        logs = ["No security logs found."]

    # Show latest logs first
    logs.reverse()

    return render_template("security_logs.html", logs=logs)


@app.after_request
def add_csp(response):
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://cdn.socket.io https://cdn.jsdelivr.net; "
        "connect-src 'self' ws://127.0.0.1:5000 http://127.0.0.1:5000; "
        "style-src 'self' 'unsafe-inline';"
    )
    return response




if __name__ == "__main__":
    socketio.run(app, debug=True)
