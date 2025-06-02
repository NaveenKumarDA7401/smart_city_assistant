from crewai import Agent, Task, Crew
from langchain.tools import Tool
from backend.rag_engine import search_documents

def document_search(query):
    """Enhanced search function for agents"""
    results = search_documents(query, k=5)
    return "\n\n".join([
        f"Document {i+1}:\nTitle: {doc.metadata.get('title', 'Untitled')}\n"
        f"Category: {doc.metadata.get('category', 'General')}\n"
        f"Content: {doc.page_content[:500]}..."
        for i, doc in enumerate(results)
    ])

search_tool = Tool(
    name="KnowledgeBaseSearch",
    func=document_search,
    description="Searches the city knowledge base for relevant information"
)

# Define Agents
information_retriever = Agent(
    role="City Information Specialist",
    goal="Retrieve accurate information about city services and facilities",
    backstory="An expert in navigating city databases and information systems",
    tools=[search_tool],
    verbose=True,
    memory=True
)

policy_expert = Agent(
    role="City Policy Analyst",
    goal="Provide detailed explanations of city policies and regulations",
    backstory="A legal expert with deep knowledge of municipal codes and ordinances",
    tools=[search_tool],
    verbose=True,
    memory=True
)

service_coordinator = Agent(
    role="City Service Coordinator",
    goal="Guide citizens through city service processes and requirements",
    backstory="Experienced in all city department procedures and paperwork",
    tools=[search_tool],
    verbose=True,
    memory=True
)

def route_question(question):
    """Determine which agent should handle the question"""
    question_lower = question.lower()
    
    if any(word in question_lower for word in ["permit", "license", "application", "form"]):
        return service_coordinator
    elif any(word in question_lower for word in ["policy", "law", "regulation", "ordinance"]):
        return policy_expert
    else:
        return information_retriever

def get_agentic_response(question):
    """Get response from the appropriate agent"""
    agent = route_question(question)
    
    task = Task(
        description=f"Answer this citizen question: {question}",
        agent=agent,
        expected_output="A detailed, accurate answer based on city knowledge base with citations to relevant documents"
    )
    
    crew = Crew(
        agents=[agent],
        tasks=[task],
        verbose=2
    )
    
    return crew.kickoff()