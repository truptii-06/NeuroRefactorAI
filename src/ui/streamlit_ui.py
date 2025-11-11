# src/ui/streamlit_ui.py
import streamlit as st
import difflib

# Function to inject custom CSS for styling the UI
def inject_custom_css():
    st.markdown("""
        <style>
        .main {
            /* This targets the main content area */
            background-color: #f0ffef; /* Very light green/white for a clean look */
        }
        .stButton button {
            background-color: #28a745; /* Green button color */
            color: white;
            border-radius: 5px;
            font-size: 1.2rem;
            padding: 10px 20px;
        }
        .stButton button:hover {
            background-color: #1d9237; /* Darker green on hover */
        }
        /* Style the Title and Header to match the image theme */
        h1, h2, h3, h4 {
            color: #1d9237; 
        }
        </style>
        """, unsafe_allow_html=True)

# Function for the attractive, static homepage UI
def show_homepage_ui():
    inject_custom_css()
    
    # Use wide layout to replicate the side-by-side design
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.title("AI REFACTOR AGENT")
        st.header("Transform Your Python Code with Confidence")
        st.markdown(
            """
            Our AI-powered refactoring agent runs locally on your machine, 
            intelligently improving your Python code while guaranteeing 
            zero functionality breaks. Clean, maintainable code has never 
            been this effortless or secure.
            """
        )

        st.markdown("---")

        st.markdown("#### Key Features")
        st.markdown("✅ **Smart AI refactoring for Python**")
        st.markdown("✅ **100% local** - your code never leaves your machine")
        st.markdown("✅ **Zero-break guarantee** with rollback protection")


    with col2:
        # Display a sample code snippet to mimic the image's aesthetic
        st.subheader("Example Refactored")
        
        code_before = """
# before
def calc(x, y):
    return x + y
"""
        st.code(code_before, language="python")

        code_after = """
# AI Refactored
# after
def calculate_sum(x: int, y: int) -> int:
    \"\"\"Calculates the sum of two integers.\"\"\"
    return x + y
"""
        st.code(code_after, language="python")


# Function for the interactive UI after the button is clicked
def show_results_ui(before_code, after_code, before_metrics, after_metrics, edit_program, risk, benefit):
    inject_custom_css()
    
    st.markdown("---")
    st.subheader("💡 AI Refactoring Suggestion")

    # Display Metrics Dashboard
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Risk Score (AI Prediction)", value=f"{risk:.2f}", delta_color="inverse")
    with col2:
        st.metric(label="Complexity Reduction", value=f"{before_metrics['complexity'] - after_metrics['complexity']:.1f}", delta_color="normal")
    with col3:
        st.metric(label="Lint Errors Fixed", value=f"{before_metrics['lint_errors'] - after_metrics['lint_errors']:.1f}", delta_color="normal")

    with st.expander("Show AI-Generated Edit Program & Rationale"):
        st.code(f"EDIT: {edit_program}", language="text")
        st.write(f"Rationale: Predicted complexity reduction by {benefit.get('complexity', 0):.1f}.")


    # Show Code Diff and Metrics Tabs
    tab1, tab2 = st.tabs(["Code Diff", "Code View"])
    
    with tab1:
        st.subheader("Code Changes (Unified Diff)")
        # Generate the difference output
        diff_lines = list(difflib.unified_diff(
            before_code.splitlines(), 
            after_code.splitlines(), 
            lineterm=''
        ))
        diff_output = '\n'.join(diff_lines)
        st.code(diff_output, language='diff')

    with tab2:
        col_before, col_after = st.columns(2)
        with col_before:
            st.subheader("Before")
            st.code(before_code, language="python")
        with col_after:
            st.subheader("After (Refactored)")
            st.code(after_code, language="python")
            
    st.markdown("---")
    
    # Interaction buttons are handled in main.py to trigger report generation