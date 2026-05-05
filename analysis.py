import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load Excel file
file = "EduPro Online Platform.xlsx"

teachers = pd.read_excel(file, sheet_name="Teachers")
courses = pd.read_excel(file, sheet_name="Courses")
transactions = pd.read_excel(file, sheet_name="Transactions")

# Merge datasets
df = transactions.merge(teachers, on="TeacherID")
df = df.merge(courses, on="CourseID")

# Save final dataset
df.to_csv("final_dataset.csv", index=False)

print("Merged Dataset Created!")

# ----------------------------
# EDA START
# ----------------------------

# 1. Teacher Rating Distribution
plt.figure()
df["TeacherRating"].hist()
plt.title("Teacher Rating Distribution")
plt.savefig("teacher_rating.png")

# 2. Experience vs Rating
plt.figure()
sns.scatterplot(x="YearsOfExperience", y="TeacherRating", data=df)
plt.title("Experience vs Teacher Rating")
plt.savefig("experience_vs_rating.png")

# 3. Expertise vs Rating
plt.figure()
df.groupby("Expertise")["TeacherRating"].mean().plot(kind="bar")
plt.title("Expertise vs Teacher Rating")
plt.savefig("expertise_rating.png")

# 4. Course Category vs Rating
pivot = df.pivot_table(values="CourseRating", index="CourseCategory", columns="CourseLevel")
sns.heatmap(pivot, annot=True)
plt.title("Course Category vs Rating Heatmap")
plt.savefig("heatmap.png")

print("EDA Completed!")