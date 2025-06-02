import streamlit as st
import requests
from datetime import datetime
import time

# Configuration
API_URL = "http://localhost:8000"
LOGO = "🏙️"

# Initialize session state
if "conversation" not in st.session_state:
    st.session_state.conversation = []
if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = str(datetime.now().timestamp())

# UI Setup
st.set_page_config(
    page_title="Smart City Assistant",
    page_icon=LOGO,
    layout="centered"
)

# Sidebar
with st.sidebar:
    st.title("Settings")
    st.markdown("---")
    top_k = st.slider("Number of sources to show", 1, 5, 3)
    show_sources = st.checkbox("Show source documents", True)

    if st.button("Clear Conversation"):
        st.session_state.conversation = []
        st.session_state.conversation_id = str(datetime.now().timestamp())
        st.rerun()

    st.markdown("---")
    st.markdown("**Example Questions:**")
    st.markdown("- How do I get a building permit?")
    st.markdown("- What are the library hours?")
    st.markdown("- When is garbage collection in Zone A?")
    st.markdown("- What's the bus fare?")

# Main Interface
st.title(f"{LOGO} Smart City Information Assistant")
st.markdown("Ask anything about city services, facilities, transportation, policies, or emergencies.")

# Chat interface
for role, message in st.session_state.conversation:
    with st.chat_message(role):
        st.write(message)

# User input
if prompt := st.chat_input("Ask your question..."):
    st.session_state.conversation.append(("user", prompt))

    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching city knowledge base..."):
            try:
                start_time = time.time()
                response = requests.post(
                    f"{API_URL}/query",
                    json={
                        "question": prompt,
                        "conversation_id": st.session_state.conversation_id
                    }
                ).json()

                if "answer" in response:
                    st.write(response["answer"])
                    st.session_state.conversation.append(("assistant", response["answer"]))

                    if show_sources and "source_documents" in response:
                        with st.expander(f"📄 Source Documents ({len(response['source_documents'])})"):
                            for doc in response["source_documents"][:top_k]:
                                st.markdown(f"**{doc['metadata'].get('title', 'Document')}**")
                                st.caption(f"Category: {doc['metadata'].get('category', 'General')}")
                                st.markdown(f"```\n{doc['content'][:300]}...\n```")
                                st.markdown("---")

                    st.caption(f"Response time: {time.time() - start_time:.2f}s")
                else:
                    st.error(response.get("error", "Unknown error occurred"))
            except Exception as e:
                st.error(f"Failed to get response: {str(e)}")
