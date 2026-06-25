from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

BASE_DIR = Path(__file__).resolve().parent
EXCEL_PATH = BASE_DIR / "edupro.xlsx"
OUTPUT_DIR = BASE_DIR / "analysis_output"


def load_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    if not EXCEL_PATH.exists():
        raise FileNotFoundError(f"Excel file not found: {EXCEL_PATH}")

    teachers = pd.read_excel(EXCEL_PATH, sheet_name="Teachers")
    courses = pd.read_excel(EXCEL_PATH, sheet_name="Courses")
    transactions = pd.read_excel(EXCEL_PATH, sheet_name="Transactions")
    return teachers, courses, transactions


def normalize_id_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    normalized = df.copy()
    for column in columns:
        if column in normalized.columns:
            normalized[column] = normalized[column].astype(str).str.extract(r"(\d+)", expand=False).fillna(normalized[column].astype(str)).str.lstrip("0")
    return normalized


def create_merged_dataset(
    teachers: pd.DataFrame,
    courses: pd.DataFrame,
    transactions: pd.DataFrame,
) -> pd.DataFrame:
    teachers = normalize_id_columns(teachers, ["TeacherID"])
    courses = normalize_id_columns(courses, ["CourseID"])
    transactions = normalize_id_columns(transactions, ["TeacherID", "CourseID"])

    merged = transactions.merge(teachers, on="TeacherID", how="left")
    merged = merged.merge(courses, on="CourseID", how="left")
    return merged


def save_plot(filename: str) -> None:
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / filename, dpi=150)
    plt.close()


def run_analysis() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    teachers, courses, transactions = load_data()
    df = create_merged_dataset(teachers, courses, transactions)

    final_dataset_path = OUTPUT_DIR / "final_dataset.csv"
    df.to_csv(final_dataset_path, index=False)

    plt.figure(figsize=(8, 5))
    df["TeacherRating"].dropna().hist(bins=10)
    plt.title("Teacher Rating Distribution")
    plt.xlabel("Rating")
    plt.ylabel("Count")
    save_plot("teacher_rating.png")

    plt.figure(figsize=(8, 5))
    sns.scatterplot(x="YearsOfExperience", y="TeacherRating", data=df)
    plt.title("Experience vs Teacher Rating")
    save_plot("experience_vs_rating.png")

    plt.figure(figsize=(9, 5))
    expertise_rating = df.groupby("Expertise")["TeacherRating"].mean().dropna().sort_values()
    if not expertise_rating.empty:
        expertise_rating.plot(kind="bar")
        plt.title("Average Teacher Rating by Expertise")
        plt.xlabel("Expertise")
        plt.ylabel("Average Rating")
        save_plot("expertise_rating.png")
    else:
        plt.close()

    pivot = df.pivot_table(values="CourseRating", index="CourseCategory", columns="CourseLevel", aggfunc="mean")
    if not pivot.empty:
        plt.figure(figsize=(10, 6))
        sns.heatmap(pivot, annot=True, cmap="viridis")
        plt.title("Course Rating by Category and Level")
        save_plot("course_rating_heatmap.png")

    print(f"Analysis completed. Files saved in: {OUTPUT_DIR}")


if __name__ == "__main__":
    run_analysis()


