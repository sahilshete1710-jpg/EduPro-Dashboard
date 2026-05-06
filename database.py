import sqlite3
import pandas as pd

# =========================================================
# DATABASE CONNECTION
# =========================================================
conn = sqlite3.connect(
    "erp.db",
    check_same_thread=False
)

c = conn.cursor()

# =========================================================
# CREATE TABLES
# =========================================================
def create_tables():

    # USERS TABLE
    c.execute('''
    CREATE TABLE IF NOT EXISTS users(
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    ''')

    # STUDENTS TABLE
    c.execute('''
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        class TEXT,
        age INTEGER
    )
    ''')

    # ATTENDANCE TABLE
    c.execute('''
    CREATE TABLE IF NOT EXISTS attendance(
        student_id INTEGER,
        date TEXT,
        status TEXT
    )
    ''')

    # MARKS TABLE
    c.execute('''
    CREATE TABLE IF NOT EXISTS marks(
        student_id INTEGER,
        subject TEXT,
        marks INTEGER
    )
    ''')

    # TEACHERS TABLE
    c.execute('''
    CREATE TABLE IF NOT EXISTS teachers(
        TeacherID INTEGER,
        TeacherName TEXT,
        Age INTEGER,
        Gender TEXT,
        Expertise TEXT,
        YearsOfExperience INTEGER,
        TeacherRating REAL
    )
    ''')

    conn.commit()

# =========================================================
# USER FUNCTIONS
# =========================================================
def add_user(username, password, role):

    c.execute(
        "SELECT * FROM users WHERE username=?",
        (username,)
    )

    existing_user = c.fetchone()

    if existing_user:
        return False

    c.execute(
        '''
        INSERT INTO users(username, password, role)
        VALUES (?, ?, ?)
        ''',
        (username, password, role)
    )

    conn.commit()

    return True


def login_user(username, password):

    c.execute(
        '''
        SELECT * FROM users
        WHERE username=? AND password=?
        ''',
        (username, password)
    )

    return c.fetchone()

# =========================================================
# STUDENT FUNCTIONS
# =========================================================
def add_student_bulk(df):

    for _, row in df.iterrows():

        c.execute(
            '''
            INSERT INTO students(name, class, age)
            VALUES (?, ?, ?)
            ''',
            (
                row["Name"],
                row["Class"],
                row["Age"]
            )
        )

    conn.commit()


def view_students():

    c.execute("SELECT * FROM students")

    return c.fetchall()

# =========================================================
# ATTENDANCE FUNCTIONS
# =========================================================
def add_attendance(student_id, date, status):

    c.execute(
        '''
        INSERT INTO attendance(student_id, date, status)
        VALUES (?, ?, ?)
        ''',
        (student_id, date, status)
    )

    conn.commit()


def view_attendance():

    c.execute('''
    SELECT students.name, attendance.date, attendance.status
    FROM attendance
    JOIN students
    ON students.id = attendance.student_id
    ''')

    return c.fetchall()

# =========================================================
# MARKS FUNCTIONS
# =========================================================
def add_marks(student_id, subject, marks):

    c.execute(
        '''
        INSERT INTO marks(student_id, subject, marks)
        VALUES (?, ?, ?)
        ''',
        (student_id, subject, marks)
    )

    conn.commit()


def view_marks():

    c.execute('''
    SELECT students.name, marks.subject, marks.marks
    FROM marks
    JOIN students
    ON students.id = marks.student_id
    ''')

    return c.fetchall()

# =========================================================
# REPORT CARD FUNCTIONS
# =========================================================
def get_student_report(student_id):

    # TOTAL ATTENDANCE
    c.execute(
        '''
        SELECT COUNT(*)
        FROM attendance
        WHERE student_id=?
        ''',
        (student_id,)
    )

    total = c.fetchone()[0]

    # PRESENT COUNT
    c.execute(
        '''
        SELECT COUNT(*)
        FROM attendance
        WHERE student_id=? AND status='Present'
        ''',
        (student_id,)
    )

    present = c.fetchone()[0]

    attendance_pct = (
        (present / total) * 100
        if total > 0 else 0
    )

    # AVERAGE MARKS
    c.execute(
        '''
        SELECT AVG(marks)
        FROM marks
        WHERE student_id=?
        ''',
        (student_id,)
    )

    avg_marks = c.fetchone()[0]

    if avg_marks is None:
        avg_marks = 0

    # SUBJECT MARKS
    c.execute(
        '''
        SELECT subject, marks
        FROM marks
        WHERE student_id=?
        ''',
        (student_id,)
    )

    marks_data = c.fetchall()

    return attendance_pct, avg_marks, marks_data

# =========================================================
# TEACHER FUNCTIONS
# =========================================================
def add_teacher(
    teacher_id,
    teacher_name,
    age,
    gender,
    expertise,
    experience,
    rating
):

    c.execute(
        '''
        INSERT INTO teachers(
            TeacherID,
            TeacherName,
            Age,
            Gender,
            Expertise,
            YearsOfExperience,
            TeacherRating
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''',
        (
            teacher_id,
            teacher_name,
            age,
            gender,
            expertise,
            experience,
            rating
        )
    )

    conn.commit()


def import_teachers_from_excel(df):

    for _, row in df.iterrows():

        c.execute(
            '''
            INSERT INTO teachers(
                TeacherID,
                TeacherName,
                Age,
                Gender,
                Expertise,
                YearsOfExperience,
                TeacherRating
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''',
            (
                row["TeacherID"],
                row["TeacherName"],
                row["Age"],
                row["Gender"],
                row["Expertise"],
                row["YearsOfExperience"],
                row["TeacherRating"]
            )
        )

    conn.commit()


def view_teachers():

    c.execute("SELECT * FROM teachers")

    return c.fetchall()