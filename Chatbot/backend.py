import streamlit as st
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langgraph.checkpoint.memory import MemorySaver # <--- Use Memory
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import uuid

load_dotenv()

# Setup Model
model = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

# --- IN-MEMORY STORAGE (Stable for Cloud Demos) ---
# We use global dictionaries to simulate a DB. 
# This works perfectly for the lifespan of the Cloud container.

if "THREAD_DB" not in st.session_state:
    st.session_state["THREAD_DB"] = {}

# We need a checkpointer that survives reruns but is in memory
@st.cache_resource
def get_checkpointer():
    return MemorySaver()

checkpointer = get_checkpointer()

# --- Graph Setup ---
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def chat_node(state: ChatState):
    return {"messages": [model.invoke(state['messages'])]}

graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

chatbot = graph.compile(checkpointer=checkpointer)

# --- Helper Functions ---

def generate_title(thread_id, user_message, user_id):
    """Generates a title and stores it in the global dictionary."""
    try:
        summary_prompt = f"Summarize this query in 3-5 words for a chat title: {user_message}"
        title_response = model.invoke(summary_prompt)
        title = title_response.content.strip().replace('"', '')
        
        # Save to our simulated DB
        # Structure: {user_id: {thread_id: title}}
        if "simulated_db" not in st.session_state:
            st.session_state.simulated_db = {}
            
        if user_id not in st.session_state.simulated_db:
            st.session_state.simulated_db[user_id] = {}
            
        st.session_state.simulated_db[user_id][thread_id] = title
        
    except Exception as e:
        print(f"Error generating title: {e}")

def retrieve_all_threads(user_id):
    """Retrieves threads from the simulated DB."""
    if "simulated_db" not in st.session_state:
        st.session_state.simulated_db = {}
        
    user_threads = st.session_state.simulated_db.get(user_id, {})
    
    results = []
    for tid, title in user_threads.items():
        results.append({'id': tid, 'title': title})
    
    return results

def flush_user_history(user_id):
    """Clears history for the specific user."""
    if "simulated_db" in st.session_state and user_id in st.session_state.simulated_db:
        del st.session_state.simulated_db[user_id]