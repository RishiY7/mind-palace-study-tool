"""
Acronym Generator Page - Generate mnemonic devices
"""
import streamlit as st
from utils.db import Database
from utils.helpers import load_prompt, call_gemini

st.set_page_config(page_title="Acronym Generator", page_icon="🧠", layout="wide")

db = Database()

st.title("🧠 Acronym Generator")

if 'current_notebook' not in st.session_state:
    st.warning("⚠️ No notebook selected. Please upload a PDF from the home page.")
    if st.button("Go to Home"):
        st.switch_page("app.py")
else:
    notebook = db.get_notebook(st.session_state.current_notebook)
    
    if notebook:
        st.header(f"📓 {notebook['filename']}")
        
        st.markdown("""
        Generate memorable acronyms and mnemonic devices to help you remember key concepts!
        
        Select a topic or enter custom text to create powerful memory aids.
        """)
        
        # Topic selection
        topics = notebook.get('topics', [])
        
        tab1, tab2 = st.tabs(["📚 From Topics", "✍️ Custom Text"])
        
        with tab1:
            if topics:
                selected_topic = st.selectbox(
                    "Select a topic:",
                    topics,
                    key="topic_acronym"
                )
                
                if st.button("🧠 Generate Acronym from Topic", type="primary"):
                    with st.spinner(f"Creating mnemonic for '{selected_topic}'..."):
                        try:
                            # Get relevant text
                            text_content = notebook.get('text_content', '')
                            
                            # Load acronym prompt
                            prompt_config = load_prompt('acronym_prompt.json')
                            
                            # Generate acronym
                            response = call_gemini(prompt_config, text_content[:8000], text=selected_topic)
                            
                            # Store in session state
                            st.session_state.acronym_result = response
                            st.session_state.acronym_topic = selected_topic
                            
                        except Exception as e:
                            st.error(f"Error generating acronym: {str(e)}")
                            st.exception(e)
            else:
                st.warning("No topics found. Please check the Summary page or use custom text.")
        
        with tab2:
            custom_text = st.text_area(
                "Enter a list or concept:",
                height=150,
                placeholder="Example: Planets in our solar system\nMercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune",
                help="Enter the concept or list you want to create a mnemonic for"
            )
            
            if st.button("🧠 Generate Acronym from Custom Text", type="primary"):
                if custom_text.strip():
                    with st.spinner("Creating your mnemonic..."):
                        try:
                            # Load acronym prompt
                            prompt_config = load_prompt('acronym_prompt.json')
                            
                            # Generate acronym
                            response = call_gemini(prompt_config, "", text=custom_text)
                            
                            # Store in session state
                            st.session_state.acronym_result = response
                            st.session_state.acronym_topic = "Custom Text"
                            
                        except Exception as e:
                            st.error(f"Error generating acronym: {str(e)}")
                            st.exception(e)
                else:
                    st.warning("Please enter some text first!")
        
        # Display result
        if 'acronym_result' in st.session_state:
            st.divider()
            st.subheader(f"🎯 Mnemonic Device")
            
            st.info(f"**Topic:** {st.session_state.get('acronym_topic', 'N/A')}")
            
            # Display the acronym in a nice box
            st.markdown(f"""
            <div style="padding: 1.5rem; border-radius: 10px; background-color: #e8f4f8; 
                        border-left: 5px solid #4A90E2;">
                {st.session_state.acronym_result}
            </div>
            """, unsafe_allow_html=True)
            
            # Tips section
            st.divider()
            st.subheader("💡 Memory Tips")
            st.markdown("""
            **How to use mnemonics effectively:**
            
            1. 🔄 **Review regularly** - Practice the acronym daily for best retention
            2. 🎨 **Visualize** - Create mental images for each letter
            3. 📝 **Write it down** - Writing helps reinforce memory
            4. 🗣️ **Say it aloud** - Verbal repetition strengthens recall
            5. 🎭 **Make it personal** - Adapt the mnemonic to your own experiences
            
            The more you engage with the mnemonic, the stronger your memory will become!
            """)
    else:
        st.error("Notebook not found!")
