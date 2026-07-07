# Paquetes a descargar:
# pip install google-generativeai python-dotenv
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client()

# 1. Herramienta local (La "mano" del agente)
def get_schedule() -> str:
    return "Lunes: Programacion 1 (15:00 to 18:00)."

# 2. El System Prompt forzando la estructura del bucle ReAct
system_prompt = """
Solve the user query step-by-step following this strict format:
THOUGHT: Describe your thinking process.
ACTION: Write ONLY the name of the tool to use (Available options: get_schedule).

When you receive the OBSERVATION, repeat the process or finish with:
ANSWER: Your final response to the user.
"""

# 3. The Manual ReAct Loop (The core orchestrator)
query = "¿Tengo clases el lunes a las 4 PM?"
history = [
    {"type": "user_input", "content": [{"type": "text", "text": query}]}
]

while True: # Bucle infinito para mantener la conversacion
    # Enviar el historial acumulado al modelo
    interaction = client.interactions.create(
        model="gemini-3.5-flash",
        system_instruction=system_prompt,
        store=False,
        input=history
    )
    
    output = interaction.output_text
    print(output) # Imprime el PENSAMIENTO y la ACCION activos en la consola
    
    # Almacenar los pensamientos del agente en el historial
    history.append({"type": "model_output", "content": [{"type": "text", "text": output}]})
    
    if "ANSWER:" in output:
        break # El agente resolvio el problema, salir del bucle
        
    if "ACTION:" in output:
        # Extraer el nombre de la herramienta de forma segura sin Regex
        # Dividimos por 'ACTION:' y tomamos la cadena limpia de la derecha
        tool_name = output.split("ACTION:")[-1].strip()
        
        if tool_name == "get_schedule":
            result = get_schedule()
            # Inyectar el resultado de vuelta como una Observacion
            observation = f"\nOBSERVATION: {result}"
            history.append({"type": "user_input", "content": [{"type": "text", "text": observation}]})
            print(f"⚙️ System executed tool. Result: {observation}")