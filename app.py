import streamlit as st
import pandas as pd
import plotly.express as px
from database import *

create_tables()

# ---------------- SESSION INIT ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

st.set_page_config(page_title="EduPro ERP + Analytics", layout="wide")

# ---------------- LOGIN / SIGNUP ----------------
menu = ["Login", "Signup"]
choice = st.sidebar.selectbox("Menu", menu)

if not st.session_state.logged_in:

    if choice == "Login":
        st.title("🔐 Login")

        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")

        if st.button("Login"):
            result = login_user(user, pwd)
            if result:
                st.session_state.logged_in = True
                st.session_state.user = result[0]
                st.session_state.role = result[2]
                st.success("Login Successful")
                st.rerun()
            else:
                st.error("Invalid credentials")

    elif choice == "Signup":
        st.title("📝 Signup")

        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")
        role = st.selectbox("Role", ["Student", "Admin", "Teacher"])

        if st.button("Create Account"):
            add_user(user, pwd, role)
            st.success("Account Created")

# ---------------- MAIN SYSTEM ----------------
if st.session_state.logged_in:

    st.sidebar.title("🎓 EduPro ERP")
    st.sidebar.write(f"User: {st.session_state.user}")
    st.sidebar.write(f"Role: {st.session_state.role}")

    module = st.sidebar.radio(
        "Navigation",
        ["Dashboard", "Analytics", "Students", "Attendance", "Marks"]
    )

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    df = pd.read_csv("final_dataset.csv")

    # ---------------- DASHBOARD ----------------
    if module == "Dashboard":
        st.title("🏠 Dashboard")

        col1, col2, col3 = st.columns(3)
        col1.metric("Courses", df["CourseID"].nunique())
        col2.metric("Teachers", df["TeacherID"].nunique())
        col3.metric("Enrollments", len(df))

    # ---------------- ANALYTICS ----------------
    elif module == "Analytics":
        st.title("📊 Analytics")

        fig = px.scatter(
            df,
            x="YearsOfExperience",
            y="TeacherRating",
            color="Expertise",
            template="plotly_dark"
        )
        st.plotly_chart(fig, use_container_width=True)

    # ---------------- STUDENTS ----------------
    elif module == "Students":
        st.title("👨‍🎓 Students")

        users_df = pd.read_excel("EduPro Online Platform.xlsx", sheet_name="Users")

        if st.button("Import Users"):
            try:
                add_student_bulk(users_df)
                st.success("Imported!")
            except:
                st.warning("Students may already exist")

        data = view_students()
        st.dataframe(pd.DataFrame(data, columns=["ID", "Name", "Class", "Age"]))

    # ---------------- ATTENDANCE ----------------
    elif module == "Attendance":
        st.title("📅 Attendance")

        students = view_students()
        student_df = pd.DataFrame(students, columns=["ID", "Name", "Class", "Age"])

        if student_df.empty:
            st.warning("No students found. Import students first.")
        else:
            name_to_id = dict(zip(student_df["Name"], student_df["ID"]))

            selected = st.selectbox("Student", list(name_to_id.keys()))
            status = st.selectbox("Status", ["Present", "Absent"])
            date = st.date_input("Date")

            if st.button("Save"):
                add_attendance(name_to_id[selected], str(date), status)
                st.success("Saved")

        st.dataframe(pd.DataFrame(view_attendance(),
                                 columns=["Student", "Date", "Status"]))

    # ---------------- MARKS ----------------
    elif module == "Marks":
        st.title("📊 Marks")

        students = view_students()
        student_df = pd.DataFrame(students, columns=["ID", "Name", "Class", "Age"])

        if student_df.empty:
            st.warning("No students found. Import students first.")
        else:
            name_to_id = dict(zip(student_df["Name"], student_df["ID"]))

            selected = st.selectbox("Student", list(name_to_id.keys()))
            subject = st.text_input("Subject")
            marks = st.slider("Marks", 0, 100)

            if st.button("Save"):
                add_marks(name_to_id[selected], subject, marks)
                st.success("Saved")

        st.dataframe(pd.DataFrame(view_marks(),
                                 columns=["Student", "Subject", "Marks"]))
