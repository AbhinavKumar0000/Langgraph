import streamlit as st
import time
import uuid
from langchain_core.messages import HumanMessage
from backend import chatbot, retrieve_all_threads, generate_title, flush_user_history

# **************************************** Page Config *************************

st.set_page_config(
    page_title="AI Workspace",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded" 
)

# **************************************** GEMINI / LOVABLE CSS *************************

st.markdown("""
<style>
    /* 1. ANIMATED BACKGROUND */
    .stApp {
        background: linear-gradient(-45deg, #0d0d0d, #1a1a2e, #16213e, #0f3460);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        color: #e0e0e0;
    }
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* 2. SIDEBAR STYLING */
    [data-testid="stSidebar"] {
        background-color: #131314;
        border-right: 1px solid #2d2d2d;
    }

    /* Restore Hamburger, Hide Footer */
    header[data-testid="stHeader"] { background-color: transparent; }
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}

    /* 3. BUTTONS (List Style) */
    div.stButton > button {
        width: 100%;
        border: none;
        background: transparent;
        text-align: left;
        color: #9aa0a6;
        font-size: 14px;
        padding: 8px 12px;
        margin: 0;
        border-radius: 20px;
        transition: background-color 0.1s ease;
    }
    div.stButton > button:hover {
        background-color: #303134;
        color: #e8eaed;
    }
    div.stButton > button:focus {
        background-color: #303134;
        color: #e8eaed;
        border: none;
        outline: none;
    }

    /* 4. NEW CHAT BUTTON */
    [data-testid="stSidebar"] div.stButton:first-of-type {
        padding-bottom: 20px;
    }
    [data-testid="stSidebar"] div.stButton:first-of-type > button {
        background-color: #1b1b1b;
        color: #e8eaed;
        border: 1px solid #3c4043;
        border-radius: 20px;
        text-align: left;
        padding-left: 15px;
        font-weight: 500;
        display: flex;
        align-items: center;
    }
    [data-testid="stSidebar"] div.stButton:first-of-type > button:hover {
        background-color: #303134;
        box-shadow: 0 1px 3px rgba(0,0,0,0.3);
    }

    /* 5. TYPOGRAPHY */
    .sidebar-header {
        color: #9aa0a6;
        font-size: 12px;
        font-weight: 600;
        margin-top: 10px;
        margin-bottom: 5px;
        padding-left: 10px;
    }

    /* 6. CHAT INPUT FIX (Transparent Bottom) */
    div[data-testid="stBottom"] {
        background-color: transparent;
        border-top: none;
    }
    .stChatInput textarea {
        background-color: rgba(30, 30, 30, 0.8) !important;
        border: 1px solid #444;
        color: white;
    }

    /* 7. AVATARS */
    [data-testid="chatAvatarIcon-user"] { background-color: transparent !important; }
    [data-testid="chatAvatarIcon-assistant"] { background-color: #4b6cb7 !important; }
</style>
""", unsafe_allow_html=True)

# **************************************** Session & User Setup *************************

# 1. User ID (Persists as long as tab is open)
if 'user_id' not in st.session_state:
    st.session_state['user_id'] = str(uuid.uuid4())

# 2. Helper Utils
def generate_thread_id():
    return str(uuid.uuid4())

def reset_chat():
    st.session_state['thread_id'] = generate_thread_id()
    st.session_state['message_history'] = []

def load_conversation(thread_id):
    state = chatbot.get_state(config={'configurable': {'thread_id': thread_id}})
    return state.values.get('messages', [])

# 3. Initialize State
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_threads' not in st.session_state:
    # Load threads specific to THIS user
    st.session_state['chat_threads'] = retrieve_all_threads(st.session_state['user_id']) or []

# **************************************** Sidebar UI *********************************

with st.sidebar:
    # New Chat
    if st.button("➕  New chat", use_container_width=True):
        reset_chat()
        st.rerun()

    st.markdown('<div class="sidebar-header">Recent</div>', unsafe_allow_html=True)
    
    # History List
    for thread in st.session_state['chat_threads'][::-1]:
        clean_title = thread['title']
        if len(clean_title) > 25:
            clean_title = clean_title[:25] + "..."
            
        if st.button(clean_title, key=thread['id'], use_container_width=True):
            st.session_state['thread_id'] = thread['id']
            
            messages = load_conversation(thread['id'])
            temp_messages = []
            for msg in messages:
                role = 'user' if isinstance(msg, HumanMessage) else 'assistant'
                temp_messages.append({'role': role, 'content': msg.content})

            st.session_state['message_history'] = temp_messages
            st.rerun()

    st.markdown("---")
    if st.button("🗑️  Clear History", use_container_width=True):
        flush_user_history(st.session_state['user_id'])
        st.session_state['chat_threads'] = []
        st.session_state['message_history'] = []
        st.rerun()

# **************************************** Main Chat UI ******************************

# Welcome Screen
if not st.session_state['message_history']:
    st.markdown("""
        <div style='display: flex; flex-direction: column; align-items: center; justify-content: center; height: 70vh;'>
            <h1 style='
                background: linear-gradient(to right, #4facfe 0%, #00f2fe 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                font-size: 3rem;
                font-weight: 700;
            '>Hello, Human.</h1>
            <p style='color: #9aa0a6; font-size: 1.2rem; margin-top: 10px;'>How can I help you today?</p>
        </div>
    """, unsafe_allow_html=True)

# Messages
for message in st.session_state['message_history']:
    role = message['role']
    avatar = "✨" if role == 'assistant' else None 
    with st.chat_message(role, avatar=avatar):
        st.write(message['content'])

# Input
user_input = st.chat_input('Message chatbot...')

if user_input:
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.write(user_input)

    CONFIG = {
        "configurable": {"thread_id": st.session_state["thread_id"]},
        "metadata": {"thread_id": st.session_state["thread_id"]},
    }

    # Generate Title (First Message)
    if len(st.session_state['message_history']) == 1:
        generate_title(st.session_state['thread_id'], user_input, st.session_state['user_id'])
        st.session_state['chat_threads'] = retrieve_all_threads(st.session_state['user_id'])

    # Stream Response
    with st.chat_message('assistant', avatar="✨"):
        ai_message = st.write_stream(
            (time.sleep(0.02) or message_chunk.content) for message_chunk, metadata in chatbot.stream(
                {'messages': [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode='messages'
            )
        )

    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})