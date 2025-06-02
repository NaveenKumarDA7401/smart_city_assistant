from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from backend.rag_engine import qa_chain, search_documents
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Smart City Info Assistant",
    description="API for querying city information from knowledge base",
    version="1.0.0",
    docs_url="/docs",
    redoc_url=None
)

class Query(BaseModel):
    question: str
    conversation_id: Optional[str] = None

class SearchQuery(BaseModel):
    query: str
    top_k: int = 3

@app.post("/query")
async def query_chat(query: Query):
    try:
        logger.info(f"Processing query: {query.question}")
        result = qa_chain({"query": query.question, "conversation_id": query.conversation_id})
        return {
            "answer": result["result"],
            "source_documents": [{
                "content": doc.page_content,
                "metadata": doc.metadata
            } for doc in result["source_documents"]],
            "conversation_id": query.conversation_id or "new"
        }
    except Exception as e:
        logger.error(f"Query failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search")
async def vector_search(search: SearchQuery):
    try:
        logger.info(f"Vector search: {search.query}")
        docs = search_documents(search.query, search.top_k)
        return {
            "results": [{
                "content": doc.page_content,
                "metadata": doc.metadata,
                "score": float(doc.metadata.get("score", 0))
            } for doc in docs]
        }
    except Exception as e:
        logger.error(f"Search failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "Smart City Assistant API",
        "version": "1.0.0"
    }