"""
Data models for the Todo application.

This module defines the Task data structure and validation logic.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


class ValidationError(Exception):
    """Custom exception for validation errors."""

    pass


@dataclass
class Task:
    """
    Represents a single todo task.

    Attributes:
        id: Unique identifier, auto-generated, immutable
        title: Task title, required, 1-200 characters
        description: Optional details, 0-1000 characters
        status: Completion status, False=incomplete, True=complete
        created_at: ISO 8601 timestamp, auto-generated, immutable
    """

    id: int
    title: str
    description: str
    status: bool
    created_at: str

    @staticmethod
    def validate_title(title: str) -> str:
        """
        Validate and normalize a task title.

        Args:
            title: The title to validate

        Returns:
            The normalized title (trimmed whitespace, newlines converted to spaces)

        Raises:
            ValidationError: If title is empty or exceeds 200 characters
        """
        # Replace newlines with spaces
        normalized = title.replace("\n", " ").replace("\r", " ")

        # Strip leading/trailing whitespace
        normalized = normalized.strip()

        # Check if empty
        if not normalized:
            raise ValidationError("Title cannot be empty")

        # Check length (count characters, not bytes)
        title_length = len(normalized)
        if title_length > 200:
            raise ValidationError(
                f"Title cannot exceed 200 characters (provided: {title_length} characters)"
            )

        return normalized

    @staticmethod
    def validate_description(description: str) -> str:
        """
        Validate a task description.

        Args:
            description: The description to validate

        Returns:
            The validated description (preserves newlines)

        Raises:
            ValidationError: If description exceeds 1000 characters
        """
        # Check length (count characters, not bytes)
        desc_length = len(description)
        if desc_length > 1000:
            raise ValidationError(
                f"Description cannot exceed 1000 characters (provided: {desc_length} characters)"
            )

        return description

    @staticmethod
    def generate_timestamp() -> str:
        """
        Generate an ISO 8601 timestamp for the current time.

        Returns:
            ISO 8601 formatted timestamp string
        """
        return datetime.now().isoformat()

    @classmethod
    def create(
        cls,
        task_id: int,
        title: str,
        description: Optional[str] = None,
    ) -> "Task":
        """
        Create a new Task instance with validation.

        Args:
            task_id: Unique identifier for the task
            title: Task title (will be validated and normalized)
            description: Optional task description (will be validated)

        Returns:
            A new Task instance

        Raises:
            ValidationError: If validation fails for title or description
        """
        # Validate and normalize title
        validated_title = cls.validate_title(title)

        # Validate description (use empty string if None)
        desc = description if description is not None else ""
        validated_description = cls.validate_description(desc)

        # Generate timestamp
        timestamp = cls.generate_timestamp()

        # Create task with default status (incomplete)
        return cls(
            id=task_id,
            title=validated_title,
            description=validated_description,
            status=False,
            created_at=timestamp,
        )
