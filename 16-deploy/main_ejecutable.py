import time
from dotenv import load_dotenv

# 1. Seguridad: Cargamos credenciales de forma segura desde el entorno local
load_dotenv()

def main():
    print("="*50)
    print("🤖 Asistente de Soporte (Edge / CLI Nativo)")
    print("Escribe 'salir' para terminar la conversación.")
    print("="*50 + "\n")

    # 2. Inicializar la memoria (Session State adaptado a consola)
    messages = []

    # 3. Bucle infinito de interacción
    while True:
        # A) Capturar el nuevo mensaje del usuario
        prompt = input("Tú: ")
        
        if prompt.lower() == 'salir':
            print("Cerrando sistema de forma segura...")
            break
            
        # Guardar el mensaje del usuario en memoria
        messages.append({"role": "user", "content": prompt})

        # 4. Generar la respuesta del Asistente
        print("🤖 Pensando...")
        time.sleep(1.5)  # Simulamos latencia de red/inferencia
        
        # Lógica local (Mock AI - Exactamente la misma que en la versión Web)
        prompt_lower = prompt.lower()
        if "reembolso" in prompt_lower:
            respuesta = "Entiendo que buscas un reembolso. Por favor, indícame tu número de orden de 6 dígitos."
        elif "contraseña" in prompt_lower:
            respuesta = "Para recuperar tu contraseña, haz clic en 'Olvidé mi clave' en el menú principal."
        else:
            respuesta = f"He recibido tu consulta: '{prompt}'. Un operador se pondrá en contacto pronto."
        
        # Mostrar la respuesta en la interfaz de consola
        print(f"🤖 Asistente: {respuesta}\n")
            
        # B) Guardar la respuesta del asistente en la memoria
        messages.append({"role": "assistant", "content": respuesta})

if __name__ == "__main__":
    main()

# --- Pasos para crear un ejecutable (.exe) ---
# 1. Instala las dependencias (si no las tienes):
#    uv add pyinstaller python-dotenv
#
# 2. Ejecuta PyInstaller para crear el .exe:
#    pyinstaller --onefile main_ejecutable.py

# 3. El ejecutable se encontrará en la carpeta 'dist' dentro del directorio del proyecto