import streamlit as st
import base64
import google.genai as genai

# --- Page Config ---
st.set_page_config(
        page_title="MARK BOT V",
        page_icon="🤖",
        layout="centered",
        initial_sidebar_state="expanded",
    )

st.title("🤖 MARK-BOT V",text_alignment="center")

# --- Gemini API Key Input ---
st.sidebar.header("Configuration")
api_key_from_input = st.sidebar.text_input(
    "Enter your Gemini API Key", 
    type="password",
    help="Get your key from Google AI Studio."
)

# Add a button to apply the key. This is more user-friendly than "press enter".
if st.sidebar.button("Apply Key"):
    if api_key_from_input:
        st.session_state.gemini_api_key = api_key_from_input
        st.rerun() # Rerun the app to show the chat interface immediately

# --- Chat Interface ---
# Only show the chat interface if the API key has been provided.
if "gemini_api_key" in st.session_state and st.session_state.gemini_api_key:
    # Initialize the Gemini Client. We store it in the session state to avoid
    # re-creating it on every interaction.
    if "gemini_client" not in st.session_state:
        try:
            st.session_state.gemini_client = genai.Client(
                api_key=st.session_state.gemini_api_key
            )
        except Exception as e:
            st.error(f"Failed to initialize Gemini client: {e}")
            st.stop()

    # --- Vision UI Components ---
    st.sidebar.header("Vision")
    uploaded_image = st.sidebar.file_uploader(
        "🖼️ Upload an image",
        type=["png", "jpg", "jpeg"],
        help="Upload an image to ask questions about its content."
    )
    camera_image = st.sidebar.camera_input(
        "📸 Take a picture",
        help="Use your device's camera to take a picture."
    )

    # --- Role and State Management ---
    st.sidebar.header("Chat Controls")
    # Button to clear chat history and state
    if st.sidebar.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        if "previous_interaction_id" in st.session_state:
            del st.session_state.previous_interaction_id
        st.rerun()


    # Initialize the chat history in Streamlit's session state if it doesn't exist
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages from the session state
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field for the user to enter their message
    if prompt := st.chat_input("What is up?"):
        # Add and display the user's message
        with st.chat_message("user"):
            # Display the image first if it exists
            if uploaded_image:
                st.image(uploaded_image)
            if camera_image:
                st.image(camera_image)
            st.markdown(prompt)

        # Store the user's message in the history
        # We'll reconstruct the full display message later if needed,
        # but for the API, we only need the text part.
        st.session_state.messages.append({"role": "user", "content": prompt})

        # --- Prepare the multimodal payload for the API ---
        # The input can be a simple string or a list of parts.
        api_input = [
            {"type": "text", "text": prompt}
        ]
        image_source = uploaded_image or camera_image
        if image_source:
            # Read the raw bytes and encode to base64
            image_bytes = image_source.getvalue()
            image_b64 = base64.b64encode(image_bytes).decode("utf-8")
            api_input.append(
                {
                    "type": "image",
                    "data": image_b64,
                    "mime_type": image_source.type
                }
            )

        # --- Fetch and display AI response ---
        with st.chat_message("assistant"):
            with st.spinner("The AI is thinking..."):
                try:
                    # Check for previous interaction to maintain conversation context
                    previous_id = st.session_state.get("previous_interaction_id", None)

                    # Call the Gemini API with the potentially multimodal input
                    interaction = st.session_state.gemini_client.interactions.create(
                        model="gemini-3.5-flash", # Or any other supported model
                        # Generic, helpful AI assistant role
                        system_instruction="You are a helpful and friendly AI assistant.",
                        input=api_input, # Pass the list of parts
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
                    st.error(f"An error occurred with the Gemini API: {e}")
else:
    st.info("Please enter your Gemini API key in the sidebar to unlock the application.")