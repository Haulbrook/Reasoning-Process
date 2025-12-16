"""
Comprehensive Reasoning Test Suite Template

This test suite validates AI reasoning capabilities across all 7 failure categories.
Copy and adapt this for your specific bot/skill training validation.

Usage:
    1. Replace `Bot` class with your actual bot implementation
    2. Customize test scenarios for your domain
    3. Run: pytest reasoning-test-suite.py -v
"""

import pytest
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from abc import ABC, abstractmethod


# =============================================================================
# BOT INTERFACE - Replace with your actual implementation
# =============================================================================

class Bot(ABC):
    """Abstract base class for bot implementations."""

    @abstractmethod
    def execute(self, prompt: str, context: Optional[List[str]] = None) -> str:
        """Execute a prompt and return the response."""
        pass

    @abstractmethod
    def analyze_requirements(self, prompt: str) -> Dict[str, Any]:
        """Analyze a prompt and return identified requirements."""
        pass

    @abstractmethod
    def generate_plan(self, task: str) -> Dict[str, Any]:
        """Generate a plan for a task."""
        pass


# Placeholder implementation for testing
class MockBot(Bot):
    """Mock bot for template testing. Replace with actual implementation."""

    def execute(self, prompt: str, context: Optional[List[str]] = None) -> str:
        return f"Response to: {prompt}"

    def analyze_requirements(self, prompt: str) -> Dict[str, Any]:
        return {"requirements": [], "constraints": []}

    def generate_plan(self, task: str) -> Dict[str, Any]:
        return {"approaches": [], "steps": []}


# =============================================================================
# TEST FIXTURES
# =============================================================================

@pytest.fixture
def bot():
    """Return bot instance. Replace MockBot with your implementation."""
    return MockBot()


@pytest.fixture
def conversation_context():
    """Sample conversation context for context integration tests."""
    return [
        "User: My name is Alice",
        "Bot: Hello Alice!",
        "User: I prefer Python for coding",
        "Bot: Noted, I'll use Python for examples",
        "User: I'm building a web application",
    ]


# =============================================================================
# CATEGORY 1: COMPREHENSION TESTS
# =============================================================================

class TestComprehension:
    """
    Tests for comprehension failures (15% of errors).

    Validates that the bot correctly:
    - Identifies explicit requirements
    - Recognizes implicit requirements
    - Notes constraints
    - Understands the actual question
    """

    @pytest.mark.parametrize("prompt,expected_requirements", [
        (
            "Write a function that sorts numbers",
            ["function", "sort", "numbers"]
        ),
        (
            "Create a REST API endpoint for user registration with email validation",
            ["REST API", "endpoint", "user registration", "email validation"]
        ),
        (
            "Fix the bug where users can't log in after password reset",
            ["fix", "bug", "login", "password reset"]
        ),
    ])
    def test_identifies_explicit_requirements(self, bot, prompt, expected_requirements):
        """Bot should identify all explicitly stated requirements."""
        result = bot.analyze_requirements(prompt)

        for req in expected_requirements:
            assert any(req.lower() in r.lower() for r in result.get("requirements", [])), \
                f"Missing explicit requirement: {req}"

    @pytest.mark.parametrize("prompt,implicit_requirements", [
        (
            "Write a sorting function",
            ["handle empty input", "return same type"]  # Implied
        ),
        (
            "Create a user login system",
            ["security", "password hashing", "session management"]  # Implied
        ),
        (
            "Build a file upload feature",
            ["size limits", "file type validation", "error handling"]  # Implied
        ),
    ])
    def test_identifies_implicit_requirements(self, bot, prompt, implicit_requirements):
        """Bot should recognize requirements implied but not stated."""
        result = bot.analyze_requirements(prompt)

        # At least some implicit requirements should be identified
        found = sum(
            1 for req in implicit_requirements
            if any(req.lower() in r.lower() for r in result.get("requirements", []))
        )

        assert found >= len(implicit_requirements) // 2, \
            f"Should identify at least half of implicit requirements. Found: {found}/{len(implicit_requirements)}"

    def test_doesnt_answer_different_question(self, bot):
        """Bot should answer the actual question, not a related one."""
        prompt = "How do I CENTER a div in CSS?"  # Specific question
        response = bot.execute(prompt)

        # Response should be about centering, not general CSS
        assert "center" in response.lower() or "flexbox" in response.lower() or "margin" in response.lower(), \
            "Response should address centering specifically"

    def test_recognizes_constraints(self, bot):
        """Bot should identify constraints in the prompt."""
        prompt = "Write a sorting algorithm without using built-in sort functions, in O(n log n) time"

        result = bot.analyze_requirements(prompt)
        constraints = result.get("constraints", [])

        expected_constraints = ["no built-in sort", "O(n log n)"]

        for constraint in expected_constraints:
            assert any(constraint.lower() in c.lower() for c in constraints), \
                f"Missing constraint: {constraint}"


