# AI Workspace: Next-Gen Intelligent Assistant

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://abhinavkumar0000-langgraph-chatbotfrontend-ruuvj4.streamlit.app/)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-Orchestration-orange?style=for-the-badge)
![Gemini](https://img.shields.io/badge/AI-Gemini%202.0%20Flash-4285F4?style=for-the-badge&logo=google&logoColor=white)
![SQLite](https://img.shields.io/badge/Database-SQLite3-green?style=for-the-badge&logo=sqlite&logoColor=white)

> **A state-aware, multi-user AI chat application built with LangGraph orchestration and a custom high-fidelity Streamlit UI.**

---

## Live Demo
**[Click here to view the deployed application](https://abhinavkumar0000-langgraph-chatbotfrontend-ruuvj4.streamlit.app/)**

---

## Interface Preview

![App Screenshot]<img width="1919" height="850" alt="image" src="https://github.com/user-attachments/assets/53303a35-2b8f-46c5-934b-f9a1b0a67543" />


---

## Key Features

### Advanced Backend Architecture
* **Graph-Based Orchestration:** Unlike simple chatbot wrappers, this project uses **LangGraph** to model conversation flows as nodes and edges, allowing for scalable state management.
* **Persistent Memory:** Utilizes **SQLite** (with thread-safe caching) to store conversation history, allowing users to switch between chats without losing context.
* **Multi-User Session Isolation:** Implements unique UUID generation for browser sessions, ensuring that **User A's data is completely isolated from User B**, even on a shared server deployment.
* **Auto-Summarization:** A background agent analyzes the first message of every thread to generate a concise 3-5 word title for the sidebar history.

### Premium UI/UX (Glassmorphism)
* **Custom CSS Injection:** Heavily modified Streamlit DOM elements to achieve a transparent, "floating" interface.
* **Animated Gradient Background:** A high-performance CSS keyframe animation providing a dynamic, high-contrast monochrome aesthetic.
* **Fixed Footer Layout:** Solved Streamlit's native padding issues to create a seamless, app-like input experience.
* **Streaming Responses:** Real-time token streaming gives the AI a natural "typewriter" feel.

---

## Tech Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Frontend** | Streamlit | The web framework used for the UI. |
| **Styling** | CSS3 | Custom injected CSS for animations and layout overrides. |
| **Orchestration** | LangGraph | Manages the conversation state and control flow. |
| **LLM** | Gemini 2.0 Flash | Google's high-efficiency model for rapid inference. |
| **Database** | SQLite3 | Local storage for chat threads and message checkpoints. |
| **Deployment** | Streamlit Cloud | Cloud hosting environment. |

---

## Project Structure

```bash
AI-Workspace/
├── backend.py            # Core Logic: Graph definition, DB connection, & LLM integration
├── frontend.py           # UI Logic: Streamlit layout, Session State, & Custom CSS
├── requirements.txt      # Project dependencies (langgraph, streamlit, etc.)
├── .env                  # Environment variables (API Keys) - Not committed to repo
├── chatbot.db            # Local database file (Generated automatically)
└── README.md             # Project documentation
