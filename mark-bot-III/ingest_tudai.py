import chromadb
import uuid

# 1. Initialize persistent Vector Database
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="tudai_knowledge")

# 2. Read the raw Markdown data
with open("data/tudai_knowledge.md", "r", encoding="utf-8") as file:
    markdown_content = file.read()

# 3. Document structure-based chunking (splitting by main headers)
raw_chunks = markdown_content.split("\n## ")
processed_chunks = []

for index, chunk in enumerate(raw_chunks):
    # Re-attach the header syntax removed by the split (except for the title)
    clean_chunk = chunk if index == 0 else "## " + chunk
    processed_chunks.append(clean_chunk.strip())

# 4. Embed and store the chunks in ChromaDB
for chunk in processed_chunks:
    chunk_id = str(uuid.uuid4())
    collection.add(
        documents=[chunk],
        metadatas=[{"source": "tudai.md"}],
        ids=[chunk_id]
    )

print(f"Ingestion complete! {len(processed_chunks)} chunks saved to ChromaDB.")