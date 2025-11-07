import libcst as cst
from libcst.tool import get_module_from_code
import os
from typing import List, Dict, Any
class RenameTransformer(cst.CSTTransformer):
"""
A CSTTransformer to rename a specific variable within a module.
This is a simplified example and does not handle scope correctly.
For production, you'd need proper scope analysis.
"""
def __init__(self, old_name: str, new_name: str):
self.old_name = old_name
self.new_name = new_name
def leave_Name(self, original_node: cst.Name, updated_node: cst.Name) ->
cst.Name:
"""
Called when leaving a Name node (e.g., variable names, function
calls).
"""
if original_node.value == self.old_name:
# Create a new Name node with the updated value
return updated_node.with_changes(value=self.new_name)
return updated_node
def leave_FunctionDef(self, original_node: cst.FunctionDef, updated_node:
cst.FunctionDef) -> cst.FunctionDef:
"""
Called when leaving a FunctionDef node.
This is an example of how to modify parts of a function definition,
e.g., renaming a parameter.
"""
# Example: if the function name itself needs to be renamed
if original_node.name.value == self.old_name:
return
updated_node.with_changes(name=updated_node.name.with_changes(value=self.new_
name))
return updated_node
class AutomatedRefactorer:
def __init__(self):
pass
def apply_refactoring(self, file_path: str, refactoring_suggestion:
Dict[str, Any]) -> Dict[str, Any]:
"""
Applies a refactoring suggestion to a given file.
This is a simplified dispatcher for demonstration.
"""
result = {
"success": False,
"message": "",
"original_code": "",
"refactored_code": ""
}
if not os.path.exists(file_path):
result["message"] = f"File not found: {file_path}"
return result
with open(file_path, "r", encoding="utf-8") as f:
original_code = f.read()
result["original_code"] = original_code
try:
# Parse the code into a CST
module = get_module_from_code(original_code)
refactoring_type = refactoring_suggestion.get("type")
# Dispatch based on refactoring type
if refactoring_type == "rename_variable":
old_name = refactoring_suggestion.get("old_name")
new_name = refactoring_suggestion.get("new_name")
if not old_name or not new_name:
result["message"] = "Missing old_name or new_name for
rename_variable refactoring."
return result
# Apply the transformation
transformed_module = module.visit(RenameTransformer(old_name,
new_name))
refactored_code = transformed_module.code
result["success"] = True
result["message"] = f"Successfully applied rename_variable:
{old_name} -> {new_name}"
# Add more refactoring types here (e.g., extract_method,
simplify_conditional)
# elif refactoring_type == "extract_method":
# # Implement ExtractMethodTransformer
# pass
else:
result["message"] = f"Unsupported refactoring type:
{refactoring_type}"
return result
result["refactored_code"] = refactored_code
except cst.ParserSyntaxError as e:
result["message"] = f"Syntax error in code: {e}"
except Exception as e:
result["message"] = f"Error applying refactoring: {e}"
return result
def save_refactored_code(self, file_path: str, refactored_code: str,
create_backup: bool = True) -> bool:
"""
Saves the refactored code to the file, optionally creating a backup.
"""
try:
if create_backup:
backup_path = f"{file_path}.bak"
os.rename(file_path, backup_path)
print(f"Created backup: {backup_path}")
with open(file_path, "w", encoding="utf-8") as f:
f.write(refactored_code)
print(f"Refactored code saved to: {file_path}")
return True
except Exception as e:
print(f"Error saving refactored code or creating backup: {e}")
return False
if __name__ == "__main__":
# --- Example Usage ---
# Create a dummy Python file for testing
dummy_code = """
def calculate_area(length, width):
# This function calculates the area of a rectangle
area = length * width
return area
class ShapeCalculator:
def __init__(self, factor):
self.factor = factor
def process_shape(self, value):
result = value * self.factor
return result
"""
original_file_path = "dummy_code_to_refactor.py"
with open(original_file_path, "w", encoding="utf-8") as f:
f.write(dummy_code)
refactorer = AutomatedRefactorer()
# Example 1: Rename a variable
print("\n--- Applying rename_variable refactoring ---")
rename_suggestion = {
"type": "rename_variable",
"old_name": "area",
"new_name": "rectangle_area"
}
refactoring_result = refactorer.apply_refactoring(original_file_path,
rename_suggestion)
if refactoring_result["success"]:
print("Refactoring successful. Proposed code:")
print(refactoring_result["refactored_code"])
# Optional: Developer override mode - ask for confirmation
confirm = input("Apply this refactoring to the file? (y/n):
").lower()
if confirm == 'y':
if refactorer.save_refactored_code(original_file_path,
refactoring_result["refactored_code"]):
print("File updated successfully.")
else:
print("Failed to update file.")
else:
print("Refactoring not applied to file.")
# Restore original file if not applied and backup was made
if os.path.exists(f"{original_file_path}.bak") and not
os.path.exists(original_file_path):
os.rename(f"{original_file_path}.bak", original_file_path)
print("Original file restored from backup.")
else:
print(f"Refactoring failed: {refactoring_result["message"]}")
# Clean up dummy files (restore original if it was renamed)
if os.path.exists(f"{original_file_path}.bak"):
if os.path.exists(original_file_path):
os.remove(original_file_path) # Remove the refactored version
os.rename(f"{original_file_path}.bak", original_file_path) # Restore
original
elif os.path.exists(original_file_path):
os.remove(original_file_path)
print("\n--- Demonstration Complete ---")