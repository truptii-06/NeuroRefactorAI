import libcst as cst
import json
import os
import subprocess
import sys
from typing import Dict, Any, List, Tuple
# Assuming preprocessor.py is in the same directory for AST parsing
from preprocessor import preprocess_code
class CodeValidator:
def __init__(self):
pass
def _compare_asts(self, original_code: str, refactored_code: str) ->
Dict[str, Any]:
"""
Compares the ASTs of two code snippets to identify structural
differences.
Returns a summary of changes (simplified for this example).
A more robust implementation would use a dedicated AST diffing
library.
"""
try:
original_tree = cst.parse_module(original_code)
refactored_tree = cst.parse_module(refactored_code)
# For a true AST comparison, you'd need a sophisticated diffing
algorithm.
# For simplicity, we'll just compare their string representations
of the AST.
# This is a very basic check and not robust for all refactorings.
original_ast_str = str(original_tree.body)
refactored_ast_str = str(refactored_tree.body)
is_structural_similar = (original_ast_str == refactored_ast_str)
# A more advanced comparison would involve traversing both trees
# and identifying added, removed, or modified nodes.
# For example, using a library like tree-sitter or custom
algorithms.
return {
"structural_similarity": is_structural_similar,
"message": "ASTs are identical" if is_structural_similar else
"ASTs differ"
}
except cst.ParserSyntaxError as e:
return {"structural_similarity": False, "message": f"Syntax error
in code: {e}"}
except Exception as e:
return {"structural_similarity": False, "message": f"Error
comparing ASTs: {e}"}
def _run_unit_tests(self, test_file_path: str, code_file_path: str) ->
Dict[str, Any]:
"""
Runs pytest on a specified test file and captures the results.
Temporarily modifies sys.path to ensure the code file can be imported
by tests.
"""
results = {
"tests_run": 0,
"tests_passed": 0,
"tests_failed": 0,
"test_output": "",
"success": False
}
if not os.path.exists(test_file_path):
results["test_output"] = f"Test file not found: {test_file_path}"
return results
# Add the directory of the code file to sys.path so tests can import
it
code_dir = os.path.dirname(os.path.abspath(code_file_path))
original_sys_path = list(sys.path) # Save original sys.path
if code_dir not in sys.path:
sys.path.insert(0, code_dir)
try:
# Run pytest programmatically
# -s to show print statements, --json-report to get structured
output
# --json-report-file to specify output file
json_report_path = "pytest_report.json"
command = [sys.executable, "-m", "pytest", test_file_path, "--
json-report", f"--json-report-file={json_report_path}"]
process = subprocess.run(command, capture_output=True, text=True,
check=False)
results["test_output"] = process.stdout + process.stderr
if os.path.exists(json_report_path):
with open(json_report_path, "r", encoding="utf-8") as f:
pytest_data = json.load(f)
summary = pytest_data.get("summary", {})
results["tests_run"] = summary.get("total", 0)
results["tests_passed"] = summary.get("passed", 0)
results["tests_failed"] = summary.get("failed", 0) +
summary.get("errors", 0)
results["success"] = (results["tests_failed"] == 0)
os.remove(json_report_path) # Clean up report file
else:
results["test_output"] += "\nPytest JSON report not
generated."
except Exception as e:
results["test_output"] = f"Error running tests: {e}"
finally:
# Restore original sys.path
sys.path = original_sys_path
return results
def validate_refactoring(self, original_code_path: str,
refactored_code_path: str, test_file_path: str = None) -> Dict[str, Any]:
"""
Performs a comprehensive validation of a refactoring.
"""
validation_results = {
"ast_comparison": {},
"unit_tests": {},
"overall_success": False,
"message": ""
}
# 1. AST Comparison
with open(original_code_path, "r", encoding="utf-8") as f:
original_code = f.read()
with open(refactored_code_path, "r", encoding="utf-8") as f:
refactored_code = f.read()
validation_results["ast_comparison"] =
self._compare_asts(original_code, refactored_code)
# 2. Unit Test Execution (if test_file_path is provided)
if test_file_path:
validation_results["unit_tests"] =
self._run_unit_tests(test_file_path, refactored_code_path)
# Determine overall success based on AST and tests
ast_ok =
validation_results["ast_comparison"].get("structural_similarity", False)
tests_ok = validation_results["unit_tests"].get("success", False)
validation_results["overall_success"] = ast_ok and tests_ok
if validation_results["overall_success"]:
validation_results["message"] = "Refactoring validated: ASTs
are similar and all tests passed."
elif not ast_ok:
validation_results["message"] = "Validation failed: ASTs
differ significantly or syntax error."
elif not tests_ok:
validation_results["message"] = "Validation failed: Unit
tests failed after refactoring."
else:
# If no tests provided, rely solely on AST comparison
validation_results["overall_success"] =
validation_results["ast_comparison"].get("structural_similarity", False)
if validation_results["overall_success"]:
validation_results["message"] = "Refactoring validated: ASTs
are similar (no unit tests provided)."
else:
validation_results["message"] = "Validation failed: ASTs
differ significantly or syntax error (no unit tests provided)."
return validation_results
if __name__ == "__main__":
# --- Example Usage ---
# Create dummy code files
original_dummy_code = """
def add(a, b):
return a + b
def subtract(a, b):
return a - b
"""
refactored_dummy_code_ok = """
def add(x, y):
return x + y # Renamed variables, functionally same
def subtract(a, b):
return a - b
"""
refactored_dummy_code_bad = """
def add(a, b):
return a * b # Functional change
def subtract(a, b):
return a - b
"""
with open("original_code.py", "w", encoding="utf-8") as f:
f.write(original_dummy_code)
with open("refactored_code_ok.py", "w", encoding="utf-8") as f:
f.write(refactored_dummy_code_ok)
with open("refactored_code_bad.py", "w", encoding="utf-8") as f:
f.write(refactored_dummy_code_bad)
# Create a dummy test file for original_code.py
dummy_test_code = """
import pytest
from original_code import add, subtract
def test_add():
assert add(1, 2) == 3
assert add(-1, 1) == 0
def test_subtract():
assert subtract(5, 2) == 3
assert subtract(10, 10) == 0
"""
with open("test_original_code.py", "w", encoding="utf-8") as f:
f.write(dummy_test_code)
validator = CodeValidator()
print("\n--- Validating refactored_code_ok.py (should pass) ---")
results_ok = validator.validate_refactoring(
"original_code.py",
"refactored_code_ok.py",
"test_original_code.py"
)
print(json.dumps(results_ok, indent=2))
print("\n--- Validating refactored_code_bad.py (should fail tests) ---")
results_bad = validator.validate_refactoring(
"original_code.py",
"refactored_code_bad.py",
"test_original_code.py"
)
print(json.dumps(results_bad, indent=2))
print("\n--- Validating refactored_code_ok.py (no tests provided) ---")
results_no_tests = validator.validate_refactoring(
"original_code.py",
"refactored_code_ok.py",
test_file_path=None
)
print(json.dumps(results_no_tests, indent=2))
# Clean up dummy files
os.remove("original_code.py")
os.remove("refactored_code_ok.py")
os.remove("refactored_code_bad.py")
os.remove("test_original_code.py")