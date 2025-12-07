"""
Study Scheduler Page - Generate personalized study schedules
"""
import streamlit as st
import json
from utils.db import Database
from utils.helpers import load_prompt, call_gemini, parse_json_response
from utils.sidebar_utils import show_sidebar_on_all_pages

st.set_page_config(page_title="Study Scheduler", page_icon="📅", layout="wide")

# Show common sidebar on all pages
show_sidebar_on_all_pages()

db = Database()

st.title("📅 Study Scheduler")

if 'current_notebook' not in st.session_state:
    st.warning("⚠️ No notebook selected. Please upload a PDF from the home page.")
    if st.button("Go to Home"):
        st.switch_page("app.py")
else:
    notebook = db.get_notebook(st.session_state.current_notebook)
    
    if notebook:
        filename = notebook.get('filename', 'Untitled Notebook')
        st.header(f"📓 {filename}")
        
        st.markdown("""
        Create a personalized study schedule based on your target completion date.
        The schedule will break down your learning material into manageable daily tasks!
        """)
        
        # Check if schedule already exists
        existing_schedule = notebook.get('schedule')
        
        if existing_schedule:
            st.success("✅ You already have a study schedule!")
            
            if st.button("🔄 Generate New Schedule"):
                # Clear existing schedule
                db.update_notebook(st.session_state.current_notebook, {
                    'schedule': None,
                    'schedule_days': None
                })
                st.rerun()
        else:
            # Schedule creation form
            col1, col2 = st.columns([2, 1])
            
            with col1:
                days = st.number_input(
                    "How many days do you want to complete this in?",
                    min_value=1,
                    max_value=365,
                    value=7,
                    help="Enter the number of days for your study plan"
                )
            
            with col2:
                st.metric("Days", days)
            
            if st.button("📅 Generate Schedule", type="primary"):
                with st.spinner("Creating your personalized study schedule..."):
                    try:
                        # Get text content
                        text_content = notebook.get('text_content', '')
                        
                        # Load scheduler prompt
                        prompt_config = load_prompt('scheduler_prompt.json')
                        
                        # Generate schedule
                        response = call_gemini(prompt_config, text_content[:8000], days=days)
                        
                        # Parse JSON response
                        schedule = parse_json_response(response)
                        
                        # Save schedule to database
                        db.save_schedule(st.session_state.current_notebook, schedule, days)
                        
                        st.success("✅ Schedule created successfully!")
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"Error generating schedule: {str(e)}")
                        st.exception(e)
        
        # Display existing schedule
        if existing_schedule:
            st.divider()
            st.subheader("📋 Your Study Schedule")
            
            schedule_days = notebook.get('schedule_days', 0)
            st.info(f"📆 {schedule_days}-Day Study Plan")
            
            # Get progress
            progress_data = db.get_progress(st.session_state.current_notebook)
            completed_tasks = progress_data.get('completed_tasks', [])
            
            # Display schedule
            if isinstance(existing_schedule, list):
                for day_data in existing_schedule:
                    if isinstance(day_data, dict):
                        day = day_data.get('day', '?')
                        tasks = day_data.get('tasks', [])
                        
                        with st.expander(f"📅 Day {day}", expanded=False):
                            for idx, task in enumerate(tasks):
                                if isinstance(task, dict):
                                    task_id = f"{day}_{idx}"
                                    is_completed = task_id in completed_tasks
                                    
                                    col1, col2, col3 = st.columns([3, 1, 1])
                                    
                                    with col1:
                                        if is_completed:
                                            st.markdown(f"✅ ~~{task.get('description', 'Task')}~~")
                                        else:
                                            st.markdown(f"📌 {task.get('description', 'Task')}")
                                    
                                    with col2:
                                        st.markdown(f"**{task.get('points', 10)} pts**")
                                    
                                    with col3:
                                        if not is_completed:
                                            if st.button("✓", key=f"complete_{day}_{idx}"):
                                                db.mark_task_complete(
                                                    st.session_state.current_notebook,
                                                    day,
                                                    idx,
                                                    task.get('points', 10)
                                                )
                                                st.rerun()
                                else:
                                    st.markdown(f"- {task}")
            else:
                # Display as text if not JSON
                st.markdown(existing_schedule)
    else:
        st.error("Notebook not found!")
