# Health Habit Buddy

**Health Habit Buddy** is a minimalist wellness app built with **Streamlit** and powered by **local AI via Ollama**. It lets users track daily health habits and receive personalized encouragement using LLaMA 2 — all offline and privacy-focused.

---

## Features

- Add and track daily health habits
- Keep count of habits completed each day
- Get friendly, AI-generated motivational messages for each completed task
- Clean, modern black-and-white interface
- Designed for wellness creators, health-conscious users, and minimalist tech lovers

---

## Tech Stack

- Python 3
- Streamlit (for UI)
- Ollama + LLaMA 2 (for local AI text generation)
- No cloud APIs used – 100% local and private

---

## Run Locally

1. Clone this repo  
   ```bash
   git clone https://github.com/yourname/health-habit-buddy.git
   cd health-habit-buddy


2. Install Python dependencies

    pip install streamlit
    (Make sure Ollama is installed and running:)

    ollama run llama2
    Run the app:

    streamlit run main.py