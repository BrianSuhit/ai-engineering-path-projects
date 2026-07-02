from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel

load_dotenv()
client = genai.Client()

# Paso 1: Definimos la estructura de datos que nuestro software necesita usando Pydantic.
# El modelo estará obligado a devolver exactamente estas llaves y estos tipos de datos.
class SentimentAnalysis(BaseModel):
    sentiment: str
    confidence: float
    key_phrases: list[str]

# Paso 2: Creamos las instrucciones y la consulta del usuario
system_instruction = "You are a data extraction assistant. Analyze the text and return ONLY a valid JSON."
user_query = "Review: The battery life is decent, but the screen scratches easily."

# Paso 3: Ejecutamos la inferencia forzando la salida estructurada.
# Pasamos nuestro esquema de Pydantic directamente en la configuración de la API.
interaction = client.interactions.create(
    model="gemini-3.5-flash",
    system_instruction=system_instruction,
    input=user_query,
    response_format={
        "type": "text",
        "mime_type": "application/json",
        "schema": SentimentAnalysis.model_json_schema()  # <- Convierte Pydantic a JSON Schema crudo
    }
)
valid_result = SentimentAnalysis.model_validate_json(interaction.output_text)

print(f"Sentimiento: {valid_result.sentiment}")
print(f"Confianza: {valid_result.confidence}")
print(f"Frases clave: {valid_result.key_phrases}")