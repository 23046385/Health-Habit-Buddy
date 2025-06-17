import streamlit as st
import subprocess
from config import HABITS, LLM_MODEL, UI_THEME
import pandas as pd
from datetime import datetime, timedelta

# --- In-memory habit completions log ---
habit_log = {habit: [] for habit in HABITS}

# --- Function to get encouragement message from Ollama ---
def get_encouragement(habit):
    prompt = f"Give a short, friendly, encouraging message for someone who just completed the habit: {habit}"
    try:
        result = subprocess.run(
            ["ollama", "run", LLM_MODEL, prompt],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"AI error: {e}"

# --- Streamlit UI setup ---
st.set_page_config(page_title="Health Habit Buddy", layout="centered")
st.markdown(
    f"""
    <style>
    body {{
        background-color: {UI_THEME['background']};
        color: {UI_THEME['text']};
    }}
    div.stButton > button {{
        background-color: {UI_THEME['button_color']};
        color: {UI_THEME['button_text']};
        border-radius: 8px;
        padding: 8px 24px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Health Habit Buddy")

# --- Habit encouragement buttons ---
for habit in HABITS:
    if st.button(f"Complete {habit}"):
        # Log completion date
        habit_log[habit].append(datetime.now().date())
        encouragement = get_encouragement(habit)
        st.success(f"{habit} completed! Message: {encouragement}")

# --- Weekly calendar heatmap ---

def get_week_dates():
    today = datetime.now().date()
    start = today - timedelta(days=today.weekday())  # Monday this week
    return [start + timedelta(days=i) for i in range(7)]

week_dates = get_week_dates()

# Prepare data for calendar graph
data = []
for habit in HABITS:
    counts = []
    for day in week_dates:
        c = [d for d in habit_log[habit] if d == day]
        counts.append(len(c))
    data.append(counts)

df = pd.DataFrame(data, index=HABITS, columns=[d.strftime("%a\n%d-%b") for d in week_dates])

st.subheader("Habit Completion This Week")

# Style for heatmap with black and white theme
def color_map(val):
    if val == 0:
        return f"background-color: #222222; color: #555555"
    else:
        return f"background-color: #00FF00; color: #000000; font-weight: bold"

st.dataframe(df.style.applymap(color_map), height=250)

st.markdown(
    "<p style='color:#888;font-size:0.8em;margin-top:20px;'>Note: Data resets on app reload (no persistent storage).</p>",
    unsafe_allow_html=True
)
