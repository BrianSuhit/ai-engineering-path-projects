from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

documents = [
    "A man is playing a guitar in the park.",
    "The new AI model is extremely fast and efficient.",
    "A woman is watching a movie on her laptop."
]
doc_embeddings = model.encode(documents)

query = "How is artificial intelligence evolving?"
query_embedding = model.encode(query)


cosine_scores = util.cos_sim(query_embedding, doc_embeddings)

print(f"Similarity scores: {cosine_scores}")