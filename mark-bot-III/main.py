import streamlit as st
import google.genai as genai
from rag_engine import retrieve_and_augment
from models import AVAILABLE_GEMINI_MODELS
import os


SCRIPT_DIR = os.path.dirname(__file__)
ICON_PATH = os.path.abspath(os.path.join(SCRIPT_DIR, "assets", "exa.png"))

if os.path.exists(ICON_PATH):
    page_icon_setting = ICON_PATH
else:
    page_icon_setting = "🤖"

st.set_page_config(
        page_title="TUDAI CHATBOT",
        page_icon=page_icon_setting,
        layout="centered",
        initial_sidebar_state="expanded",
    )

st.title("TUDAI CHATBOT", text_alignment="center")
    
st.warning(
    "⚠️ **Aviso Legal:** Este chatbot es un proyecto académico y personal creado para un portfolio estudiantil."
    " **No es un canal oficial** ni tiene afiliación directa con la carrera TUDAI, la Facultad de Ciencias Exactas o la UNICEN. "
    "Las respuestas son generadas por Inteligencia Artificial utilizando una arquitectura RAG (Retrieval-Augmented Generation) "
    "que busca y recupera datos que extraye manualmente de la página oficial de la facultad. Aunque el sistema está diseñado para ser preciso, "
    "te recomiendo verificar siempre la información crítica a través de los canales de contacto oficiales."
)


st.sidebar.header("Configuración")
api_key_from_input = st.sidebar.text_input(
    "Ingresa tu clave API de Gemini", 
    type="password",
    help="Obtén tu clave desde Google AI Studio."
)

if st.sidebar.button("Aplicar Clave", key="apply_key_button"):
    if api_key_from_input:
        st.session_state.gemini_api_key = api_key_from_input
        st.rerun() 


def is_prompt_injection(user_input: str) -> bool:
    """Input Guardrail: Busca firmas clásicas de ataques adversarios."""
    blacklist = [
        "ignora",
        "ignore",
        "instrucciones",
        "instructions",
        "nuevo rol",
        "new role",
        "system prompt",
        "olvida",
        "###"
    ]
    input_lower = user_input.lower()
    return any(phrase in input_lower for phrase in blacklist)

# Only show the chat interface if the API key has been provided.
if "gemini_api_key" in st.session_state and st.session_state.gemini_api_key:
    # Initialize the chat history in Streamlit's session state if it doesn't exist
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Initialize the Gemini Client. We store it in the session state to avoid
    # re-creating it on every interaction.
    if "gemini_client" not in st.session_state:
        try:
            st.session_state.gemini_client = genai.Client(
                api_key=st.session_state.gemini_api_key
            )
        except Exception as e:
            st.error(f"Failed to initialize Gemini client: {e}")
            st.error(f"Error al inicializar el cliente de Gemini: {e}")
            st.stop()

    st.sidebar.header("Controles del Chat")
    
    selected_model = st.sidebar.selectbox(
        "Selecciona el modelo de Gemini",
        options=AVAILABLE_GEMINI_MODELS,
        index=0
    )

    if st.sidebar.button("🗑️ Limpiar Chat", key="clear_chat_button"):
        st.session_state.messages = []
        if "previous_interaction_id" in st.session_state:
            del st.session_state.previous_interaction_id
        st.rerun()


    # Display the existing chat messages from the session state
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field for the user to enter their message
    if prompt := st.chat_input("Escribe tu pregunta aquí..."):
        # 1. Input Guardrail: Bloqueador de Inyecciones
        if is_prompt_injection(prompt):
            with st.chat_message("assistant"):
                st.error("⚠️ Bloqueo de Seguridad: Se ha detectado un intento de manipular las instrucciones del sistema.")
        else:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # --- Fetch and display AI response ---
            with st.chat_message("assistant", avatar=page_icon_setting):
                with st.spinner("La IA está pensando..."):
                    try:
                        # Check for previous interaction to maintain conversation context
                        previous_id = st.session_state.get("previous_interaction_id", None)

                        augmented_prompt = retrieve_and_augment(prompt)

                        interaction = st.session_state.gemini_client.interactions.create(
                            model=selected_model,
                            input=augmented_prompt,
                            previous_interaction_id=previous_id
                        )

                        # Extract the response text and display it
                        response_text = interaction.output_text
                        st.markdown(response_text)

                        # Store the new interaction ID for the next turn
                        st.session_state.previous_interaction_id = interaction.id
                        # Add the AI's response to the message history
                        st.session_state.messages.append({"role": "assistant", "content": response_text})
                    except Exception as e:
                        st.error(f"Ocurrió un error con la API de Gemini: {e}")
else:
    st.info("Por favor, ingresa tu :yellow[clave API de Gemini] en la barra lateral para comenzar a chatear.")