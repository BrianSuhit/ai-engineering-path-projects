# No te olvides de los paquetes: 
# uv add chromadb python-dotenv google-genai

import chromadb
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client()

chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="brian_university_syllabus")

pdf_chunks = [
    "Brian cursa Programación en el 2do cuatrimestre.",
    "Brian cursa Web 1 en el 2do cuatrimestre.",
    "Brian cursa Inglés 2 en el 2do cuatrimestre.",
    "Brian cursa Teoría de la información en las organizaciones en el 2do cuatrimestre."
]

collection.add(
    documents=pdf_chunks,
    ids=["chunk_1", "chunk_2", "chunk_3", "chunk_4"]
)

user_query = "¿Qué materias tengo en el segundo cuatrimestre que impliquen escribir código?"

results = collection.query(
    query_texts=[user_query],
    n_results=2
)

retrieved_context = " ".join(results['documents'][0])

final_prompt = f"""
You are a helpful university assistant. Answer the student's question using ONLY the provided information below.
Do not hallucinate or invent subjects.

Retrieved Information:
{retrieved_context}

Student Question: {user_query}
"""

interaction = client.interactions.create(
    model="gemini-3.5-flash",
    input=final_prompt
)

print("=== RAG SYSTEM RESPONSE ===")
print(interaction.output_text)
