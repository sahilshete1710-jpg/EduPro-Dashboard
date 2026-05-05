import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("final_dataset.csv")

st.title("🎓 EduPro Instructor Performance Dashboard")

# Sidebar Filters
st.sidebar.header("Filters")

expertise = st.sidebar.selectbox("Select Expertise", df["Expertise"].unique())
category = st.sidebar.selectbox("Select Category", df["CourseCategory"].unique())

filtered_df = df[(df["Expertise"] == expertise) & (df["CourseCategory"] == category)]

# Top Instructors
st.subheader("🏆 Top Instructors")
top = filtered_df.groupby("TeacherName")["TeacherRating"].mean().sort_values(ascending=False).head(5)
st.write(top)

# Scatter Plot
st.subheader("📈 Experience vs Rating")
fig, ax = plt.subplots()
sns.scatterplot(x="YearsOfExperience", y="TeacherRating", data=filtered_df)
st.pyplot(fig)

# Bar Chart
st.subheader("📊 Expertise Performance")
fig2, ax2 = plt.subplots()
filtered_df.groupby("Expertise")["TeacherRating"].mean().plot(kind="bar")
st.pyplot(fig2)

# Heatmap
st.subheader("🔥 Course Quality Heatmap")
pivot = filtered_df.pivot_table(values="CourseRating", index="CourseCategory", columns="CourseLevel")
fig3, ax3 = plt.subplots()
sns.heatmap(pivot, annot=True)
st.pyplot(fig3)