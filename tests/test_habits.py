# tests/test_habits.py
import pytest
from utils import format_ai_prompt, complete_habit_logic

def test_format_ai_prompt():
    habit = "Walk"
    prompt = format_ai_prompt(habit)
    assert "encouraging message" in prompt.lower()
    assert habit in prompt

def test_complete_habit_logic():
    completed = []
    habit = "Run"
    completed = complete_habit_logic(completed, habit)
    assert habit in completed
