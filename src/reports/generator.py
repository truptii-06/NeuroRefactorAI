# src/reports/generator.py
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def generate_audit_report(edit_program, before_metrics, after_metrics):
    """Generates a PDF audit report."""
    filename = "audit_report.pdf"
    
    # Create the reports directory if it doesn't exist
    report_dir = "reports"
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
        
    c = canvas.Canvas(os.path.join(report_dir, filename), pagesize=letter)
    width, height = letter
    y_pos = height - 50

    c.drawString(50, y_pos, "AI Refactor Agent - Audit Report")
    y_pos -= 30
    c.drawString(50, y_pos, f"Suggested Change: {edit_program}")
    
    y_pos -= 40
    c.drawString(50, y_pos, "Metrics Before Refactoring:")
    y_pos -= 20
    c.drawString(50, y_pos, f"  - Complexity: {before_metrics.get('complexity', 'N/A')}")
    y_pos -= 20
    c.drawString(50, y_pos, f"  - Lint Errors: {before_metrics.get('lint_errors', 'N/A')}")

    y_pos -= 30
    c.drawString(50, y_pos, "Metrics After Refactoring:")
    y_pos -= 20
    c.drawString(50, y_pos, f"  - Complexity: {after_metrics.get('complexity', 'N/A')}")
    y_pos -= 20
    c.drawString(50, y_pos, f"  - Lint Errors: {after_metrics.get('lint_errors', 'N/A')}")
    
    y_pos -= 40
    c.drawString(50, y_pos, "Rollback Instructions:")
    y_pos -= 20
    c.drawString(50, y_pos, "1. Ensure your code is under version control (e.g., Git).")
    y_pos -= 20
    c.drawString(50, y_pos, "2. Run 'git revert <commit-hash>' to undo the changes.")
    
    c.save()
    print(f"PDF report saved to {os.path.join(report_dir, filename)}")