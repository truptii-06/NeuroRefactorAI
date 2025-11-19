# tests/test_ai_agent.py
"""
Comprehensive test suite for AI Refactoring Agent
Run with: pytest tests/ -v --cov=src
"""

import pytest
import os
from unittest.mock import Mock, patch, MagicMock
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.ai.refactoring_agent import AIRefactoringAgent, RefactoringResult


class TestAIRefactoringAgent:
    """Test suite for AI Refactoring Agent"""

    @pytest.fixture
    def mock_api_key(self):
        """Provide mock API key"""
        return "sk-ant-test-key-123"

    @pytest.fixture
    def agent(self, mock_api_key):
        """Create agent instance with mock API key"""
        with patch.dict(os.environ, {'ANTHROPIC_API_KEY': mock_api_key}):
            return AIRefactoringAgent(api_key=mock_api_key)

    @pytest.fixture
    def simple_code(self):
        """Simple test code"""
        return """
def add(a, b):
    return a + b
"""

    @pytest.fixture
    def complex_code(self):
        """Complex test code with issues"""
        return """
def calc(x, y, z):
    tmp = 0
    if x > 0:
        if y > 0:
            if z > 0:
                tmp = x + y + z
    return tmp
"""

    # --- Initialization Tests ---

    def test_agent_initialization(self, mock_api_key):
        """Test agent initializes correctly"""
        agent = AIRefactoringAgent(api_key=mock_api_key)
        assert agent.api_key == mock_api_key
        assert agent.model == "claude-sonnet-4-20250514"

    def test_agent_initialization_no_key(self):
        """Test agent fails without API key"""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="ANTHROPIC_API_KEY"):
                AIRefactoringAgent()

    # --- Metrics Tests ---

    def test_compute_metrics_simple(self, agent, simple_code):
        """Test metrics computation on simple code"""
        metrics = agent._compute_metrics(simple_code)

        assert 'cyclomatic_complexity' in metrics
        assert 'maintainability_index' in metrics
        assert 'lines_of_code' in metrics
        assert 'complexity_rank' in metrics

        assert metrics['cyclomatic_complexity'] >= 0
        assert metrics['lines_of_code'] > 0

    def test_compute_metrics_complex(self, agent, complex_code):
        """Test metrics show higher complexity for nested code"""
        metrics = agent._compute_metrics(complex_code)

        assert metrics['cyclomatic_complexity'] > 1
        assert metrics['complexity_rank'] in ['A', 'B', 'C', 'F']

    def test_complexity_ranking(self, agent):
        """Test complexity ranking system"""
        # Low complexity -> A rank
        simple = "def f(): return 1"
        assert agent._compute_metrics(simple)['complexity_rank'] == 'A'

        # High complexity -> worse rank
        complex_nested = """
def f(a, b, c, d, e):
    if a:
        if b:
            if c:
                if d:
                    if e:
                        return 1
    return 0
"""
        rank = agent._compute_metrics(complex_nested)['complexity_rank']
        assert rank in ['B', 'C', 'F']

    # --- Validation Tests ---

    def test_validate_syntax_valid(self, agent, simple_code):
        """Test syntax validation with valid code"""
        assert agent._validate_syntax(simple_code) is True

    def test_validate_syntax_invalid(self, agent):
        """Test syntax validation with invalid code"""
        invalid_code = "def broken(\n    return"
        assert agent._validate_syntax(invalid_code) is False

    # --- Risk Score Tests ---

    def test_risk_score_no_change(self, agent, simple_code):
        """Test risk score when code unchanged"""
        risk = agent._calculate_risk_score(simple_code, simple_code)
        assert risk == 0.0

    def test_risk_score_minor_change(self, agent):
        """Test risk score for minor changes"""
        original = "def add(a, b):\n    return a + b"
        modified = "def add(x, y):\n    return x + y"

        risk = agent._calculate_risk_score(original, modified)
        assert 0 < risk < 100

    def test_risk_score_major_change(self, agent):
        """Test risk score for major changes"""
        original = "def f(): return 1"
        modified = """
def complex_function(a, b, c):
    result = 0
    for i in range(a):
        result += b * c
    return result
"""
        risk = agent._calculate_risk_score(original, modified)
        assert risk > 50  # Major change = high risk

    # --- Analysis Tests ---

    @patch('anthropic.Anthropic')
    def test_analyze_code_success(self, mock_anthropic, agent, complex_code):
        """Test successful code analysis"""
        # Mock API response
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text='''{
            "issues": [
                {
                    "type": "poor_naming",
                    "severity": "high",
                    "line_range": [1, 8],
                    "description": "Variable 'tmp' is not descriptive",
                    "suggestion": "Use meaningful variable name"
                }
            ],
            "overall_quality": "fair",
            "priority_fixes": ["poor_naming", "nested_conditions"]
        }''')]

        agent.client.messages.create = Mock(return_value=mock_response)

        analysis = agent.analyze_code(complex_code)

        assert 'issues' in analysis
        assert 'overall_quality' in analysis
        assert len(analysis['issues']) > 0
        assert analysis['overall_quality'] == 'fair'

    @patch('anthropic.Anthropic')
    def test_analyze_code_with_markdown(self, mock_anthropic, agent, simple_code):
        """Test analysis with markdown-wrapped JSON"""
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text='''```json
        {
            "issues": [],
            "overall_quality": "excellent",
            "priority_fixes": []
        }
        ```''')]

        agent.client.messages.create = Mock(return_value=mock_response)

        analysis = agent.analyze_code(simple_code)
        assert analysis['overall_quality'] == 'excellent'

    # --- Refactoring Tests ---

    @patch('anthropic.Anthropic')
    def test_refactor_code_success(self, mock_anthropic, agent, complex_code):
        """Test successful code refactoring"""
        # Mock API response
        refactored = """
def calculate_sum(x: int, y: int, z: int) -> int:
    if all([x > 0, y > 0, z > 0]):
        return x + y + z
    return 0
"""

        mock_response = MagicMock()
        mock_response.content = [MagicMock(text=f'''{{
            "refactored_code": {repr(refactored)},
            "changes": [
                {{
                    "type": "rename_variable",
                    "description": "Renamed 'tmp' to meaningful name",
                    "reason": "Improved readability"
                }},
                {{
                    "type": "simplify_conditions",
                    "description": "Flattened nested if statements",
                    "reason": "Reduced complexity"
                }}
            ],
            "explanation": "Improved naming and reduced complexity",
            "confidence": 0.92
        }}''')]

        agent.client.messages.create = Mock(return_value=mock_response)

        result = agent.refactor_code(complex_code)

        assert result.success is True
        assert result.refactored_code != complex_code
        assert len(result.changes) > 0
        assert result.confidence > 0.5
        assert result.risk_score >= 0

    @patch('anthropic.Anthropic')
    def test_refactor_code_preserves_functionality(self, mock_anthropic, agent):
        """Test that refactoring preserves code functionality"""
        original = "def multiply(a, b):\n    return a * b"
        refactored = "def multiply(x, y):\n    '''Multiply two numbers'''\n    return x * y"

        mock_response = MagicMock()
        mock_response.content = [MagicMock(text=f'''{{
            "refactored_code": {repr(refactored)},
            "changes": [{{"type": "add_docstring", "description": "Added docstring", "reason": "Better documentation"}}],
            "explanation": "Added documentation",
            "confidence": 0.95
        }}''')]

        agent.client.messages.create = Mock(return_value=mock_response)

        result = agent.refactor_code(original)

        assert result.success is True
        # Both should be valid Python
        assert agent._validate_syntax(result.original_code)
        assert agent._validate_syntax(result.refactored_code)

    @patch('anthropic.Anthropic')
    def test_refactor_code_syntax_error(self, mock_anthropic, agent, simple_code):
        """Test handling of syntax errors in refactored code"""
        invalid_refactored = "def broken(\n    return"

        mock_response = MagicMock()
        mock_response.content = [MagicMock(text=f'''{{
            "refactored_code": {repr(invalid_refactored)},
            "changes": [],
            "explanation": "Attempted refactoring",
            "confidence": 0.5
        }}''')]

        agent.client.messages.create = Mock(return_value=mock_response)

        result = agent.refactor_code(simple_code)

        assert result.success is False
        assert "syntax error" in result.explanation.lower()

    # --- Suggestion Tests ---

    @patch('anthropic.Anthropic')
    def test_suggest_improvements(self, mock_anthropic, agent, complex_code):
        """Test improvement suggestions"""
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text='''{
            "issues": [
                {"type": "high_priority", "severity": "high", "description": "Fix this"},
                {"type": "medium_priority", "severity": "medium", "description": "Consider this"},
                {"type": "low_priority", "severity": "low", "description": "Nice to have"}
            ],
            "overall_quality": "fair",
            "priority_fixes": []
        }''')]

        agent.client.messages.create = Mock(return_value=mock_response)

        suggestions = agent.suggest_improvements(complex_code, max_suggestions=2)

        assert len(suggestions) <= 2
        assert suggestions[0]['severity'] == 'high'  # Sorted by severity

    # --- Batch Processing Tests ---

    @patch('anthropic.Anthropic')
    def test_batch_refactor(self, mock_anthropic, agent):
        """Test batch refactoring"""
        codes = [
            "def f1(): return 1",
            "def f2(): return 2",
        ]

        mock_response = MagicMock()
        mock_response.content = [MagicMock(text='''{
            "refactored_code": "def refactored(): return 1",
            "changes": [],
            "explanation": "Refactored",
            "confidence": 0.9
        }''')]

        agent.client.messages.create = Mock(return_value=mock_response)

        results = agent.batch_refactor(codes)

        assert len(results) == len(codes)
        assert all(isinstance(r, RefactoringResult) for r in results)

    # --- Edge Cases ---

    def test_empty_code(self, agent):
        """Test handling of empty code"""
        metrics = agent._compute_metrics("")
        assert metrics['lines_of_code'] == 1  # Empty string counts as 1 line
        assert metrics['cyclomatic_complexity'] == 0

    def test_very_long_code(self, agent):
        """Test handling of very long code"""
        long_code = "def f():\n    pass\n" * 1000
        metrics = agent._compute_metrics(long_code)
        assert metrics['lines_of_code'] > 1000

    def test_unicode_code(self, agent):
        """Test handling of Unicode in code"""
        unicode_code = "def greet():\n    return '你好世界'"
        assert agent._validate_syntax(unicode_code)

    # --- Integration Tests ---

    @pytest.mark.integration
    @patch('anthropic.Anthropic')
    def test_full_refactoring_pipeline(self, mock_anthropic, agent, complex_code):
        """Test complete refactoring pipeline"""
        # Setup mock
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text='''{
            "issues": [{"type": "complexity", "severity": "high", "line_range": [1, 8], "description": "Too complex", "suggestion": "Simplify"}],
            "overall_quality": "poor",
            "priority_fixes": ["complexity"]
        }''')]

        refactor_response = MagicMock()
        refactor_response.content = [MagicMock(text=f'''{{
            "refactored_code": "def calculate_sum(x, y, z):\\n    return x + y + z if all([x > 0, y > 0, z > 0]) else 0",
            "changes": [{{"type": "simplify", "description": "Simplified logic", "reason": "Better readability"}}],
            "explanation": "Simplified the nested conditions",
            "confidence": 0.88
        }}''')]

        agent.client.messages.create = Mock(side_effect=[mock_response, refactor_response])

        # Step 1: Analyze
        analysis = agent.analyze_code(complex_code)
        assert len(analysis['issues']) > 0

        # Step 2: Get suggestions
        suggestions = agent.suggest_improvements(complex_code)
        assert len(suggestions) > 0

        # Step 3: Refactor
        result = agent.refactor_code(complex_code)
        assert result.success

        # Verify improvements
        assert result.metrics_after['cyclomatic_complexity'] <= result.metrics_before['cyclomatic_complexity']


