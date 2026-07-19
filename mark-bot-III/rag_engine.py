import chromadb

def retrieve_and_augment(query: str) -> str:
    # 1. Connect to the persistent Vector Database
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    collection = chroma_client.get_collection(name="tudai_knowledge")

    # 2. Similarity Search: Fetch the 3 most relevant chunks
    results = collection.query(
        query_texts=[query],
        n_results=3
    )

    # 3. Extract the payload (the original text chunks)
    # ChromaDB returns a list of lists, so we extract the first one [0]
    retrieved_chunks = results["documents"][0]
    context = "\n\n---\n\n".join(retrieved_chunks)

    # 4. Grounded Generation: Assemble the Prompt Template
    augmented_prompt = f"""Relevant information:
{context}

Provide a concise answer to the following question using the relevant information provided above:
{query}"""

    return augmented_prompt