import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="shashankraj@2005",
        database="ai_ids"
    )