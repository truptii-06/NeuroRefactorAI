import json
import os
import difflib
from typing import Dict, Any, List
class ReportGenerator:
def __init__(self):
pass
def _generate_code_diff(self, original_code: str, refactored_code: str,
lang: str = "python") -> str:
"""
Generates a side-by-side diff of two code snippets in Markdown
format.
"""
diff_lines = difflib.unified_diff(
original_code.splitlines(keepends=True),
refactored_code.splitlines(keepends=True),
fromfile="> Original Code",
tofile="> Refactored Code",
lineterm=
)
# Filter out the '---' and '+++' lines that difflib adds
filtered_diff = [line for line in diff_lines if not
line.startswith("--- ") and not line.startswith("+++ ") and not
line.startswith("@@ ")]
# Add syntax highlighting for the diff
return f"```diff\n{''.join(filtered_diff)}```\n"
def generate_report(self,
original_file_path: str,
refactored_file_path: str,
suggestions: List[Dict[str, Any]],
validation_results: Dict[str, Any],
report_output_path: str = "refactoring_report.md") ->
str:
"""
Generates a comprehensive Markdown report for the refactoring
session.
"""
report_content = []
# --- Report Header ---
report_content.append(f"# AI Code Refactoring Report\n")
report_content.append(f"**Date**:
{os.path.basename(original_file_path)}\n")
report_content.append(f"**Original File**: `{original_file_path}`\n")
report_content.append(f"**Refactored File**:
`{refactored_file_path}`\n\n")
# --- Overall Summary ---
report_content.append("## 📊 Overall Summary\n")
report_content.append(f"- **Total Refactorings Suggested**:
{len(suggestions)}\n")
report_content.append(f"- **Validation Status**:
{validation_results.get("message", "N/A")}\n")
report_content.append(f"- **Overall Success**: {'✅' if
validation_results.get('overall_success', False) else '❌'}\n\n")
# --- Refactoring Suggestions Details ---
report_content.append("## 💡 Refactoring Details\n")
if not suggestions:
report_content.append("No specific refactoring suggestions were
provided.\n\n")
else:
for i, suggestion in enumerate(suggestions):
report_content.append(f"### {i+1}. {suggestion.get('type',
'Unknown Refactoring')}\n")
report_content.append(f"- **Location**: Line(s)
{suggestion.get('start_line', 'N/A')}-{suggestion.get('end_line', 'N/A')}\n")
report_content.append(f"- **Reason**:
{suggestion.get('reason', 'No reason provided.')}\n")
report_content.append(f"- **Expected Impact**:
{suggestion.get('impact', 'Improved code quality.')}\n\n")
# --- Code Changes (Diff) ---
report_content.append("## 📝 Code Changes\n")
try:
with open(original_file_path, "r", encoding="utf-8") as f:
original_code = f.read()
with open(refactored_file_path, "r", encoding="utf-8") as f:
refactored_code = f.read()
report_content.append(self._generate_code_diff(original_code,
refactored_code))
except FileNotFoundError:
report_content.append("Could not generate diff: one or both code
files not found.\n")
except Exception as e:
report_content.append(f"Error generating diff: {e}\n")
report_content.append("\n")
# --- Validation Results ---
report_content.append("## ✅ Validation Results\n")
report_content.append(f"### AST Comparison\n")
ast_comp = validation_results.get("ast_comparison", {})
report_content.append(f"- **Structural Similarity**:
{ast_comp.get('structural_similarity', 'N/A')}\n")
report_content.append(f"- **Message**: {ast_comp.get('message',
'N/A')}\n\n")
report_content.append(f"### Unit Test Results\n")
unit_tests = validation_results.get("unit_tests", {})
if unit_tests:
report_content.append(f"- **Tests Run**:
{unit_tests.get('tests_run', 'N/A')}\n")
report_content.append(f"- **Tests Passed**:
{unit_tests.get('tests_passed', 'N/A')}\n")
report_content.append(f"- **Tests Failed**:
{unit_tests.get('tests_failed', 'N/A')}\n")
report_content.append(f"- **Success**: {'✅' if
unit_tests.get('success', False) else '❌'}\n")
if unit_tests.get('test_output'):
report_content.append(f"\n```\n{unit_tests['test_output']}\n```\n")
else:
report_content.append("No unit tests were executed or results not
available.\n")
report_content.append("\n")
# --- Final Recommendations ---
report_content.append("## 🚀 Next Steps & Recommendations\n")
if validation_results.get('overall_success', False):
report_content.append("The refactoring appears successful and
validated. Consider reviewing the changes and committing them to your version
control system.\n")
else:
report_content.append("The refactoring encountered issues during
validation. Please review the details above, manually inspect the code, and
address any failures before proceeding.\n")
report_content.append("\n")
full_report_content = "".join(report_content)
with open(report_output_path, "w", encoding="utf-8") as f:
f.write(full_report_content)
print(f"Refactoring report generated at: {report_output_path}")
return report_output_path
if __name__ == "__main__":
# --- Example Usage ---
# Create dummy code files
original_code_content = """
def old_function_name(a, b):
# This is an old function
result = a + b
return result
"""
refactored_code_content = """
def new_function_name(x, y):
# This is a new and improved function
sum_val = x + y
return sum_val
"""
original_file = "example_original.py"
refactored_file = "example_refactored.py"
with open(original_file, "w", encoding="utf-8") as f:
f.write(original_code_content)
with open(refactored_file, "w", encoding="utf-8") as f:
f.write(refactored_code_content)
# Dummy AI Suggestions (from Step 3)
dummy_suggestions = [
{
"type": "Rename Function",
"start_line": 1,
"end_line": 4,
"reason": "Function name 'old_function_name' was not descriptive.
Renamed to 'new_function_name' for clarity.",
"impact": "Improved readability and maintainability."
},
{
"type": "Rename Variable",
"start_line": 3,
"end_line": 3,
"reason": "Variable 'result' was too generic. Renamed to
'sum_val' for better context.",
"impact": "Enhanced code clarity."
}
]
# Dummy Validation Results (from Step 4)
dummy_validation_results = {
"ast_comparison": {
"structural_similarity": False, # ASTs will differ due to renames
"message": "ASTs differ due to function and variable renames, but
logic is preserved."
},
"unit_tests": {
"tests_run": 2,
"tests_passed": 2,
"tests_failed": 0,
"test_output": "============================= test session starts
==============================\nplatform linux -- Python 3.x.x, pytest-x.x.x,
pluggy-x.x.x\nrootdir: /path/to/project\n\nPASSED
[100%]\n============================== 2 passed in x.xs
==============================\n",
"success": True
},
"overall_success": True,
"message": "Refactoring validated: ASTs differ but all tests passed."
}
generator = ReportGenerator()
report_path = generator.generate_report(
original_file,
refactored_file,
dummy_suggestions,
dummy_validation_results,
"refactoring_session_report.md"
)
print(f"Report saved to {report_path}")
# Clean up dummy files
os.remove(original_file)
os.remove(refactored_file)