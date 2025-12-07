"""
Talk to Doc Page - RAG Chatbot (Placeholder)
"""
import streamlit as st
from utils.db import Database

st.set_page_config(page_title="Talk to Doc", page_icon="💬", layout="wide")

db = Database()

st.title("💬 Talk to Doc")

if 'current_notebook' not in st.session_state:
    st.warning("⚠️ No notebook selected. Please upload a PDF from the home page.")
    if st.button("Go to Home"):
        st.switch_page("app.py")
else:
    notebook = db.get_notebook(st.session_state.current_notebook)
    
    if notebook:
        filename = notebook.get('filename', 'Untitled Notebook')
        st.header(f"📓 {filename}")
        
        st.info("🚧 **Coming Soon!**")
        
        st.markdown("""
        The Talk to Doc chatbot is currently under development. Soon you'll be able to:
        
        - 💬 Ask questions about your document in natural language
        - 🔍 Get answers with relevant excerpts from the PDF
        - 📚 Explore topics through conversational interaction
        - 🎯 Get clarifications on complex concepts
        - 💡 Receive study tips and explanations
        
        This feature will use Retrieval-Augmented Generation (RAG) to provide accurate, context-aware responses!
        """)
        
        # Placeholder chatbot interface
        st.divider()
        st.subheader("Preview: Chatbot Interface")
        
        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {"role": "assistant", "content": "Hello! I'm your document assistant. Ask me anything about your PDF! (Feature coming soon)"}
            ]
        
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input (disabled)
        if prompt := st.chat_input("Ask a question about your document...", disabled=True):
            pass
    else:
        st.error("Notebook not found!")
