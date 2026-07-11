# paquetes necesarios:
# 4. uv add google-genai pydantic python-dotenv

from google import genai
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# 1. Setup inicial
load_dotenv()
client = genai.Client()

# 2. Output Guardrail para el Juez: Forzamos la salida estructurada
class EvaluationResult(BaseModel):
    reasoning: str = Field(description="Step by step explanation of the evaluation based on the rubric.")
    score: int = Field(description="Integer score from 1 to 5. 1 is completely wrong, 5 is perfect.")

# 3. Nuestro dataset de prueba (Gold Standard)
eval_dataset = [
    {
        "question": "What is the capital of France?",
        "expected_context": "The capital of France is Paris."
    },
    {
        "question": "Which open source vector database did we use in the course?",
        "expected_context": "We used ChromaDB as our local open source vector database."
    }
]

# Función generadora (El sistema que estamos evaluando)
def generate_answer(question: str) -> str:
    interaction = client.interactions.create(
        model="gemini-3.5-flash",
        input=question
    )
    return interaction.output_text

# Función evaluadora (El Juez)
def evaluate_response(question: str, expected: str, actual: str) -> EvaluationResult:
    judge_prompt = f"""
    You are an expert AI judge. Evaluate the ACTUAL ANSWER based on the EXPECTED CONTEXT.
    Score it from 1 to 5 based on factual correctness and relevance.

    Question: {question}
    Expected Context: {expected}
    Actual Answer: {actual}
    """

    interaction = client.interactions.create(
        model="gemini-3.5-flash",
        input=judge_prompt,
        response_format={
            "type": "text",
            "mime_type": "application/json",
            "schema": EvaluationResult.model_json_schema()
        }
    )
    return EvaluationResult.model_validate_json(interaction.output_text)

if __name__ == "__main__":
    total_score = 0
    print("🚀 Starting Vanilla Eval Pipeline...\n")

    # 4. El bucle de orquestación de la evaluación
    for i, data in enumerate(eval_dataset):
        print(f"--- Test {i+1} ---")
        print(f"Q: {data['question']}")

        # Fase A: Generar
        actual_answer = generate_answer(data["question"])
        print(f"Generated: {actual_answer}")

        # Fase B: Evaluar (con manejo de errores)
        try:
            eval_result = evaluate_response(data["question"], data["expected_context"], actual_answer)
            print(f"🔎 Judge Score: {eval_result.score}/5")
            print(f"🧠 Judge Reasoning: {eval_result.reasoning}\n")
            total_score += eval_result.score
        except Exception as e:
            print(f"🚨 Error evaluating test {i+1}: {e}\n")
            # Opcionalmente, puedes asignar una puntuación de 0 en caso de error
            # total_score += 0

    # 5. Cálculo de la métrica final del sistema
    average_score = total_score / len(eval_dataset)
    print(f"📊 Final System Average Score: {average_score}/5")