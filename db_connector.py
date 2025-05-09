# database.py
import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",       # <-- тут свої дані
        password="never-put-passwords-in-files",
        database="personnel"
    )
