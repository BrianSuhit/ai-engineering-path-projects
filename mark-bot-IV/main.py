import streamlit as st
import google.genai as genai
from rag_engine import retrieve_and_augment
import chromadb

# --- Page Config ---
st.set_page_config(
        page_title="MARK BOT IV",
        page_icon="🤖",
        layout="centered",
        initial_sidebar_state="expanded",
    )

st.title("🤖 MARK-BOT IV",text_alignment="center")

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

    # --- File Uploader ---
    st.sidebar.header("📁 Upload Your Data")
    uploaded_file = st.sidebar.file_uploader(
        "Upload a file to chat with",
        type=["md", "txt"],
        help="Upload a Markdown or text file to ask questions about its content."
    )

    # --- Dynamic Ingestion and Ephemeral DB ---
    if uploaded_file:
        # This block runs only if the uploaded file is different from the one already processed.
        if st.session_state.get("processed_file") != uploaded_file.name:
            with st.spinner("Processing your document... This may take a moment."):
                # Initialize an in-memory ChromaDB client. It's ephemeral for the session.
                chroma_client = chromadb.Client()

                # Cleanup step: Delete the old collection if a new file is uploaded
                try:
                    chroma_client.delete_collection(name="user_data")
                except Exception:
                    pass # Collection might not exist on the first run

                # Create a new collection for the new file's data
                collection = chroma_client.create_collection(name="user_data")

                # Read, chunk, and ingest the new file
                file_contents = uploaded_file.getvalue().decode("utf-8")
                chunks = file_contents.split("\n\n")
                collection.add(
                    documents=chunks,
                    ids=[f"chunk_{i}" for i in range(len(chunks))]
                )

                # Store the new collection in the session state
                st.session_state.chroma_collection = collection
                
                # Seal the state by recording the name of the processed file
                st.session_state.processed_file = uploaded_file.name
                st.success("✅ Document processed! You can now ask questions about it.")

    # --- Role and State Management ---
    st.sidebar.header("Chat Controls")
    # Button to clear chat history and state
    if st.sidebar.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        if "previous_interaction_id" in st.session_state:
            del st.session_state.previous_interaction_id
        if "chroma_collection" in st.session_state:
            del st.session_state.chroma_collection # Also clear the DB on chat clear
        if "processed_file" in st.session_state:
            del st.session_state.processed_file # Clear the processed file tracker
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
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # --- Fetch and display AI response ---
        with st.chat_message("assistant"):
            with st.spinner("The AI is thinking..."):
                try:
                    # Check for previous interaction to maintain conversation context
                    previous_id = st.session_state.get("previous_interaction_id", None)

                    # If a document has been uploaded, use the RAG engine. Otherwise, use the raw prompt.
                    if "chroma_collection" in st.session_state:
                        augmented_prompt = retrieve_and_augment(prompt, st.session_state.chroma_collection)
                    else:
                        # Add a message to guide the user if they ask a question without uploading a file
                        st.info("Upload a document in the sidebar to ask questions about it.")
                        augmented_prompt = prompt

                    # Call the Gemini API, now including the system instruction
                    interaction = st.session_state.gemini_client.interactions.create(
                        model="gemini-3.5-flash", # Or any other supported model
                        # Updated, more generic system instruction
                        system_instruction="You are a helpful and friendly assistant. You must only answer based on the relevant information provided in the prompt.",
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
                    st.error(f"An error occurred with the Gemini API: {e}")
else:
    st.info("Please enter your Gemini API key in the sidebar to unlock the application.")