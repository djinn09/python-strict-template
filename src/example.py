"""Example module demonstrating best practices for LLM-generated code.

This module shows how to use:
- Pydantic for data validation
- Beartype for runtime type checking
- Type annotations throughout
- Proper error handling
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import datetime
from enum import Enum, StrEnum

from beartype import beartype
from pydantic import BaseModel, EmailStr, Field, field_validator

# =============================================================================
# Enums - Use for restricted choices
# =============================================================================


class UserRole(StrEnum):
    """User roles in the system."""

    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


class Priority(int, Enum):
    """Task priority levels."""

    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


# =============================================================================
# Pydantic Models - Validate data at boundaries
# =============================================================================


class User(BaseModel):
    """User model with validation.

    LLM code often has type mismatches - Pydantic catches them immediately.
    """

    id: int = Field(..., gt=0, description="Unique user identifier")
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    role: UserRole = UserRole.USER
    created_at: datetime = Field(default_factory=datetime.now)

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        """Validate that name is not just whitespace."""
        if not v.strip():
            msg = "Name cannot be empty or whitespace"
            raise ValueError(msg)
        return v.strip()


class Task(BaseModel):
    """Task model with validation."""

    id: int = Field(..., gt=0)
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(default="")
    priority: Priority = Priority.MEDIUM
    completed: bool = False
    assignee_id: int | None = None


# =============================================================================
# Beartype - Runtime type checking for functions
# =============================================================================


@beartype
def calculate_sum(numbers: Sequence[int | float]) -> float:
    """Calculate sum of numbers with runtime type checking.

    Beartype verifies types at runtime with O(1) overhead.
    LLM-generated code often passes wrong types - this catches it.

    Args:
        numbers: Sequence of numeric values

    Returns:
        Sum of all numbers as float

    Raises:
        BeartypeCallHintException: If wrong types are passed
    """
    return float(sum(numbers))


@beartype
def create_greeting(user: User, *, include_role: bool = False) -> str:
    """Create a greeting message for a user.

    Args:
        user: The user to greet
        include_role: Whether to include role in greeting

    Returns:
        Greeting message string
    """
    greeting = f"Hello, {user.name}!"
    if include_role:
        greeting += f" You are logged in as {user.role.value}."
    return greeting


@beartype
def process_tasks(
    tasks: list[Task], *, priority_filter: Priority | None = None
) -> list[Task]:
    """Process and filter tasks.

    Args:
        tasks: List of tasks to process
        priority_filter: Optional priority to filter by

    Returns:
        Filtered list of tasks
    """
    if priority_filter is None:
        return tasks
    return [t for t in tasks if t.priority == priority_filter]


# =============================================================================
# Safe Patterns - Avoid common LLM mistakes
# =============================================================================


class SafeCalculator:
    """Calculator with safe operations.

    LLMs often forget edge cases - this class handles them properly.
    """

    @staticmethod
    @beartype
    def divide(a: int | float, b: int | float) -> float:  # noqa: PYI041
        """Safely divide two numbers.

        Args:
            a: Dividend
            b: Divisor

        Returns:
            Result of a / b

        Raises:
            ValueError: If b is zero
        """
        if b == 0:
            msg = "Cannot divide by zero"
            raise ValueError(msg)
        return a / b

    @staticmethod
    @beartype
    def safe_get(
        data: Mapping[str, object], key: str, default: object | None = None
    ) -> object:
        """Safely get a value from a dictionary.

        Args:
            data: Dictionary to get value from
            key: Key to look up
            default: Default value if key not found

        Returns:
            Value at key or default
        """
        return data.get(key, default)