# =============================================================================
# CATEGORY 2: PLANNING TESTS
# =============================================================================

class TestPlanning:
    """
    Tests for planning failures (20% of errors).

    Validates that the bot:
    - Generates multiple approaches
    - Provides selection reasoning
    - Creates actionable plans
    - Identifies risks
    """

    def test_generates_multiple_approaches(self, bot):
        """Bot should consider multiple approaches for non-trivial tasks."""
        task = "Implement a caching system for API responses"
        plan = bot.generate_plan(task)

        assert len(plan.get("approaches", [])) >= 2, \
            "Should generate at least 2 approaches for non-trivial tasks"

    def test_provides_selection_reasoning(self, bot):
        """Bot should explain why it chose a particular approach."""
        task = "Design a database schema for a blog"
        plan = bot.generate_plan(task)

        assert plan.get("selection_reasoning") is not None, \
            "Should provide reasoning for approach selection"
        assert len(plan.get("selection_reasoning", "")) > 20, \
            "Selection reasoning should be substantive"

    def test_creates_actionable_steps(self, bot):
        """Bot should create concrete, actionable steps."""
        task = "Add user authentication to the application"
        plan = bot.generate_plan(task)

        steps = plan.get("steps", [])
        assert len(steps) >= 3, "Should have at least 3 steps for complex task"

        for step in steps:
            # Steps should be actionable (contain verbs)
            action_words = ["create", "add", "implement", "configure", "set", "define", "write", "test"]
            has_action = any(word in step.lower() for word in action_words)
            assert has_action, f"Step should be actionable: {step}"

    def test_identifies_risks(self, bot):
        """Bot should identify potential risks."""
        task = "Migrate the database to a new schema"
        plan = bot.generate_plan(task)

        risks = plan.get("risks", [])
        assert len(risks) >= 1, "Should identify at least one risk for risky operations"

    def test_doesnt_skip_planning(self, bot):
        """Bot should not jump straight to implementation."""
        task = "Build a payment processing system"
        response = bot.execute(task)

        # Response should show planning before code
        planning_indicators = ["approach", "plan", "first", "then", "steps", "consider"]
        has_planning = any(indicator in response.lower() for indicator in planning_indicators)

        # If code is present, planning should come first
        if "```" in response:
            code_position = response.find("```")
            planning_position = min(
                (response.lower().find(ind) for ind in planning_indicators if ind in response.lower()),
                default=float('inf')
            )
            assert planning_position < code_position, \
                "Planning discussion should come before code"


# =============================================================================
# CATEGORY 3: EXECUTION TESTS
# =============================================================================

class TestExecution:
    """
    Tests for execution drift (18% of errors).

    Validates that the bot:
    - Stays on task
    - Follows its plan
    - Doesn't add unrequested features
    - Maintains consistency
    """

    def test_stays_on_task(self, bot):
        """Bot should not drift to unrelated topics."""
        prompt = "Write a function to validate email addresses"
        response = bot.execute(prompt)

        # Should not include unrelated functionality
        unrelated = ["phone number", "address validation", "name validation"]
        for item in unrelated:
            assert item not in response.lower(), \
                f"Response includes unrequested functionality: {item}"

    def test_no_scope_creep(self, bot):
        """Bot should not add features not requested."""
        prompt = "Create a function that adds two numbers"
        response = bot.execute(prompt)

        # Should be simple addition, not a calculator
        scope_creep_indicators = [
            "subtract", "multiply", "divide",  # Calculator creep
            "history", "memory",  # Feature creep
            "gui", "interface",  # UI creep
        ]

        for indicator in scope_creep_indicators:
            assert indicator not in response.lower(), \
                f"Scope creep detected: {indicator}"

    def test_completes_task(self, bot):
        """Bot should complete the full task, not stop partway."""
        prompt = "Write a function that: 1) takes a list, 2) filters even numbers, 3) squares them, 4) returns the sum"
        response = bot.execute(prompt)

        # All parts should be addressed
        required_parts = ["filter", "even", "square", "sum"]
        for part in required_parts:
            assert part in response.lower(), f"Missing required part: {part}"

    def test_maintains_consistency(self, bot):
        """Bot should not contradict itself within a response."""
        prompt = "Explain the difference between let and const in JavaScript"
        response = bot.execute(prompt)

        # Should not say both are the same and different
        assert not ("exactly the same" in response.lower() and "different" in response.lower()), \
            "Response contains contradiction"


