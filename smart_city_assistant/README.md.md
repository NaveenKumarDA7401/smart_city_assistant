# Smart City Information Assistant

## Setup
1. Install requirements: `pip install -r requirements.txt`
2. Download Ollama model: `ollama pull llama3`
3. Place knowledge base files in `knowledge_base/` folder

## Running the System
1. Start FastAPI backend: `uvicorn backend.main:app --reload`
2. Run Streamlit frontend: `streamlit run frontend/app.py`

## Features
- Natural language queries about city services
- Conversation history
- Source document references
- Multi-agent system (CrewAI) for complex queries

## API Endpoints
- `POST /query` - Main question endpoint
- `POST /agent_query` - Agent-based response
- `POST /search` - Direct vector search
- `GET /health` - Service status