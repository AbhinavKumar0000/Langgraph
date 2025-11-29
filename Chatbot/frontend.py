import streamlit as st
import time
import uuid
from langchain_core.messages import HumanMessage
from backend import chatbot, retrieve_all_threads, generate_title, flush_db

# **************************************** Page Config *************************

st.set_page_config(
    page_title="AI Workspace",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded" 
)

# **************************************** GEMINI-STYLE CSS *************************

st.markdown("""
<style>
    /* -------------------------------------------------------------------------- */
    /* 1. ANIMATED BACKGROUND (Fixed)                                             */
    /* -------------------------------------------------------------------------- */
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

    /* -------------------------------------------------------------------------- */
    /* 2. SIDEBAR STYLING (Clean & Minimal)                                       */
    /* -------------------------------------------------------------------------- */
    [data-testid="stSidebar"] {
        background-color: #131314; /* Gemini Dark Grey */
        border-right: 1px solid #2d2d2d;
    }

    /* RESTORE HAMBURGER MENU (Do not hide header completely) */
    header[data-testid="stHeader"] {
        background-color: transparent;
    }
    
    /* Hide the default footer */
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}

    /* -------------------------------------------------------------------------- */
    /* 3. BUTTON STYLING (The "List" Look)                                        */
    /* -------------------------------------------------------------------------- */
    
    /* Reset all buttons first */
    div.stButton > button {
        width: 100%;
        border: none;
        background: transparent;
        text-align: left;
        color: #9aa0a6; /* Muted text */
        font-size: 14px;
        padding: 8px 12px;
        margin: 0;
        border-radius: 20px; /* Rounded pill shape on hover */
        transition: background-color 0.1s ease;
    }

    /* Hover effect for List Items */
    div.stButton > button:hover {
        background-color: #303134; /* Darker grey hover */
        color: #e8eaed; /* White text on hover */
    }
    
    /* Focus/Active effect */
    div.stButton > button:focus {
        background-color: #303134;
        color: #e8eaed;
        border: none;
        outline: none;
    }

    /* -------------------------------------------------------------------------- */
    /* 4. "NEW CHAT" BUTTON (Special Styling)                                     */
    /* -------------------------------------------------------------------------- */
    /* Target the first button in sidebar */
    [data-testid="stSidebar"] div.stButton:first-of-type {
        padding-bottom: 20px; /* Space after new chat */
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
    
    /* Add a "+" icon before text using CSS if needed, 
       but we will just use text in the python code */

    /* -------------------------------------------------------------------------- */
    /* 5. TYPOGRAPHY                                                              */
    /* -------------------------------------------------------------------------- */
    .sidebar-header {
        color: #9aa0a6;
        font-size: 12px;
        font-weight: 600;
        margin-top: 10px;
        margin-bottom: 5px;
        padding-left: 10px;
    }

    /* -------------------------------------------------------------------------- */
    /* 6. CHAT MESSAGE STYLING                                                    */
    /* -------------------------------------------------------------------------- */
    .stChatMessage {
        background-color: transparent;
    }
    
    /* User Avatar & Bubble */
    [data-testid="chatAvatarIcon-user"] {
        background-color: transparent !important;
    }
    
    /* Assistant Avatar */
    [data-testid="chatAvatarIcon-assistant"] {
        background-color: #4b6cb7 !important;
    }

    div[data-testid="stBottom"] {
        background-color: transparent; /* Makes the bar invisible */
        border-top: none;
    }
    

</style>
""", unsafe_allow_html=True)

# **************************************** Utility Functions *************************

def generate_thread_id():
    return str(uuid.uuid4())

def reset_chat():
    st.session_state['thread_id'] = generate_thread_id()
    st.session_state['message_history'] = []

def load_conversation(thread_id):
    state = chatbot.get_state(config={'configurable': {'thread_id': thread_id}})
    return state.values.get('messages', [])

# **************************************** Session Setup ******************************

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = retrieve_all_threads() or []

# **************************************** Sidebar UI *********************************

with st.sidebar:
    # 1. New Chat (Styled like Gemini's top bar)
    if st.button("New chat", use_container_width=True):
        reset_chat()
        st.rerun()

    # 2. History Header
    st.markdown('<div class="sidebar-header">Recent</div>', unsafe_allow_html=True)
    
    # 3. History List (The List Look)
    for thread in st.session_state['chat_threads'][::-1]:
        clean_title = thread['title']
        if len(clean_title) > 25:
            clean_title = clean_title[:25] + "..."
            
        # If active, we can add a visual cue or just let the focus state handle it
        # We use a simple text label. The CSS makes it look like a list item.
        display_text = clean_title
        
        if st.button(display_text, key=thread['id'], use_container_width=True):
            st.session_state['thread_id'] = thread['id']
            
            messages = load_conversation(thread['id'])
            temp_messages = []
            for msg in messages:
                role = 'user' if isinstance(msg, HumanMessage) else 'assistant'
                temp_messages.append({'role': role, 'content': msg.content})

            st.session_state['message_history'] = temp_messages
            st.rerun()

    st.markdown("---")
    # Optional Clear Button
    if st.button("Clear History", use_container_width=True):
        flush_db()
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

# Display Messages
for message in st.session_state['message_history']:
    role = message['role']
    # Gemini uses specific colors/icons. 
    avatar = "✨" if role == 'assistant' else None 
    
    with st.chat_message(role, avatar=avatar):
        st.write(message['content'])

# Chat Input
user_input = st.chat_input('Message chatbot...')

if user_input:
    # 1. UI Update
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.write(user_input)

    # 2. Config
    CONFIG = {
        "configurable": {"thread_id": st.session_state["thread_id"]},
        "metadata": {"thread_id": st.session_state["thread_id"]},
    }

    # 3. Generate Title (First message only)
    if len(st.session_state['message_history']) == 1:
        generate_title(st.session_state['thread_id'], user_input)
        st.session_state['chat_threads'] = retrieve_all_threads()

    # 4. Stream Response
    with st.chat_message('assistant', avatar="✨"):
        ai_message = st.write_stream(
            (time.sleep(0.02) or message_chunk.content) for message_chunk, metadata in chatbot.stream(
                {'messages': [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode='messages'
            )
        )

    # 5. Save History
    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})