# =============================================================================
# CATEGORY 4: EDGE CASE TESTS
# =============================================================================

class TestEdgeCases:
    """
    Tests for edge case blindness (15% of errors).

    Validates that the bot:
    - Handles empty input
    - Handles null/None
    - Handles boundary values
    - Considers error conditions
    """

    def test_handles_empty_input(self, bot):
        """Bot should address empty input handling."""
        prompt = "Write a function to find the maximum value in a list"
        response = bot.execute(prompt)

        empty_handling_indicators = [
            "empty", "no elements", "length 0", "len(", "if not",
            "[]", "null", "none", "edge case"
        ]

        has_empty_handling = any(ind in response.lower() for ind in empty_handling_indicators)
        assert has_empty_handling, "Should address empty input handling"

    def test_handles_null_input(self, bot):
        """Bot should consider null/None input."""
        prompt = "Write a function to get the length of a string"
        response = bot.execute(prompt)

        null_handling = ["null", "none", "undefined", "if not", "is none", "is null"]
        has_null_handling = any(ind in response.lower() for ind in null_handling)

        # At minimum should mention it
        assert has_null_handling or "assume" in response.lower(), \
            "Should handle null input or state assumption"

    def test_considers_boundary_values(self, bot):
        """Bot should consider boundary values in numeric operations."""
        prompt = "Write a function to calculate percentage"
        response = bot.execute(prompt)

        boundary_indicators = [
            "zero", "0", "negative", "100", "overflow",
            "divide", "division", "edge"
        ]

        has_boundary_consideration = any(ind in response.lower() for ind in boundary_indicators)
        assert has_boundary_consideration, "Should consider boundary values"

    def test_mentions_error_handling(self, bot):
        """Bot should include error handling for risky operations."""
        prompt = "Write a function to read a file and parse JSON"
        response = bot.execute(prompt)

        error_indicators = [
            "try", "except", "catch", "error", "exception",
            "invalid", "fail", "handle"
        ]

        has_error_handling = any(ind in response.lower() for ind in error_indicators)
        assert has_error_handling, "Should include error handling for I/O operations"


# =============================================================================
# CATEGORY 5: VERIFICATION TESTS
# =============================================================================

class TestVerification:
    """
    Tests for verification skipping (12% of errors).

    Validates that the bot:
    - Verifies syntax correctness
    - Checks logical consistency
    - Validates against requirements
    - Performs self-checks
    """

    def test_provides_examples_or_tests(self, bot):
        """Bot should verify with examples or tests."""
        prompt = "Write a function to check if a number is prime"
        response = bot.execute(prompt)

        verification_indicators = [
            "example", "test", ">>> ", "print(", "assert",
            "returns true", "returns false", "output:"
        ]

        has_verification = any(ind in response.lower() for ind in verification_indicators)
        assert has_verification, "Should include examples or tests"

    def test_no_syntax_errors(self, bot):
        """Bot-generated code should not have obvious syntax errors."""
        prompt = "Write a Python function to reverse a string"
        response = bot.execute(prompt)

        # Extract code blocks
        if "```python" in response:
            code_start = response.find("```python") + len("```python")
            code_end = response.find("```", code_start)
            code = response[code_start:code_end]

            # Basic syntax check
            try:
                compile(code, "<string>", "exec")
            except SyntaxError as e:
                pytest.fail(f"Generated code has syntax error: {e}")

    def test_logic_is_sound(self, bot):
        """Bot's logic should be internally consistent."""
        prompt = "If A implies B, and B implies C, what can we conclude about A and C?"
        response = bot.execute(prompt)

        # Should conclude A implies C (transitive)
        correct_indicators = ["a implies c", "a → c", "if a then c", "transitive"]
        has_correct_logic = any(ind in response.lower() for ind in correct_indicators)

        assert has_correct_logic, "Should correctly apply transitive logic"


# =============================================================================
# CATEGORY 6: SELF-CORRECTION TESTS
# =============================================================================

