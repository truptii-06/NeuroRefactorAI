import streamlit as st
import difflib

def inject_custom_css():
    st.markdown("""
        <style>
        /* --- GLOBAL RESET & FONTS --- */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
            color: #e5e7eb; /* Light Gray text */
        }

        /* --- DARK THEME BACKGROUND --- */
        .stApp {
            background-color: #0e1117; /* Deep Dark Blue/Gray */
            background-image: radial-gradient(#1f2937 1px, transparent 1px);
            background-size: 24px 24px;
        }

        /* --- NAVBAR --- */
        .navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1.5rem 0;
            margin-bottom: 4rem;
            border-bottom: 1px solid #1f2937;
        }
        .nav-logo {
            font-size: 1.5rem;
            font-weight: 800;
            color: #ffffff;
            text-decoration: none;
            letter-spacing: -0.02em;
        }
        .nav-logo span { color: #3b82f6; } /* Brand Blue */

        .nav-links {
            display: flex;
            gap: 2rem;
            align-items: center;
            font-weight: 500;
            font-size: 0.95rem;
        }
        .nav-link {
            text-decoration: none;
            color: #9ca3af;
            transition: color 0.2s;
        }
        .nav-link:hover { color: #ffffff; }

        .nav-btn-login {
            background-color: #ffffff;
            color: #000000 !important;
            padding: 0.5rem 1.2rem;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
            font-size: 0.9rem;
        }

        /* --- HERO SECTION --- */
        .hero-section {
            text-align: center;
            padding: 3rem 1rem 5rem;
            max-width: 900px;
            margin: 0 auto;
        }
        .hero-title {
            font-size: 4rem;
            font-weight: 800;
            line-height: 1.1;
            color: #ffffff;
            margin-bottom: 1.5rem;
            letter-spacing: -0.03em;
        }
        .text-blue {
            color: #60a5fa; /* Lighter Blue for Dark Mode */
            background: linear-gradient(to right, #60a5fa, #3b82f6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .hero-sub {
            font-size: 1.25rem;
            color: #9ca3af;
            margin-bottom: 3rem;
            line-height: 1.6;
            max-width: 700px;
            margin-left: auto;
            margin-right: auto;
        }

        /* --- BUTTONS --- */
        div.stButton > button {
            width: 100%;
            border: none;
            padding: 0.8rem 2rem;
            font-weight: 600;
            border-radius: 100px;
            font-size: 1rem;
            transition: all 0.2s ease;
        }

        /* Primary Hero Button */
        div.stButton > button:first-child {
            background-color: #ffffff;
            color: #000000;
            box-shadow: 0 0 20px rgba(255,255,255,0.1);
        }
        div.stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 0 30px rgba(255,255,255,0.2);
        }

        /* Secondary/Blue Links as Buttons */
        .btn-blue-outline {
            display: inline-block;
            padding: 0.8rem 2rem;
            background-color: rgba(59, 130, 246, 0.1);
            color: #60a5fa;
            border: 1px solid #3b82f6;
            border-radius: 100px;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.2s;
            text-align: center;
            width: 100%;
        }
        .btn-blue-outline:hover {
            background-color: #3b82f6;
            color: white;
        }

        /* --- FEATURES SECTION --- */
        .feature-container {
            padding: 2rem 0;
        }
        .feature-title {
            font-size: 2.5rem;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 1.5rem;
            letter-spacing: -0.02em;
        }
        .check-list {
            list-style: none;
            padding: 0;
            margin-bottom: 2rem;
        }
        .check-item {
            display: flex;
            gap: 15px;
            margin-bottom: 1.2rem;
            color: #d1d5db;
            font-size: 1.1rem;
            align-items: start;
        }
        .check-icon {
            color: #10b981; /* Emerald-500 */
            background: rgba(16, 185, 129, 0.1);
            border-radius: 50%;
            width: 24px;
            height: 24px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.8rem;
            flex-shrink: 0;
        }

        /* --- CODE CARD (Glassmorphism) --- */
        .code-card-bg {
            background: linear-gradient(145deg, #1e293b 0%, #0f172a 100%);
            padding: 2rem;
            border-radius: 1.5rem;
            position: relative;
            border: 1px solid #334155;
            box-shadow: 0 20px 40px -10px rgba(0,0,0,0.5);
        }
        .code-window {
            background: #020617; /* Nearly black */
            border-radius: 10px;
            padding: 1.5rem;
            color: #e2e8f0;
            font-family: 'Courier New', monospace;
            font-size: 0.9rem;
            border: 1px solid #1e293b;
            margin-bottom: 1.5rem;
            position: relative;
        }
        .code-window.good { border-left: 4px solid #10b981; }
        .code-window.bad { border-left: 4px solid #ef4444; opacity: 0.7; }

        .badge {
            position: absolute;
            top: 10px;
            right: 10px;
            font-size: 0.75rem;
            font-weight: 700;
            padding: 4px 10px;
            border-radius: 12px;
            text-transform: uppercase;
        }
        .badge-good { background: rgba(16, 185, 129, 0.2); color: #10b981; }
        .badge-bad { background: rgba(239, 68, 68, 0.2); color: #ef4444; }

        /* --- COMIC BOX (CSS Drawing) --- */
        .comic-box {
            background: #ffffff;
            color: #000; /* Black text for the comic part */
            padding: 2rem;
            border-radius: 12px;
            font-family: 'Comic Sans MS', 'Chalkboard SE', sans-serif;
            border: 2px solid #e5e7eb;
            transform: rotate(-1deg);
        }
        .comic-title { font-weight: bold; border-bottom: 2px solid #000; padding-bottom: 10px; margin-bottom: 20px; font-size: 1.2rem; }
        .door {
            border: 2px solid #000;
            height: 120px;
            width: 80px;
            margin: 0 auto;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            position: relative;
        }
        .knob { width: 8px; height: 8px; background: #000; border-radius: 50%; position: absolute; right: 10px; top: 60px; }
        .wtf-label { font-size: 0.8rem; color: #ef4444; font-weight: bold; margin-top: 5px;}

        /* --- TESTIMONIALS --- */
        .testi-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem;
            margin-top: 4rem;
        }
        .testi-card {
            background: #111827;
            padding: 2rem;
            border-radius: 16px;
            border: 1px solid #1f2937;
        }
        .testi-text {
            font-size: 1rem;
            color: #d1d5db;
            margin-bottom: 1.5rem;
            line-height: 1.6;
        }
        .user-profile {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .avatar {
            width: 48px; height: 48px;
            border-radius: 50%;
            background-size: cover;
            border: 2px solid #374151;
        }

        /* --- FAQ --- */
        .faq-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 3rem;
            margin-top: 4rem;
        }
        .faq-item h3 { color: #fff; margin-bottom: 0.5rem; font-size: 1.1rem; }
        .faq-item p { color: #9ca3af; line-height: 1.6; font-size: 0.95rem; }

        </style>
    """, unsafe_allow_html=True)

