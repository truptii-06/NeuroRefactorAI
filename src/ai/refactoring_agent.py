# src/ai/refactoring_agent.py
import anthropic
import json
import os
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import libcst as cst
from radon.complexity import cc_visit
from radon.metrics import mi_visit

@dataclass
class RefactoringResult:
    """Result of a refactoring operation"""
    success: bool
    original_code: str
    refactored_code: str
    changes: List[Dict[str, Any]]
    explanation: str
    metrics_before: Dict[str, Any]
    metrics_after: Dict[str, Any]
    risk_score: float
    confidence: float

class AIRefactoringAgent:
    """
    AI-powered code refactoring agent using Claude API.
    Analyzes code and suggests intelligent refactorings.
    """

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the AI agent with Anthropic API"""
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")

        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model = "claude-sonnet-4-20250514"

    def _compute_metrics(self, code: str) -> Dict[str, Any]:
        """Compute code quality metrics"""
        metrics = {
            "cyclomatic_complexity": 0,
            "maintainability_index": 0.0,
            "lines_of_code": len(code.splitlines()),
            "complexity_rank": "A"
        }

        try:
            cc_results = cc_visit(code)
            if cc_results:
                metrics["cyclomatic_complexity"] = sum(b.complexity for b in cc_results)
                max_complexity = max(b.complexity for b in cc_results)

                # Rank complexity
                if max_complexity <= 5:
                    metrics["complexity_rank"] = "A"
                elif max_complexity <= 10:
                    metrics["complexity_rank"] = "B"
                elif max_complexity <= 20:
                    metrics["complexity_rank"] = "C"
                else:
                    metrics["complexity_rank"] = "F"

            mi_results = mi_visit(code, multi=True)
            if mi_results:
                metrics["maintainability_index"] = round(mi_results, 2)

        except Exception as e:
            print(f"Metrics computation error: {e}")

        return metrics

    def _validate_syntax(self, code: str) -> bool:
        """Validate Python syntax using LibCST"""
        try:
            cst.parse_module(code)
            return True
        except Exception:
            return False

    def _calculate_risk_score(self, original: str, refactored: str) -> float:
        """Calculate risk score based on code changes"""
        try:
            original_lines = set(original.splitlines())
            refactored_lines = set(refactored.splitlines())

            added = len(refactored_lines - original_lines)
            removed = len(original_lines - refactored_lines)
            total_lines = len(original_lines)

            if total_lines == 0:
                return 0.0

            # Risk increases with percentage of changed lines
            change_ratio = (added + removed) / (2 * total_lines)
            risk = min(change_ratio * 100, 100.0)

            return round(risk, 2)

        except Exception:
            return 50.0  # Medium risk if calculation fails

    def analyze_code(self, code: str) -> Dict[str, Any]:
        """
        Analyze code and identify refactoring opportunities using AI
        """
        system_prompt = """You are an expert Python code reviewer and refactoring specialist.
Your task is to analyze Python code and identify specific refactoring opportunities.

Analyze the code for:
1. Code smells (long methods, complex conditions, magic numbers, poor naming)
2. Design pattern opportunities
3. Performance improvements
4. Readability issues
5. Best practices violations

