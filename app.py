import streamlit as st
import pandas as pd
import plotly.express as px
import os

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
# PREMIUM ANIMATED CSS
# =========================================================

st.markdown("""
<style>

/* =========================================================
MAIN BACKGROUND
========================================================= */

.stApp {

    background:
    linear-gradient(
        -45deg,
        #020617,
        #0f172a,
        #1e3a8a,
        #4c1d95,
        #0f766e,
        #2563eb
    );

    background-size: 500% 500%;

    animation: gradientBG 18s ease infinite;

    overflow-x: hidden;

    color: white;
}

/* =========================================================
ANIMATION
========================================================= */

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

/* =========================================================
FLOATING GLOW EFFECT
========================================================= */

.stApp::before {

    content: "";

    position: fixed;

    width: 500px;

    height: 500px;

    background: rgba(37,99,235,0.20);

    border-radius: 50%;

    top: -150px;

    left: -150px;

    filter: blur(120px);

    animation: floatBlue 12s infinite alternate;

    z-index: -1;
}

.stApp::after {

    content: "";

    position: fixed;

    width: 450px;

    height: 450px;

    background: rgba(168,85,247,0.18);

    border-radius: 50%;

    bottom: -120px;

    right: -120px;

    filter: blur(120px);

    animation: floatPurple 15s infinite alternate;

    z-index: -1;
}

@keyframes floatBlue {

    from {
        transform: translateX(0px) translateY(0px);
    }

    to {
        transform: translateX(150px) translateY(100px);
    }
}

@keyframes floatPurple {

    from {
        transform: translateX(0px) translateY(0px);
    }

    to {
        transform: translateX(-120px) translateY(-80px);
    }
}

/* =========================================================
SIDEBAR
========================================================= */

section[data-testid="stSidebar"] {

    background: rgba(15,23,42,0.92);

    backdrop-filter: blur(20px);

    border-right: 1px solid rgba(255,255,255,0.08);
}

section[data-testid="stSidebar"] * {

    color: white !important;
}

/* =========================================================
HEADINGS
========================================================= */

h1, h2, h3 {

    color: white !important;

    font-weight: 700;
}

/* =========================================================
HERO SECTION
========================================================= */

.hero {

    background: rgba(255,255,255,0.08);

    padding: 45px;

    border-radius: 30px;

    text-align: center;

    backdrop-filter: blur(18px);

    margin-bottom: 30px;

    box-shadow: 0px 10px 40px rgba(0,0,0,0.35);

    animation: fadeUp 1s ease;
}

@keyframes fadeUp {

    from {

        opacity: 0;

        transform: translateY(30px);
    }

    to {

        opacity: 1;

        transform: translateY(0px);
    }
}

/* =========================================================
METRIC CARDS
========================================================= */

[data-testid="metric-container"] {

    background: rgba(255,255,255,0.08);

    border-radius: 22px;

    padding: 20px;

    border: 1px solid rgba(255,255,255,0.08);

    backdrop-filter: blur(16px);

    box-shadow: 0px 8px 25px rgba(0,0,0,0.3);

    transition: 0.3s;
}

[data-testid="metric-container"]:hover {

    transform: translateY(-8px) scale(1.02);

    box-shadow: 0px 15px 35px rgba(0,0,0,0.45);
}

/* =========================================================
BUTTONS
========================================================= */

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

    transition: 0.3s;
}

.stButton > button:hover {

    transform: scale(1.03);

    box-shadow: 0px 0px 20px rgba(96,165,250,0.6);
}

/* =========================================================
INPUTS
========================================================= */

.stTextInput input,
.stSelectbox div {

    background: rgba(255,255,255,0.08);

    color: white;

    border-radius: 12px;
}

/* =========================================================
TABLES
========================================================= */

[data-testid="stDataFrame"] {

    background: rgba(255,255,255,0.06);

    border-radius: 20px;

    padding: 10px;
}

/* =========================================================
FOOTER
========================================================= */

.footer {

    text-align: center;

    color: white;

    margin-top: 40px;

    opacity: 0.8;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# SESSION STATE
# =========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "users_db" not in st.session_state:

    st.session_state.users_db = {

        "admin": {

            "password": "admin123",

            "role": "Admin"
        },

        "teacher": {

            "password": "teacher123",

            "role": "Teacher"
        },

        "student": {

            "password": "student123",

            "role": "Student"
        }
    }

# =========================================================
# LOGIN MENU
# =========================================================

menu = ["Login", "Signup"]

choice = st.sidebar.selectbox(
    "Menu",
    menu
)

# =========================================================
# LOGIN & SIGNUP
# =========================================================

if not st.session_state.logged_in:

    # =====================================================
    # LOGIN
    # =====================================================

    if choice == "Login":

        st.markdown("""
        <div class='hero'>

        <h1>🚀 EduPro Smart ERP</h1>

        <h3>
        Next Generation AI Powered Education Platform
        </h3>

        <p>
        Premium School • College • University Management System
        </p>

        </div>
        """, unsafe_allow_html=True)

        username = st.text_input("Username")

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login"):

            if username in st.session_state.users_db:

                if st.session_state.users_db[username]["password"] == password:

                    st.session_state.logged_in = True

                    st.session_state.user = username

                    st.session_state.role = st.session_state.users_db[username]["role"]

                    st.success("Login Successful")

                    st.rerun()

                else:

                    st.error("Wrong Password")

            else:

                st.error("Invalid Username")

    # =====================================================
    # SIGNUP
    # =====================================================

    elif choice == "Signup":

        st.markdown("""
        <div class='hero'>

        <h1>📝 Create Account</h1>

        <h3>
        Join EduPro ERP Platform
        </h3>

        </div>
        """, unsafe_allow_html=True)

        new_user = st.text_input(
            "Create Username"
        )

        new_password = st.text_input(
            "Create Password",
            type="password"
        )

        role = st.selectbox(
            "Select Role",
            ["Student", "Teacher","Admin"]
        )

        if st.button("Create Account"):

            st.session_state.users_db[new_user] = {

                "password": new_password,

                "role": role
            }

            st.success("Account Created Successfully")

            st.info("Now login using your new account")

# =========================================================
# MAIN APP
# =========================================================

else:

    st.sidebar.markdown("""
    <center>

    <img src='https://cdn-icons-png.flaticon.com/512/3135/3135755.png'
    width='130'>

    <h2>EduPro ERP</h2>

    <p>
    Premium AI Education Platform
    </p>

    </center>
    """, unsafe_allow_html=True)

    st.sidebar.write(
        f"👤 User: {st.session_state.user}"
    )

    st.sidebar.write(
        f"🛡 Role: {st.session_state.role}"
    )

    # =====================================================
    # ROLE BASED MODULES
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

    else:

        modules = [

            "Dashboard",
            "Students",
            "Courses",
            "Transactions",
            "Analytics",
            "Attendance",
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
    # CHECK EXCEL
    # =====================================================

    if not os.path.exists("edupro.xlsx"):

        st.error("edupro.xlsx file not found")
        st.stop()

    # =====================================================
    # LOAD DATA
    # =====================================================

    teachers_df = pd.read_excel(
        "edupro.xlsx",
        sheet_name="Teachers"
    )

    courses_df = pd.read_excel(
        "edupro.xlsx",
        sheet_name="Courses"
    )

    transactions_df = pd.read_excel(
        "edupro.xlsx",
        sheet_name="Transactions"
    )

    users_df = pd.read_excel(
        "edupro.xlsx",
        sheet_name="Users"
    )

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
            st.metric("👨‍🏫 Teachers", len(teachers_df))

        with col2:
            st.metric("👨‍🎓 Students", len(users_df))

        with col3:
            st.metric("📚 Courses", len(courses_df))

        with col4:
            st.metric("💳 Transactions", len(transactions_df))

    # =====================================================
    # TEACHERS
    # =====================================================

    elif module == "Teachers":

        if st.session_state.role == "Student":

            st.error("Access Denied")
            st.stop()

        st.title("👨‍🏫 Teachers Dashboard")

        st.dataframe(
            teachers_df,
            use_container_width=True
        )

        fig = px.bar(
            teachers_df,
            x="TeacherName",
            y="TeacherRating",
            color="Expertise",
            template="plotly_dark",
            title="Teacher Performance"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # =====================================================
    # STUDENTS
    # =====================================================

    elif module == "Students":

        st.title("👨‍🎓 Students Dashboard")

        st.dataframe(
            users_df,
            use_container_width=True
        )

    # =====================================================
    # COURSES
    # =====================================================

    elif module == "Courses":

        st.title("📚 Courses Dashboard")

        st.dataframe(
            courses_df,
            use_container_width=True
        )

        fig = px.pie(
            courses_df,
            names="CourseCategory",
            hole=0.5,
            template="plotly_dark",
            title="Course Categories"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # =====================================================
    # TRANSACTIONS
    # =====================================================

    elif module == "Transactions":

        st.title("💳 Transactions Dashboard")

        st.dataframe(
            transactions_df,
            use_container_width=True
        )

        fig = px.histogram(
            transactions_df,
            x="CourseID",
            color="TeacherID",
            template="plotly_dark",
            title="Transactions Analysis"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # =====================================================
    # ANALYTICS
    # =====================================================

    elif module == "Analytics":

    st.title("📊 Analytics Dashboard")

    teachers_df.columns = teachers_df.columns.str.strip()
    courses_df.columns = courses_df.columns.str.strip()
    transactions_df.columns = transactions_df.columns.str.strip()

    merged_df = transactions_df.merge(
        teachers_df,
        on="TeacherID",
        how="left"
    ).merge(
        courses_df,
        on="CourseID",
        how="left"
    )

    st.dataframe(
        merged_df,
        use_container_width=True
    )

    fig = px.scatter(
        merged_df,
        x="YearsOfExperience",
        y="TeacherRating",
        color="Expertise",
        size="CourseRating",
        hover_data=[
            "TeacherName",
            "CourseName",
            "Amount"
        ],
        template="plotly_dark",
        title="Teacher Experience vs Course Rating"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
    # =====================================================
    # ATTENDANCE
    # =====================================================

    elif module == "Attendance":

        st.title("📅 Attendance Dashboard")

        attendance_data = {

            "Student": [
                "Rahul",
                "Priya",
                "Amit",
                "Sneha"
            ],

            "Attendance %": [
                92,
                88,
                95,
                90
            ]
        }

        attendance_df = pd.DataFrame(
            attendance_data
        )

        st.dataframe(
            attendance_df,
            use_container_width=True
        )

    # =====================================================
    # MARKS
    # =====================================================

    elif module == "Marks":

        st.title("📊 Marks Dashboard")

        marks_data = {

            "Student": [
                "Rahul",
                "Priya",
                "Amit"
            ],

            "Marks": [
                85,
                92,
                88
            ]
        }

        marks_df = pd.DataFrame(
            marks_data
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

        report_data = {

            "Subject": [
                "Python",
                "DBMS",
                "AI",
                "Maths"
            ],

            "Marks": [
                88,
                91,
                84,
                95
            ]
        }

        report_df = pd.DataFrame(
            report_data
        )

        st.dataframe(
            report_df,
            use_container_width=True
        )

        fig = px.bar(
            report_df,
            x="Subject",
            y="Marks",
            color="Marks",
            template="plotly_dark",
            title="Subject Performance"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # =====================================================
    # FOOTER
    # =====================================================

    st.markdown("""
    <div class='footer'>

    <hr>

    <h3>
    🎓 EduPro Smart ERP
    </h3>

    <p>
    Premium AI Powered Education Platform
    </p>

    </div>
    """, unsafe_allow_html=True)