from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client()

system_instruction = """
You are an expert logical reasoner.
Always think step-by-step and write down your reasoning steps before providing the final answer.
End your response strictly with 'FINAL ANSWER: [result]'.
"""

user_query = "If John has 3 apples, gives away 1, buys 5 more, and splits them equally with his brother, how many apples does each get?"


reasoning_paths = []
for i in range(3):
    interaction = client.interactions.create(
        model="gemini-3.5-flash",
        system_instruction=system_instruction,
        generation_config={"temperature": 0.7},
        input=user_query
    )
    reasoning_paths.append(interaction.output_text)


for idx, path in enumerate(reasoning_paths):
    print(f"--- Reasoning Path {idx + 1} ---")
    print(path, "\n")