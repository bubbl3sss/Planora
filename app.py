import streamlit as st
import pandas as pd


st.set_page_config(
    page_title="Planora",
    page_icon="📚",
    layout="centered"
)

st.title("Planora")
st.caption("An AI-powered study planner that adapts to your energy, time, and deadlines")



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

DISPLAY_NAMES = {
    "subject": "Subject",
    "days_to_exam": "Days until exam",
    "difficulty": "Difficulty level",
    "hours_needed": "Estimated hours",
    "urgency_score": "Urgency",
    "energy_fit_score": "Energy match",
    "priority_score": "Overall priority",
    "recommended_reason": "Why this comes first"
}

def prettify_df(df):
    return df.rename(columns=DISPLAY_NAMES)



st.header("Your current state")

energy_level = st.slider(
    "How’s your energy right now?",
    min_value=1,
    max_value=10,
    value=5
)

available_hours = st.number_input(
    "How many hours can you realistically study today?",
    min_value=0.0,
    max_value=24.0,
    value=4.0,
    step=0.5
)

student_profile = {
    "energy_level_on_10": energy_level,
    "available_hours": available_hours
}


st.header("Your subjects")

num_tasks = st.number_input(
    "How many subjects do you want to plan for?",
    min_value=1,
    max_value=10,
    value=3
)

tasks = []

for i in range(int(num_tasks)):
    st.subheader(f"Subject {i + 1}")

    subject = st.text_input("Subject name", key=f"subject_{i}")

    days_to_exam = st.number_input(
        "Days until exam",
        min_value=0,
        value=10,
        key=f"days_{i}"
    )

    difficulty = st.slider(
        "Difficulty level",
        min_value=1,
        max_value=10,
        value=5,
        key=f"difficulty_{i}"
    )

    hours_needed = st.number_input(
        "Estimated hours needed",
        min_value=0.0,
        value=2.0,
        step=0.5,
        key=f"hours_{i}"
    )

    tasks.append({
        "subject": subject,
        "days_to_exam": days_to_exam,
        "difficulty": difficulty,
        "hours_needed": hours_needed
    })


st.divider()

if st.button("✨ Generate my study plan"):

    tasks_df = pd.DataFrame(tasks)

    if tasks_df["subject"].isnull().any() or (tasks_df["subject"] == "").any():
        st.warning("Please fill in all subject names.")
    else:
        final_plan = prioritize_tasks(tasks_df, student_profile)

        st.header("Your personalised plan")

        st.dataframe(prettify_df(final_plan), use_container_width=True)

        st.header(" How to read this")
        st.write(
            """
            Subjects at the top deserve your attention first.
            Planora balances **exam urgency**, **difficulty**, and **your current energy**
            so you don’t burn out while still staying on track.
            """
        )

        st.success("Plan generated successfully")

