import sqlite3

# create connection
def create_connection():
    conn = sqlite3.connect("users.db")
    return conn

# create table
def create_table():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT,
        role TEXT
    )
    """)

    conn.commit()
    conn.close()

# add user
def add_user(username, password, role):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO users VALUES (?, ?, ?)", (username, password, role))

    conn.commit()
    conn.close()

# get user
def get_user(username):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cursor.fetchone()

    conn.close()
    return user

from src.database import create_table, add_user

create_table()

add_user("admin", "admin123", "admin")
add_user("user", "user123", "user")