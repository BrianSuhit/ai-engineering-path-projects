import streamlit as st
import google.genai as genai

# Set the title for the Streamlit app
st.title("🤖 MARK-BOT II")

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

# --- Role and State Management ---
st.sidebar.header("Chat Controls")
# Input for the assistant's role/persona
st.session_state.assistant_role = st.sidebar.text_area(
    "Assistant's Role",
    value="You are a helpful and friendly assistant.",
    help="Define the personality and instructions for the assistant."
)

# Button to clear chat history and state
if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    if "previous_interaction_id" in st.session_state:
        del st.session_state.previous_interaction_id
    st.rerun()


# Initialize the chat history in Streamlit's session state if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

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

    # Display the existing chat messages from the session state
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field for the user to enter their message
    if prompt := st.chat_input("What is up?"):
        # Add and display the user's message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # --- Fetch and display AI response ---
        with st.chat_message("assistant"):
            with st.spinner("The AI is thinking..."):
                try:
                    # Check for previous interaction to maintain conversation context
                    previous_id = st.session_state.get("previous_interaction_id", None)

                    # Call the Gemini API, now including the system instruction
                    interaction = st.session_state.gemini_client.interactions.create(
                        model="gemini-3.5-flash", # Or any other supported model
                        # Inject the role from the sidebar as a system instruction
                        system_instruction=st.session_state.assistant_role,
                        input=prompt,
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
    st.info("Please enter your Gemini API key in the sidebar to start chatting.")