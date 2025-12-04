import asyncio
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool, BaseTool
from langchain_mcp_adapters.client import MultiServerMCPClient
from dotenv import load_dotenv
import aiosqlite
import requests

load_dotenv()

# -------------------
# 1. LLM & Tools
# -------------------
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
search_tool = DuckDuckGoSearchRun(region="us-en")

@tool
def get_stock_price(symbol: str) -> dict:
    """Fetch latest stock price for a given symbol."""
    # Note: Ensure API Key is valid or use env var
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey=C9PE94QUEW9VWGFM"
    r = requests.get(url)
    return r.json()

# Initialize MCP Client
# Note: Ensure paths strictly use \\ for Windows or /
client = MultiServerMCPClient(
    {
        "Demo Server": {
            "command": "C:/Users/abhin/anaconda3/Scripts/uv.exe",
            "args": [
                "run", "--with", "fastmcp", "fastmcp", "run",
                "C:\\Codes\\Learning\\Model_Cotext_Protocal\\Expense_Tracker\\main.py"
            ],
        },
        "expense": {
            "transport": "sse", # Changed to sse (standard for remote MCP)
            "url": "https://amateur-green-duck.fastmcp.app/sse" # Ensure this endpoint supports SSE
        }
    }
)

async def load_mcp_tools() -> list[BaseTool]:
    """Async loader for MCP tools"""
    try:
        # We must await the connection and tool retrieval
        await client.initialize()
        return await client.get_tools()
    except Exception as e:
        print(f"Error loading MCP tools: {e}")
        return []

# -------------------
# 2. Graph Setup (Encapsulated)
# -------------------
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

async def build_graph():
    # Load tools asynchronously
    mcp_tools = await load_mcp_tools()
    tools = [search_tool, get_stock_price, *mcp_tools]
    
    llm_with_tools = llm.bind_tools(tools)

    async def chat_node(state: ChatState):
        messages = state["messages"]
        response = await llm_with_tools.ainvoke(messages)
        return {"messages": [response]}

    tool_node = ToolNode(tools)

    # Database connection
    conn = await aiosqlite.connect(database="chatbot.db")
    checkpointer = AsyncSqliteSaver(conn)

    graph = StateGraph(ChatState)
    graph.add_node("chat_node", chat_node)
    graph.add_node("tools", tool_node)
    
    graph.add_edge(START, "chat_node")
    graph.add_conditional_edges("chat_node", tools_condition)
    graph.add_edge("tools", "chat_node")

    return graph.compile(checkpointer=checkpointer)

# -------------------
# 3. Streamlit Runner
# -------------------
# Use this function in your frontend_mcp.py
async def run_chat(user_input: str, thread_id: str):
    bot = await build_graph()
    config = {"configurable": {"thread_id": thread_id}}
    
    async for event in bot.astream({"messages": [("user", user_input)]}, config):
        yield event