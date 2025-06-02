import json
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.docstore.document import Document
import os
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama

# Custom prompt template
prompt_template = """You are a helpful assistant for Metro City. Use the following context to answer the question.
If you don't know the answer, say you don't know. Don't make up answers.

Context: {context}

Question: {question}
Helpful Answer:"""
QA_PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)

def load_knowledge_base(json_path):
    """Load and process the knowledge base JSON file"""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    documents = []
    for category, items in data['knowledge_base'].items():
        if category == "test_queries":
            continue
            
        for item in items:
            metadata = {
                "category": category,
                "title": item.get("title", ""),
                "id": item.get("id", ""),
                **{k:v for k,v in item.items() if k not in ["content", "title", "id"]}
            }
            documents.append(Document(
                page_content=item["content"],
                metadata=metadata
            ))
    return documents

# Initialize components
documents = load_knowledge_base("knowledge_base/knowledge.json")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len
)
split_docs = text_splitter.split_documents(documents)

# Initialize embeddings and vector store
embeddings = OllamaEmbeddings(model="llama3")
vectordb = Chroma.from_documents(
    documents=split_docs,
    embedding=embeddings,
    persist_directory="embeddings"
)
vectordb.persist()

# Initialize LLM
llm = Ollama(model="llama3", temperature=0.2)

# Create QA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectordb.as_retriever(search_kwargs={"k": 4}),
    chain_type_kwargs={"prompt": QA_PROMPT},
    return_source_documents=True
)

def search_documents(query, k=3):
    """Direct vector similarity search"""
    return vectordb.similarity_search(query, k=k)