# Paquetes a descargar:
# pip install google-generativeai python-dotenv
import json
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client()

def get_schedule(day: str) -> dict:
    """Consulta tus horarios de la universidad en base al día."""
    day_clean = day.lower().strip()
    
    if day_clean == "lunes":
        return {"day": day, "subject": "Taller Matematica Computacional", "time": "18:00 a 21:00"}
    elif day_clean == "martes":
        return {"day": day, "subject": "Programacion 1", "time": "15:00 a 18:00"}
    else:
        return {"day": day, "subject": "Libre", "time": "Todo el día"}


# 1. Define el esquema de la herramienta (La "mano" del agente)
schedule_tool = {
    "type": "function",
    "name": "get_schedule",
    "description": "Gets the class schedule for a specific day of the week.",
    "parameters": {
        "type": "object",
        "properties": {
            "day": {
                "type": "string",
                "description": "The day of the week, e.g. Lunes, Martes"
            },
        },
        "required": ["day"],
    },
}

# 2. Mapea el nombre del esquema a la función local de Python
available_functions = {
    "get_schedule": get_schedule
}

user_input = "Do I have classes next monday?"
previous_id = None

# 3. El Bucle Orquestador (Modo con estado)
while True:
    interaction = client.interactions.create(
        model="gemini-3.5-flash",
        input=user_input,
        tools=[schedule_tool],
        previous_interaction_id=previous_id,
    )
    
    function_results = []
    
    # 4. Comprueba si el modelo decidió llamar a una función
    for step in interaction.steps:
        if step.type == "function_call":
            # Ejecuta la función real de Python de forma segura
            result = available_functions[step.name](**step.arguments)
            print(f"⚙️ System executed tool {step.name}({step.arguments}) -> Result: {result}")
            
            # Empaqueta el resultado para enviarlo de vuelta al modelo
            function_results.append({
                "type": "function_result",
                "name": step.name,
                "call_id": step.id,
                "result": [{"type": "text", "text": json.dumps(result)}],
            })
            
    # 5. Rompe el bucle si el modelo no llamó a ninguna herramienta (Respuesta final alcanzada)
    if not function_results:
        print(f"\n🤖 ANSWER: {interaction.output_text}")
        break
        
    # 6. Vuelve a introducir los resultados de la función en el bucle
    user_input = function_results
    previous_id = interaction.id