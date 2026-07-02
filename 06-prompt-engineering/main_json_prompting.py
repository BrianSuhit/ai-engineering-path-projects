from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel

load_dotenv()
client = genai.Client()

class SentimentAnalysis(BaseModel):
    sentiment: str
    confidence: float
    key_phrases: list[str]

system_instruction = "You are a data extraction assistant. Analyze the text and return ONLY a valid JSON."
user_query = "Review: The battery life is decent, but the screen scratches easily."


interaction = client.interactions.create(
    model="gemini-3.5-flash",
    system_instruction=system_instruction,
    input=user_query,
    response_format={
        "type": "text",
        "mime_type": "application/json",
        "schema": SentimentAnalysis.model_json_schema()
    }
)
valid_result = SentimentAnalysis.model_validate_json(interaction.output_text)

print(f"Sentimiento: {valid_result.sentiment}")
print(f"Confianza: {valid_result.confidence}")
print(f"Frases clave: {valid_result.key_phrases}")