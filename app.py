import streamlit as st
import pandas as pd
import plotly.express as px
import os
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
        #4c1d95,
        #0f766e,
        #1d4ed8
    );

    background-size: 600% 600%;

    animation: gradientAnimation 18s ease infinite;

    color: white;
}

@keyframes gradientAnimation {

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

.stApp::before {

    content: '';

    position: fixed;

    width: 600px;

    height: 600px;

    background: rgba(59,130,246,0.25);

    border-radius: 50%;

    top: -200px;

    left: -150px;

    filter: blur(120px);

    z-index: -1;
}

.stApp::after {

    content: '';

    position: fixed;

    width: 500px;

    height: 500px;

    background: rgba(168,85,247,0.22);

    border-radius: 50%;

    bottom: -150px;

    right: -120px;

    filter: blur(120px);

    z-index: -1;
}

section[data-testid="stSidebar"] {

    background: rgba(15,23,42,0.88);

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

    border-radius: 22px;

    padding: 22px;

    border: 1px solid rgba(255,255,255,0.1);

    backdrop-filter: blur(16px);

    box-shadow: 0px 10px 35px rgba(0,0,0,0.35);

    transition: 0.3s;
}

[data-testid="metric-container"]:hover {

    transform: translateY(-8px);
}

.stButton > button {

    width: 100%;

    height: 50px;

    border-radius: 15px;

    border: none;

    background: linear-gradient(
        90deg,
        #2563eb,
        #7c3aed,
        #06b6d4
    );

    color: white;

    font-size: 16px;

    font-weight: bold;
}

.stButton > button:hover {

    transform: scale(1.03);

    transition: 0.3s;
}

[data-testid="stDataFrame"] {

    background: rgba(255,255,255,0.06);

    border-radius: 20px;

    padding: 10px;
}

.hero {

    background: rgba(255,255,255,0.08);

    padding: 40px;

    border-radius: 30px;

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
# DATABASE
# =========================================================

create_tables()

# =========================================================
# DEFAULT USERS
# =========================================================

try:
    add_user("admin", "admin123", "Admin")
except:
    pass

try:
    add_user("teacher", "teacher123", "Teacher")
except:
    pass

try:
    add_user("student", "student123", "Student")
except:
    pass

# =========================================================
# SESSION STATE
# =========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# =========================================================
# LOGIN MENU
# =========================================================

menu = ["Login", "Signup"]

choice = st.sidebar.selectbox(
    "Menu",
    menu
)

# =========================================================
# LOGIN SYSTEM
# =========================================================

if not st.session_state.logged_in:

    if choice == "Login":

        st.markdown("""
        <div class='hero'>

        <h1>🎓 EduPro Smart ERP</h1>

        <h3>Premium School & College Management System</h3>

        </div>
        """, unsafe_allow_html=True)

        user = st.text_input("Username")

        pwd = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login"):

            result = login_user(user, pwd)

            if result:

                st.session_state.logged_in = True
                st.session_state.user = result[0]
                st.session_state.role = result[2]

                st.success("Login Successful")

                st.rerun()

            else:

                st.error("Invalid Credentials")

    elif choice == "Signup":

        st.title("📝 Create Account")

        user = st.text_input("Username")

        pwd = st.text_input(
            "Password",
            type="password"
        )

        role = st.selectbox(
            "Role",
            ["Student", "Teacher", "Admin"]
        )

        if st.button("Create Account"):

            result = add_user(
                user,
                pwd,
                role
            )

            if result:
                st.success("Account Created")
            else:
                st.warning("Username already exists")

# =========================================================
# MAIN SYSTEM
# =========================================================

else:

    st.sidebar.markdown("""
    <center>

    <img src='https://cdn-icons-png.flaticon.com/512/3135/3135755.png'
    width='130'>

    <h2>EduPro ERP</h2>

    <p>Smart Education Portal</p>

    </center>
    """, unsafe_allow_html=True)

    st.sidebar.write(
        f"👤 User: {st.session_state.user}"
    )

    st.sidebar.write(
        f"🛡 Role: {st.session_state.role}"
    )

    # =====================================================
    # ROLE BASED ACCESS
    # =====================================================

    if st.session_state.role == "Admin":

        modules = [
            "Dashboard",
            "Teachers",
            "Students",
            "Courses",
            "Transactions",
            "Analytics",
            "Attendance",
            "Marks",
            "Report Card"
        ]

    elif st.session_state.role == "Teacher":

        modules = [
            "Dashboard",
            "Teachers",
            "Students",
            "Courses",
            "Transactions",
            "Analytics",
            "Attendance",
            "Marks",
            "Report Card"
        ]

    elif st.session_state.role == "Student":

        modules = [
            "Dashboard",
            "Students",
            "Transactions",
            "Analytics",
            "Attendance",
            "Courses",
            "Report Card"
        ]

    else:

        modules = ["Dashboard"]

    module = st.sidebar.radio(
        "Navigation",
        modules
    )

    if st.sidebar.button("Logout"):

        st.session_state.logged_in = False
        st.rerun()

    # =====================================================
    # LOAD DATASET
    # =====================================================

    if os.path.exists("final_dataset.csv"):

        df = pd.read_csv("final_dataset.csv")

    else:

        st.error("final_dataset.csv not found")
        st.stop()

    # =====================================================
    # DASHBOARD
    # =====================================================

    if module == "Dashboard":

        st.markdown("""
        <div class='hero'>

        <h1>🎓 EduPro Smart ERP Dashboard</h1>

        <h3>
        AI Powered Education Analytics Platform
        </h3>

        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "👨‍🎓 Students",
                len(view_students())
            )

        with col2:
            st.metric(
                "👨‍🏫 Teachers",
                df["TeacherID"].nunique()
            )

        with col3:
            st.metric(
                "📚 Courses",
                df["CourseID"].nunique()
            )

        with col4:
            st.metric(
                "💳 Transactions",
                len(df)
            )

    # =====================================================
    # TEACHERS
    # =====================================================

    elif module == "Teachers":

        if st.session_state.role == "Student":

            st.error("Access Denied")
            st.stop()

        st.title("👨‍🏫 Teachers")

        teacher_data = view_teachers()

        teacher_df = pd.DataFrame(
            teacher_data,
            columns=[
                "TeacherID",
                "TeacherName",
                "Age",
                "Gender",
                "Expertise",
                "YearsOfExperience",
                "TeacherRating"
            ]
        )

        st.dataframe(
            teacher_df,
            use_container_width=True
        )

    # =====================================================
    # STUDENTS
    # =====================================================

    elif module == "Students":

        st.title("👨‍🎓 Students")

        student_data = view_students()

        student_df = pd.DataFrame(
            student_data,
            columns=[
                "ID",
                "Name",
                "Class",
                "Age"
            ]
        )

        st.dataframe(
            student_df,
            use_container_width=True
        )

    # =====================================================
    # COURSES
    # =====================================================

    elif module == "Courses":

        st.title("📚 Courses")

        courses_df = pd.read_excel(
            "edupro.xlsx",
            sheet_name="Courses"
        )

        st.dataframe(
            courses_df,
            use_container_width=True
        )

        fig = px.bar(
            courses_df,
            x="CourseCategory",
            y="CourseRating",
            color="CourseLevel",
            template="plotly_dark"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # =====================================================
    # TRANSACTIONS
    # =====================================================

    elif module == "Transactions":

        st.title("💳 Transactions")

        transactions_df = pd.read_excel(
            "edupro.xlsx",
            sheet_name="Transactions"
        )

        st.dataframe(
            transactions_df,
            use_container_width=True
        )

    # =====================================================
    # ANALYTICS
    # =====================================================

    elif module == "Analytics":

        st.title("📊 Analytics Dashboard")

        fig = px.scatter(
            df,
            x="YearsOfExperience",
            y="TeacherRating",
            color="Expertise",
            size="CourseRating",
            hover_data=[
                "TeacherName",
                "CourseName"
            ],
            template="plotly_dark",
            title="Instructor Experience vs Performance",
            size_max=35
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white")
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # =====================================================
    # ATTENDANCE
    # =====================================================

    elif module == "Attendance":

        st.title("📅 Attendance")

        attendance_df = pd.DataFrame(
            view_attendance(),
            columns=[
                "Student",
                "Date",
                "Status"
            ]
        )

        st.dataframe(
            attendance_df,
            use_container_width=True
        )

    # =====================================================
    # MARKS
    # =====================================================

    elif module == "Marks":

        if st.session_state.role == "Student":

            st.error("Access Denied")
            st.stop()

        st.title("📊 Marks")

        marks_df = pd.DataFrame(
            view_marks(),
            columns=[
                "Student",
                "Subject",
                "Marks"
            ]
        )

        st.dataframe(
            marks_df,
            use_container_width=True
        )

    # =====================================================
    # REPORT CARD
    # =====================================================

    elif module == "Report Card":

        st.title("📄 Report Card")

        students = view_students()

        student_df = pd.DataFrame(
            students,
            columns=[
                "ID",
                "Name",
                "Class",
                "Age"
            ]
        )

        if student_df.empty:

            st.warning("No students available")

        else:

            name_to_id = dict(
                zip(
                    student_df["Name"],
                    student_df["ID"]
                )
            )

            selected = st.selectbox(
                "Select Student",
                list(name_to_id.keys())
            )

            student_id = name_to_id[selected]

            attendance_pct, avg_marks, marks_data = get_student_report(
                student_id
            )

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Attendance %",
                    f"{attendance_pct:.2f}%"
                )

            with col2:
                st.metric(
                    "Average Marks",
                    f"{avg_marks:.2f}"
                )

    # =====================================================
    # FOOTER
    # =====================================================

    st.markdown("""
    <div class='footer'>

    <hr>

    <h3>
    🎓 EduPro Smart ERP System
    </h3>

    <p>
    Premium AI Powered Education Platform
    </p>

    </div>
    """, unsafe_allow_html=True)