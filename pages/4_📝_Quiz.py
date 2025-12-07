"""
Quiz Page - Interactive quiz generation (Placeholder)
"""
import streamlit as st
from utils.db import Database

st.set_page_config(page_title="Quiz", page_icon="📝", layout="wide")

db = Database()

st.title("📝 Interactive Quiz")

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
        The Interactive Quiz feature is currently under development. Soon you'll be able to:
        
        - 📊 Take multiple-choice quizzes based on your document
        - ⏱️ Set time limits for each question
        - 🎯 Get instant feedback on your answers
        - 📈 Track your quiz scores over time
        - 🏆 Earn bonus points for perfect scores
        
        Stay tuned for this exciting feature!
        """)
        
        # Placeholder quiz demo
        st.divider()
        st.subheader("Preview: Sample Quiz Format")
        
        with st.container():
            st.markdown("**Question 1:** What is the main topic of this document?")
            st.radio(
                "Select your answer:",
                ["Option A", "Option B", "Option C", "Option D"],
                key="demo_q1",
                disabled=True
            )
            
        with st.container():
            st.markdown("**Question 2:** Which of the following is a key concept?")
            st.radio(
                "Select your answer:",
                ["Option A", "Option B", "Option C", "Option D"],
                key="demo_q2",
                disabled=True
            )
        
        st.button("Submit Quiz", disabled=True, type="primary")
    else:
        st.error("Notebook not found!")