def show_homepage_ui():
    inject_custom_css()

    # 1. NAVBAR
    st.markdown("""
        <div class="navbar">
            <a href="#" class="nav-logo">Neuro<span>RefactorAI</span></a>
            <div class="nav-links">
                <a href="#" class="nav-link">AI Code Roast</a>
                <a href="#" class="nav-link">Go Pro</a>
                <a href="#" class="nav-link">Exercises</a>
                <a href="#" class="nav-btn-login">Login</a>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 2. HERO SECTION
    st.markdown("""
        <div class="hero-section">
            <div class="hero-title">
                Become a 10x engineer, learn to <span class="text-blue">refactor</span> and write <span class="text-blue">clean code</span>
            </div>
            <div class="hero-sub">
                Solve real-world refactoring challenges and improve your skills.
                NeuroRefactorAI offers automated roasts to help you refactor real world code.
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Centered Hero Buttons
    c1, c2, c3, c4 = st.columns([2, 3, 3, 2])
    with c2:
        # Primary Action Button
        if st.button("Try our AI Code Roast 🔥", key="hero_start"):
            st.session_state.app_state = 'refactor_tool'
            st.rerun()
    with c3:
        # Secondary Action Link
        st.markdown('<a href="#" class="btn-blue-outline">Start Learning For Free</a>', unsafe_allow_html=True)

    st.markdown("<div style='text-align:center; margin-top:30px; color:#6b7280; font-size:0.9rem;'>Loved by 500+ Engineers ❤️</div>", unsafe_allow_html=True)

    st.markdown("<div style='height: 80px;'></div>", unsafe_allow_html=True)

    # 3. FEATURE SECTION 1: "Learn to write Clean Code"
    c1, c2 = st.columns([1, 1], gap="large")

    with c1:
        st.markdown("""
            <div class="feature-container">
                <div class="feature-title">Learn to write Clean Code</div>
                <p style="color:#9ca3af; margin-bottom:30px; line-height:1.7; font-size:1.1rem;">
                    Instead of sitting through hours of lectures, you'll be presented with problematic code and a concise explanation of what needs to be done.
                </p>
                <ul class="check-list">
                    <li class="check-item">
                        <span class="check-icon">✓</span>
                        <div>13+ Code Smell and Refactoring techniques to help you learn in real life world</div>
                    </li>
                    <li class="check-item">
                        <span class="check-icon">✓</span>
                        <div>Build in VS Code IDE to help you write code on the web</div>
                    </li>
                    <li class="check-item">
                        <span class="check-icon">✓</span>
                        <div>Don't like our answer? Generate better answer through AI.</div>
                    </li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

    with c2:
        # Visual Code Card Representation
        st.markdown("""
            <div class="code-card-bg">
                <div style="text-align:center; font-weight:800; color:white; margin-bottom:1.5rem; font-size:1.5rem; letter-spacing:2px;">CLEAN CODE 👍</div>

                <div class="code-window good">
                    <div class="badge badge-good">Optimized</div>
                    <span style="color:#c678dd">const</span> GRAVITY = 9.81;<br><br>
                    <span style="color:#c678dd">export function</span> <span style="color:#61afef">potentialEnergy</span>(mass, height) {<br>
                    &nbsp;&nbsp;<span style="color:#c678dd">return</span> mass * height * GRAVITY;<br>
                    }
                </div>

                <div class="code-window bad">
                    <div class="badge badge-bad">Smelly</div>
                    <span style="color:#c678dd">function</span> <span style="color:#61afef">calc</span>(m, h) {<br>
                    &nbsp;&nbsp;<span style="color:#c678dd">return</span> m * h * 9.81; <span style="color:#6b7280">// magic number</span><br>
                    }
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 80px;'></div>", unsafe_allow_html=True)

    # 4. FEATURE SECTION 2: "Why Clean Code" + Comic
    d1, d2 = st.columns([1, 1], gap="large")

    with d1:
        # Recreating the "WTFs/minute" comic using CSS
        st.markdown("""
            <div class="comic-box">
                <div class="comic-title">The only valid measurement of code quality: WTFs/minute</div>
                <div style="display:flex; justify-content:space-around; padding-top:20px;">
                    <div style="text-align:center;">
                        <div class="wtf-label" style="color:#10b981; margin-bottom:10px;">GOOD CODE</div>
                        <div class="door"><div class="knob"></div>Code<br>Review</div>
                        <p style="margin-top:10px; font-weight:bold;">2 WTFs/min</p>
                    </div>
                    <div style="text-align:center;">
                        <div class="wtf-label" style="margin-bottom:10px;">BAD CODE</div>
                        <div class="door" style="background:#fee2e2;"><div class="knob"></div>Code<br>Review</div>
                        <p style="margin-top:10px; font-weight:bold;">50 WTFs/min</p>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with d2:
        st.markdown("""
            <div class="feature-container">
                <div class="feature-title">Why Clean Code?</div>
                <p style="color:#9ca3af; margin-bottom:20px; font-size:1.1rem;">
                    Do you waste most your time trying to fix bugs caused by poorly written and unmaintainable code?
                </p>
                <ul class="check-list">
                    <li class="check-item"><span class="check-icon">✓</span> Improved code quality and maintainability resulting in reduced bugs.</li>
                    <li class="check-item"><span class="check-icon">✓</span> Reduced technical debt significantly.</li>
                    <li class="check-item"><span class="check-icon">✓</span> Enhanced collaboration with team members through readable code.</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

        # Action Buttons
        b1, b2 = st.columns([1, 2])
        with b1:
            st.markdown('<a href="#" class="btn-blue-outline">Go Pro</a>', unsafe_allow_html=True)
        with b2:
            st.button("Try out an exercise", key="btn_exercise")

    # 5. TESTIMONIALS
    st.markdown("<div style='height: 80px;'></div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center;'><h2 style='font-size:2.5rem; font-weight:800; color:#fff;'>Loved by developers worldwide.</h2></div>", unsafe_allow_html=True)

    st.markdown("""
        <div class="testi-grid">
            <div class="testi-card">
                <p class="testi-text">"this should have more attention! awesome edu tool for junior-middle devs."</p>
                <div class="user-profile">
                    <div class="avatar" style="background: #fcd34d;"></div>
                    <div><h4 style="margin:0; color:white;">Pavel Kaluhin</h4><span style="color:#6b7280; font-size:0.8rem;">Tech Lead @ Paralect</span></div>
                </div>
            </div>
            <div class="testi-card">
                <p class="testi-text">"Looks like an amazing tool! Going great Saad Pasta 💯"</p>
                <div class="user-profile">
                    <div class="avatar" style="background: #34d399;"></div>
                    <div><h4 style="margin:0; color:white;">Ali Khan</h4><span style="color:#6b7280; font-size:0.8rem;">Software Engineer @ SadaPay</span></div>
                </div>
            </div>
            <div class="testi-card">
                <p class="testi-text">"This can prove to be far more useful than LeetCode honestly, great initiative! 🚀"</p>
                <div class="user-profile">
                    <div class="avatar" style="background: #60a5fa;"></div>
                    <div><h4 style="margin:0; color:white;">Osama Mateen</h4><span style="color:#6b7280; font-size:0.8rem;">Software Engineer @ Abhi</span></div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 6. FAQ SECTION
    st.markdown("<div style='height: 80px;'></div>", unsafe_allow_html=True)
    st.markdown("<div style='margin-bottom:40px;'><h2 style='font-size:2.5rem; font-weight:800; color:#fff;'>Frequently asked questions</h2></div>", unsafe_allow_html=True)

    st.markdown("""
        <div class="faq-grid">
            <div class="faq-item">
                <h3>Why should I pay for this when I can learn Refactoring online?</h3>
                <p>RefactorNow approach is different. Instead of hours of lectures, you get hands-on problematic code and immediate feedback.</p>
            </div>
            <div class="faq-item">
                <h3>Will there be more exercises?</h3>
                <p>Probably Yes. We will keep adding new exercises for different code smells in the future.</p>
            </div>
            <div class="faq-item">
                <h3>What will I learn?</h3>
                <p>You will learn to identify code smells, refactor complex code into simpler structures, and understand software design.</p>
            </div>
            <div class="faq-item">
                <h3>I am Junior Dev can I take this course?</h3>
                <p>This is designed to introduce beginners to fundamental concepts. No prior experience beyond basic coding is required.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:100px;'></div>", unsafe_allow_html=True)


def show_results_ui(before_code, after_code, before_metrics, after_metrics, edit_program, risk, benefit):
    """
    Displays the analysis results with the same Dark Theme aesthetic.
    """
    inject_custom_css()

    st.markdown("## 💡 Refactoring Results")

    # Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Risk Score", f"{risk:.2f}", delta="Low Risk", delta_color="inverse")
    with col2:
        diff = before_metrics['complexity'] - after_metrics['complexity']
        st.metric("Complexity", f"{after_metrics['complexity']}", delta=f"-{diff} (Improved)", delta_color="normal")
    with col3:
        lint_diff = before_metrics['lint_errors'] - after_metrics['lint_errors']
        st.metric("Lint Errors", f"{after_metrics['lint_errors']}", delta=f"-{lint_diff} (Fixed)", delta_color="normal")

    st.markdown("---")

    # Code Comparison Tabs
    tab1, tab2 = st.tabs(["⚡ Unified Diff", "📝 Side-by-Side View"])

    with tab1:
        diff_lines = list(difflib.unified_diff(
            before_code.splitlines(),
            after_code.splitlines(),
            lineterm=''
        ))
        diff_output = '\n'.join(diff_lines)
        if diff_output:
            st.code(diff_output, language='diff')
        else:
            st.info("No textual changes detected.")

    with tab2:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Original Code**")
            st.code(before_code, language="python")
        with c2:
            st.markdown("**Refactored Code**")
            st.code(after_code, language="python")
