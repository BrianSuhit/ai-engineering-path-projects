# Project Specification: AI personalized chatbot

## Constitution

**Mission:** 
Build a simple, AI chatbot to understand the foundational workflow of Flet and LLM API integration. 
construir un ai chatbot simple y deployable en streamlit para aplicar fundamentos de ia aprendidos en un proyecto desplegable.

**Target Audience:** 
Personal learning and foundational portfolio.

**MVP Scope:** 
una interfaz basica en streamlit y flujo de chat donde el usuario ingresa su clave api, escribe su mensaje, lo envia a la api de gemini y ve la respuesta de la ia.


**Tech Stack:**
- **Language:** Pure Python.
- **Frontend/UI:** `streamlit`.
- **Environment:** `uv` for dependency management.
- **Model Provider:** Gemini API.
- **STRICT API RULE:** The project MUST use the modern Interactions API via the `google-genai` package (version >= 2.3.0). DO NOT use the legacy `google.generativeai` package or `generateContent` methods.
- **Documentation Anchor:** The agent MUST read the `gemini-interactions-docs.md` file located in the root directory to understand the exact syntax (`interactions.create`, `previous_interaction_id`, etc.) before implementing any API calls.

---

## Roadmap (Implementation Phases) - ✅ COMPLETED

### Phase 1: Basic Setup, Documentation Reading & CLI Test
- Initialize the Python environment using `uv`. ( complete by the human )
- Install `streamlit` and `google-genai`. ( complete by the human )
- **CRITICAL STEP:** Read the local `gemini-interactions-docs.md` file to learn the new Interactions API syntax.
- Create a basic terminal script (`main.py`) that takes a hardcoded Gemini API key and successfully prints a response from the model in the console using `interactions.create`.
- *Goal: Verify the modern API connection works perfectly following the new documentation before touching the UI.*

### Phase 2: Basic Streamlit Chat UI - ✅ COMPLETED
- modified `main.py` and set up a basic streamlit application.
- Build a chat interface with a message history container (ListView or Column), a TextField for the user to type messages, and a "Send" button.
- *Goal: Have a visual chat layout, but without AI connection yet.*

### Phase 3: BYOK (Bring Your Own Key) Integration - ✅ COMPLETED
- Add a startup screen or a settings field in the streamlit UI where the user must input their Gemini API Key.
- Store this key in Streamlit session state or equal. Hide the input field (password mode) for security.
- *Goal: The app must not use hardcoded `.env` files for the final user.*

### Phase 4: Connect UI to Gemini API (MVP Completion) - ✅ COMPLETED
- Connect the Streamlit "Send" button to the Gemini API using the session's API key.
- Display the user's message in the chat UI.
- Fetch the response from Gemini and display the AI's message in the chat UI.
- Implement a basic `while` loop or session state array to keep the conversation history so the AI remembers the context of the chat.

---

## Constitution 2.0
**Mission:** Upgrade the existing Vanilla Assistant into a specialized, stateful AI web application with dynamic role-playing and explicit memory management.

## Roadmap 2.0 (New implementation Phases) - ✅ COMPLETED

### Phase 5: Role-playing & State Wiping - ✅ COMPLETED
- **Task 1: Add Role Input.** In the `st.sidebar`, add a text input or text area for the user to define the Assistant's Role (e.g., "You are an expert Python engineer...").
- **Task 2: Inject System Prompt.** Update the Gemini Client initialization logic. Pass the user-defined role into the `config` parameter as `system_instruction` when calling `gemini_client.interactions.create`.
- **Task 3: Add Clear Chat Button.** Create a "Clear Chat" button in the sidebar or main UI.
- **Task 4: Implement State Wiping.** When the clear button is clicked, reset `st.session_state.messages = []` and explicitly set `st.session_state.previous_interaction_id = None`. Rerun the app (`st.rerun()`) to refresh the UI.
- **Strict Rule:** Do not add any guardrails, eval, or observability code yet. Modify only the existing `app.py`.


