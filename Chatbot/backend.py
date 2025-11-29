import sqlite3
import streamlit as st
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

# Setup Model
model = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

# --- DATABASE SETUP (Cached & Thread Safe) ---
@st.cache_resource
def setup_database():
    """
    Sets up the SQLite connection ONCE per session.
    """
    conn = sqlite3.connect("chatbot.db", check_same_thread=False)
    
    # Create table to map Threads to Users
    conn.execute("""
        CREATE TABLE IF NOT EXISTS thread_titles (
            thread_id TEXT PRIMARY KEY, 
            title TEXT,
            user_id TEXT
        )
    """)
    conn.commit()
    
    checkpointer = SqliteSaver(conn=conn)
    return conn, checkpointer

# Initialize DB
conn, checkpointer = setup_database()

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
    """Generates a title and links it to the specific User ID"""
    try:
        summary_prompt = f"Summarize this query in 3-5 words for a chat title: {user_message}"
        title_response = model.invoke(summary_prompt)
        title = title_response.content.strip().replace('"', '')
        
        # Insert with User ID
        conn.execute(
            "INSERT OR REPLACE INTO thread_titles (thread_id, title, user_id) VALUES (?, ?, ?)", 
            (str(thread_id), title, user_id)
        )
        conn.commit()
    except Exception as e:
        print(f"Error generating title: {e}")

def retrieve_all_threads(user_id):
    """Retrieves only the threads belonging to the current user"""
    cursor = conn.cursor()
    
    # Filter by user_id
    cursor.execute("SELECT thread_id, title FROM thread_titles WHERE user_id = ?", (user_id,))
    
    results = []
    for row in cursor.fetchall():
        results.append({'id': row[0], 'title': row[1]})
    
    return results

def flush_user_history(user_id):
    """Clears history for the specific user only"""
    try:
        conn.execute("DELETE FROM thread_titles WHERE user_id = ?", (user_id,))
        conn.commit()
    except Exception as e:
        print(f"Error flushing DB: {e}")