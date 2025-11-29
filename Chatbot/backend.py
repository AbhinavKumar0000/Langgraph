import sqlite3
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from dotenv import load_dotenv

load_dotenv()

# Setup Model and DB
model = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
conn = sqlite3.connect(database='chatbot.db', check_same_thread=False)

# Ensure our custom titles table exists
conn.execute("CREATE TABLE IF NOT EXISTS thread_titles (thread_id TEXT PRIMARY KEY, title TEXT)")
conn.commit()

checkpointer = SqliteSaver(conn=conn)

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

def generate_title(thread_id, user_message):
    """Generates a title and saves it to the custom table immediately."""
    try:
        # Generate a short 3-5 word title
        summary_prompt = f"Summarize this query in 3-5 words for a chat title: {user_message}"
        title_response = model.invoke(summary_prompt)
        title = title_response.content.strip().replace('"', '')
        
        # Force thread_id to string to ensure consistency
        t_id_str = str(thread_id)
        
        conn.execute("INSERT OR REPLACE INTO thread_titles (thread_id, title) VALUES (?, ?)", (t_id_str, title))
        conn.commit()
    except Exception as e:
        print(f"Error generating title: {e}")

def retrieve_all_threads():
    """Retrieves threads from BOTH checkpoints and titles table to ensure list is up to date."""
    cursor = conn.cursor()
    
    # 1. Get all threads that we have explicitly named (from our custom table)
    cursor.execute("SELECT thread_id, title FROM thread_titles")
    titled_threads = {row[0]: row[1] for row in cursor.fetchall()}
    
    # 2. Get all threads that exist in LangGraph checkpoints (legacy/untitled ones)
    # Note: We use try/except because 'checkpoints' table is created by LangGraph on first run
    checkpoint_threads = []
    try:
        cursor.execute("SELECT DISTINCT thread_id FROM checkpoints")
        checkpoint_threads = [row[0] for row in cursor.fetchall()]
    except sqlite3.OperationalError:
        pass # Table might not exist yet if no chats happened
    
    # 3. Combine them (Union of keys)
    all_ids = set(titled_threads.keys()).union(set(checkpoint_threads))
    
    results = []
    for tid in all_ids:
        # Use the saved title, or fallback to 'New Chat' or the ID itself
        display_title = titled_threads.get(tid, "New Chat")
        results.append({'id': tid, 'title': display_title})
    
    return results


def flush_db():
    conn = sqlite3.connect(database='chatbot.db')
    conn.execute("DELETE FROM checkpoints")
    conn.execute("DELETE FROM thread_titles")
    conn.commit()
    conn.close()