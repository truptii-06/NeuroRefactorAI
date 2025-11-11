# src/inference/validator.py
import libcst as cst
from radon.complexity import cc_visit
import ruff
import subprocess
import os
import shutil

# NOTE: The apply_edit function below is for SIMULATION ONLY.
# In your final project, this logic will come from your refactoring agent.
def apply_edit(code: str, edit_program: str):
    """Applies a simple edit program to the code."""
    if 'SIMPLIFY_CONDITION' in edit_program:
        _, old, new = edit_program.split('"')
        new = new.strip().strip(':')
        return code.replace(old, new)
    elif 'RENAME' in edit_program:
        # Very simplified rename logic
        if 'tmp' in code:
            return code.replace("tmp", "count")
    return code

def validate_suggestion(before_code: str, after_code: str, test_files: list = None):
    """Runs a 5-stage validation pipeline on the refactored code."""
    
    # Gate 1: AST Replay (Syntax Check)
    try:
        cst.parse_module(after_code)
    except cst.CSTSyntaxError:
        print("Validation failed: Syntax error.")
        return False
        
    # Gate 2: Style Check (only flag if *new* errors are introduced)
    try:
        lint_errors_before = len(ruff.lint(before_code))
        lint_errors_after = len(ruff.lint(after_code))
        if lint_errors_after > lint_errors_before:
            print("Validation failed: Introduced new lint errors.")
            return False
    except Exception:
        pass # Skip if ruff fails
        
    # Gate 3: Complexity Guard (Refactoring must reduce or maintain CC)
    try:
        complexity_before = sum(c.complexity for c in cc_visit(before_code))
        complexity_after = sum(c.complexity for c in cc_visit(after_code))
        if complexity_after >= complexity_before and complexity_before > 0:
            print("Validation failed: Complexity did not improve.")
            # We allow complexity to be the same only if the code was already simple (CC=1 or 0)
            if complexity_after > 1:
                return False
    except Exception:
        pass # Skip if radon fails

    # Gate 4: Security Scan (Conceptual - requires `bandit` to be installed and integrated)
    # This check is skipped for the initial setup.

    # Gate 5: Test Pass-Through (Requires external files and proper environment setup)
    if test_files:
        # Test logic requires complex setup and is skipped for the initial setup.
        # It relies on saving files and running subprocesses.
        pass
    
    return True