import streamlit as st
import subprocess
import json
from datetime import datetime, timedelta
import pandas as pd
import altair as alt

from config import HABITS, LLM_MODEL, UI_THEME

# Initialize or load habit completion history from session state
if "history" not in st.session_state:
    st.session_state.history = []

def run_ollama_prompt(habit):
    try:
        # Ollama command without --stdin flag, prompt passed directly
        result = subprocess.run(
            ["ollama", "run", LLM_MODEL, "--prompt", f"Give a short, friendly, encouraging message for someone who just completed the habit: {habit}"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"AI error: {e}"

def update_history(completed_habits):
    timestamp = datetime.now()
    for habit in completed_habits:
        st.session_state.history.append({"habit": habit, "time": timestamp})

def draw_calendar_graph(history):
    if not history:
        st.write("No habit completion data yet.")
        return
    
    # Create DataFrame of completion dates and habits
    df = pd.DataFrame(history)
    df["date"] = df["time"].dt.date

    # Count completions per day
    daily_counts = df.groupby("date").size().reset_index(name="count")
    
    # Create calendar-like heatmap for last 7 days
    today = datetime.now().date()
    last_week = [today - timedelta(days=i) for i in range(6, -1, -1)]
    counts = []
    for day in last_week:
        c = daily_counts.loc[daily_counts["date"] == day, "count"]
        counts.append(int(c) if not c.empty else 0)
    
    calendar_df = pd.DataFrame({
        "date": last_week,
        "count": counts
    })

    chart = alt.Chart(calendar_df).mark_rect().encode(
        x=alt.X("date:T", title="Date"),
        color=alt.Color("count:Q", scale=alt.Scale(scheme="greys"), title="Habits completed")
    ).properties(
        width=500,
        height=100
    )

    st.altair_chart(chart)

def main():
    st.set_page_config(page_title="Health Habit Buddy", layout="centered")
    st.markdown(
        f"""
        <style>
        .reportview-container {{
            background-color: {UI_THEME['background']};
            color: {UI_THEME['text']};
        }}
        .stButton > button {{
            background-color: {UI_THEME['button']};
            color: {UI_THEME['button_text']};
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("Health Habit Buddy")

    # Habit selection - multiselect for completing multiple habits
    completed = st.multiselect("Select completed habits", HABITS)

    if st.button("Generate Encouragements"):
        if not completed:
            st.warning("Please select at least one habit.")
        else:
            update_history(completed)
            for habit in completed:
                message = run_ollama_prompt(habit)
                st.write(f"{habit} completed! Message: {message}")

    st.markdown("---")
    st.subheader("Weekly Habit Completion Calendar")
    draw_calendar_graph(st.session_state.history)

if __name__ == "__main__":
    main()
