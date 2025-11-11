# src/core/parser.py
import libcst as cst
from radon.complexity import cc_visit
import ruff
import json

def parse_code(code: str):
    """Parses code into a LibCST tree."""
    return cst.parse_module(code)

def compute_metrics(code: str):
    """Computes code quality metrics (Cyclomatic Complexity and Lint Errors)."""
    try:
        # Calculate Cyclomatic Complexity (CC)
        cc = cc_visit(code)
        # Check if cc is not empty before summing complexities
        complexity_score = sum(c.complexity for c in cc) if cc else 0
    except Exception:
        complexity_score = -1 # Handle parsing errors

    # Check linting violations using Ruff
    try:
        # ruff.lint() returns a list of violations, we just need the count
        lint_violations = ruff.lint(code)
        lint_score = len(lint_violations)
    except Exception:
        lint_score = -1

    return {"complexity": complexity_score, "lint_errors": lint_score}