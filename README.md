# 🦜🕸️ Advanced LangGraph: From Workflows to Agents

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![LangGraph](https://img.shields.io/badge/LangGraph-Latest-orange)
![LangChain](https://img.shields.io/badge/LangChain-Integration-green)

## Overview

This repository serves as a comprehensive **reference implementation and learning hub** for building stateful, multi-actor LLM applications using **LangGraph**.

It is structured to guide developers from foundational graph concepts (nodes, edges, conditional logic) to complex, production-ready architectures involving **RAG (Retrieval Augmented Generation)**, **MCP (Model Context Protocol)**, **Asynchronous Event Loops**, and **Human-in-the-Loop** workflows.

Whether you are looking to understand how to cycle through agent steps or deploy a full-stack chatbot with memory persistence, this repository contains the blueprints.

## 🏗Repository Architecture

The project is split into two core distinct domains: **Educational Notebooks** for concept mastery and a **Production Chatbot** module.

### 1. Educational Workflows (`/`)

These notebooks demonstrate specific LangGraph design patterns:

| Notebook File                          | Concept Covered         | Description                                                             |
| :------------------------------------- | :---------------------- | :---------------------------------------------------------------------- |
| `simple_llm_workflow.ipynb`            | **Linear Chains**       | Basic node-edge connections without complex routing.                    |
| `llm_workflow.ipynb`                   | **LLM Integration**     | Initial LangGraph learning with LLM workflows                           |
| `conditional_workflow.ipynb`           | **Conditional Logic**   | Dynamic decision-making based on conditions                             |
| `llm_based_conditional_workflow.ipynb` | **LLM Decision Making** | Using LLMs for conditional routing decisions                            |
| `Iterative_workflow.ipynb`             | **Cycles & Loops**      | Self-correcting agents that loop until a condition is met.              |
| `parallel_workflow.ipynb`              | **Map-Reduce**          | Running multiple specialized agents effectively in parallel.            |
| `prompt_chaining.ipynb`                | **Prompt Engineering**  | Breaking complex tasks into a sequence of chained prompts.              |
| `fault_tolerance.ipynb`                | **Robustness**          | Handling API errors and implementing retry mechanisms within the graph. |
| `human_in_the_loop.ipynb`              | **Human Interaction**   | Integrating human feedback and approval into workflows                  |
| `ram_memory_chatbot.ipynb`             | **State Management**    | Managing conversation history using in-memory checkpoints.              |
| `sequencialflow_withoutllm.ipynb`      | **Basic Workflows**     | Sequential workflows without LLM integration                            |
| `subgraph.ipynb`                       | **Modular Design**      | Creating reusable subgraph components                                   |
| `shared_subgraph.ipynb`                | **Shared Components**   | Implementing shared subgraphs across multiple workflows                 |
| `tools.ipynb`                          | **Tool Integration**    | Integrating external tools with LangGraph agents                        |
| `test_installation.ipynb`              | **Setup Verification**  | Testing the installation and environment setup                          |

### 2. The Agentic Chatbot (`/Chatbot`)

A modular, scalable chatbot application designed for deployment.

- **`chatbot_mcp.py`**: Implementation of the **Model Context Protocol**, allowing the LLM to interface with standardized external contexts.
- **`rag_backend.py`**: A specialized graph integrating Vector Search for grounding responses in private data.
- **`backend_withdb.py`**: Incorporates persistent storage (SQL/SQLite) for long-term user memory (Checkpointers).
- **`async_backend.py`**: Leverages Python's `asyncio` for non-blocking high-concurrency performance.
- **`frontend.py` / `frontend_mcp.py`**: Streamlit-based user interfaces to interact with the underlying graph agents.

### 3. HITL Implementations (`/`)

Production-ready Human-in-the-Loop implementations:

- **`with_HITL.py`**: Complete HITL implementation with human intervention points
- **`without_HITL.py`**: Baseline workflow for comparison without human intervention

### 4. Development Configuration

- **`.devcontainer/`**: Development container configuration for consistent environments
- **`.vscode/`**: VS Code settings and launch configurations
- **`.gitignore`**: Git ignore file for Python projects
- **`requirements.txt`**: Simplified project dependencies
- **`Iterative_workflow.ipynb`**: Updated workflow examples

## Getting Started

### Prerequisites

- Python 3.10+
- An API Key (OpenAI, Anthropic, or similar)
- VS Code or Jupyter Notebook for development

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/AbhinavKumar0000/subgraphs.git
   cd subgraphs
   ```

2. **Environment Setup**
   It is recommended to use a virtual environment:

   ```bash
   python -m venv venv
   # Windows:
   .\venv\Scripts\activate
   # Mac/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configuration**
   Create a `.env` file in the root directory and add your credentials:
   ```env
   OPENAI_API_KEY=sk-...
   TAVILY_API_KEY=tvly-...
   LANGCHAIN_API_KEY=... # Optional for LangSmith Tracing
   LANGCHAIN_TRACING_V2=true
   ```

### Development with Dev Container

For a consistent development environment using VS Code:

1. Install the "Dev Containers" extension in VS Code
2. Open the command palette (Ctrl+Shift+P)
3. Select "Dev Containers: Reopen in Container"
4. The environment will be automatically configured

## Usage Guide

### Learning Mode

To study the graph structures visually:

1. Launch Jupyter Lab/Notebook:
   ```bash
   jupyter notebook
   ```
2. Open any workflow notebook (e.g., `subgraph.ipynb` or `human_in_the_loop.ipynb`)
3. Run the cells to see the `.get_graph().draw_png()` outputs which visualize the state machine

### Application Mode

To run the full-stack chatbot:

**For the Standard RAG Chatbot:**

```bash
streamlit run Chatbot/frontend.py
```

## For Human-in-the-Loop Workflow:

```bash
python with_HITL.py
```

## For Subgraph Testing:

```bash
python
python -c "import subgraph; subgraph.main()"
```

# Core Features

- Graph Patterns
- Sequential Workflows: Linear execution paths

- Conditional Routing: Dynamic decision points

- Parallel Execution: Concurrent node processing

- Iterative Loops: Self-correcting workflows

- Subgraph Composition: Modular, reusable components

- Human-in-the-Loop: Integration of human feedback

- State Management
- In-memory checkpoints

- Persistent storage options

- Conversation memory

- Error recovery states

- Tool Integration
- External API calls

- Database operations

- File system interactions

- Custom tool creation

## Project Structure

```bash
subgraphs/
├── .devcontainer/          # Dev container configuration
├── .vscode/               # VS Code settings
├── Chatbot/               # Production chatbot module
│   ├── chatbot_mcp.py     # Model Context Protocol implementation
│   ├── rag_backend.py     # RAG integration backend
│   ├── backend_withdb.py  # Database persistence
│   ├── async_backend.py   # Asynchronous implementation
│   └── frontend.py        # Streamlit UI
├── __pycache__/           # Python cache files
├── __pycache__/           # Chatbot cache files
├── *.ipynb                # Educational notebooks (17+ workflow examples)
├── with_HITL.py          # HITL implementation
├── without_HITL.py       # Baseline workflow
├── requirements.txt      # Project dependencies
└── README.md            # This documentation file

```
