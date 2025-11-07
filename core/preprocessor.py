import libcst as cst
import json
import os
class CodeMetadataExtractor(cst.CSTVisitor):
"""
A CSTVisitor to extract key metadata from Python source code.
"""
def __init__(self):
self.metadata = {
"imports": [],
"functions": [],
"classes": [],
"comments": [],
"lines_of_code": 0,
"indentation_style": "", # To be determined from first indented
line
"file_path": ""
}
self._indent_counts = {}
def visit_Module(self, node: cst.Module) -> None:
self.metadata["lines_of_code"] = len(node.code.splitlines())
# Basic attempt to determine indentation style
for line in node.code.splitlines():
if line.strip() and (line.startswith(' ') or
line.startswith('\t')):
indent = len(line) - len(line.lstrip())
self._indent_counts[indent] = self._indent_counts.get(indent,
0) + 1
if self._indent_counts:
# Most common indentation
most_common_indent = max(self._indent_counts,
key=self._indent_counts.get)
self.metadata["indentation_style"] = f"{most_common_indent}
spaces" if most_common_indent > 0 and most_common_indent % 2 == 0 else "tabs"
if '\t' in node.code else "mixed/unknown"
def visit_Import(self, node: cst.Import) -> None:
for import_alias in node.names:
self.metadata["imports"].append({
"module": import_alias.name.value,
"alias": import_alias.asname.name.value if
import_alias.asname else None,
"line": node.start_pos.line
})
def visit_ImportFrom(self, node: cst.ImportFrom) -> None:
module_name = node.module.value if node.module else ""
for import_alias in node.names:
self.metadata["imports"].append({
"module": module_name,
"name": import_alias.name.value,
"alias": import_alias.asname.name.value if
import_alias.asname else None,
"line": node.start_pos.line
})
def visit_FunctionDef(self, node: cst.FunctionDef) -> None:
# Extract signature details
params = []
for param in node.params.params:
param_info = {"name": param.name.value}
if param.annotation:
param_info["annotation"] =
cst.helpers.get_full_name_for_node(param.annotation)
if param.default:
param_info["default"] =
cst.helpers.get_full_name_for_node(param.default)
params.append(param_info)
returns_annotation = cst.helpers.get_full_name_for_node(node.returns)
if node.returns else None
self.metadata["functions"].append({
"name": node.name.value,
"signature": f"({', '.join([p['name'] for p in params])})", #
Simplified signature
"parameters": params,
"returns_annotation": returns_annotation,
"start_line": node.start_pos.line,
"end_line": node.end_pos.line,
"docstring": node.get_docstring() # Extract docstring
})
def visit_ClassDef(self, node: cst.ClassDef) -> None:
bases = []
for base in node.bases:
bases.append(cst.helpers.get_full_name_for_node(base.value))
self.metadata["classes"].append({
"name": node.name.value,
"bases": bases,
"start_line": node.start_pos.line,
"end_line": node.end_pos.line,
"docstring": node.get_docstring() # Extract docstring
})
def visit_Comment(self, node: cst.Comment) -> None:
self.metadata["comments"].append({
"value": node.value,
"line": node.start_pos.line
})
def preprocess_code(file_path: str) -> dict:
"""
Parses a Python file and extracts structured metadata.
"""
if not os.path.exists(file_path):
raise FileNotFoundError(f"File not found: {file_path}")
with open(file_path, "r", encoding="utf-8") as f:
source_code = f.read()
try:
tree = cst.parse_module(source_code)
extractor = CodeMetadataExtractor()
tree.visit(extractor)
extractor.metadata["file_path"] = os.path.abspath(file_path)
return extractor.metadata
except cst.ParserSyntaxError as e:
print(f"Error parsing {file_path}: {e}")
return {"error": str(e), "file_path": os.path.abspath(file_path)}
if __name__ == "__main__":
# Example Usage:
# Create a dummy Python file for testing
dummy_code = """
import os
from collections import defaultdict as dd
# This is a global comment
def calculate_sum(a: int, b: int = 10) -> int:
"""Calculates the sum of two numbers."""
# Inline comment inside function
result = a + b
return result
class MyClass(object):
"""A simple example class."""
def __init__(self, name):
self.name = name
def greet(self):
return f"Hello, {self.name}!"
if __name__ == "__main__":
total = calculate_sum(5)
print(f"Total: {total}")
"""
with open("dummy_code.py", "w", encoding="utf-8") as f:
f.write(dummy_code)
print("Processing dummy_code.py...")
metadata = preprocess_code("dummy_code.py")
print(json.dumps(metadata, indent=2))
# Clean up dummy file
os.remove("dummy_code.py")