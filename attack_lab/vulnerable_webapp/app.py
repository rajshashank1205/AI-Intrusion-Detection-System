from flask import Flask, render_template, request
import sqlite3
from pathlib import Path
from capture.http_capture import inspect_http_request

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "users.db"


@app.before_request
def monitor_request():

    # Ignore browser requests for favicon
    if request.path == "/favicon.ico":
        return

    inspect_http_request(request)


@app.route("/")
def home():
    return """
    <h1>AI Intrusion Detection System - Attack Lab</h1>
    <p>Welcome to the Vulnerable Web Application.</p>

    <ul>
        <li><a href="/login">Login</a></li>
        <li><a href="/search">Search</a></li>
        <li><a href="/comments">Comments (XSS Lab)</a></li>
        <li><a href="/admin">Admin</a></li>
    </ul>
    """


# ==========================================================
# SQL INJECTION LAB
# ==========================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    message = ""

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        # ==================================================
        # INTENTIONALLY VULNERABLE SQL QUERY
        # FOR SQL INJECTION TESTING ONLY
        # ==================================================

        query = (
            f"SELECT * FROM users "
            f"WHERE username='{username}' "
            f"AND password='{password}'"
        )

        print("\n========== SQL QUERY ==========")
        print(query)
        print("================================\n")

        try:
            cursor.execute(query)
            user = cursor.fetchone()

            if user:
                message = "Login Successful!"
            else:
                message = "Invalid Credentials"

        except Exception as e:
            message = f"Database Error: {e}"

        connection.close()

    return render_template("login.html", message=message)


# ==========================================================
# SEARCH PAGE
# ==========================================================

@app.route("/search")
def search():
    return "<h2>Search Page (Coming Soon)</h2>"


# ==========================================================
# XSS LAB
# ==========================================================

@app.route("/comments", methods=["GET", "POST"])
def comments():

    comment = ""

    if request.method == "POST":
        comment = request.form.get("comment", "")

    return f"""
    <!DOCTYPE html>

    <html>

    <head>
        <title>XSS Attack Lab</title>
    </head>

    <body>

        <h2>XSS Vulnerable Comments Page</h2>

        <p>
        Enter any comment below.
        This page intentionally displays your input without
        sanitization for XSS testing.
        </p>

        <form method="POST">

            <input
                type="text"
                name="comment"
                placeholder="Enter your comment"
                style="width:400px;"
            >

            <button type="submit">
                Post Comment
            </button>

        </form>

        <hr>

        <h3>Latest Comment</h3>

        {comment}

    </body>

    </html>
    """


# ==========================================================
# ADMIN PAGE
# ==========================================================

@app.route("/admin")
def admin():
    return "<h2>Admin Page (Coming Soon)</h2>"


if __name__ == "__main__":
    app.run(debug=True)