---

## Constitution 3.0 
**Mission:** Upgrade the existing Vanilla Assistant into a Static RAG Assistant (The TUDAI Librarian) that strictly answers questions based on a local vector database, eliminating hallucinations.

## Roadmap 3.0 (New Implementation Phases) - ✅ COMPLETED

### Phase 6: Implement Static RAG System - ✅ COMPLETED
- **Task 1: Remove Dynamic Role Input.** Remove the `st.text_area` and the "Apply" button from the sidebar that allowed users to insert a custom role. 
- **Task 2: Inject Static System Prompt.** Hardcode the `system_instruction` in the Gemini Client initialization to be: "You are a TUDAI assistant for new students who are aspiring to enter the university. You must only answer based on the relevant information provided in the prompt."
- **Task 3: Integrate RAG Engine.** Import the `rag_engine` script into `app.py`. When the user submits a prompt, pass it through `rag_engine.retrieve_and_augment(prompt)` to generate the context-enriched prompt. Send this augmented prompt to the Gemini API, while displaying only the original short prompt to the user in the UI.
- **Strict Rule:** Do not add any guardrails, eval, or observability code yet. Modify only the existing `app.py` to connect it with `rag_engine.py`.

---

## 1. Constitution 4.0
**Mission:** Upgrade the Static RAG system into a Dynamic RAG Assistant (Bring Your Own Data). The user will be able to upload their own files via the UI, and the model will parse, embed, and answer questions based strictly on the uploaded context on the fly.

## 4. Roadmap 4.0 (New Implementation Phases) - ✅ COMPLETED

### Phase 7: Implement Dynamic RAG (File Upload) - ✅ COMPLETED
- **Task 1: Add File Uploader UI.** Implement `st.file_uploader` in the Streamlit sidebar allowing the user to upload a Markdown or text file, add an folder icon too.
- **Task 2: Dynamic Ingestion Pipeline.** When a file is uploaded, read its content, apply a basic text splitting (chunking) strategy to keep tokens manageable, and generate embeddings.
- **Task 3: Ephemeral Vector Database.** Save the generated chunks into a temporary, in-memory ChromaDB collection (do not persist to disk) so the user's data is private to the session.
- **Task 4: Update the RAG Engine.** Modify the existing retrieve and augment logic to point to this new dynamic collection instead of the static TUDAI database.
- **Task 5: Improve Static System Prompt.** Improve the system intruction to be: "You are a helpful and friendly assistant. You must only answer based on the relevant information provided in the prompt."
- **Strict Rule:** Maintain the existing `previous_interaction_id` logic to keep the chat memory intact. 


---

## 1. Constitution 5.0
**Mission:** Strip out the RAG architecture and upgrade the system into an Omnisensorial Assistant (Multimodal AI - Vision First) leveraging Gemini's Interactions API native inline image data support.

## 5. Roadmap 5.0 (New Implementation Phases) - ✅ COMPLETED

### Phase 8: Implement Native Vision (Image Processing) - ✅ COMPLETED
- **Task 1: Architecture Cleanup.** Remove all ChromaDB dependencies, `rag_engine` imports, and ephemeral vector database logic from `main.py`. Update the `system_instruction` in the API call to a generic, helpful AI assistant role.
- **Task 2: Vision UI Components.** Inside the existing Authentication Gate, replace the text file uploader with an image-focused `st.file_uploader` (restricted to png, jpg, jpeg) and add a `st.camera_input` component. 
- **Task 3: Inline Image Data Payload (Base64).** When the user submits a text prompt, check if an image is provided. Do NOT use the `PIL` library. Instead, read the raw bytes from Streamlit's uploaded file, encode them to a Base64 string using Python's native `base64` library, and pass it to the Interactions API as inline image data alongside the text prompt.
- **Strict Rule:** Maintain the existing `previous_interaction_id` state management so the bot remembers the conversation context across multiple turns.