import streamlit as st
import time
import uuid
from langchain_core.messages import HumanMessage
from backend import chatbot, retrieve_all_threads, generate_title, flush_user_history

# **************************************** Page Config *************************

st.set_page_config(
    page_title="AI Workspace",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded" 
)

# **************************************** B&W STYLING *************************

st.markdown("""
<style>
    /* 1. HIGH VISIBILITY B&W GRADIENT */
    .stApp {
        /* Moving between Black, Dark Grey, and Silver */
        background: linear-gradient(-45deg, #000000, #2c2c2c, #1a1a1a, #ffffff);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        color: #e0e0e0;
    }
    
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* 2. SIDEBAR (Pure Black) */
    [data-testid="stSidebar"] {
        background-color: #000000;
        border-right: 1px solid #333;
    }
    header[data-testid="stHeader"] { background: transparent; }
    footer { visibility: hidden; }
    #MainMenu { visibility: hidden; }

    /* 3. BOTTOM CONTAINER (Pure Black to match Sidebar) */
    div[data-testid="stBottom"] {
        background-color: #000000 !important;
        border-top: 1px solid #333;
        padding-bottom: 20px !important;
        padding-top: 20px !important;
    }

    /* 4. CHAT INPUT (Monochrome Fix) */
    .stChatInput {
        border: none !important;
        padding: 0 !important;
    }
    
    div[data-testid="stChatInput"] > div {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }

    .stChatInput textarea {
        background-color: #111111 !important;  /* Very Dark Grey */
        color: #ffffff !important;             /* Pure White Text */
        border: 1px solid #555 !important;     /* Grey Border */
        border-radius: 30px !important;
        
        /* Padding Fix */
        padding-left: 20px !important; 
        padding-right: 20px !important;
        padding-top: 10px !important;
        padding-bottom: 10px !important;
    }
    
    /* Focus State (White Glow) */
    .stChatInput textarea:focus {
        border-color: #ffffff !important;
        box-shadow: 0 0 10px rgba(255, 255, 255, 0.2) !important;
    }
    
    /* Send Button (White) */
    .stChatInput button {
        background: transparent !important;
        border: none !important;
        color: #ffffff !important;
    }
    
    /* 5. SIDEBAR BUTTONS */
    div.stButton > button {
        width: 100%;
        border: none;
        background: transparent;
        text-align: left;
        color: #888;
        padding: 8px 12px;
        border-radius: 4px;
    }
    div.stButton > button:hover {
        background-color: #222;
        color: white;
    }
    
    /* New Chat Button (White/Grey) */
    [data-testid="stSidebar"] div.stButton:first-of-type > button {
        background-color: #111;
        color: white;
        border: 1px solid #555;
        border-radius: 8px;
        padding-left: 15px;
        margin-bottom: 20px;
    }

    /* 6. AVATARS (Monochrome) */
    [data-testid="chatAvatarIcon-user"] { background-color: transparent !important; }
    [data-testid="chatAvatarIcon-assistant"] { 
        background-color: #ffffff !important; /* White Avatar */
        color: #000000 !important;
    }
</style>
""", unsafe_allow_html=True)

# **************************************** LOGIC *************************

if 'user_id' not in st.session_state:
    st.session_state['user_id'] = str(uuid.uuid4())

def generate_thread_id():
    return str(uuid.uuid4())

def reset_chat():
    st.session_state['thread_id'] = generate_thread_id()
    st.session_state['message_history'] = []

def load_conversation(thread_id):
    state = chatbot.get_state(config={'configurable': {'thread_id': thread_id}})
    return state.values.get('messages', [])

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = retrieve_all_threads(st.session_state['user_id']) or []

# **************************************** UI *************************

with st.sidebar:
    if st.button("New chat", use_container_width=True):
        reset_chat()
        st.rerun()

    st.markdown('<p style="color:#555; font-size:12px; font-weight:bold; margin-top:20px;">HISTORY</p>', unsafe_allow_html=True)
    
    for thread in st.session_state['chat_threads'][::-1]:
        clean_title = thread['title'][:25] + "..." if len(thread['title']) > 25 else thread['title']
        if st.button(clean_title, key=thread['id'], use_container_width=True):
            st.session_state['thread_id'] = thread['id']
            st.session_state['message_history'] = [{
                'role': 'user' if isinstance(m, HumanMessage) else 'assistant',
                'content': m.content
            } for m in load_conversation(thread['id'])]
            st.rerun()

    st.markdown("---")
    if st.button("Clear History", use_container_width=True):
        flush_user_history(st.session_state['user_id'])
        st.session_state['chat_threads'] = []
        st.session_state['message_history'] = []
        st.rerun()

# **************************************** MAIN *************************

if not st.session_state['message_history']:
    st.markdown("""
        <div style='height: 70vh; display: flex; flex-direction: column; justify-content: center; align-items: center;'>
            <h1 style='color: white; font-size: 3em; font-weight: 100;'>
                AI Workspace.
            </h1>
        </div>
    """, unsafe_allow_html=True)

for message in st.session_state['message_history']:
    role = message['role']
    avatar = "⚫" if role == 'assistant' else None
    with st.chat_message(role, avatar=avatar):
        st.write(message['content'])

user_input = st.chat_input('Type a message...')

if user_input:
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.write(user_input)

    CONFIG = {"configurable": {"thread_id": st.session_state["thread_id"]}}

    if len(st.session_state['message_history']) == 1:
        generate_title(st.session_state['thread_id'], user_input, st.session_state['user_id'])
        st.session_state['chat_threads'] = retrieve_all_threads(st.session_state['user_id'])

    with st.chat_message('assistant', avatar="⚫"):
        ai_message = st.write_stream(
            (time.sleep(0.02) or chunk.content) for chunk, _ in chatbot.stream(
                {'messages': [HumanMessage(content=user_input)]}, 
                config=CONFIG, 
                stream_mode='messages'
            )
        )
    
    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})