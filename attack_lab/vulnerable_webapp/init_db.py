import sqlite3

# Connect to the database (creates it if it doesn't exist)
connection = sqlite3.connect("users.db")

cursor = connection.cursor()

# Create the users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
)
""")

# Clear existing records (optional, for repeatable tests)
cursor.execute("DELETE FROM users")

# Insert sample users
users = [
    ("admin", "admin123"),
    ("alice", "alice123"),
    ("bob", "bob123")
]

cursor.executemany(
    "INSERT INTO users (username, password) VALUES (?, ?)",
    users
)

connection.commit()
connection.close()

print("Database initialized successfully.")