# 🦜🕸️ Advanced LangGraph: From Workflows to Agents

![Python](https://img.shields.io/badge/Python-3.10%2B-blue) ![LangGraph](https://img.shields.io/badge/LangGraph-Latest-orange) ![LangChain](https://img.shields.io/badge/LangChain-Integration-green)

##  Overview

This repository serves as a comprehensive **reference implementation and learning hub** for building stateful, multi-actor LLM applications using **LangGraph**. 

It is structured to guide developers from foundational graph concepts (nodes, edges, conditional logic) to complex, production-ready architectures involving **RAG (Retrieval Augmented Generation)**, **MCP (Model Context Protocol)**, and **Asynchronous Event Loops**.

Whether you are looking to understand how to cycle through agent steps or deploy a full-stack chatbot with memory persistence, this repository contains the blueprints.

---

## Repository Architecture

The project is split into two core distinct domains: **Educational Notebooks** for concept mastery and a **Production Chatbot** module.

### 1. Educational Workflows (`/`)
These notebooks demonstrate specific LangGraph design patterns:

| Notebook File | Concept Covered | Description |
| :--- | :--- | :--- |
| `simple_llm_workflow.ipynb` | **Linear Chains** | Basic node-edge connections without complex routing. |
| `conditional_workflow.ipynb` | **Conditional Logic** | Dynamic decision-making where the LLM chooses the next step. |
| `Iterative_workflow.ipynb` | **Cycles & Loops** | Self-correcting agents that loop until a condition is met. |
| `parallel_workflow.ipynb` | **Map-Reduce** | Running multiple specialized agents effectively in parallel. |
| `prompt_chaining.ipynb` | **Prompt Engineering** | Breaking complex tasks into a sequence of chained prompts. |
| `fault_tolerance.ipynb` | **Robustness** | Handling API errors and implementing retry mechanisms within the graph. |
| `ram_memory_chatbot.ipynb` | **State Management** | Managing conversation history using in-memory checkpoints. |

### 2. The Agentic Chatbot (`/Chatbot`)
A modular, scalable chatbot application designed for deployment.

* **`chatbot_mcp.py`**: Implementation of the **Model Context Protocol**, allowing the LLM to interface with standardized external contexts.
* **`rag_backend.py`**: A specialized graph integrating Vector Search for grounding responses in private data.
* **`backend_withdb.py`**: Incorporates persistent storage (SQL/SQLite) for long-term user memory (Checkpointers).
* **`async_backend.py`**: Leverages Python's `asyncio` for non-blocking high-concurrency performance.
* **`frontend.py` / `frontend_mcp.py`**: Streamlit-based user interfaces to interact with the underlying graph agents.

---

##  Getting Started

### Prerequisites
* Python 3.10+
* An API Key (OpenAI, Anthropic, or similar)

### Installation

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/AbhinavKumar0000/Langgraph.git](https://github.com/AbhinavKumar0000/Langgraph.git)
    cd Langgraph
    ```

2.  **Environment Setup**
    It is recommended to use a virtual environment:
    ```bash
    python -m venv venv
    # Windows:
    .\venv\Scripts\activate
    # Mac/Linux:
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configuration**
    Create a `.env` file in the root directory and add your credentials:
    ```env
    OPENAI_API_KEY=sk-...
    TAVILY_API_KEY=tvly-...
    LANGCHAIN_API_KEY=... # Optional for LangSmith Tracing
    LANGCHAIN_TRACING_V2=true
    ```

---

## Usage Guide

### Learning Mode
To study the graph structures visually:
1.  Launch Jupyter Lab/Notebook:
    ```bash
    jupyter notebook
    ```
2.  Open `visualize_graph.ipynb` (or any workflow file).
3.  Run the cells to see the `.get_graph().draw_png()` outputs which visualize the state machine.

### Application Mode
To run the full-stack chatbot:

**For the Standard RAG Chatbot:**
```bash
streamlit run Chatbot/frontend.py
