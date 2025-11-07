import json
import os
from typing import Dict, Any, List
# For code metrics
from radon.complexity import cc_rank, cc_visit
from radon.metrics import mi_visit
# For code embeddings
from transformers import AutoTokenizer, AutoModel
import torch
# Assuming preprocessor.py is in the same directory
from preprocessor import preprocess_code
class CodeFeatureExtractor:
def __init__(self, model_name: str = "microsoft/codebert-base"):
"""
Initializes the feature extractor with a pre-trained CodeBERT model.
"""
self.tokenizer = AutoTokenizer.from_pretrained(model_name)
self.model = AutoModel.from_pretrained(model_name)
self.device = torch.device("cuda" if torch.cuda.is_available() else
"cpu")
self.model.to(self.device)
self.model.eval() # Set model to evaluation mode
def _get_code_metrics(self, code_snippet: str) -> Dict[str, Any]:
"""
Calculates cyclomatic complexity and maintainability index for a code
snippet.
"""
metrics = {
"cyclomatic_complexity": 0,
"cyclomatic_complexity_rank": "A",
"maintainability_index": 0.0,
"maintainability_index_rank": "A"
}
try:
# Cyclomatic Complexity
cc_results = cc_visit(code_snippet)
if cc_results:
# Sum CC for all blocks (functions, classes, methods)
metrics["cyclomatic_complexity"] = sum(b.complexity for b in
cc_results)
# Get rank for the highest complexity block, or overall if
only one
metrics["cyclomatic_complexity_rank"] =
cc_rank(max(b.complexity for b in cc_results) if cc_results else 0)
# Maintainability Index
mi_results = mi_visit(code_snippet)
if mi_results:
metrics["maintainability_index"] = mi_results[0] # MI is a
single value
metrics["maintainability_index_rank"] = mi_results[1] # MI
rank
except Exception as e:
print(f"Error calculating metrics: {e}")
# Return default values on error
return metrics
def _get_code_embedding(self, code_snippet: str) -> List[float]:
"""
Generates a CodeBERT embedding for a given code snippet.
"""
if not code_snippet.strip():
return [] # Return empty list for empty snippets
try:
# Tokenize and encode the input
inputs = self.tokenizer(code_snippet, return_tensors="pt",
truncation=True, max_length=512)
inputs = {k: v.to(self.device) for k, v in inputs.items()}
with torch.no_grad():
outputs = self.model(**inputs)
# Get the last hidden state and take the mean of the token
embeddings
# This is a common way to get a fixed-size embedding for a
sequence
embedding =
outputs.last_hidden_state.mean(dim=1).squeeze().cpu().numpy().tolist()
return embedding
except Exception as e:
print(f"Error generating embedding: {e}")
return []
def extract_features(self, file_path: str) -> Dict[str, Any]:
"""
Extracts features from a Python file, including metadata, metrics,
and embeddings.
"""
# Step 1: Get structured metadata from the preprocessor
metadata = preprocess_code(file_path)
if "error" in metadata:
return metadata # Return error if preprocessing failed
# Read raw code for metrics and embeddings
with open(file_path, "r", encoding="utf-8") as f:
raw_code = f.read()
# Add file-level metrics and embedding
file_metrics = self._get_code_metrics(raw_code)
metadata["file_metrics"] = file_metrics
metadata["file_embedding"] = self._get_code_embedding(raw_code)
# Add metrics and embeddings for functions and classes
for func in metadata.get("functions", []):
# Extract the function's code snippet
func_snippet = "\n".join(raw_code.splitlines()
[func["start_line"]-1 : func["end_line"]])
func["metrics"] = self._get_code_metrics(func_snippet)
func["embedding"] = self._get_code_embedding(func_snippet)
for cls in metadata.get("classes", []):
# Extract the class's code snippet
cls_snippet = "\n".join(raw_code.splitlines()[cls["start_line"]-1
: cls["end_line"]])
cls["metrics"] = self._get_code_metrics(cls_snippet)
cls["embedding"] = self._get_code_embedding(cls_snippet)
return metadata
if __name__ == "__main__":
# Example Usage:
# Create a dummy Python file for testing
dummy_code = """
import os
def complex_function(x, y):
if x > 0:
for i in range(y):
if i % 2 == 0:
print(f"Even: {i}")
else:
print(f"Odd: {i}")
return x * y
class MyUtility:
def __init__(self, value):
self.value = value
def process(self, data):
# This is a simple process method
if data > self.value:
return data * 2
return data / 2
# Main execution
if __name__ == "__main__":
result = complex_function(5, 3)
print(f"Result: {result}")
util = MyUtility(10)
print(util.process(15))
"""
with open("dummy_code_for_features.py", "w", encoding="utf-8") as f:
f.write(dummy_code)
print("Initializing CodeFeatureExtractor (this may download model
weights)...")
extractor = CodeFeatureExtractor()
print("Extracting features from dummy_code_for_features.py...")
features = extractor.extract_features("dummy_code_for_features.py")
print(json.dumps(features, indent=2))
# Clean up dummy file
os.remove("dummy_code_for_features.py")