class TestSelfCorrection:
    """
    Tests for self-correction failure (10% of errors).

    Validates that the bot:
    - Can recognize its own errors
    - Corrects errors when pointed out
    - Doesn't defensively double down
    - Shows appropriate uncertainty
    """

    def test_can_correct_when_wrong(self, bot):
        """Bot should be able to correct itself when wrong."""
        # First, get an answer
        response1 = bot.execute("What is 15% of 80?")

        # Then, question it (even if correct)
        response2 = bot.execute(
            "Are you sure that's correct? Please double-check your arithmetic."
        )

        # Should show work, not just repeat
        shows_work = any(
            word in response2.lower()
            for word in ["calculate", "15", "80", "0.15", "12", "verify", "check"]
        )

        assert shows_work, "Should show verification work when questioned"

    def test_acknowledges_uncertainty(self, bot):
        """Bot should express uncertainty when appropriate."""
        prompt = "What will the stock market do next week?"
        response = bot.execute(prompt)

        uncertainty_indicators = [
            "uncertain", "cannot predict", "impossible to know",
            "might", "could", "may", "possible", "unlikely to know",
            "no one can", "speculation"
        ]

        shows_uncertainty = any(ind in response.lower() for ind in uncertainty_indicators)
        assert shows_uncertainty, "Should acknowledge uncertainty for unpredictable topics"

    def test_doesnt_double_down(self, bot):
        """Bot should not defensively maintain errors."""
        # Provide obviously wrong information and see if bot corrects
        response = bot.execute(
            "Earlier you said Python was created in 2010. Actually it was created in 1991. "
            "Can you tell me more about Python's history?"
        )

        # Should acknowledge the correction
        assert "1991" in response, "Should accept correction about Python's creation date"
        assert "2010" not in response or "incorrect" in response.lower(), \
            "Should not repeat the wrong date"


# =============================================================================
# CATEGORY 7: CONTEXT INTEGRATION TESTS
# =============================================================================

class TestContextIntegration:
    """
    Tests for context integration failure (10% of errors).

    Validates that the bot:
    - Uses conversation history
    - Remembers stated preferences
    - Doesn't ask for given information
    - Builds on previous work
    """

    def test_uses_conversation_context(self, bot, conversation_context):
        """Bot should use information from conversation history."""
        prompt = "Can you write a simple hello world program for me?"
        response = bot.execute(prompt, context=conversation_context)

        # Should use Python based on context
        python_indicators = ["python", "print(", "def "]
        uses_python = any(ind in response.lower() for ind in python_indicators)

        # Should not ask about language preference (already established)
        asks_preference = "what language" in response.lower() or "which language" in response.lower()

        assert uses_python or not asks_preference, \
            "Should use established Python preference or not ask again"

    def test_remembers_user_name(self, bot, conversation_context):
        """Bot should remember user's name from context."""
        prompt = "Can you address me by name?"
        response = bot.execute(prompt, context=conversation_context)

        assert "alice" in response.lower(), "Should remember user's name is Alice"

    def test_builds_on_previous_work(self, bot):
        """Bot should build on established work, not start fresh."""
        context = [
            "User: Let's create a User class with name and email",
            "Bot: class User:\n    def __init__(self, name, email):\n        self.name = name\n        self.email = email",
        ]

        prompt = "Now add a method to validate the email"
        response = bot.execute(prompt, context=context)

        # Should add to existing class, not create new one
        adds_to_class = "def validate" in response or "def is_valid" in response
        creates_new_class = response.count("class User") > 0 and "def __init__" in response

        assert adds_to_class, "Should add method to existing class"
        # Should not redefine the whole class
        assert not creates_new_class or "# Adding to existing" in response, \
            "Should not recreate entire class"


# =============================================================================
# INTEGRATION TESTS
# =============================================================================

