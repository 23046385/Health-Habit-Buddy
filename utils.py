# utils.py
def format_ai_prompt(habit):
    return f"Give a short, friendly, encouraging message for someone who just completed the habit: {habit}"

def complete_habit_logic(completed_list, habit):
    completed_list.append(habit)
    return completed_list
