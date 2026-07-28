import sqlite3

DATABASE = "users.db"

def get_connection():
    return sqlite3.connect(DATABASE)