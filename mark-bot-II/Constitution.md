# Project Specification: AI personalized chatbot

## 1. Constitution

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

## 2. Roadmap (Implementation Phases) - COMPLETED

### Phase 1: Basic Setup, Documentation Reading & CLI Test
- Initialize the Python environment using `uv`. ( complete by the human )
- Install `streamlit` and `google-genai`. ( complete by the human )
- **CRITICAL STEP:** Read the local `gemini-interactions-docs.md` file to learn the new Interactions API syntax.
- Create a basic terminal script (`main.py`) that takes a hardcoded Gemini API key and successfully prints a response from the model in the console using `interactions.create`.
- *Goal: Verify the modern API connection works perfectly following the new documentation before touching the UI.*

### Phase 2: Basic Streamlit Chat UI - COMPLETED
- modified `main.py` and set up a basic streamlit application.
- Build a chat interface with a message history container (ListView or Column), a TextField for the user to type messages, and a "Send" button.
- make a comment seccion at the last of main.py for indicate to the user how to run the streamlit project.
- *Goal: Have a visual chat layout, but without AI connection yet.*

### Phase 3: BYOK (Bring Your Own Key) Integration - COMPLETED
- Add a startup screen or a settings field in the streamlit UI where the user must input their Gemini API Key.
- Store this key in Streamlit session state or equal. Hide the input field (password mode) for security.
- *Goal: The app must not use hardcoded `.env` files for the final user.*

### Phase 4: Connect UI to Gemini API (MVP Completion) - COMPLETED
- Connect the Streamlit "Send" button to the Gemini API using the session's API key.
- Display the user's message in the chat UI.
- Fetch the response from Gemini and display the AI's message in the chat UI.
- Implement a basic `while` loop or session state array to keep the conversation history so the AI remembers the context of the chat.

---

## 1. Constitution 2.0
**Mission:** Upgrade the existing Vanilla Assistant into a specialized, stateful AI web application with dynamic role-playing and explicit memory management.

## 4. Roadmap 2.0 (New implementation Phases)

### Phase 5: Role-playing & State Wiping
- **Task 1: Add Role Input.** In the `st.sidebar`, add a text input or text area for the user to define the Assistant's Role (e.g., "You are an expert Python engineer...").
- **Task 2: Inject System Prompt.** Update the Gemini Client initialization logic. Pass the user-defined role into the `config` parameter as `system_instruction` when calling `gemini_client.interactions.create`.
- **Task 3: Add Clear Chat Button.** Create a "Clear Chat" button in the sidebar or main UI.
- **Task 4: Implement State Wiping.** When the clear button is clicked, reset `st.session_state.messages = []` and explicitly set `st.session_state.previous_interaction_id = None`. Rerun the app (`st.rerun()`) to refresh the UI.
- **Strict Rule:** Do not add any guardrails, eval, or observability code yet. Modify only the existing `app.py`.

### Phase 6: Build and Deploy Test 
- The human developer will test the executable to ensure it opens, accepts the key, and chats successfully without needing a terminal.