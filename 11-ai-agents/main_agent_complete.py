# Packages required:
# pip install google-generativeai python-dotenv

import json
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client()

# ==========================================
# 1. LOCAL TOOLS (The "hands" of the agent)
# ==========================================

def get_schedule(day: str) -> dict:
    """Fetches the university schedule based on the day."""
    day_clean = day.lower().strip()

    if day_clean == "lunes":
        return {"day": day, "subject": "Taller Matematica Computacional", "time": "18:00 a 21:00"}
    elif day_clean == "martes":
        return {"subject": "Programacion 1", "time": "15:00 a 18:00"}
    else:
        return {"subject": "Libre", "time": "Todo el día"}

def get_academic_calendar(query: str) -> dict:
    """Fetches academic calendar events from exa.unicen.edu.ar/calendario-academico/"""
    query_clean = query.lower().strip()

    # Simulating data fetching from the UNICEN website
    if "feriado" in query_clean or "holiday" in query_clean:
        return {"event": "Feriado Nacional", "date": "9 de Julio (Día de la Independencia)", "source": "exa.unicen.edu.ar"}
    elif "examen" in query_clean or "finales" in query_clean:
        return {"event": "Llamado a Finales", "date": "Agosto 2026", "source": "exa.unicen.edu.ar"}
    else:
        return {"event": "Unknown", "message": "No specific dates found. Please check https://exa.unicen.edu.ar/calendario-academico/"}


# ==========================================
# 2. TOOL SCHEMAS & MAPPING
# ==========================================

schedule_tool = {
    "type": "function",
    "name": "get_schedule",
    "description": "Gets the class schedule for a specific day of the week.",
    "parameters": {
        "type": "object",
        "properties": {
            "day": {"type": "string", "description": "The day of the week, e.g. Lunes, Martes"}
        },
        "required": ["day"],
    },
}

calendar_tool = {
    "type": "function",
    "name": "get_academic_calendar",
    "description": "Checks the UNICEN exactas academic calendar for exams, holidays, or important dates.",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "The type of event to look for, e.g. feriado, finales, examen"}
        },
        "required": ["query"],
    },
}

available_functions = {
    "get_schedule": get_schedule,
    "get_academic_calendar": get_academic_calendar
}

# ==========================================
# 3. SYSTEM PROMPT (Guardrails)
# ==========================================
system_prompt = """
You are an academic assistant for the Facultad de Ciencias Exactas at UNICEN.
Your goal is to help students with their schedules and the academic calendar.
STRICT GUARDRAIL: You must ONLY answer questions related to university schedules, holidays, and exams.
If the user asks about anything else (e.g., politics, coding, general knowledge), politely refuse to answer.
"""

# ==========================================
# 4. THE AGENT ORCHESTRATOR LOOP
# ==========================================

user_input = "Tengo clases el martes? Y decime si hay algún feriado pronto según la facultad."
previous_id = None

MAX_ITERATIONS = 5
iteration_count = 0

print(f"👤 USER: {user_input}\n")

while iteration_count < MAX_ITERATIONS:
    iteration_count += 1

    # We pass tools and system_instruction in every call because they are interaction-scoped
    interaction = client.interactions.create(
        model="gemini-3.5-flash",
        input=user_input,
        tools=[schedule_tool, calendar_tool],
        system_instruction=system_prompt,
        previous_interaction_id=previous_id,
    )

    function_results = []

    # Check if the model decided to call any tools
    if interaction.steps:
        for step in interaction.steps:
            if step.type == "function_call":
                # Execute the real Python function safely
                result = available_functions[step.name](**step.arguments)
                print(f"⚙️  System executed tool {step.name}({step.arguments}) -> Result: {result}")

                # Package the result to send it back to the model
                function_results.append({
                    "type": "function_result",
                    "name": step.name,
                    "call_id": step.id,
                    "result": [{"type": "text", "text": json.dumps(result)}],
                })

    # Break the loop if the model didn't call any tools (Final Answer reached)
    if not function_results:
        print(f"\n🤖 ANSWER: {interaction.output_text}")
        break

    # Feed the function results back into the loop
    user_input = function_results
    previous_id = interaction.id

# Failsafe check
if iteration_count >= MAX_ITERATIONS:
    print("\n🚨 ERROR: Agent reached maximum iterations. Stopping to prevent infinite loop and token burning.")