# --- Performance Tests ---

class TestPerformance:
    """Performance and stress tests"""

    @pytest.mark.performance
    def test_metrics_computation_speed(self, benchmark):
        """Test metrics computation performance"""
        agent = AIRefactoringAgent(api_key="test-key")
        code = "def f(x):\n    return x * 2\n" * 100

        result = benchmark(agent._compute_metrics, code)
        assert result is not None

    @pytest.mark.performance
    def test_syntax_validation_speed(self, benchmark):
        """Test syntax validation performance"""
        agent = AIRefactoringAgent(api_key="test-key")
        code = "def f():\n    pass\n" * 100

        result = benchmark(agent._validate_syntax, code)
        assert result is True


# --- Fixtures for Integration Testing ---

@pytest.fixture(scope="session")
def real_api_key():
    """Get real API key for integration tests (if available)"""
    return os.environ.get('ANTHROPIC_API_KEY')


@pytest.fixture(scope="session")
def real_agent(real_api_key):
    """Create agent with real API key for integration tests"""
    if not real_api_key:
        pytest.skip("ANTHROPIC_API_KEY not set")
    return AIRefactoringAgent(api_key=real_api_key)


# --- Real API Tests (Optional) ---

class TestRealAPI:
    """Tests that use real API (run only when needed)"""

    @pytest.mark.real_api
    @pytest.mark.skipif(not os.environ.get('ANTHROPIC_API_KEY'),
                       reason="ANTHROPIC_API_KEY not set")
    def test_real_refactoring(self, real_agent):
        """Test real refactoring with actual API"""
        code = """
def calc(items):
    total = 0
    for i in range(len(items)):
        total = total + items[i]
    return total
"""

        result = real_agent.refactor_code(code)

        assert result.success
        assert result.refactored_code != code
        assert len(result.changes) > 0
        print(f"\nOriginal complexity: {result.metrics_before['cyclomatic_complexity']}")
        print(f"Refactored complexity: {result.metrics_after['cyclomatic_complexity']}")


# --- Pytest Configuration ---

def pytest_configure(config):
    """Configure custom markers"""
    config.addinivalue_line("markers", "integration: mark test as integration test")
    config.addinivalue_line("markers", "performance: mark test as performance test")
    config.addinivalue_line("markers", "real_api: mark test as using real API")


if __name__ == "__main__":
    # Run tests with coverage
    pytest.main([__file__, "-v", "--cov=src", "--cov-report=html"])
