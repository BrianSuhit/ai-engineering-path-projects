import streamlit as st
import time

# Configuración básica de la página
st.set_page_config(page_title="Soporte AI", page_icon="🤖")
st.title("🤖 Asistente de Soporte (Local)")
st.caption("Un chatbot de interfaz web simulando respuestas sin APIs externas.")

# PASO 1: Inicializar la memoria (Session State)
# Si es la primera vez que el usuario abre la página, la lista "messages" no existirá.
# La creamos vacía para empezar a guardar el historial.
if "messages" not in st.session_state:
    st.session_state.messages = []

# PASO 2: Renderizar el historial en pantalla
# Como Streamlit recarga todo el código con cada interacción, 
# volvemos a dibujar todos los mensajes guardados en la memoria.
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# PASO 3: Capturar el nuevo mensaje del usuario
# La caja de texto queda en la parte inferior. Si el usuario escribe algo y da Enter, entra al 'if'.
if prompt := st.chat_input("Escribe tu consulta aquí..."):
    
    # A) Guardar el mensaje en memoria y mostrarlo en la interfaz
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # PASO 4: Generar la respuesta del Asistente
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            time.sleep(1.5)  # Simulamos el tiempo de latencia/procesamiento de una IA real
            
            # Lógica creíble pero sin API (Mock AI basado en palabras clave)
            prompt_lower = prompt.lower()
            if "reembolso" in prompt_lower:
                respuesta = "Entiendo que buscas un reembolso. Por favor, indícame tu número de orden de 6 dígitos."
            elif "contraseña" in prompt_lower:
                respuesta = "Para recuperar tu contraseña, haz clic en 'Olvidé mi clave' en el menú principal."
            else:
                respuesta = f"He recibido tu consulta: '{prompt}'. Un operador se pondrá en contacto pronto."
            
            # Mostrar la respuesta en la interfaz
            st.markdown(respuesta)
            
    # B) Guardar la respuesta del asistente en la memoria
    st.session_state.messages.append({"role": "assistant", "content": respuesta})

# --- Pasos para ejecutar esta aplicación ---
# 1. Abre una terminal (o línea de comandos).
# 2. Instala la biblioteca de Streamlit:
#    uv add streamlit
# 3. Ejecuta la aplicación con el comando:
#    streamlit run main.py