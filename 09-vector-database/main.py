# Primero se importa el paquete de chromadb con 'uv add chromadb'

import chromadb

chroma_client = chromadb.Client()

collection = chroma_client.create_collection(name="brian_university_subjects")

collection.add(
    documents=[
        "Brian cursa Programación en el 2do cuatrimestre.",
        "Brian cursa Web 1 en el 2do cuatrimestre.",
        "Brian cursa Inglés 2 en el 2do cuatrimestre.",
        "Brian cursa Teoría de la información en las organizaciones en el 2do cuatrimestre."
    ],
    metadatas=[
        {"category": "software"},
        {"category": "software"},
        {"category": "language"},
        {"category": "business"}
    ],
    ids=["subj_prog", "subj_web", "subj_eng", "subj_teo"]
)

user_query = "¿Qué materia tiene Brian que sirva para hacer páginas en internet?"

results = collection.query(
    query_texts=[user_query],
    n_results=1
)

print("User Query:", user_query)
print("Retrieved Context:", results['documents'])