class TestIntegration:
    """
    Integration tests that validate multiple reasoning capabilities together.
    """

    def test_complex_task_full_reasoning(self, bot):
        """Bot should demonstrate full reasoning on complex tasks."""
        prompt = """
        Design a rate limiting system for an API that:
        1. Limits users to 100 requests per minute
        2. Uses token bucket algorithm
        3. Must be thread-safe
        4. Should return informative error messages when limit exceeded
        """

        response = bot.execute(prompt)

        # Check for planning
        has_planning = any(
            word in response.lower()
            for word in ["approach", "design", "first", "implement", "consider"]
        )

        # Check for requirements coverage
        requirements_covered = sum([
            "100" in response,
            "token" in response.lower() or "bucket" in response.lower(),
            "thread" in response.lower() or "lock" in response.lower() or "concurrent" in response.lower(),
            "error" in response.lower() or "message" in response.lower(),
        ])

        # Check for edge cases
        has_edge_cases = any(
            word in response.lower()
            for word in ["empty", "zero", "negative", "edge", "boundary", "overflow"]
        )

        assert has_planning, "Should show planning for complex task"
        assert requirements_covered >= 3, f"Should cover most requirements, covered {requirements_covered}/4"

    def test_multi_turn_consistency(self, bot):
        """Bot should maintain consistency across multiple turns."""
        context = []

        # Turn 1: Establish approach
        response1 = bot.execute("Let's use a linked list to implement a queue", context)
        context.append(f"User: Let's use a linked list to implement a queue")
        context.append(f"Bot: {response1}")

        # Turn 2: Continue with implementation
        response2 = bot.execute("Now implement the enqueue method", context)
        context.append(f"User: Now implement the enqueue method")
        context.append(f"Bot: {response2}")

        # Turn 3: Should still be consistent
        response3 = bot.execute("And the dequeue method", context)

        # All responses should use linked list terminology
        linked_list_terms = ["node", "next", "head", "tail", "pointer"]

        uses_linked_list = any(
            term in response2.lower() or term in response3.lower()
            for term in linked_list_terms
        )

        assert uses_linked_list, "Should consistently use linked list approach across turns"


# =============================================================================
# SCORING TESTS
# =============================================================================

class TestScoring:
    """
    Tests that produce scores for reasoning quality.
    """

    def calculate_reasoning_score(self, bot, task: str) -> Dict[str, int]:
        """
        Calculate comprehensive reasoning score.

        Returns dict with scores for each category and total.
        """
        response = bot.execute(task)
        plan = bot.generate_plan(task)
        requirements = bot.analyze_requirements(task)

        scores = {
            "comprehension": 0,  # /20
            "planning": 0,  # /20
            "execution": 0,  # /20
            "edge_cases": 0,  # /15
            "verification": 0,  # /15
            "self_awareness": 0,  # /10
        }

        # Score comprehension (0-20)
        if requirements.get("requirements"):
            scores["comprehension"] += 10
        if requirements.get("constraints"):
            scores["comprehension"] += 5
        if requirements.get("implicit_requirements"):
            scores["comprehension"] += 5

        # Score planning (0-20)
        if len(plan.get("approaches", [])) >= 2:
            scores["planning"] += 10
        if plan.get("selection_reasoning"):
            scores["planning"] += 5
        if len(plan.get("steps", [])) >= 3:
            scores["planning"] += 5

        # Score execution (0-20)
        if response and len(response) > 50:
            scores["execution"] += 10
        if "```" in response:  # Has code
            scores["execution"] += 5
        if not any(word in response.lower() for word in ["todo", "fixme", "incomplete"]):
            scores["execution"] += 5

        # Score edge cases (0-15)
        edge_terms = ["empty", "null", "none", "zero", "negative", "error", "invalid"]
        edge_count = sum(1 for term in edge_terms if term in response.lower())
        scores["edge_cases"] = min(15, edge_count * 3)

        # Score verification (0-15)
        if any(word in response.lower() for word in ["test", "example", "verify"]):
            scores["verification"] += 10
        if "assert" in response or ">>>" in response:
            scores["verification"] += 5

        # Score self-awareness (0-10)
        if any(word in response.lower() for word in ["note", "caveat", "limitation", "assume"]):
            scores["self_awareness"] += 5
        if any(word in response.lower() for word in ["consider", "alternatively", "might"]):
            scores["self_awareness"] += 5

        scores["total"] = sum(scores.values())
        scores["percentage"] = round(scores["total"] / 100 * 100, 1)

        return scores

    def test_scoring_sample_task(self, bot):
        """Test scoring on a sample task."""
        task = "Write a function to validate and parse a date string"
        scores = self.calculate_reasoning_score(bot, task)

        print(f"\nReasoning Score Breakdown:")
        print(f"  Comprehension:  {scores['comprehension']}/20")
        print(f"  Planning:       {scores['planning']}/20")
        print(f"  Execution:      {scores['execution']}/20")
        print(f"  Edge Cases:     {scores['edge_cases']}/15")
        print(f"  Verification:   {scores['verification']}/15")
        print(f"  Self-Awareness: {scores['self_awareness']}/10")
        print(f"  ---")
        print(f"  TOTAL:          {scores['total']}/100 ({scores['percentage']}%)")

        # Target: 85%+
        assert scores["percentage"] >= 75, f"Score {scores['percentage']}% below 75% threshold"


# =============================================================================
# RUN CONFIGURATION
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
