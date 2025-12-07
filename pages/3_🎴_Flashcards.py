"""
Flashcard Generator Page - Generate topic-based flashcards
"""
import streamlit as st
import json
from utils.db import Database
from utils.helpers import load_prompt, call_gemini, parse_json_response

st.set_page_config(page_title="Flashcards", page_icon="🎴", layout="wide")

db = Database()

st.title("🎴 Flashcard Generator")

if 'current_notebook' not in st.session_state:
    st.warning("⚠️ No notebook selected. Please upload a PDF from the home page.")
    if st.button("Go to Home"):
        st.switch_page("app.py")
else:
    notebook = db.get_notebook(st.session_state.current_notebook)
    
    if notebook:
        st.header(f"📓 {notebook['filename']}")
        
        # Topic selection
        topics = notebook.get('topics', [])
        
        if not topics:
            st.warning("No topics found. Please check the Summary page.")
        else:
            selected_topic = st.selectbox(
                "Select a topic to generate flashcards:",
                topics,
                key="topic_selector"
            )
            
            if st.button("🎴 Generate Flashcards", type="primary"):
                with st.spinner(f"Generating flashcards for '{selected_topic}'..."):
                    try:
                        # Get relevant text for the topic (simplified: use full text)
                        text_content = notebook.get('text_content', '')
                        
                        # Load flashcard prompt
                        prompt_config = load_prompt('flashcard_prompt.json')
                        
                        # Generate flashcards
                        response = call_gemini(prompt_config, text_content[:8000], topic=selected_topic)
                        
                        # Parse JSON response
                        flashcards = parse_json_response(response)
                        
                        # Store in session state
                        st.session_state.flashcards = flashcards
                        st.session_state.selected_topic = selected_topic
                        
                    except Exception as e:
                        st.error(f"Error generating flashcards: {str(e)}")
                        st.exception(e)
            
            # Display flashcards
            if 'flashcards' in st.session_state and st.session_state.get('selected_topic') == selected_topic:
                st.divider()
                st.subheader(f"📚 Flashcards for: {selected_topic}")
                
                flashcards = st.session_state.flashcards
                
                # Handle both JSON array and plain text responses
                if isinstance(flashcards, list):
                    for idx, card in enumerate(flashcards):
                        with st.expander(f"Flashcard {idx + 1}"):
                            if isinstance(card, dict):
                                st.markdown(f"**Question:** {card.get('question', 'N/A')}")
                                st.markdown(f"**Answer:** {card.get('answer', 'N/A')}")
                            else:
                                st.markdown(str(card))
                else:
                    # Display as text if not JSON
                    st.markdown(flashcards)
    else:
        st.error("Notebook not found!")
