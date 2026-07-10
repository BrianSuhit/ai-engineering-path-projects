
import base64
import json
from google import genai
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()
client = genai.Client()

class ImageAnalysis(BaseModel):
    description: str = Field(description="Una breve descripción general de la imagen.")
    dominant_colors: list[str] = Field(description="Lista de los colores predominantes.")
    objects_detected: list[str] = Field(description="Lista de objetos reconocibles en la escena.")

try:
    with open("images/sample.jpg", "rb") as f:
        image_bytes = f.read()
        image_b64 = base64.b64encode(image_bytes).decode("utf-8")
except FileNotFoundError:
    print("🚨 Error: No se encontró el archivo 'images/sample.jpg'. Asegurate que la imagen exista en esa ruta.")
    exit()

print("📸 Analizando imagen...")

interaction = client.interactions.create(
    model="gemini-3.5-flash",
    input=[
        {"type": "text", "text": "Analizá esta imagen en detalle y extraé la información solicitada."},
        {
            "type": "image",
            "data": image_b64,
            "mime_type": "image/jpeg"
        }
    ],
    response_format={
        "type": "text",
        "mime_type": "application/json",
        "schema": ImageAnalysis.model_json_schema()
    }
)

analysis_result = ImageAnalysis.model_validate_json(interaction.output_text)

print("\n🤖 Resultado Estructurado:")
print(json.dumps(analysis_result.model_dump(), indent=2, ensure_ascii=False))