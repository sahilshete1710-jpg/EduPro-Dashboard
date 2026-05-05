import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------
# PAGE CONFIG
# -----------------------
st.set_page_config(
    page_title="EduPro AI Dashboard",
    page_icon="🎓",
    layout="wide"
)

# -----------------------
# LOAD DATA
# -----------------------
@st.cache_data
def load_data():
    return pd.read_csv("final_dataset.csv")

df = load_data()

# -----------------------
# HEADER WITH BRANDING
# -----------------------
col_logo, col_title = st.columns([1, 5])

with col_logo:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135755.png", width=80)

with col_title:
    st.title("EduPro AI Analytics Dashboard")
    st.caption("Smart Insights for Instructor & Course Performance")

# -----------------------
# SIDEBAR
# -----------------------
st.sidebar.title("🎯 Smart Filters")

expertise = st.sidebar.multiselect(
    "Expertise",
    df["Expertise"].unique(),
    default=df["Expertise"].unique()
)

category = st.sidebar.multiselect(
    "Course Category",
    df["CourseCategory"].unique(),
    default=df["CourseCategory"].unique()
)

level = st.sidebar.multiselect(
    "Course Level",
    df["CourseLevel"].unique(),
    default=df["CourseLevel"].unique()
)

filtered_df = df[
    (df["Expertise"].isin(expertise)) &
    (df["CourseCategory"].isin(category)) &
    (df["CourseLevel"].isin(level))
]

# -----------------------
# EMPTY STATE
# -----------------------
if filtered_df.empty:
    st.warning("⚠️ No data available for selected filters")
    st.stop()

# -----------------------
# KPI SECTION
# -----------------------
st.subheader("📊 Key Performance Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("⭐ Avg Teacher Rating", round(filtered_df["TeacherRating"].mean(), 2))
col2.metric("📚 Avg Course Rating", round(filtered_df["CourseRating"].mean(), 2))
col3.metric("🎯 Enrollments", len(filtered_df))
col4.metric("👨‍🏫 Instructors", filtered_df["TeacherID"].nunique())

# -----------------------
# CHARTS
# -----------------------
st.subheader("📈 Experience vs Rating")

fig1 = px.scatter(
    filtered_df,
    x="YearsOfExperience",
    y="TeacherRating",
    color="Expertise",
    size="CourseRating",
    hover_data=["TeacherName"],
    template="plotly_dark"
)
st.plotly_chart(fig1, use_container_width=True)

# -----------------------
st.subheader("🔥 Course Quality Heatmap")

pivot = filtered_df.pivot_table(
    values="CourseRating",
    index="CourseCategory",
    columns="CourseLevel"
)

fig2 = px.imshow(
    pivot,
    text_auto=True,
    color_continuous_scale="RdBu",
    template="plotly_dark"
)
st.plotly_chart(fig2, use_container_width=True)

# -----------------------
st.subheader("🏆 Top Instructors")

top = (
    filtered_df.groupby("TeacherName")["TeacherRating"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig3 = px.bar(
    top,
    x="TeacherName",
    y="TeacherRating",
    color="TeacherRating",
    template="plotly_dark"
)
st.plotly_chart(fig3, use_container_width=True)

# -----------------------
# SMART INSIGHTS (AUTO)
# -----------------------
st.subheader("🤖 AI Insights")

avg_rating = round(filtered_df["TeacherRating"].mean(), 2)
top_teacher = top.iloc[0]["TeacherName"]
top_rating = round(top.iloc[0]["TeacherRating"], 2)

best_category = (
    filtered_df.groupby("CourseCategory")["CourseRating"]
    .mean()
    .sort_values(ascending=False)
    .index[0]
)

st.success(f"""
• Average instructor rating is **{avg_rating}**, indicating overall platform quality  
• Top instructor is **{top_teacher}** with rating **{top_rating}**  
• Best performing course category is **{best_category}**  
• Instructor quality strongly impacts course success and enrollments  
""")

# -----------------------
# DOWNLOAD
# -----------------------
st.subheader("⬇️ Export Data")

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "Download Filtered Dataset",
    csv,
    "EduPro_Data.csv",
    "text/csv"
)

# -----------------------
# FOOTER
# -----------------------
st.markdown("---")
st.caption("Built with ❤️ using Streamlit | EduPro Analytics Project")