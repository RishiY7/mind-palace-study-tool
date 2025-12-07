"""
Flashcards Page - Study with topic-based flashcards
"""
import streamlit as st
import json
from utils.db import Database
from utils.helpers import load_prompt, call_gemini, parse_json_response
from utils.text_extraction import get_topic_text
from utils.sidebar_utils import show_sidebar_on_all_pages

st.set_page_config(page_title="Flashcards", page_icon="🎴", layout="wide")

# Show common sidebar on all pages
show_sidebar_on_all_pages()

db = Database()

# Initialize session state
if 'current_card_index' not in st.session_state:
    st.session_state.current_card_index = 0
if 'show_answer' not in st.session_state:
    st.session_state.show_answer = False
if 'view_mode' not in st.session_state:
    st.session_state.view_mode = "study"  # "study" or "show"

# Custom CSS for flashcards
st.markdown("""
    <style>
    .flashcard {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        color: white;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        min-height: 200px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
    }
    .flashcard-question {
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .flashcard-answer {
        font-size: 1.2rem;
        margin-top: 1rem;
        padding-top: 1rem;
        border-top: 2px solid rgba(255,255,255,0.3);
    }
    .flashcard-grid {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 0.5rem;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
    }
    .flashcard-grid-question {
        color: #667eea;
        font-weight: bold;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }
    .flashcard-grid-answer {
        color: #333;
        font-size: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🎴 Flashcard Generator")

if 'current_notebook' not in st.session_state:
    st.warning("⚠️ No notebook selected. Please upload a PDF from the home page.")
    if st.button("Go to Home"):
        st.switch_page("app.py")
else:
    notebook = db.get_notebook(st.session_state.current_notebook)
    
    if notebook:
        filename = notebook.get('filename', 'Untitled Notebook')
        st.header(f"📓 {filename}")
        
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
            
            # Number of flashcards input
            col1, col2 = st.columns([3, 1])
            with col1:
                num_flashcards = st.number_input(
                    "Number of flashcards to generate:",
                    min_value=3,
                    max_value=20,
                    value=5,
                    step=1,
                    help="Choose how many flashcards you want (3-20)"
                )
            
            with col2:
                st.metric("Cards", num_flashcards)
            
            if st.button("🎴 Generate Flashcards", type="primary"):
                with st.spinner(f"Generating flashcards for '{selected_topic}'..."):
                    try:
                        # Get text relevant to the selected topic
                        text_content = notebook.get('text_content', '')
                        
                        # Use semantic extraction to get topic-specific text
                        st.info(f"🔍 Extracting content relevant to '{selected_topic}'...")
                        topic_specific_text = get_topic_text(text_content, selected_topic)
                        
                        # Load flashcard prompt
                        prompt_config = load_prompt('flashcard_prompt.json')
                        
                        # Update prompt to request specific number of flashcards
                        original_instruction = prompt_config['user_instruction']
                        prompt_config['user_instruction'] = original_instruction.replace('5 flashcards', f'{num_flashcards} flashcards')
                        
                        # Generate flashcards
                        response = call_gemini(prompt_config, topic_specific_text, topic=selected_topic)
                        
                        # Parse JSON response
                        flashcards = parse_json_response(response)
                        
                        # Store in session state
                        st.session_state.flashcards = flashcards
                        st.session_state.selected_topic = selected_topic
                        st.session_state.current_card_index = 0
                        st.session_state.show_answer = False
                        
                    except Exception as e:
                        st.error(f"Error generating flashcards: {str(e)}")
                        st.exception(e)
            
            # Display flashcards
            if 'flashcards' in st.session_state and st.session_state.get('selected_topic') == selected_topic:
                st.divider()
                st.subheader(f"📚 Flashcards for: {selected_topic}")
                
                flashcards = st.session_state.flashcards
                
                # Handle both JSON array and plain text responses
                if isinstance(flashcards, list) and len(flashcards) > 0:
                    # View mode selector
                    col1, col2, col3 = st.columns([1, 1, 2])
                    with col1:
                        st.session_state.view_mode = st.radio(
                            "View Mode:",
                            ["study", "show"],
                            format_func=lambda x: "🎯 Study Mode" if x == "study" else "📋 Show All",
                            horizontal=False,
                            key="view_mode_radio"
                        )
                    
                    with col2:
                        st.metric("Total Cards", len(flashcards))
                    
                    st.divider()
                    
                    # STUDY MODE - One card at a time
                    if st.session_state.view_mode == "study":
                        current_idx = st.session_state.current_card_index
                        
                        # Ensure index is valid
                        if current_idx >= len(flashcards):
                            st.session_state.current_card_index = 0
                            current_idx = 0
                        
                        card = flashcards[current_idx]
                        
                        if isinstance(card, dict):
                            question = card.get('question', 'N/A')
                            answer = card.get('answer', 'N/A')
                            
                            # Display flashcard
                            st.markdown(f"""
                            <div class="flashcard">
                                <div class="flashcard-question">
                                    💭 Question {current_idx + 1} of {len(flashcards)}
                                </div>
                                <div style="font-size: 1.8rem; margin: 1rem 0;">
                                    {question}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Show/Hide answer button
                            col1, col2, col3 = st.columns([1, 2, 1])
                            with col2:
                                if st.button("🔍 Reveal Answer", use_container_width=True, type="primary"):
                                    st.session_state.show_answer = not st.session_state.show_answer
                            
                            # Display answer if revealed
                            if st.session_state.show_answer:
                                st.markdown(f"""
                                <div class="flashcard-answer">
                                    <div style="font-size: 1.3rem; font-weight: bold; margin-bottom: 0.5rem;">
                                        ✅ Answer:
                                    </div>
                                    <div style="font-size: 1.5rem;">
                                        {answer}
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            # Navigation buttons
                            st.divider()
                            col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
                            
                            with col1:
                                if st.button("⏮️ First", use_container_width=True, disabled=current_idx == 0):
                                    st.session_state.current_card_index = 0
                                    st.session_state.show_answer = False
                                    st.rerun()
                            
                            with col2:
                                if st.button("◀️ Previous", use_container_width=True, disabled=current_idx == 0):
                                    st.session_state.current_card_index -= 1
                                    st.session_state.show_answer = False
                                    st.rerun()
                            
                            with col3:
                                st.markdown(f"<div style='text-align: center; padding: 0.5rem;'><b>{current_idx + 1} / {len(flashcards)}</b></div>", unsafe_allow_html=True)
                            
                            with col4:
                                if st.button("Next ▶️", use_container_width=True, disabled=current_idx >= len(flashcards) - 1):
                                    st.session_state.current_card_index += 1
                                    st.session_state.show_answer = False
                                    st.rerun()
                            
                            with col5:
                                if st.button("Last ⏭️", use_container_width=True, disabled=current_idx >= len(flashcards) - 1):
                                    st.session_state.current_card_index = len(flashcards) - 1
                                    st.session_state.show_answer = False
                                    st.rerun()
                        
                        else:
                            st.warning("Flashcard format not recognized. Please regenerate.")
                    
                    # SHOW MODE - All cards at once
                    else:
                        st.info("📋 Showing all flashcards - perfect for quick review!")
                        
                        # Display in grid (2 columns)
                        for idx in range(0, len(flashcards), 2):
                            cols = st.columns(2)
                            
                            for col_idx, col in enumerate(cols):
                                card_idx = idx + col_idx
                                if card_idx < len(flashcards):
                                    card = flashcards[card_idx]
                                    
                                    if isinstance(card, dict):
                                        question = card.get('question', 'N/A')
                                        answer = card.get('answer', 'N/A')
                                        
                                        with col:
                                            st.markdown(f"""
                                            <div class="flashcard-grid">
                                                <div style="font-weight: bold; color: #999; font-size: 0.9rem; margin-bottom: 0.5rem;">
                                                    Card {card_idx + 1}
                                                </div>
                                                <div class="flashcard-grid-question">
                                                    ❓ {question}
                                                </div>
                                                <div class="flashcard-grid-answer">
                                                    ✅ {answer}
                                                </div>
                                            </div>
                                            """, unsafe_allow_html=True)
                                    else:
                                        with col:
                                            st.markdown(f"""
                                            <div class="flashcard-grid">
                                                <div class="flashcard-grid-answer">
                                                    {str(card)}
                                                </div>
                                            </div>
                                            """, unsafe_allow_html=True)
                
                else:
                    # Display as text if not JSON
                    st.markdown(flashcards)
    else:
        st.error("Notebook not found!")
