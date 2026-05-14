# database.py

import sqlite3


# =========================================
# DATABASE CONNECTION
# =========================================
def get_connection():

    conn = sqlite3.connect(
        "edupro.db",
        check_same_thread=False
    )

    return conn


# =========================================
# CREATE TABLES
# =========================================
def create_tables():

    conn = get_connection()

    c = conn.cursor()

    # USERS TABLE
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT,
        role TEXT
    )
    """)

    # STUDENTS TABLE
    c.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_name TEXT,
        student_email TEXT,
        student_phone TEXT,
        course TEXT,
        attendance INTEGER DEFAULT 0
    )
    """)

    # TEACHERS TABLE
    c.execute("""
    CREATE TABLE IF NOT EXISTS teachers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        teacher_name TEXT,
        teacher_email TEXT,
        subject TEXT,
        experience INTEGER
    )
    """)

    # COURSES TABLE
    c.execute("""
    CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_name TEXT,
        duration TEXT,
        fees REAL
    )
    """)

    # FEES TABLE
    c.execute("""
    CREATE TABLE IF NOT EXISTS fees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        amount REAL,
        payment_status TEXT
    )
    """)

    # ATTENDANCE TABLE
    c.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        attendance_date TEXT,
        status TEXT
    )
    """)

    # REPORT CARDS TABLE
    c.execute("""
    CREATE TABLE IF NOT EXISTS report_cards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        subject TEXT,
        marks INTEGER,
        grade TEXT
    )
    """)

    conn.commit()

    c.close()

    conn.close()


# =========================================
# ADD USER
# =========================================
def add_user(username, password, role):

    conn = get_connection()

    c = conn.cursor()

    query = """
    INSERT INTO users (username, password, role)
    VALUES (?, ?, ?)
    """

    c.execute(query, (username, password, role))

    conn.commit()

    c.close()

    conn.close()

    return True


# =========================================
# LOGIN USER
# =========================================
def login_user(username, password):

    conn = get_connection()

    c = conn.cursor()

    query = """
    SELECT * FROM users
    WHERE username=? AND password=?
    """

    c.execute(query, (username, password))

    data = c.fetchone()

    c.close()

    conn.close()

    return data


# =========================================
# ADD STUDENT
# =========================================
def add_student(name, email, phone, course):

    conn = get_connection()

    c = conn.cursor()

    query = """
    INSERT INTO students
    (student_name, student_email, student_phone, course)
    VALUES (?, ?, ?, ?)
    """

    c.execute(query, (name, email, phone, course))

    conn.commit()

    c.close()

    conn.close()


# =========================================
# VIEW STUDENTS
# =========================================
def view_students():

    conn = get_connection()

    c = conn.cursor()

    c.execute("SELECT * FROM students")

    data = c.fetchall()

    c.close()

    conn.close()

    return data


# =========================================
# ADD TEACHER
# =========================================
def add_teacher(name, email, subject, experience):

    conn = get_connection()

    c = conn.cursor()

    query = """
    INSERT INTO teachers
    (teacher_name, teacher_email, subject, experience)
    VALUES (?, ?, ?, ?)
    """

    c.execute(query, (name, email, subject, experience))

    conn.commit()

    c.close()

    conn.close()


# =========================================
# VIEW TEACHERS
# =========================================
def view_teachers():

    conn = get_connection()

    c = conn.cursor()

    c.execute("SELECT * FROM teachers")

    data = c.fetchall()

    c.close()

    conn.close()

    return data


# =========================================
# VIEW ATTENDANCE
# =========================================
def view_attendance():

    conn = get_connection()

    c = conn.cursor()

    c.execute("SELECT * FROM attendance")

    data = c.fetchall()

    c.close()

    conn.close()

    return data


# =========================================
# VIEW MARKS
# =========================================
def view_marks():

    conn = get_connection()

    c = conn.cursor()

    c.execute("SELECT * FROM report_cards")

    data = c.fetchall()

    c.close()

    conn.close()

    return data


# =========================================
# GET STUDENT REPORT
# =========================================
def get_student_report(student_id):

    conn = get_connection()

    c = conn.cursor()

    query = """
    SELECT * FROM report_cards
    WHERE student_id=?
    """

    c.execute(query, (student_id,))

    data = c.fetchall()

    c.close()

    conn.close()

    return data