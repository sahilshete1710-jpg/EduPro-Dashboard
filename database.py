import sqlite3
import bcrypt

def connect_db():
    return sqlite3.connect("erp.db", check_same_thread=False)

# ---------------- CREATE TABLES ----------------
def create_tables():
    conn = connect_db()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users(
        username TEXT PRIMARY KEY,
        password TEXT,
        role TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS attendance(
        student TEXT,
        date TEXT,
        status TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS marks(
        student TEXT,
        subject TEXT,
        marks INTEGER
    )
    """)

    conn.commit()
    conn.close()

# ---------------- USERS ----------------
def add_user(username, password, role):
    conn = connect_db()
    c = conn.cursor()
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    c.execute("INSERT INTO users VALUES (?, ?, ?)", (username, hashed, role))
    conn.commit()
    conn.close()

def login_user(username, password):
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    data = c.fetchone()
    conn.close()

    if data and bcrypt.checkpw(password.encode(), data[1]):
        return data
    return None

# ---------------- ATTENDANCE ----------------
def add_attendance(student, date, status):
    conn = connect_db()
    c = conn.cursor()
    c.execute("INSERT INTO attendance VALUES (?, ?, ?)", (student, date, status))
    conn.commit()
    conn.close()

def view_attendance():
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT * FROM attendance")
    data = c.fetchall()
    conn.close()
    return data

# ---------------- MARKS ----------------
def add_marks(student, subject, marks):
    conn = connect_db()
    c = conn.cursor()
    c.execute("INSERT INTO marks VALUES (?, ?, ?)", (student, subject, marks))
    conn.commit()
    conn.close()

def view_marks():
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT * FROM marks")
    data = c.fetchall()
    conn.close()
    return data