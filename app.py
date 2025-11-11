# main.py
import streamlit as st
import os
import sys

# Import core project modules
# NOTE: Ensure these functions are correctly defined and exported in their respective files.
from src.core.parser import compute_metrics
from src.inference.validator import validate_suggestion
from src.ui.streamlit_ui import show_homepage_ui, show_results_ui 
from src.reports.generator import generate_audit_report

# --- 1. STATE MANAGEMENT ---

# Initialize session state variables to control the view
if 'app_state' not in st.session_state:
    st.session_state.app_state = 'homepage'
if 'code_input' not in st.session_state:
    st.session_state.code_input = ''

def switch_to_tool():
    """Callback function to switch to the interactive tool view."""
    st.session_state.app_state = 'refactor_tool'

def switch_to_homepage():
    """Callback function to return to the homepage, clearing state."""
    st.session_state.app_state = 'homepage'
    st.session_state.code_input = ''


# --- 2. UI DISPLAY FUNCTIONS ---

def display_homepage():
    """Renders the attractive, static homepage UI."""
    # show_homepage_ui() renders the attractive static content from the image.
    show_homepage_ui() 
    
    # Add the transition button logic here, triggering the state change
    st.markdown("---")
    st.button("Start Refactoring Now", on_click=switch_to_tool)


def display_refactor_tool():
    """The interactive UI for pasting code and showing results."""
    st.title("🚀 AI REFACTOR AGENT")
    
    # Button to go back to the homepage
    st.button("↩️ Back to Homepage", on_click=switch_to_homepage)

    # Use a container for the input area
    input_container = st.container()

    with input_container:
        code_input = st.text_area("Paste your Python code here:", value=st.session_state.code_input, height=400)
        
        if st.button("Analyze & Refactor"):
            st.session_state.code_input = code_input # Save input
            if not code_input:
                st.warning("Please paste some code to get started!")
                return

            with st.spinner("Analyzing code..."):
                # --- CORE ANALYSIS AND SIMULATION ---
                before_metrics = compute_metrics(code_input)
                
                # SIMULATED AI GENERATION (REPLACE THIS LOGIC WITH YOUR TRAINED MODEL)
                simulated_edit = 'RENAME("tmp", "count")'
                after_code = code_input.replace("tmp", "count")

                if "tmp" in code_input or "if True:" in code_input: # Simulating the AI finding a refactoring
                    
                    # 4. Validation Pipeline Check
                    if validate_suggestion(code_input, after_code, None):
                        after_metrics = compute_metrics(after_code)
                        st.success("Refactoring suggestion found and validated! ✨")
                        
                        # 5. Display results using the dedicated UI function
                        show_results_ui(code_input, after_code, before_metrics, after_metrics, simulated_edit, 0.05, {"complexity": 2.5, "lint": 1})
                        
                        # 6. Audit Report Generation
                        if st.button("Generate Audit Report"):
                            generate_audit_report(simulated_edit, before_metrics, after_metrics)
                            st.success("Audit report generated in /reports folder!")
                            
                    else:
                        st.error("Validation failed for the suggested change.")
                else:
                    st.info("No refactoring suggestions found (Try code with 'tmp' variable or 'if True:').")


# --- 3. MAIN APPLICATION FLOW ---

def main():
    if st.session_state.app_state == 'homepage':
        display_homepage()
    elif st.session_state.app_state == 'refactor_tool':
        display_refactor_tool()


if __name__ == "__main__":
    main()