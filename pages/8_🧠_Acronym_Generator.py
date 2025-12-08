"""
Memory Aid Generator Page - Generates various mnemonic devices like acronyms, songs, and phrases.
"""
import streamlit as st
from utils.db import Database
from utils.helpers import load_prompt, call_gemini
from utils.text_extraction import get_topic_text
from utils.sidebar_utils import show_sidebar_on_all_pages

st.set_page_config(page_title="Memory Generator", page_icon="🧠", layout="wide")

show_sidebar_on_all_pages()

db = Database()

# --- Configuration: All Available Generator Types and their corresponding prompt file names ---
GENERATOR_OPTIONS = {
    "Acronym/Initialism": "acronym_prompt.json",
    "Mnemonic Song/Rhyme": "song_prompt.json",
    "General Mnemonic Phrase": "phrase_prompt.json",
    "Mnemonic Story": "story_prompt.json",
}
# --- End Configuration ---

st.title("🧠 Memory Aid Generator")
st.markdown("Generate various memory devices: **Acronyms**, **Songs**, **Phrases**, or **Stories**!")

# --- Generator Selection ---
selected_generator = st.selectbox(
    "Choose the type of memory aid:",
    options=list(GENERATOR_OPTIONS.keys()),
    key="generator_type"
)
# --- End Generator Selection ---


if 'current_notebook' not in st.session_state:
    st.warning("⚠️ No notebook selected. Please upload a PDF from the home page.")
    if st.button("Go to Home"):
        st.switch_page("app.py")
else:
    notebook = db.get_notebook(st.session_state.current_notebook)
    
    if notebook:
        filename = notebook.get('filename', 'Untitled Notebook')
        st.header(f"📓 {filename}")
        
        # --- Unified Generation Function ---
        def run_generation(context_text, concept_text):
            """
            Core function that handles all generation types.
            It dynamically loads the correct prompt based on the selected generator.
            """
            generator_type = st.session_state.generator_type
            prompt_filename = GENERATOR_OPTIONS.get(generator_type)

            if not prompt_filename:
                st.error(f"Error: Unknown generator type '{generator_type}'.")
                return

            with st.spinner(f"Creating {generator_type} for '{concept_text}'..."):
                try:
                    # 1. Dynamically load the correct JSON prompt
                    prompt_config = load_prompt(prompt_filename) 

                    # 2. Call the single, unified model function
                    response = call_gemini(
                        prompt_config, 
                        context_text=context_text, # PDF content (or empty string)
                        target_text=concept_text   # Topic name or Custom text
                    ) 
                    
                    st.session_state.generator_result = response
                    st.session_state.generator_concept = concept_text
                    st.session_state.generator_type_used = generator_type
                    st.success(f"{generator_type} successfully generated for **{concept_text}**!")

                except Exception as e:
                    st.error(f"Error generating {generator_type}. Check prompt files or API connection.")
                    st.exception(e)
        # --- End Unified Generation Function ---
        
        
        topics = notebook.get('topics', [])
        tab1, tab2 = st.tabs(["📚 From Topics", "✍️ Custom Text"])
        
        # --- TAB 1: From Topics ---
        with tab1:
            if topics:
                selected_topic = st.selectbox(
                    "Select a topic:",
                    topics,
                    key="topic_concept"
                )
                
                if st.button(f"🧠 Generate {selected_generator} from Topic", type="primary"):
                    with st.spinner(f"🔍 Extracting content for '{selected_topic}'..."):
                        text_content = notebook.get('text_content', '')
                        # This line likely calls the embedding model
                        topic_specific_text = get_topic_text(text_content, selected_topic) 
                    
                    run_generation(topic_specific_text, selected_topic)
            else:
                st.warning("No topics found. Please check the Summary page or use custom text.")
        
        # --- TAB 2: Custom Text ---
        with tab2:
            custom_text = st.text_area(
                "Enter a list or concept:",
                height=150,
                placeholder="Example: Planets in our solar system\nMercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune",
                key="custom_text_input"
            )
            
            if st.button(f"🧠 Generate {selected_generator} from Custom Text", type="primary"):
                if custom_text.strip():
                    # context_text is "" for custom text, concept_text is the input
                    run_generation("", custom_text) 
                else:
                    st.warning("Please enter some text first!")
        
        
        # --- Display Result (Unified) ---
        if 'generator_result' in st.session_state:
            st.divider()
            st.subheader(f"🎯 Generated {st.session_state.generator_type_used}")
            
            st.info(f"**Concept:** {st.session_state.get('generator_concept', 'N/A')}")
            
            st.markdown(f"""
            <div style="padding: 1.5rem; border-radius: 10px; background-color: #f0f0f5; 
                         border-left: 5px solid #4A90E2;">
                {st.session_state.generator_result}
            </div>
            """, unsafe_allow_html=True)
            
            st.divider()
            st.subheader("💡 Memory Tips")
            st.markdown("""
            **How to use mnemonics effectively:**
            
            1. 🔄 **Review regularly** - Practice the memory aid daily for best retention.
            2. 🎨 **Visualize** - Create mental images for the concept.
            3. 📝 **Write it down** - Writing helps reinforce memory.
            """)
            
    else:
        st.error("Notebook not found!")