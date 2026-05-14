import mysql.connector


# =========================================
# DATABASE CONNECTION
# =========================================
def get_connection():

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root123",  
        database="edupro",
        auth_plugin="mysql_native_password",
        ssl_disabled=True
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
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255),
        password VARCHAR(255),
        role VARCHAR(50)
    )
    """)

    # STUDENTS TABLE
    c.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INT AUTO_INCREMENT PRIMARY KEY,
        student_name VARCHAR(255),
        student_email VARCHAR(255),
        student_phone VARCHAR(20),
        course VARCHAR(255),
        attendance INT DEFAULT 0
    )
    """)

    # TEACHERS TABLE
    c.execute("""
    CREATE TABLE IF NOT EXISTS teachers (
        id INT AUTO_INCREMENT PRIMARY KEY,
        teacher_name VARCHAR(255),
        teacher_email VARCHAR(255),
        subject VARCHAR(255),
        experience INT
    )
    """)

    # COURSES TABLE
    c.execute("""
    CREATE TABLE IF NOT EXISTS courses (
        id INT AUTO_INCREMENT PRIMARY KEY,
        course_name VARCHAR(255),
        duration VARCHAR(100),
        fees DECIMAL(10,2)
    )
    """)

    # FEES TABLE
    c.execute("""
    CREATE TABLE IF NOT EXISTS fees (
        id INT AUTO_INCREMENT PRIMARY KEY,
        student_id INT,
        amount DECIMAL(10,2),
        payment_status VARCHAR(50)
    )
    """)

    # ATTENDANCE TABLE
    c.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id INT AUTO_INCREMENT PRIMARY KEY,
        student_id INT,
        attendance_date DATE,
        status VARCHAR(50)
    )
    """)

    # REPORT CARDS TABLE
    c.execute("""
    CREATE TABLE IF NOT EXISTS report_cards (
        id INT AUTO_INCREMENT PRIMARY KEY,
        student_id INT,
        subject VARCHAR(255),
        marks INT,
        grade VARCHAR(10)
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
    VALUES (%s, %s, %s)
    """

    values = (username, password, role)

    c.execute(query, values)

    conn.commit()

    c.close()
    conn.close()


# =========================================
# LOGIN USER
# =========================================
def login_user(username, password):

    conn = get_connection()
    c = conn.cursor()

    query = """
    SELECT * FROM users
    WHERE username=%s AND password=%s
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
    VALUES (%s, %s, %s, %s)
    """

    values = (name, email, phone, course)

    c.execute(query, values)

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
    VALUES (%s, %s, %s, %s)
    """

    values = (name, email, subject, experience)

    c.execute(query, values)

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
# ADD COURSE
# =========================================
def add_course(course_name, duration, fees):

    conn = get_connection()
    c = conn.cursor()

    query = """
    INSERT INTO courses
    (course_name, duration, fees)
    VALUES (%s, %s, %s)
    """

    values = (course_name, duration, fees)

    c.execute(query, values)

    conn.commit()

    c.close()
    conn.close()


# =========================================
# VIEW COURSES
# =========================================
def view_courses():

    conn = get_connection()
    c = conn.cursor()

    c.execute("SELECT * FROM courses")

    data = c.fetchall()

    c.close()
    conn.close()

    return data


# =========================================
# ADD FEES
# =========================================
def add_fees(student_id, amount, payment_status):

    conn = get_connection()
    c = conn.cursor()

    query = """
    INSERT INTO fees
    (student_id, amount, payment_status)
    VALUES (%s, %s, %s)
    """

    values = (student_id, amount, payment_status)

    c.execute(query, values)

    conn.commit()

    c.close()
    conn.close()


# =========================================
# VIEW FEES
# =========================================
def view_fees():

    conn = get_connection()
    c = conn.cursor()

    c.execute("SELECT * FROM fees")

    data = c.fetchall()

    c.close()
    conn.close()

    return data


# =========================================
# ADD ATTENDANCE
# =========================================
def add_attendance(student_id, attendance_date, status):

    conn = get_connection()
    c = conn.cursor()

    query = """
    INSERT INTO attendance
    (student_id, attendance_date, status)
    VALUES (%s, %s, %s)
    """

    values = (student_id, attendance_date, status)

    c.execute(query, values)

    conn.commit()

    c.close()
    conn.close()


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
# ADD MARKS
# =========================================
def add_marks(student_id, subject, marks, grade):

    conn = get_connection()
    c = conn.cursor()

    query = """
    INSERT INTO report_cards
    (student_id, subject, marks, grade)
    VALUES (%s, %s, %s, %s)
    """

    values = (student_id, subject, marks, grade)

    c.execute(query, values)

    conn.commit()

    c.close()
    conn.close()


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
    WHERE student_id=%s
    """

    c.execute(query, (student_id,))

    data = c.fetchall()

    c.close()
    conn.close()

    return data