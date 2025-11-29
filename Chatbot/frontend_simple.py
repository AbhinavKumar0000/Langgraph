import streamlit as st
import time
import uuid
from langchain_core.messages import HumanMessage
# Make sure to import generate_title from your backend
from backend import chatbot, retrieve_all_threads, generate_title

# **************************************** Utility Functions *************************

def generate_thread_id():
    return str(uuid.uuid4())

def reset_chat():
    st.session_state['thread_id'] = generate_thread_id()
    st.session_state['message_history'] = []

def load_conversation(thread_id):
    # Fetch state for the specific thread
    state = chatbot.get_state(config={'configurable': {'thread_id': thread_id}})
    return state.values.get('messages', [])

# **************************************** Session Setup ******************************

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

# Load threads (now expects a list of dicts: [{'id':..., 'title':...}])
if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = retrieve_all_threads() or []

# **************************************** Sidebar UI *********************************

st.sidebar.title('LangGraph Chatbot')

if st.sidebar.button('New Chat'):
    reset_chat()
    st.rerun()

st.sidebar.header('My Conversations')

# Loop through threads (reversed to show newest on top)
# We use thread['id'] as the unique key for the button
for thread in st.session_state['chat_threads'][::-1]:
    if st.sidebar.button(thread['title'], key=thread['id']):
        st.session_state['thread_id'] = thread['id']
        
        # Load messages and format them for Streamlit
        messages = load_conversation(thread['id'])
        temp_messages = []
        for msg in messages:
            role = 'user' if isinstance(msg, HumanMessage) else 'assistant'
            temp_messages.append({'role': role, 'content': msg.content})

        st.session_state['message_history'] = temp_messages
        st.rerun()

# **************************************** Main UI ************************************

# Display conversation history
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

user_input = st.chat_input('Type here')

if user_input:
    # 1. Add user message to UI
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)

    # 2. Config for the specific thread
    CONFIG = {
        "configurable": {"thread_id": st.session_state["thread_id"]},
        "metadata": {"thread_id": st.session_state["thread_id"]},
        "run_name": "chat_turn",
    }

    # 3. TITLE GENERATION LOGIC
    # If this is the first message in the history, generate a title
    if len(st.session_state['message_history']) == 1:
        # Generate title in DB
        generate_title(st.session_state['thread_id'], user_input)
        # Refresh sidebar list to show the new title immediately
        st.session_state['chat_threads'] = retrieve_all_threads()

    # 4. Generate Response with Stream Delay
    with st.chat_message('assistant'):
        ai_message = st.write_stream(
            (time.sleep(0.05) or message_chunk.content) for message_chunk, metadata in chatbot.stream(
                {'messages': [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode='messages'
            )
        )

    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})