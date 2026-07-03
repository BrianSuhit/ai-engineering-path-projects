from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client()

user_preferences = {"favorite_color": "#46778F", "profession": "AI Engineer"}
system_instruction = f"User context: {user_preferences}. Personalize your answers based on this context."

interaction_1 = client.interactions.create(
    model="gemini-3.5-flash",
    system_instruction=system_instruction,
    input="Hi! Remind me, what is my favorite color?"
)
print("Turno 1:", interaction_1.output_text)


interaction_2 = client.interactions.create(
    model="gemini-3.5-flash",
    previous_interaction_id=interaction_1.id,
    input="Awesome. Can you suggest a secondary color that matches well with it?"
)
print("Turno 2:", interaction_2.output_text)