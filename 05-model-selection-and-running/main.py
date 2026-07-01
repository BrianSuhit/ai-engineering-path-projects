from dotenv import load_dotenv

from google import genai

load_dotenv()

client = genai.Client()

interaction = client.interactions.create(
    model="gemini-3.5-flash",
    input="Hello world! Explain AI Engineering in one short sentence."
)
    
print(interaction.output_text)