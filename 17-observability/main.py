import time
import json
from functools import wraps

# 1. La Arquitectura del Tracer: Un decorador reutilizable
def trace_step(step_name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            status = "SUCCESS"
            error_msg = None
            
            # Ejecutamos la "caja negra" (la función original)
            try:
                result = func(*args, **kwargs)
            except Exception as e:
                result = None
                status = "ERROR"
                error_msg = str(e)
                raise e
            finally:
                end_time = time.time()
                latency_ms = round((end_time - start_time) * 1000, 2)
                
                # 2. Empaquetamos la radiografía completa del evento
                trace_data = {
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "step": step_name,
                    "latency_ms": latency_ms,
                    "status": status,
                    "inputs": {"args": args, "kwargs": kwargs},
                    "outputs": result,
                    "error": error_msg
                }
                
                # 3. Guardamos la traza de forma persistente (Append-only)
                with open("agent_traces.jsonl", "a", encoding="utf-8") as f:
                    f.write(json.dumps(trace_data, ensure_ascii=False) + "\n")
                    
            return result
        return wrapper
    return decorator

# ==========================================
# Implementación en nuestro Sistema RAG
# ==========================================

@trace_step(step_name="Vectorial_Retrieval")
def retrieve_context(query: str):
    # Simulamos la latencia de una Vector DB como ChromaDB
    time.sleep(0.4)
    return ["El protocolo MCP estandariza la conexión con herramientas externas."]

@trace_step(step_name="LLM_Inference")
def generate_response(query: str, context: list):
    # Simulamos la latencia y respuesta de Gemini
    time.sleep(1.2)
    return f"Basado en tus datos: {context}"

@trace_step(step_name="LLM_Inference_WithError")
def generate_response_with_error(query: str, context: list):
    # Simulamos un error en la API de Gemini
    time.sleep(0.5)
    raise ValueError("API Key not valid or quota exceeded")

if __name__ == "__main__":
    # --- Ejemplo 1: Flujo Exitoso ---
    print("🚀 Procesando consulta exitosa...\n")
    
    user_query = "¿Qué hace el protocolo MCP?"
    
    retrieved_docs = retrieve_context(user_query)
    final_answer = generate_response(query=user_query, context=retrieved_docs)
    
    print(f"🤖 Asistente: {final_answer}\n")
    print("-" * 50)

    # --- Ejemplo 2: Flujo con Falla ---
    print("🔥 Procesando consulta con falla...\n")
    
    failing_query = "Esta consulta va a fallar"
    
    try:
        retrieved_docs_fail = retrieve_context(failing_query)
        # Usamos la función que simula un error
        generate_response_with_error(query=failing_query, context=retrieved_docs_fail)
    except Exception as e:
        print(f"🔴 Error capturado en el flujo principal: {e}\n")

    print("✅ Operación finalizada. Revisá el archivo 'agent_traces.jsonl' para ver todas las trazas.")