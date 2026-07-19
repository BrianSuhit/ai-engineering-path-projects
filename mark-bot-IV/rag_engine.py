from chromadb.types import Collection

def retrieve_and_augment(query: str, collection: Collection) -> str:
    # 1. Similarity Search: Fetch the 3 most relevant chunks from the provided collection
    results = collection.query(
        query_texts=[query],
        n_results=3
    )

    # 2. Extract the payload (the original text chunks)
    # ChromaDB returns a list of lists, so we extract the first one [0]
    retrieved_chunks = results["documents"][0]
    context = "\n\n---\n\n".join(retrieved_chunks)

    # 3. Grounded Generation: Assemble the Prompt Template
    augmented_prompt = f"""Relevant information:
{context}

Provide a concise answer to the following question using the relevant information provided above:
{query}"""

    return augmented_prompt