Return a JSON object with this structure:
{
    "issues": [
        {
            "type": "code_smell_type",
            "severity": "high|medium|low",
            "line_range": [start, end],
            "description": "What's wrong",
            "suggestion": "How to fix it"
        }
    ],
    "overall_quality": "poor|fair|good|excellent",
    "priority_fixes": ["list of most important issues"]
}"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                system=system_prompt,
                messages=[{
                    "role": "user",
                    "content": f"Analyze this Python code and identify refactoring opportunities:\n\n```python\n{code}\n```"
                }]
            )

            # Extract JSON from response
            content = response.content[0].text

            # Try to extract JSON if wrapped in markdown
            if "```json" in content:
                json_start = content.find("```json") + 7
                json_end = content.find("```", json_start)
                content = content[json_start:json_end].strip()
            elif "```" in content:
                json_start = content.find("```") + 3
                json_end = content.find("```", json_start)
                content = content[json_start:json_end].strip()

            analysis = json.loads(content)
            return analysis

        except Exception as e:
            print(f"Analysis error: {e}")
            return {
                "issues": [],
                "overall_quality": "unknown",
                "priority_fixes": []
            }

    def refactor_code(self, code: str, focus_areas: Optional[List[str]] = None) -> RefactoringResult:
        """
        Perform AI-powered refactoring on the provided code

        Args:
            code: Source code to refactor
            focus_areas: Optional list of specific areas to focus on

        Returns:
            RefactoringResult with original and refactored code
        """
        # First, analyze the code
        analysis = self.analyze_code(code)
        metrics_before = self._compute_metrics(code)

        # Build refactoring prompt
        focus_instruction = ""
        if focus_areas:
            focus_instruction = f"\nFocus specifically on: {', '.join(focus_areas)}"

        system_prompt = """You are an expert Python refactoring assistant.
Your task is to refactor Python code to improve quality while preserving functionality.

Rules:
1. Preserve all functionality - behavior must remain identical
2. Improve readability and maintainability
3. Follow PEP 8 and Python best practices
4. Add helpful comments for complex logic
5. Use descriptive variable and function names
6. Reduce complexity where possible
7. Remove code smells

Return a JSON object:
{
    "refactored_code": "the improved code",
    "changes": [
        {
            "type": "change_type",
            "description": "what was changed",
            "reason": "why it was changed"
        }
    ],
    "explanation": "overall summary of improvements",
    "confidence": 0.95
}"""

        user_prompt = f"""Refactor this Python code:

```python
{code}
```

Issues identified:
{json.dumps(analysis.get('issues', []), indent=2)}
{focus_instruction}

Provide the refactored code that fixes these issues."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=8000,
                system=system_prompt,
                messages=[{
                    "role": "user",
                    "content": user_prompt
                }]
            )

            # Parse response
            content = response.content[0].text

            # Extract JSON
            if "```json" in content:
                json_start = content.find("```json") + 7
                json_end = content.find("```", json_start)
                content = content[json_start:json_end].strip()
            elif "```" in content:
                json_start = content.find("```") + 3
                json_end = content.find("```", json_start)
                content = content[json_start:json_end].strip()

            result = json.loads(content)
            refactored_code = result.get("refactored_code", code)

            # Validate syntax
            if not self._validate_syntax(refactored_code):
                raise ValueError("Refactored code has syntax errors")

            # Compute metrics for refactored code
            metrics_after = self._compute_metrics(refactored_code)

            # Calculate risk
            risk_score = self._calculate_risk_score(code, refactored_code)

            return RefactoringResult(
                success=True,
                original_code=code,
                refactored_code=refactored_code,
                changes=result.get("changes", []),
                explanation=result.get("explanation", "Code refactored successfully"),
                metrics_before=metrics_before,
                metrics_after=metrics_after,
                risk_score=risk_score,
                confidence=result.get("confidence", 0.85)
            )

        except Exception as e:
            print(f"Refactoring error: {e}")
            return RefactoringResult(
                success=False,
                original_code=code,
                refactored_code=code,
                changes=[],
                explanation=f"Refactoring failed: {str(e)}",
                metrics_before=metrics_before,
                metrics_after=metrics_before,
                risk_score=0.0,
                confidence=0.0
            )

    def suggest_improvements(self, code: str, max_suggestions: int = 5) -> List[Dict[str, Any]]:
        """
        Get specific improvement suggestions without full refactoring
        """
        analysis = self.analyze_code(code)
        issues = analysis.get("issues", [])

        # Sort by severity
        severity_order = {"high": 0, "medium": 1, "low": 2}
        sorted_issues = sorted(
            issues,
            key=lambda x: severity_order.get(x.get("severity", "low"), 3)
        )

        return sorted_issues[:max_suggestions]

    def batch_refactor(self, code_snippets: List[str]) -> List[RefactoringResult]:
        """
        Refactor multiple code snippets
        """
        results = []
        for code in code_snippets:
            result = self.refactor_code(code)
            results.append(result)

        return results


# Example usage and testing
if __name__ == "__main__":
    # Test code with issues
    test_code = """
def calc(x, y, z):
    tmp = 0
    if x > 0:
        if y > 0:
            if z > 0:
                tmp = x + y + z
            else:
                tmp = x + y
        else:
            tmp = x
    return tmp

def process(data):
    result = []
    for i in range(len(data)):
        if data[i] > 10:
            result.append(data[i] * 2)
    return result
"""

    print("=" * 60)
    print("AI Refactoring Agent - Test Run")
    print("=" * 60)

    # Note: Requires ANTHROPIC_API_KEY environment variable
    try:
        agent = AIRefactoringAgent()

        print("\n1. Analyzing code...")
        analysis = agent.analyze_code(test_code)
        print(f"Quality: {analysis.get('overall_quality')}")
        print(f"Issues found: {len(analysis.get('issues', []))}")

        print("\n2. Getting improvement suggestions...")
        suggestions = agent.suggest_improvements(test_code)
        for i, suggestion in enumerate(suggestions, 1):
            print(f"\n   {i}. [{suggestion.get('severity')}] {suggestion.get('type')}")
            print(f"      {suggestion.get('description')}")

        print("\n3. Performing full refactoring...")
        result = agent.refactor_code(test_code)

        if result.success:
            print(f"\n✓ Refactoring successful!")
            print(f"  Confidence: {result.confidence * 100:.1f}%")
            print(f"  Risk Score: {result.risk_score:.1f}%")
            print(f"\n  Changes made: {len(result.changes)}")
            for change in result.changes[:3]:
                print(f"    - {change.get('type')}: {change.get('description')}")

            print(f"\n  Metrics Comparison:")
            print(f"    Complexity: {result.metrics_before['cyclomatic_complexity']} → {result.metrics_after['cyclomatic_complexity']}")
            print(f"    Maintainability: {result.metrics_before['maintainability_index']:.1f} → {result.metrics_after['maintainability_index']:.1f}")
        else:
            print(f"\n✗ Refactoring failed: {result.explanation}")

    except ValueError as e:
        print(f"\n⚠ Configuration Error: {e}")
        print("\nTo use this agent, set your Anthropic API key:")
        print("  export ANTHROPIC_API_KEY='your-api-key-here'")

    except Exception as e:
        print(f"\n✗ Error: {e}")
