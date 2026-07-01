import ollama

response = ollama.chat(
    model="gemma4:e2b",
    messages=[
        {"role": "user", "content": "Hello World! Explain AI Engineering in one short sentence."}
    ]
)

print(response["message"]["content"])