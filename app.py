# app.py - Enhanced Industry-Level Version
import streamlit as st
import os
import sys
import difflib
from typing import Optional

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import modules
from src.ui.streamlit_ui import inject_custom_css, show_homepage_ui
from src.reports.generator import generate_audit_report

# Try to import AI agent (gracefully handle if API key not set)
try:
    from src.ai.refactoring_agent import AIRefactoringAgent, RefactoringResult
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False

# --- Configuration ---
st.set_page_config(
    page_title="NeuroRefactorAI - Professional Code Refactoring",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- State Management ---
if 'app_state' not in st.session_state:
    st.session_state.app_state = 'homepage'
if 'code_input' not in st.session_state:
    st.session_state.code_input = ''
if 'refactoring_result' not in st.session_state:
    st.session_state.refactoring_result = None
if 'api_key' not in st.session_state:
    st.session_state.api_key = os.environ.get('ANTHROPIC_API_KEY', '')

def switch_to_homepage():
    st.session_state.app_state = 'homepage'
    st.session_state.code_input = ''
    st.session_state.refactoring_result = None

def get_ai_agent() -> Optional['AIRefactoringAgent']:
    """Get AI agent instance with API key"""
    if not st.session_state.api_key:
        return None
    try:
        return AIRefactoringAgent(api_key=st.session_state.api_key)
    except Exception as e:
        st.error(f"Failed to initialize AI agent: {e}")
        return None

# --- UI Components ---

def show_api_key_setup():
    """Show API key configuration if not set"""
    with st.expander("⚙️ API Configuration", expanded=not st.session_state.api_key):
        st.markdown("""
        ### Anthropic API Key Required

        This tool uses Claude AI for intelligent code refactoring. You need an API key:

        1. Get your key from: [console.anthropic.com](https://console.anthropic.com/)
        2. Enter it below (it will be stored in your session only)
        """)

        api_key_input = st.text_input(
            "Enter your Anthropic API Key:",
            type="password",
            value=st.session_state.api_key,
            help="Your API key is only stored in this session and never saved"
        )

        if st.button("Save API Key"):
            st.session_state.api_key = api_key_input
            os.environ['ANTHROPIC_API_KEY'] = api_key_input
            st.success("✅ API Key saved for this session!")
            st.rerun()

def display_refactor_tool():
    """Main refactoring interface"""
    inject_custom_css()

    # Header
    st.markdown("""
        <div style="text-align: center; margin-bottom: 40px; padding-top: 20px;">
            <h2 style="font-weight: 800; color: #ffffff; font-size: 2.5rem;">🚀 AI-Powered Refactoring Workspace</h2>
            <p style="color: #9ca3af; font-size: 1.1rem;">Paste your Python code below for intelligent analysis and refactoring</p>
        </div>
    """, unsafe_allow_html=True)

    # Navigation
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("← Back to Home"):
            switch_to_homepage()
            st.rerun()

    # API Key Setup
    show_api_key_setup()

    # Main Interface
    if not st.session_state.api_key:
        st.warning("⚠️ Please configure your Anthropic API key above to use AI refactoring")
        return

    # Code Input Section
    st.markdown("### 📝 Your Code")
    code_input = st.text_area(
        "Python Code",
        value=st.session_state.code_input,
        height=400,
        placeholder="""def calculate_total(items):
    total = 0
    for i in range(len(items)):
        if items[i] > 0:
            total = total + items[i]
    return total
""",
        label_visibility="collapsed"
    )

    # Refactoring Options
    col1, col2 = st.columns([2, 1])
    with col1:
        focus_areas = st.multiselect(
            "Focus Areas (Optional)",
            ["Naming", "Complexity", "Performance", "Readability", "Best Practices"],
            help="Select specific areas to focus on, or leave empty for general refactoring"
        )

    with col2:
        mode = st.radio(
            "Mode",
            ["Full Refactor", "Analysis Only"],
            horizontal=True,
            help="Choose whether to get suggestions only or full refactored code"
        )

    # Action Buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if mode == "Analysis Only":
            analyze_btn = st.button("🔍 Analyze Code", use_container_width=True, type="primary")
        else:
            analyze_btn = st.button("✨ Refactor Code", use_container_width=True, type="primary")

    # Process Code
    if analyze_btn and code_input.strip():
        st.session_state.code_input = code_input

        agent = get_ai_agent()
        if not agent:
            st.error("Failed to initialize AI agent. Please check your API key.")
            return

        with st.spinner("🤖 AI is analyzing your code..."):
            if mode == "Analysis Only":
                # Analysis mode
                suggestions = agent.suggest_improvements(code_input, max_suggestions=10)

                if suggestions:
                    st.success(f"✅ Found {len(suggestions)} improvement opportunities!")

                    st.markdown("### 💡 Suggested Improvements")

                    for i, suggestion in enumerate(suggestions, 1):
                        severity = suggestion.get('severity', 'low')
                        severity_color = {
                            'high': '#ef4444',
                            'medium': '#f59e0b',
                            'low': '#10b981'
                        }.get(severity, '#6b7280')

                        with st.expander(
                            f"**{i}. {suggestion.get('type', 'Issue').replace('_', ' ').title()}** "
                            f"[{severity.upper()}]",
                            expanded=(i <= 3)
                        ):
                            st.markdown(f"""
                            **Severity:** <span style="color:{severity_color}; font-weight:bold;">{severity.upper()}</span>

                            **Issue:** {suggestion.get('description', 'No description')}

                            **Suggestion:** {suggestion.get('suggestion', 'No suggestion')}

                            **Location:** Lines {suggestion.get('line_range', [0, 0])[0]}-{suggestion.get('line_range', [0, 0])[1]}
                            """, unsafe_allow_html=True)
                else:
                    st.info("✅ No major issues found! Your code looks good.")

            else:
                # Full refactoring mode
                result = agent.refactor_code(
                    code_input,
                    focus_areas=focus_areas if focus_areas else None
                )

                st.session_state.refactoring_result = result

                if result.success:
                    st.success("✅ Refactoring completed successfully!")

                    # Display results
                    display_refactoring_results(result)
                else:
                    st.error(f"❌ Refactoring failed: {result.explanation}")

    elif analyze_btn:
        st.warning("Please enter some code to analyze")

def display_refactoring_results(result: RefactoringResult):
    """Display refactoring results in a beautiful format"""

    # Metrics Overview
    st.markdown("### 📊 Quality Metrics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        complexity_diff = result.metrics_before['cyclomatic_complexity'] - result.metrics_after['cyclomatic_complexity']
        st.metric(
            "Cyclomatic Complexity",
            result.metrics_after['cyclomatic_complexity'],
            delta=f"{-complexity_diff}" if complexity_diff != 0 else "No change",
            delta_color="inverse"
        )

    with col2:
        mi_diff = result.metrics_after['maintainability_index'] - result.metrics_before['maintainability_index']
        st.metric(
            "Maintainability Index",
            f"{result.metrics_after['maintainability_index']:.1f}",
            delta=f"{mi_diff:+.1f}" if mi_diff != 0 else "No change",
            delta_color="normal"
        )

    with col3:
        st.metric(
            "Risk Score",
            f"{result.risk_score:.1f}%",
            delta="Low" if result.risk_score < 30 else "Medium" if result.risk_score < 60 else "High",
            delta_color="inverse"
        )

    with col4:
        st.metric(
            "AI Confidence",
            f"{result.confidence * 100:.0f}%",
            delta="High" if result.confidence > 0.8 else "Medium",
            delta_color="normal"
        )

    # Explanation
    st.markdown("### 💭 What Changed")
    st.info(result.explanation)

    # Detailed Changes
    if result.changes:
        with st.expander("📋 Detailed Changes", expanded=True):
            for i, change in enumerate(result.changes, 1):
                st.markdown(f"""
                **{i}. {change.get('type', 'Change').replace('_', ' ').title()}**

                {change.get('description', 'No description')}

                *Reason:* {change.get('reason', 'No reason provided')}
                """)
                if i < len(result.changes):
                    st.divider()

    # Code Comparison
    st.markdown("### 📝 Code Comparison")

    tab1, tab2, tab3 = st.tabs(["📊 Unified Diff", "⚖️ Side by Side", "📋 Refactored Code"])

    with tab1:
        diff_lines = list(difflib.unified_diff(
            result.original_code.splitlines(keepends=True),
            result.refactored_code.splitlines(keepends=True),
            lineterm=''
        ))
        if diff_lines:
            diff_text = ''.join(diff_lines)
            st.code(diff_text, language='diff')
        else:
            st.info("No changes detected")

    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Original Code**")
            st.code(result.original_code, language='python', line_numbers=True)
        with col2:
            st.markdown("**Refactored Code**")
            st.code(result.refactored_code, language='python', line_numbers=True)

    with tab3:
        st.code(result.refactored_code, language='python', line_numbers=True)
        if st.button("📋 Copy to Clipboard"):
            st.code(result.refactored_code, language='python')
            st.success("✅ Code ready to copy!")

    # Action Buttons
    st.markdown("---")
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

    with col1:
        if st.button("📄 Generate Report", use_container_width=True):
            try:
                generate_audit_report(
                    "AI Refactoring",
                    result.metrics_before,
                    result.metrics_after
                )
                st.success("✅ Report generated in /reports folder!")
            except Exception as e:
                st.error(f"Report generation failed: {e}")

    with col2:
        if st.button("🔄 Refactor Again", use_container_width=True):
            st.session_state.code_input = result.refactored_code
            st.session_state.refactoring_result = None
            st.rerun()

    with col3:
        if st.button("💾 Use Refactored Code", use_container_width=True):
            st.session_state.code_input = result.refactored_code
            st.success("✅ Refactored code loaded into editor!")
            st.rerun()

    with col4:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.code_input = ''
            st.session_state.refactoring_result = None
            st.rerun()

# --- Main Application Flow ---

def main():
    if st.session_state.app_state == 'homepage':
        show_homepage_ui()

        # Override the homepage button to set state
        if st.session_state.get('_homepage_cta_clicked'):
            st.session_state.app_state = 'refactor_tool'
            st.rerun()

    elif st.session_state.app_state == 'refactor_tool':
        display_refactor_tool()

# Run the app
if __name__ == "__main__":
    # Check for button click from homepage (using session state hack)
    if 'hero_start' in st.session_state and st.session_state.hero_start:
        st.session_state.app_state = 'refactor_tool'
        st.session_state.hero_start = False

    main()
