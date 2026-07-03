from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client()

system_instruction = "You are a strict data analyst. Always provide concise answers."

massive_history_steps = [
    {"type": "user_input", "content": [{"type": "text", "text": "Analyze log file 1..."}]},
    {"type": "model_output", "content": [{"type": "text", "text": "Log 1 shows a Redis timeout."}]},
    # ... cientos de turnos y 5,000 líneas de logs viejos que ya no aportan valor ...
    {"type": "user_input", "content": [{"type": "text", "text": "Analyze log file 84..."}]},
    {"type": "model_output", "content": [{"type": "text", "text": "Log 84 shows high CPU usage."}]},
]

compressed_steps = massive_history_steps[-2:]

compressed_steps.append({
    "type": "user_input",
    "content": [{"type": "text", "text": "Based on the recent logs, what is the current system status?"}]
})


interaction = client.interactions.create(
    model="gemini-3.5-flash",
    system_instruction=system_instruction,
    store=False, 
    input=compressed_steps
)

print(interaction.output_text)