from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client()

system_instruction = """
You are a strict sentiment analyzer.
Analyze the review and reply ONLY with 'POSITIVE', 'NEGATIVE', or 'NEUTRAL'.
"""

few_shot_examples = """
Review: The product was amazing and delivery was super fast!
Sentiment: POSITIVE

Review: It broke after two days of use. Terrible quality.
Sentiment: NEGATIVE

Review: It works exactly as expected, nothing special to mention.
Sentiment: NEUTRAL
"""

user_query = "Review: The battery life is decent, but the screen scratches easily.\nSentiment:"

full_prompt = f"{few_shot_examples}\n{user_query}"


interaction = client.interactions.create(
    model="gemini-3.5-flash",
    system_instruction=system_instruction,
    input=full_prompt
)

print(interaction.output_text)