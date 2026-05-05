import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="EduPro Dashboard", layout="wide")

# -----------------------
# FAKE USER DATABASE
# -----------------------
users = {
    "admin": {"password": "admin123", "role": "Admin"},
    "student": {"password": "student123", "role": "Student"}
}

# -----------------------
# SESSION STATE
# -----------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# -----------------------
# LOGIN FUNCTION
# -----------------------
def login():
    st.title("🔐 EduPro Login Portal")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in users and users[username]["password"] == password:
            st.session_state.logged_in = True
            st.session_state.user = username
            st.session_state.role = users[username]["role"]
            st.success("Login Successful!")
            st.rerun()
        else:
            st.error("Invalid username or password")

# -----------------------
# DASHBOARD FUNCTION
# -----------------------
def dashboard():
    df = pd.read_csv("final_dataset.csv")

    st.sidebar.title("👤 User Panel")
    st.sidebar.write(f"Logged in as: **{st.session_state.user}**")
    st.sidebar.write(f"Role: **{st.session_state.role}**")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    st.title("🎓 EduPro Premium Dashboard")

    # Filters
    expertise = st.sidebar.multiselect("Expertise", df["Expertise"].unique(), default=df["Expertise"].unique())

    filtered_df = df[df["Expertise"].isin(expertise)]

    # KPI
    col1, col2, col3 = st.columns(3)
    col1.metric("Avg Teacher Rating", round(filtered_df["TeacherRating"].mean(), 2))
    col2.metric("Avg Course Rating", round(filtered_df["CourseRating"].mean(), 2))
    col3.metric("Enrollments", len(filtered_df))

    # Chart
    fig = px.scatter(filtered_df, x="YearsOfExperience", y="TeacherRating",
                     color="Expertise", template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

    # Role-based content
    if st.session_state.role == "Admin":
        st.subheader("🔧 Admin Controls")
        st.write("You can manage instructors and courses here.")

# -----------------------
# MAIN APP
# -----------------------
if not st.session_state.logged_in:
    login()
else:
    dashboard()