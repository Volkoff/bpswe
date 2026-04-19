from flask import Flask, render_template
import pymysql

app = Flask(__name__)

def get_connection():
    return pymysql.connect(
        host="mysql",
        user="student",
        password="1234",
        database="hosting_center",
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route("/")
def dashboard():
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) AS count FROM users")
        users_count = cursor.fetchone()["count"]

        cursor.execute("SELECT COUNT(*) AS count FROM domains")
        domains_count = cursor.fetchone()["count"]

        cursor.execute("SELECT COUNT(*) AS count FROM ftp_accounts")
        ftp_count = cursor.fetchone()["count"]

    conn.close()
    return render_template(
        "dashboard.html",
        users_count=users_count,
        domains_count=domains_count,
        ftp_count=ftp_count
    )

@app.route("/users")
def users():
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT user_id, username, email, role, home_directory
            FROM users
            ORDER BY user_id
        """)
        users = cursor.fetchall()
    conn.close()
    return render_template("users.html", users=users)

@app.route("/domains")
def domains():
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT d.domain_id, d.domain_name, d.document_root, d.active, u.username
            FROM domains d
            LEFT JOIN users u ON d.user_id = u.user_id
            ORDER BY d.domain_id
        """)
        domains = cursor.fetchall()
    conn.close()
    return render_template("domains.html", domains=domains)

@app.route("/ftp")
def ftp():
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT f.account_id, f.username, f.directory, f.quota, u.username AS owner
            FROM ftp_accounts f
            LEFT JOIN users u ON f.user_id = u.user_id
            ORDER BY f.account_id
        """)
        ftp_accounts = cursor.fetchall()
    conn.close()
    return render_template("ftp.html", ftp_accounts=ftp_accounts)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
