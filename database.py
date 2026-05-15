import hashlib
import os
import sqlite3
from pathlib import Path
from typing import Optional

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "edupro.db"

DEFAULT_USERS = [
    ("admin", "admin123", "Admin"),
    ("teacher", "teacher123", "Teacher"),
    ("student", "student123", "Student"),
]


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def hash_password(password: str, salt: Optional[str] = None) -> str:
    salt = salt or os.urandom(16).hex()
    digest = hashlib.sha256(f"{salt}{password}".encode("utf-8")).hexdigest()
    return f"{salt}${digest}"


def verify_password(password: str, stored_password: str) -> bool:
    if "$" not in stored_password:
        return password == stored_password
    salt, _ = stored_password.split("$", 1)
    return hash_password(password, salt) == stored_password


def create_tables() -> None:
    with get_connection() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('Admin', 'Teacher', 'Student'))
            );

            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_name TEXT NOT NULL,
                student_email TEXT,
                student_phone TEXT,
                course TEXT,
                attendance INTEGER DEFAULT 0
            );

            CREATE TABLE IF NOT EXISTS teachers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                teacher_name TEXT NOT NULL,
                teacher_email TEXT,
                subject TEXT,
                experience INTEGER DEFAULT 0
            );

            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                course_name TEXT NOT NULL,
                duration TEXT,
                fees REAL DEFAULT 0
            );

            CREATE TABLE IF NOT EXISTS fees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                amount REAL DEFAULT 0,
                payment_status TEXT DEFAULT 'Pending',
                FOREIGN KEY(student_id) REFERENCES students(id)
            );

            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                attendance_date TEXT NOT NULL,
                status TEXT NOT NULL,
                FOREIGN KEY(student_id) REFERENCES students(id)
            );

            CREATE TABLE IF NOT EXISTS report_cards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                subject TEXT NOT NULL,
                marks INTEGER DEFAULT 0,
                grade TEXT,
                FOREIGN KEY(student_id) REFERENCES students(id)
            );
            """
        )


def seed_default_users() -> None:
    for username, password, role in DEFAULT_USERS:
        add_user(username, password, role)


def add_user(username: str, password: str, role: str) -> bool:
    if role not in {"Admin", "Teacher", "Student"}:
        raise ValueError("Invalid role")

    try:
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                (username, hash_password(password), role),
            )
        return True
    except sqlite3.IntegrityError:
        return False


def login_user(username: str, password: str):
    with get_connection() as conn:
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        if not user or not verify_password(password, user["password"]):
            return None

        if "$" not in user["password"]:
            conn.execute("UPDATE users SET password = ? WHERE id = ?", (hash_password(password), user["id"]))

        return {"id": user["id"], "username": user["username"], "role": user["role"]}


def add_student(name: str, email: str, phone: str, course: str) -> None:
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO students (student_name, student_email, student_phone, course) VALUES (?, ?, ?, ?)",
            (name, email, phone, course),
        )


def view_students():
    with get_connection() as conn:
        return conn.execute("SELECT * FROM students ORDER BY id DESC").fetchall()


def add_teacher(name: str, email: str, subject: str, experience: int) -> None:
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO teachers (teacher_name, teacher_email, subject, experience) VALUES (?, ?, ?, ?)",
            (name, email, subject, experience),
        )


def view_teachers():
    with get_connection() as conn:
        return conn.execute("SELECT * FROM teachers ORDER BY id DESC").fetchall()


def view_courses():
    with get_connection() as conn:
        return conn.execute("SELECT * FROM courses ORDER BY id DESC").fetchall()


def view_fees():
    with get_connection() as conn:
        return conn.execute("SELECT * FROM fees ORDER BY id DESC").fetchall()


def view_attendance():
    with get_connection() as conn:
        return conn.execute("SELECT * FROM attendance ORDER BY attendance_date DESC").fetchall()


def view_marks():
    with get_connection() as conn:
        return conn.execute("SELECT * FROM report_cards ORDER BY id DESC").fetchall()


def get_student_report(student_id: int):
    with get_connection() as conn:
        return conn.execute("SELECT * FROM report_cards WHERE student_id = ?", (student_id,)).fetchall()
