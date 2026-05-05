import streamlit as st
import pandas as pd
import plotly.express as px
from database import *

create_tables()

st.set_page_config(page_title="EduPro ERP + Analytics", layout="wide")

# ---------------- SESSION ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------------- LOGIN ----------------
menu = ["Login", "Signup"]
choice = st.sidebar.selectbox("Menu", menu)

if not st.session_state.logged_in:

    if choice == "Login":
        st.title("🔐 EduPro Login")

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

    st.sidebar.title("🎓 EduPro System")
    st.sidebar.write(f"👤 {st.session_state.user}")
    st.sidebar.write(f"Role: {st.session_state.role}")

    module = st.sidebar.radio(
        "Navigation",
        ["Dashboard", "Analytics", "Attendance", "Marks"]
    )

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    df = pd.read_csv("final_dataset.csv")

    # ---------------- DASHBOARD ----------------
    if module == "Dashboard":
        st.title("🏠 Dashboard")

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Courses", df["CourseID"].nunique())
        col2.metric("Total Teachers", df["TeacherID"].nunique())
        col3.metric("Total Enrollments", len(df))

    # ---------------- ANALYTICS ----------------
    elif module == "Analytics":
        st.title("📊 EduPro Analytics")

        fig1 = px.scatter(
            df,
            x="YearsOfExperience",
            y="TeacherRating",
            color="Expertise",
            template="plotly_dark"
        )
        st.plotly_chart(fig1, use_container_width=True)

        pivot = df.pivot_table(
            values="CourseRating",
            index="CourseCategory",
            columns="CourseLevel"
        )

        fig2 = px.imshow(pivot, text_auto=True, template="plotly_dark")
        st.plotly_chart(fig2, use_container_width=True)

    # ---------------- ATTENDANCE ----------------
    elif module == "Attendance":
        st.title("📅 Attendance")

        student = st.text_input("Student Name")
        status = st.selectbox("Status", ["Present", "Absent"])

        if st.button("Save Attendance"):
            add_attendance(student, "2026-01-01", status)
            st.success("Saved!")

        st.subheader("Records")
        data = view_attendance()
        st.write(pd.DataFrame(data, columns=["Student", "Date", "Status"]))

    # ---------------- MARKS ----------------
    elif module == "Marks":
        st.title("📊 Marks")

        student = st.text_input("Student")
        subject = st.text_input("Subject")
        marks = st.slider("Marks", 0, 100)

        if st.button("Save Marks"):
            add_marks(student, subject, marks)
            st.success("Saved!")

        st.subheader("Records")
        data = view_marks()
        st.write(pd.DataFrame(data, columns=["Student", "Subject", "Marks"]))