import sqlite3
import bcrypt

# ---------------- CONNECTION ----------------
def connect_db():
    return sqlite3.connect("erp.db", check_same_thread=False)

# ---------------- CREATE TABLES ----------------
def create_tables():
    conn = connect_db()
    c = conn.cursor()

    # Users
    c.execute("""
    CREATE TABLE IF NOT EXISTS users(
        username TEXT PRIMARY KEY,
        password BLOB,
        role TEXT
    )
    """)

    # Students
    c.execute("""
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        class TEXT,
        age INTEGER
    )
    """)

    # Attendance
    c.execute("""
    CREATE TABLE IF NOT EXISTS attendance(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        date TEXT,
        status TEXT
    )
    """)

    # Marks
    c.execute("""
    CREATE TABLE IF NOT EXISTS marks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        subject TEXT,
        marks INTEGER
    )
    """)

    conn.commit()
    conn.close()

# ---------------- USER FUNCTIONS ----------------
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

# ---------------- STUDENTS ----------------
def add_student(name, class_name, age):
    conn = connect_db()
    c = conn.cursor()
    c.execute("INSERT INTO students(name, class, age) VALUES (?, ?, ?)",
              (name, class_name, age))
    conn.commit()
    conn.close()

def add_student_bulk(data):
    conn = connect_db()
    c = conn.cursor()

    for _, row in data.iterrows():
        c.execute("INSERT INTO students(name, class, age) VALUES (?, ?, ?)",
                  (row["UserName"], "Default", 18))

    conn.commit()
    conn.close()

def view_students():
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT * FROM students")
    data = c.fetchall()
    conn.close()
    return data

# ---------------- ATTENDANCE ----------------
def add_attendance(student_id, date, status):
    conn = connect_db()
    c = conn.cursor()
    c.execute("INSERT INTO attendance(student_id, date, status) VALUES (?, ?, ?)",
              (student_id, date, status))
    conn.commit()
    conn.close()

def view_attendance():
    conn = connect_db()
    c = conn.cursor()
    c.execute("""
        SELECT s.name, a.date, a.status
        FROM attendance a
        JOIN students s ON a.student_id = s.id
    """)
    data = c.fetchall()
    conn.close()
    return data

# ---------------- MARKS ----------------
def add_marks(student_id, subject, marks):
    conn = connect_db()
    c = conn.cursor()
    c.execute("INSERT INTO marks(student_id, subject, marks) VALUES (?, ?, ?)",
              (student_id, subject, marks))
    conn.commit()
    conn.close()

def view_marks():
    conn = connect_db()
    c = conn.cursor()
    c.execute("""
        SELECT s.name, m.subject, m.marks
        FROM marks m
        JOIN students s ON m.student_id = s.id
    """)
    data = c.fetchall()
    conn.close()
    return data
