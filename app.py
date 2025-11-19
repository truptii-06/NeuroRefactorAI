# main.py
import streamlit as st
import os
import sys

# Import core project modules
from src.core.parser import compute_metrics
from src.inference.validator import validate_suggestion
from src.ui.streamlit_ui import show_homepage_ui, show_results_ui, inject_custom_css
from src.reports.generator import generate_audit_report

# --- 1. STATE MANAGEMENT ---

if 'app_state' not in st.session_state:
    st.session_state.app_state = 'homepage'
if 'code_input' not in st.session_state:
    st.session_state.code_input = ''

def switch_to_homepage():
    st.session_state.app_state = 'homepage'
    st.session_state.code_input = ''

# --- 2. UI DISPLAY FUNCTIONS ---

def display_homepage():
    show_homepage_ui()

def display_refactor_tool():
    # Inject CSS to ensure consistent theme
    inject_custom_css()

    # Custom Tool Header - UPDATED COLORS FOR DARK THEME
    st.markdown("""
        <div style="text-align: center; margin-bottom: 40px; padding-top: 20px;">
            <h2 style="font-weight: 800; color: #ffffff; font-size: 2.5rem;">🚀 Refactor Workspace</h2>
            <p style="color: #9ca3af; font-size: 1.1rem;">Paste your Python code below to analyze complexity and auto-fix issues.</p>
        </div>
    """, unsafe_allow_html=True)

    # Back Button
    if st.button("← Back to Home"):
        switch_to_homepage()
        st.rerun()

    # Input Area
    input_container = st.container()
    with input_container:
        code_input = st.text_area(
            "Input Code",
            value=st.session_state.code_input,
            height=350,
            placeholder="def my_function():\n    # Paste your code here..."
        )

        col_c1, col_c2, col_c3 = st.columns([1, 2, 1])
        with col_c2:
            analyze_clicked = st.button("✨ Analyze & Refactor", use_container_width=True)

        if analyze_clicked:
            st.session_state.code_input = code_input
            if not code_input:
                st.warning("Please paste some code to get started!")
                return

            with st.spinner("🤖 AI is analyzing complexity and generating fixes..."):
                before_metrics = compute_metrics(code_input)

                # SIMULATED LOGIC
                simulated_edit = 'RENAME("tmp", "count")'
                after_code = code_input.replace("tmp", "count")

                if "tmp" in code_input or "if True:" in code_input:
                    if validate_suggestion(code_input, after_code, None):
                        after_metrics = compute_metrics(after_code)
                        st.toast("Refactoring successful!", icon="✅")

                        show_results_ui(
                            code_input,
                            after_code,
                            before_metrics,
                            after_metrics,
                            simulated_edit,
                            risk=0.05,
                            benefit={"complexity": 2.5, "lint": 1}
                        )

                        st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
                        col_rep1, col_rep2, col_rep3 = st.columns([1, 2, 1])
                        with col_rep2:
                            if st.button("📄 Download Audit PDF", key="btn_pdf"):
                                generate_audit_report(simulated_edit, before_metrics, after_metrics)
                                st.success("Audit report generated in /reports folder!")
                    else:
                        st.error("Validation failed: The suggested change broke functionality.")
                else:
                    st.info("No critical issues found. Try pasting code with a 'tmp' variable to see the demo.")

# --- 3. MAIN FLOW ---

def main():
    if st.session_state.app_state == 'homepage':
        display_homepage()
    elif st.session_state.app_state == 'refactor_tool':
        display_refactor_tool()

if __name__ == "__main__":
    st.set_page_config(
        page_title="NeuroRefactorAI",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    main()
