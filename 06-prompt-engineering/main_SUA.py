from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client()

system_instruction = """
You are a Senior AI Engineer. Your tone is direct and professional.
Always answer the user's question concisely and format your output using markdown bullet points.
"""

user_query = "Explain the difference between System and User prompts."

interaction = client.interactions.create(
    model="gemini-3.5-flash",
    system_instruction=system_instruction,
    input=user_query
)

print(interaction.output_text)