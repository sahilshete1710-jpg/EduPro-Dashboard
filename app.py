import streamlit as st
import pandas as pd
import plotly.express as px
from database import *

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="EduPro Smart ERP",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# PREMIUM CSS
# =========================================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        -45deg,
        #020617,
        #0f172a,
        #1e3a8a,
        #312e81,
        #4c1d95,
        #0f766e,
        #1d4ed8
    );

    background-size: 600% 600%;
    animation: gradientBG 18s ease infinite;
    color: white;
}

@keyframes gradientBG {
    0% {
        background-position: 0% 50%;
    }

    50% {
        background-position: 100% 50%;
    }

    100% {
        background-position: 0% 50%;
    }
}

section[data-testid="stSidebar"] {
    background: rgba(15,23,42,0.85);
    backdrop-filter: blur(20px);
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

h1, h2, h3, h4 {
    color: white !important;
}

[data-testid="metric-container"] {
    background: rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 20px;
    border: 1px solid rgba(255,255,255,0.1);
    backdrop-filter: blur(15px);
}

.stButton > button {
    width: 100%;
    height: 50px;
    border-radius: 14px;
    border: none;
    color: white;
    font-weight: bold;
    background: linear-gradient(
        90deg,
        #2563eb,
        #7c3aed,
        #06b6d4
    );
}

.hero {
    background: rgba(255,255,255,0.08);
    padding: 40px;
    border-radius: 25px;
    text-align: center;
    backdrop-filter: blur(18px);
    margin-bottom: 30px;
}

.footer {
    text-align: center;
    color: white;
    opacity: 0.8;
    margin-top: 40px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# CREATE TABLES
# =========================================================

create_tables()

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown(
    """
    <center>

    <img src='https://cdn-icons-png.flaticon.com/512/3135/3135755.png' width='120'>

    <h2>EduPro ERP</h2>

    <p>Premium AI Education Platform</p>

    </center>
    """,
    unsafe_allow_html=True
)

menu = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Students",
        "Teachers",
        "Courses",
        "Attendance",
        "Marks",
        "Transactions",
        "Report Card"
    ]
)

# =========================================================
# DASHBOARD
# =========================================================

if menu == "Dashboard":

    st.markdown(
        """
        <div class='hero'>

        <h1>🚀 EduPro Smart ERP</h1>

        <h3>Premium AI Powered Education Platform</h3>

        </div>
        """,
        unsafe_allow_html=True
    )

    students = view_students()
    teachers = view_teachers()
    courses = view_courses()
    fees = view_fees()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("🎓 Students", len(students))

    with col2:
        st.metric("👨‍🏫 Teachers", len(teachers))

    with col3:
        st.metric("📚 Courses", len(courses))

    with col4:
        st.metric("💳 Transactions", len(fees))

# =========================================================
# STUDENTS
# =========================================================

elif menu == "Students":

    st.title("🎓 Students")

    students = view_students()

    if students:

        df = pd.DataFrame(
            students,
            columns=[
                "ID",
                "Student Name",
                "Email",
                "Phone",
                "Course",
                "Attendance"
            ]
        )

        st.dataframe(df, use_container_width=True)

    else:
        st.warning("No Students Found")

# =========================================================
# TEACHERS
# =========================================================

elif menu == "Teachers":

    st.title("👨‍🏫 Teachers")

    teachers = view_teachers()

    if teachers:

        df = pd.DataFrame(
            teachers,
            columns=[
                "ID",
                "Teacher Name",
                "Teacher Email",
                "Subject",
                "Experience"
            ]
        )

        st.dataframe(df, use_container_width=True)

    else:
        st.warning("No Teachers Found")

# =========================================================
# COURSES
# =========================================================

elif menu == "Courses":

    st.title("📚 Courses")

    courses = view_courses()

    if courses:

        df = pd.DataFrame(
            courses,
            columns=[
                "ID",
                "Course Name",
                "Duration",
                "Fees"
            ]
        )

        st.dataframe(df, use_container_width=True)

    else:
        st.warning("No Courses Found")

# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class='footer'>

    <hr>

    <h3>🎓 EduPro Smart ERP</h3>

    <p>Premium AI Powered Education Management System</p>

    </div>
    """,
    unsafe_allow_html=True
)