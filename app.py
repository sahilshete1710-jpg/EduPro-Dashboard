import streamlit as st
import pandas as pd
import plotly.express as px
from database import *
import os

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="EduPro ERP + Analytics",
    layout="wide"
)

# =========================================================
# DATABASE INIT
# =========================================================
create_tables()

# DEFAULT USERS
try:
    add_user("admin", "admin123", "Admin")
except:
    pass

try:
    add_user("teacher", "teacher123", "Teacher")
except:
    pass

# =========================================================
# SESSION STATE
# =========================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# =========================================================
# LOGIN / SIGNUP
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

    # =====================================================
    # LOGIN
    # =====================================================
    if choice == "Login":

        st.title("🔐 Login")

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

                st.error("Invalid credentials")

    # =====================================================
    # SIGNUP
    # =====================================================
    elif choice == "Signup":

        st.title("📝 Signup")

        user = st.text_input("Username")

        pwd = st.text_input(
            "Password",
            type="password"
        )

        role = st.selectbox(
            "Role",
            ["Student", "Admin", "Teacher"]
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

                st.warning(
                    "Username already exists"
                )

# =========================================================
# MAIN SYSTEM
# =========================================================
else:

    # =====================================================
    # SIDEBAR
    # =====================================================
    st.sidebar.title("🎓 EduPro ERP")

    st.sidebar.write(
        f"User: {st.session_state.user}"
    )

    st.sidebar.write(
        f"Role: {st.session_state.role}"
    )

    # =====================================================
    # ROLE BASED MENU
    # =====================================================
    if st.session_state.role == "Admin":

        modules = [
            "Dashboard",
            "Analytics",
            "Students",
            "Teachers",
            "Attendance",
            "Marks",
            "Report Card"
        ]

    else:

        modules = [
            "Dashboard",
            "Analytics",
            "Students",
            "Attendance",
            "Marks",
            "Report Card"
        ]

    module = st.sidebar.radio(
        "Navigation",
        modules
    )

    # =====================================================
    # LOGOUT
    # =====================================================
    if st.sidebar.button("Logout"):

        st.session_state.logged_in = False

        st.rerun()

    # =====================================================
    # LOAD DATASET
    # =====================================================
    df = pd.read_csv("final_dataset.csv")

    # =====================================================
    # DASHBOARD
    # =====================================================
    if module == "Dashboard":

        st.title("🏠 Dashboard")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Courses",
            df["CourseID"].nunique()
        )

        col2.metric(
            "Teachers",
            df["TeacherID"].nunique()
        )

        col3.metric(
            "Enrollments",
            len(df)
        )

    # =====================================================
    # ANALYTICS
    # =====================================================
    elif module == "Analytics":

        st.title("📊 Analytics")

        fig = px.scatter(
            df,
            x="YearsOfExperience",
            y="TeacherRating",
            color="Expertise",
            hover_data=["TeacherName"],
            template="plotly_dark"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # =====================================================
    # STUDENTS
    # =====================================================
    elif module == "Students":

        st.title("👨‍🎓 Students")

        users_df = pd.read_excel(
            "edupro.xlsx",
            sheet_name="Users"
        )

        if st.button("Import Users"):

            try:

                add_student_bulk(users_df)

                st.success(
                    "Students Imported Successfully"
                )

            except Exception as e:

                st.error(f"Error: {e}")

        data = view_students()

        student_df = pd.DataFrame(
            data,
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
    # TEACHERS
    # =====================================================
    elif module == "Teachers":

        st.title("👨‍🏫 Teacher Management")

        if st.session_state.role != "Admin":

            st.error(
                "Only Admin can access this module"
            )

        else:

            st.subheader("📥 Import Teachers")

            if st.button(
                "Import Teachers from Excel"
            ):

                try:

                    teachers_df = pd.read_excel(
                        "edupro.xlsx",
                        sheet_name="Teachers"
                    )

                    import_teachers_from_excel(
                        teachers_df
                    )

                    st.success(
                        "Teachers Imported Successfully"
                    )

                except Exception as e:

                    st.error(f"Error: {e}")

            st.subheader("➕ Add Teacher")

            teacher_id = st.number_input(
                "Teacher ID",
                step=1
            )

            teacher_name = st.text_input(
                "Teacher Name"
            )

            age = st.number_input(
                "Age",
                18,
                80
            )

            gender = st.selectbox(
                "Gender",
                ["Male", "Female", "Other"]
            )

            expertise = st.text_input(
                "Expertise"
            )

            experience = st.slider(
                "Years Of Experience",
                0,
                40
            )

            rating = st.slider(
                "Teacher Rating",
                0.0,
                5.0,
                4.0
            )

            if st.button("Add Teacher"):

                add_teacher(
                    teacher_id,
                    teacher_name,
                    age,
                    gender,
                    expertise,
                    experience,
                    rating
                )

                st.success(
                    "Teacher Added Successfully"
                )

            st.subheader("📋 Teacher Records")

            teacher_data = view_teachers()

            if teacher_data:

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

            else:

                st.info(
                    "No teacher records found"
                )

    # =====================================================
    # ATTENDANCE
    # =====================================================
    elif module == "Attendance":

        st.title("📅 Attendance")

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

            st.warning(
                "No students found"
            )

        else:

            name_to_id = dict(
                zip(
                    student_df["Name"],
                    student_df["ID"]
                )
            )

            selected = st.selectbox(
                "Student",
                list(name_to_id.keys())
            )

            status = st.selectbox(
                "Status",
                ["Present", "Absent"]
            )

            date = st.date_input("Date")

            if st.button("Save Attendance"):

                add_attendance(
                    name_to_id[selected],
                    str(date),
                    status
                )

                st.success(
                    "Attendance Saved"
                )

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

        st.title("📊 Marks")

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

            st.warning(
                "No students found"
            )

        else:

            name_to_id = dict(
                zip(
                    student_df["Name"],
                    student_df["ID"]
                )
            )

            selected = st.selectbox(
                "Student",
                list(name_to_id.keys())
            )

            subject = st.text_input(
                "Subject"
            )

            marks = st.slider(
                "Marks",
                0,
                100
            )

            if st.button("Save Marks"):

                add_marks(
                    name_to_id[selected],
                    subject,
                    marks
                )

                st.success(
                    "Marks Saved"
                )

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

        st.title("📄 Student Report Card")

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

            st.warning(
                "No students available"
            )

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

            col1.metric(
                "Attendance %",
                f"{attendance_pct:.2f}%"
            )

            col2.metric(
                "Average Marks",
                f"{avg_marks:.2f}"
            )

            st.subheader("📊 Subject-wise Marks")

            if marks_data:

                df_marks = pd.DataFrame(
                    marks_data,
                    columns=[
                        "Subject",
                        "Marks"
                    ]
                )

                st.dataframe(
                    df_marks,
                    use_container_width=True
                )

                st.bar_chart(
                    df_marks.set_index("Subject")
                )

            else:

                st.info(
                    "No marks available"
                )