"""Tests for example module.

Demonstrates:
- Standard pytest tests
- Hypothesis property-based tests
- Type error detection with Beartype
"""

import pytest
from beartype.roar import BeartypeCallHintViolation
from hypothesis import given, settings
from hypothesis import strategies as st
from pydantic import ValidationError
from src.example import (
    Priority,
    SafeCalculator,
    Task,
    User,
    UserRole,
    calculate_sum,
    create_greeting,
    process_tasks,
)

# =============================================================================
# User Model Tests
# =============================================================================


class TestUser:
    """Tests for User model validation."""

    def test_valid_user_creation(self, sample_user: User) -> None:
        """Test creating a valid user."""
        assert sample_user.id == 1
        assert sample_user.name == "John Doe"
        assert sample_user.email == "john@example.com"
        assert sample_user.role == UserRole.USER

    def test_invalid_email_rejected(self) -> None:
        """Test that invalid emails are rejected - LLMs often miss this."""
        with pytest.raises(ValidationError):
            User(id=1, name="Test", email="not-an-email")

    def test_empty_name_rejected(self) -> None:
        """Test that empty names are rejected."""
        with pytest.raises(ValidationError):
            User(id=1, name="", email="test@example.com")

    def test_whitespace_name_rejected(self) -> None:
        """Test that whitespace-only names are rejected."""
        with pytest.raises(ValidationError):
            User(id=1, name="   ", email="test@example.com")

    def test_negative_id_rejected(self) -> None:
        """Test that negative IDs are rejected."""
        with pytest.raises(ValidationError):
            User(id=-1, name="Test", email="test@example.com")

    def test_zero_id_rejected(self) -> None:
        """Test that zero ID is rejected."""
        with pytest.raises(ValidationError):
            User(id=0, name="Test", email="test@example.com")


# =============================================================================
# Beartype Runtime Checks
# =============================================================================


class TestBeartypeValidation:
    """Tests demonstrating Beartype catches LLM type errors at runtime."""

    def test_calculate_sum_with_valid_input(self) -> None:
        """Test sum calculation with valid input."""
        assert calculate_sum([1, 2, 3]) == 6.0
        assert calculate_sum([1.5, 2.5]) == 4.0
        assert calculate_sum([]) == 0.0

    def test_calculate_sum_rejects_string_list(self) -> None:
        """Test that string list is rejected - common LLM mistake."""
        with pytest.raises(BeartypeCallHintViolation):
            calculate_sum(["1", "2", "3"])  # type: ignore[list-item]

    def test_calculate_sum_rejects_none(self) -> None:
        """Test that None is rejected."""
        with pytest.raises(BeartypeCallHintViolation):
            calculate_sum(None)  # type: ignore[arg-type]

    def test_create_greeting_requires_user_object(self) -> None:
        """Test that greeting requires actual User object."""
        with pytest.raises(BeartypeCallHintViolation):
            create_greeting({"name": "Test"})  # type: ignore[arg-type]


# =============================================================================
# Hypothesis Property-Based Tests
# =============================================================================


class TestHypothesis:
    """Property-based tests that find edge cases LLMs miss."""

    @given(st.lists(st.integers(min_value=-1000, max_value=1000)))
    @settings(max_examples=100)
    def test_sum_is_commutative(self, numbers: list[int]) -> None:
        """Test that sum works for any list of integers."""
        result = calculate_sum(numbers)
        assert result == sum(numbers)

    @given(st.lists(st.floats(allow_nan=False, allow_infinity=False)))
    @settings(max_examples=100)
    def test_sum_with_floats(self, numbers: list[float]) -> None:
        """Test sum with arbitrary floats."""
        result = calculate_sum(numbers)
        expected = sum(numbers)
        assert abs(result - expected) < 1e-10 or result == expected

    @given(
        st.integers(min_value=1, max_value=10000),
        st.text(min_size=1, max_size=100).filter(lambda x: x.strip()),
        st.emails(),
    )
    @settings(max_examples=50)
    def test_user_creation_with_random_valid_data(
        self, user_id: int, name: str, email: str
    ) -> None:
        """Test User creation with random valid data."""
        user = User(id=user_id, name=name, email=email)
        assert user.id == user_id
        assert user.name == name.strip()
        # Pydantic normalizes emails (lowercase, punycode, etc.) - just verify it's a valid string
        assert "@" in user.email


# =============================================================================
# Task Processing Tests
# =============================================================================


class TestTaskProcessing:
    """Tests for task processing functions."""

    def test_process_tasks_no_filter(self, sample_tasks: list[Task]) -> None:
        """Test processing without filter returns all tasks."""
        result = process_tasks(sample_tasks)
        assert len(result) == 4

    def test_process_tasks_with_priority_filter(self, sample_tasks: list[Task]) -> None:
        """Test filtering by priority."""
        high_priority = process_tasks(sample_tasks, priority_filter=Priority.HIGH)
        assert len(high_priority) == 1
        assert high_priority[0].priority == Priority.HIGH

    def test_process_tasks_empty_list(self) -> None:
        """Test processing empty list."""
        result = process_tasks([])
        assert result == []


# =============================================================================
# Safe Calculator Tests
# =============================================================================


class TestSafeCalculator:
    """Tests for SafeCalculator - demonstrates handling edge cases."""

    def test_divide_normal(self) -> None:
        """Test normal division."""
        assert SafeCalculator.divide(10, 2) == 5.0

    def test_divide_by_zero_raises(self) -> None:
        """Test that division by zero raises ValueError."""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            SafeCalculator.divide(10, 0)

    def test_safe_get_existing_key(self) -> None:
        """Test getting existing key."""
        data = {"key": "value"}
        assert SafeCalculator.safe_get(data, "key") == "value"

    def test_safe_get_missing_key(self) -> None:
        """Test getting missing key returns default."""
        data = {"key": "value"}
        assert SafeCalculator.safe_get(data, "missing") is None

    def test_safe_get_custom_default(self) -> None:
        """Test getting missing key with custom default."""
        data = {"key": "value"}
        assert SafeCalculator.safe_get(data, "missing", "default") == "default"
