🧠 NeuroRefactorAI - Professional AI Code Refactoring Tool
Show Image
Show Image
Show Image

An industry-grade, AI-powered code refactoring platform that helps developers write cleaner, more maintainable Python code using advanced AI technology powered by Claude.

✨ Features
🤖 AI-Powered Analysis
Intelligent Code Review: Deep analysis of code quality, complexity, and maintainability
Smart Refactoring: Automatic code improvements while preserving functionality
Multi-Aspect Analysis: Detects code smells, design pattern opportunities, and performance issues
📊 Comprehensive Metrics
Cyclomatic Complexity tracking
Maintainability Index calculation
Code quality ranking (A-F scale)
Risk assessment for each refactoring
🎯 Focus Areas
Naming Improvements: Better variable and function names
Complexity Reduction: Simplify nested conditions and loops
Performance Optimization: Identify and fix performance bottlenecks
Readability Enhancement: Make code more understandable
Best Practices: Enforce Python PEP 8 and industry standards
🔒 Safety Features
Syntax Validation: Ensures refactored code is syntactically correct
Risk Scoring: Quantifies the risk of each change
Confidence Metrics: AI confidence levels for each suggestion
Rollback Instructions: Clear guidance on reverting changes
📄 Professional Reporting
PDF audit reports with before/after metrics
Detailed change logs with explanations
Visual diff comparisons
Export capabilities for documentation
🚀 Quick Start
Prerequisites
bash
# Python 3.11 or higher
python --version

# pip package manager
pip --version
Installation
Clone the repository
bash
git clone https://github.com/yourusername/neurorefactorai.git
cd neurorefactorai
Create virtual environment
bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
Install dependencies
bash
pip install -r requirement.txt
Set up API Key
bash
# Get your API key from https://console.anthropic.com/
export ANTHROPIC_API_KEY='your-api-key-here'

# On Windows (PowerShell)
$env:ANTHROPIC_API_KEY='your-api-key-here'
Run the application
bash
streamlit run app.py
The application will open in your default browser at http://localhost:8501

📖 Usage Guide
Web Interface
Homepage: Introduction and feature overview
Refactor Tool: Main workspace for code analysis
Analysis Mode
python
# Example: Get suggestions without refactoring
1. Paste your code
2. Select "Analysis Only" mode
3. Click "Analyze Code"
4. Review suggestions sorted by priority
Refactoring Mode
python
# Example: Full AI-powered refactoring
1. Paste your code
2. Select "Full Refactor" mode
3. Optionally choose focus areas
4. Click "Refactor Code"
5. Review changes and metrics
6. Download report or use refactored code
Example Input
python
# Before Refactoring
def calc(data):
    tmp = 0
    for i in range(len(data)):
        if data[i] > 0:
            tmp = tmp + data[i]
    return tmp
Example Output
python
# After Refactoring
def calculate_positive_sum(numbers: list[float]) -> float:
    """
    Calculate the sum of all positive numbers in the list.
    
    Args:
        numbers: List of numeric values
        
    Returns:
        Sum of all positive numbers
    """
    return sum(number for number in numbers if number > 0)
Metrics Improvement
Complexity: 3 → 1 (66% reduction)
Maintainability: 45.2 → 78.5 (73% improvement)
Risk Score: 15% (Low)
Confidence: 95%
🏗️ Architecture
NeuroRefactorAI/
│
├── src/
│   ├── ai/
│   │   └── refactoring_agent.py    # Core AI refactoring engine
│   ├── core/
│   │   ├── parser.py                # Code parsing and metrics
│   │   └── validator.py             # Syntax and quality validation
│   ├── inference/
│   │   └── validator.py             # Multi-stage validation pipeline
│   ├── reports/
│   │   └── generator.py             # PDF report generation
│   └── ui/
│       └── streamlit_ui.py          # Web interface components
│
├── app.py                            # Main application entry point
├── requirement.txt                   # Python dependencies
└── README.md                         # This file
🔧 Configuration
Environment Variables
bash
# Required
ANTHROPIC_API_KEY=your-api-key-here

# Optional
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=localhost
Customization
Edit src/ai/refactoring_agent.py to customize:

AI model selection (default: claude-sonnet-4-20250514)
Analysis depth and focus
Metrics thresholds
Risk calculation parameters
📊 Metrics Explained
Cyclomatic Complexity
A (1-5): Simple, easy to test
B (6-10): Moderate complexity
C (11-20): High complexity
F (>20): Very high complexity, consider refactoring
Maintainability Index
0-25: Hard to maintain
26-50: Moderate maintainability
51-75: Good maintainability
76-100: Excellent maintainability
Risk Score
Low (<30%): Safe to apply
Medium (30-60%): Review carefully
High (>60%): Proceed with caution
🤝 Contributing
Contributions are welcome! Please follow these steps:

Fork the repository
Create a feature branch (git checkout -b feature/AmazingFeature)
Commit your changes (git commit -m 'Add some AmazingFeature')
Push to the branch (git push origin feature/AmazingFeature)
Open a Pull Request
Development Setup
bash
# Install development dependencies
pip install -r requirement.txt
pip install black isort pytest pylint

# Run tests
pytest tests/

# Format code
black src/
isort src/
🐛 Troubleshooting
Common Issues
Issue: ModuleNotFoundError: No module named 'anthropic'

bash
Solution: pip install anthropic
Issue: API key not configured

bash
Solution: Set ANTHROPIC_API_KEY environment variable
Issue: Streamlit won't start

bash
Solution: Check port 8501 is available
streamlit run app.py --server.port 8502
📝 License
This project is licensed under the MIT License - see the LICENSE file for details.

🙏 Acknowledgments
Claude AI by Anthropic for powering the refactoring engine
LibCST for Python code parsing
Radon for code metrics
Streamlit for the web framework
Open-source community for various tools and libraries
📞 Support
Issues: GitHub Issues
Email: support@neurorefactorai.com
Documentation: Full Docs
🗺️ Roadmap
 Support for more programming languages (JavaScript, Java, C++)
 Integration with GitHub/GitLab for automated PR reviews
 Team collaboration features
 Custom rule definitions
 IDE plugins (VS Code, PyCharm)
 Batch processing for multiple files
 Machine learning model for project-specific patterns
 Real-time collaboration features
📈 Performance
Typical refactoring times:

Small files (<100 lines): 2-5 seconds
Medium files (100-500 lines): 5-15 seconds
Large files (>500 lines): 15-30 seconds
🌟 Star History
If you find this project useful, please consider giving it a star! ⭐

Made with ❤️ for developers who care about code quality

Version 1.0.0 | Last Updated: November 2025

