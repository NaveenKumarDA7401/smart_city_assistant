# 🏙 Smart City Information Assistant

An intelligent assistant built with Generative AI and RAG to help citizens access city services, transportation info, policies, and emergency procedures from a structured knowledge base.

---

## 📌 Features

- Natural language querying of city knowledge base
- FastAPI backend with RAG pipeline using LLaMA3 (via Ollama)
- ChromaDB vector store with OllamaEmbeddings
- Streamlit frontend with conversational UI and source document display
- CrewAI multi-agent system for advanced routing and answers
- Conversation history + session management
- Documented API and modular backend

---

## 🧠 Architecture Overview

```
                           ┌────────────────────┐
                           │  Smart City JSON   │
                           └────────┬───────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   LangChain RAG     │
                         │   - Chunking        │
                         │   - Embeddings (Ollama)
                         │   - Vector Store (Chroma)
                         └────────┬────────────┘
                                  │
                                  ▼
   ┌────────────┐      ┌───────────────────┐      ┌────────────┐
   │  Streamlit │ ◀──▶ │   FastAPI Server  │ ◀──▶ │   Ollama   │
   │  Frontend  │      │  (Query/Search)   │      │  (LLaMA 3) │
   └────────────┘      └──────┬────────────┘      └────────────┘
                              ▼
                     ┌───────────────────┐
                     │   CrewAI Agents   │
                     │ (Info / Policy /  │
                     │   Services)       │
                     └───────────────────┘
```

---

## 🚀 Technologies Used

| Tech              | Role                                |
|-------------------|--------------------------------------|
| **Ollama**         | Local LLaMA 3 inference              |
| **LangChain**      | RAG pipeline, LLM Orchestration      |
| **ChromaDB**       | Vector similarity search             |
| **FastAPI**        | Backend API service                  |
| **Streamlit**      | Interactive frontend UI              |
| **CrewAI**         | Multi-agent decision making (bonus)  |

---

## ⚙️ Setup Instructions

### 1️⃣ Clone and install dependencies
```bash
git clone https://github.com/your-username/smart-city-assistant.git
cd smart-city-assistant
pip install -r requirements.txt
```

### 2️⃣ Pull Ollama Model (LLaMA3)
```bash
ollama pull llama3
```

### 3️⃣ Add Knowledge Base
Place your knowledge files inside:
```
smart_city_assistant/knowledge_base/knowledge.json
```

---

## 🧪 Running the Project

### 1. Start the Backend
```bash
uvicorn backend.main:app --reload
```
- Visit API docs: [http://localhost:8000/docs](http://localhost:8000/docs)

### 2. Launch the Streamlit Frontend
```bash
streamlit run frontend/app.py
```

---

## 📬 API Endpoints

| Method | Endpoint       | Description                    |
|--------|----------------|--------------------------------|
| POST   | `/query`       | RAG-based answer               |
| POST   | `/search`      | Direct vector search           |
| GET    | `/health`      | Health check                   |
| POST   | `/agent_query` | (optional) CrewAI answer       |

---

## 🤖 CrewAI Agent System

You implemented a **multi-agent architecture** using CrewAI:

| Agent               | Role                                  |
|---------------------|----------------------------------------|
| Information Specialist | Handles general city service queries |
| Policy Analyst       | Handles legal and regulatory queries  |
| Service Coordinator  | Helps with forms, applications, permits|

**Routing logic**:
- Permit-related → Service Coordinator  
- Law/policy → Policy Analyst  
- Others → Information Specialist

---
