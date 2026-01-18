"""Pytest configuration and fixtures."""

from collections.abc import Generator
from datetime import datetime

import pytest
from src.example import Priority, Task, User, UserRole


@pytest.fixture
def sample_user() -> User:
    """Create a sample user for testing."""
    return User(
        id=1,
        name="John Doe",
        email="john@example.com",
        role=UserRole.USER,
    )


@pytest.fixture
def sample_admin() -> User:
    """Create a sample admin user for testing."""
    return User(
        id=2,
        name="Admin User",
        email="admin@example.com",
        role=UserRole.ADMIN,
    )


@pytest.fixture
def sample_tasks() -> list[Task]:
    """Create a list of sample tasks for testing."""
    return [
        Task(id=1, title="Low priority task", priority=Priority.LOW),
        Task(id=2, title="Medium priority task", priority=Priority.MEDIUM),
        Task(id=3, title="High priority task", priority=Priority.HIGH),
        Task(id=4, title="Critical task", priority=Priority.CRITICAL),
    ]


@pytest.fixture
def fixed_datetime() -> Generator[datetime, None, None]:
    """Provide a fixed datetime for deterministic tests."""
    fixed = datetime(2024, 1, 15, 12, 0, 0)  # noqa: DTZ001
    yield fixed
