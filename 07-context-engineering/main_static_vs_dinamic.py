from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client()

system_instruction = "You are a helpful customer support AI. Use the provided context to answer."

def get_dynamic_context(query: str) -> str:
    if "shipping" in query.lower():
        return "Context: Shipping takes 2-3 business days via FedEx."
    elif "refund" in query.lower():
        return "Context: Refunds are processed within 5-7 business days."
    return "Context: No specific information found in the database."

user_query = "Hi! How long does shipping usually take?"

relevant_context = get_dynamic_context(user_query)

full_input = f"{relevant_context}\n\nUser Question: {user_query}"

interaction = client.interactions.create(
    model="gemini-3.5-flash",
    system_instruction=system_instruction,
    input=full_input
)

print(interaction.output_text)