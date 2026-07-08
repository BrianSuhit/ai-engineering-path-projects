# Paquetes requeridos:
# pip install google-genai python-dotenv

import json
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client()

# ==========================================
# 1. HERRAMIENTAS LOCALES (Las "manos" del agente)
# ==========================================

def get_schedule(day: str) -> dict:
    """Consulta los horarios de la universidad en base al día."""
    day_clean = day.lower().strip()

    if day_clean == "lunes":
        return {"day": day, "subject": "Taller Matematica Computacional", "time": "18:00 a 21:00"}
    elif day_clean == "martes":
        return {"subject": "Programacion 1", "time": "15:00 a 18:00"}
    else:
        return {"subject": "Libre", "time": "Todo el día"}

def get_academic_calendar(query: str) -> dict:
    """Fetches academic calendar events from exa.unicen.edu.ar/calendario-academico/"""
    """Consulta eventos del calendario académico desde exa.unicen.edu.ar/calendario-academico/"""
    query_clean = query.lower().strip()

    # Simula la obtención de datos del sitio web de la UNICEN
    if "feriado" in query_clean or "holiday" in query_clean:
        return {"event": "Feriado Nacional", "date": "9 de Julio (Día de la Independencia)", "source": "exa.unicen.edu.ar"}
    elif "examen" in query_clean or "finales" in query_clean:
        return {"event": "Llamado a Finales", "date": "Agosto 2026", "source": "exa.unicen.edu.ar"}
    else:
        return {"event": "Unknown", "message": "No specific dates found. Please check https://exa.unicen.edu.ar/calendario-academico/"}


# ==========================================
# 2. ESQUEMAS DE HERRAMIENTAS Y MAPEO
# ==========================================

schedule_tool = {
    "type": "function",
    "name": "get_schedule",
    "description": "Gets the class schedule for a specific day of the week.",
    "parameters": {
        "type": "object",
        "properties": {
            "day": {"type": "string", "description": "El día de la semana, ej. Lunes, Martes"}
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
            "query": {"type": "string", "description": "El tipo de evento a buscar, ej. feriado, finales, examen"}
        },
        "required": ["query"],
    },
}

available_functions = {
    "get_schedule": get_schedule,
    "get_academic_calendar": get_academic_calendar
}

# ==========================================
# 3. PROMPT DE SISTEMA (Barandillas de seguridad)
# ==========================================
system_prompt = """
Eres un asistente académico para la Facultad de Ciencias Exactas de la UNICEN.
Tu objetivo es ayudar a los estudiantes con sus horarios y el calendario académico.
REGLA ESTRICTA: SOLO debes responder preguntas relacionadas con horarios universitarios, feriados y exámenes.
Si el usuario pregunta sobre cualquier otra cosa (por ejemplo, política, programación, conocimiento general), rehúsa cortésmente a responder.
"""

# ==========================================
# 4. EL BUCLE ORQUESTADOR DEL AGENTE
# ==========================================

user_input = "Tengo clases el martes? Y decime si hay algún feriado pronto según la facultad."
previous_id = None

MAX_ITERATIONS = 5
iteration_count = 0

print(f"👤 USER: {user_input}\n")

while iteration_count < MAX_ITERATIONS:
    iteration_count += 1
    

    # Pasamos las herramientas y la instrucción del sistema en cada llamada porque tienen alcance de interacción
    interaction = client.interactions.create(
        model="gemini-3.5-flash",
        input=user_input,
        tools=[schedule_tool, calendar_tool],
        system_instruction=system_prompt,
        previous_interaction_id=previous_id,
    )

    function_results = []

    # Comprueba si el modelo decidió llamar a alguna herramienta
    if interaction.steps:
        for step in interaction.steps:
            if step.type == "function_call":
                # Ejecuta la función real de Python de forma segura
                result = available_functions[step.name](**step.arguments)
                print(f"⚙️  System executed tool {step.name}({step.arguments}) -> Result: {result}")

                # Empaqueta el resultado para enviarlo de vuelta al modelo
                function_results.append({
                    "type": "function_result",
                    "name": step.name,
                    "call_id": step.id,
                    "result": [{"type": "text", "text": json.dumps(result)}],
                })

    # Si el modelo no llamó a ninguna herramienta, rompe el bucle (Respuesta final alcanzada)
    if not function_results:
        print(f"\n🤖 ANSWER: {interaction.output_text}")
        break

    # Vuelve a introducir los resultados de la función en el bucle
    user_input = function_results
    previous_id = interaction.id

# Failsafe check
if iteration_count >= MAX_ITERATIONS:
    print("\n🚨 ERROR: El agente alcanzó el máximo de iteraciones. Deteniéndose para evitar bucles infinitos y consumo de tokens.")