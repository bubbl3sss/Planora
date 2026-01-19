import streamlit as st
import pandas as pd

def compute_urgency_score(tasks_df):
    max_days = tasks_df["days_to_exam"].max()
    tasks_df["urgency_score"] = max_days - tasks_df["days_to_exam"]
    return tasks_df

def compute_energy_level_score(tasks_df, student_profile):
    energy_level = student_profile["energy_level_on_10"]
    tasks_df["energy_fit_score"] = tasks_df["difficulty"] * (energy_level / 5)
    return tasks_df

def compute_priority_score(tasks_df):
    tasks_df["priority_score"] = (
        tasks_df["urgency_score"] * 0.5 +
        tasks_df["difficulty"] * 0.3 +
        tasks_df["energy_fit_score"] * 0.2
    )
    return tasks_df

def prioritize_tasks(tasks_df, student_profile):
    tasks_df = compute_urgency_score(tasks_df)
    tasks_df = compute_energy_level_score(tasks_df, student_profile)
    tasks_df = compute_priority_score(tasks_df)
    return tasks_df.sort_values(by="priority_score", ascending=False)

st.title("📚 Planora — Smart Study Planner")

st.sidebar.header("Student Profile")

energy = st.sidebar.slider("Energy level (1–10)", 1, 10, 6)
available_hours = st.sidebar.number_input("Available study hours today", 1, 12, 3)

student_profile = {
    "energy_level_on_10": energy,
    "available_hours": available_hours
}

st.header("Enter Tasks")

tasks_input = st.text_area(
    "Enter tasks as: subject,days_to_exam,attendance,difficulty,hours_needed",
    "Mathematics,12,78,4,3\nData Structures,15,82,7,4"
)

if st.button("Generate Plan"):
    rows = [row.split(",") for row in tasks_input.strip().split("\n")]
    tasks_df = pd.DataFrame(
        rows,
        columns=["subject","days_to_exam","attendance_p","difficulty","hours_needed"]
    )

    tasks_df[["days_to_exam","attendance_p","difficulty","hours_needed"]] = \
        tasks_df[["days_to_exam","attendance_p","difficulty","hours_needed"]].astype(int)

    plan = prioritize_tasks(tasks_df, student_profile)

    st.subheader("Your Optimized Study Plan")
    st.dataframe(plan)
