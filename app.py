import asyncio
import traceback
import uuid  # 1. Import UUID for random IDs
import gradio as gr

# from agent import ... (Keep your original imports)
from agent import AGENTS, make_runner_for, session_service, APP_NAME, USER_ID
from google.genai.types import Content, Part

DEFAULT_AGENT_KEY = "triage"

# 2. Helper to Initialize a Session for a specific ID
async def ensure_unique_session(session_id, agent_key=DEFAULT_AGENT_KEY):
    runner = make_runner_for(AGENTS[agent_key])
    # We don't create a new loop here; we use the existing running loop in the async handler
    try:
        await runner.session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=session_id
        )
    except Exception as e:
        # Session might already exist if the user sends a 2nd message, which is fine
        print(f"Session info (or error): {e}")

# 3. Async Response Handler accepting dynamic session_id
async def _agent_response_async(message: str, session_id: str, agent_key: str):
    # Ensure session exists for this specific random ID
    await ensure_unique_session(session_id, agent_key)
    
    runner = make_runner_for(AGENTS[agent_key])
    user_input = Content(parts=[Part(text=message)], role="user")
    final = "(no response)"
    
    try:
        # Pass the dynamic session_id here
        async for evt in runner.run_async(user_id=USER_ID, session_id=session_id, new_message=user_input):
            if evt.is_final_response() and evt.content and evt.content.parts:
                final = evt.content.parts[0].text
    except Exception as e:
        final = f"[Agent error] {e}\n{traceback.format_exc()}"
    return final

# 4. Chat function accepts session_id from State
def chat_fn(message, history, session_id):
    # asyncio.run() allows us to run the async function from this sync wrapper
    return asyncio.run(_agent_response_async(message, session_id, DEFAULT_AGENT_KEY))

# 5. Function to generate a new ID
def get_new_session_id():
    return str(uuid.uuid4())

def main():
    with gr.Blocks() as demo:
        gr.Markdown("## 🩺 MediFlow — Ask Your Question")
        
        # 6. Create a State component to hold the unique ID
        # calling get_new_session_id ensures a new ID per tab load/refresh
        session_state = gr.State(get_new_session_id)

        gr.ChatInterface(
            fn=chat_fn, 
            title="MediFlow Agent Chat",
            # 7. Pass the state as an additional input to the chat function
            additional_inputs=[session_state] 
        )
        
    demo.launch()

if __name__ == "__main__":
    main()
