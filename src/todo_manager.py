"""
Business logic and state management for the Todo application.

This module manages task storage, ID generation, and task operations.
"""

from typing import Dict, Optional, Tuple
from models import Task, ValidationError


class TodoManager:
    """
    Manages todo tasks in memory.

    Responsibilities:
    - Generate unique task IDs
    - Store and retrieve tasks
    - Coordinate task operations (add, delete, update, etc.)
    """

    def __init__(self) -> None:
        """Initialize the TodoManager with empty task storage."""
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def add_task(
        self, title: str, description: Optional[str] = None
    ) -> Tuple[Optional[Task], Optional[str]]:
        """
        Add a new task to the todo list.

        Args:
            title: The task title (will be validated)
            description: Optional task description (will be validated)

        Returns:
            A tuple of (Task, error_message):
            - If successful: (Task instance, None)
            - If failed: (None, error message string)
        """
        try:
            # Create task with validation
            task = Task.create(
                task_id=self._next_id,
                title=title,
                description=description,
            )

            # Store task
            self._tasks[task.id] = task

            # Increment ID counter
            self._next_id += 1

            return (task, None)

        except ValidationError as e:
            # Return validation error message
            return (None, str(e))

    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Retrieve a task by ID.

        Args:
            task_id: The ID of the task to retrieve

        Returns:
            The Task instance if found, None otherwise
        """
        return self._tasks.get(task_id)

    def get_all_tasks(self) -> list[Task]:
        """
        Retrieve all tasks.

        Returns:
            A list of all Task instances, sorted by ID
        """
        return sorted(self._tasks.values(), key=lambda t: t.id)

    def task_count(self) -> int:
        """
        Get the total number of tasks.

        Returns:
            The number of tasks currently stored
        """
        return len(self._tasks)

    def delete_task(self, task_id: int) -> Tuple[Optional[Task], Optional[str]]:
        """
        Delete a task by ID.

        Args:
            task_id: The ID of the task to delete

        Returns:
            A tuple of (Task, error_message):
            - If successful: (deleted Task instance, None)
            - If failed: (None, error message string)
        """
        # Look up task
        task = self.get_task(task_id)
        if not task:
            return (None, f"Task with ID {task_id} not found")

        # Remove task from storage
        del self._tasks[task_id]

        return (task, None)

    def update_task(
        self,
        task_id: int,
        new_title: Optional[str] = None,
        new_description: Optional[str] = None,
    ) -> Tuple[Optional[Task], Optional[str], bool]:
        """
        Update a task's title and/or description.

        Args:
            task_id: ID of task to update
            new_title: New title (None = keep current)
            new_description: New description (None = keep current)

        Returns:
            A tuple of (task, error_message, changes_made):
            - Success with changes: (Task, None, True)
            - Success no changes: (Task, None, False)
            - Failure: (None, error_string, False)
        """
        # Look up task
        task = self.get_task(task_id)
        if not task:
            return (None, f"Task with ID {task_id} not found", False)

        # Track if any changes made
        changes_made = False

        try:
            # Validate and update title if provided
            if new_title is not None:
                validated_title = Task.validate_title(new_title)
                if validated_title != task.title:
                    task.title = validated_title
                    changes_made = True

            # Validate and update description if provided
            if new_description is not None:
                validated_desc = Task.validate_description(new_description)
                if validated_desc != task.description:
                    task.description = validated_desc
                    changes_made = True

            return (task, None, changes_made)

        except ValidationError as e:
            # Return validation error message
            return (None, str(e), False)

    def mark_complete(self, task_id: int) -> Tuple[Optional[Task], Optional[str], bool]:
        """
        Mark a task as complete.

        Args:
            task_id: ID of task to mark complete

        Returns:
            A tuple of (task, error_message, status_changed):
            - Success with change: (Task, None, True)
            - Success already complete: (Task, None, False)
            - Failure: (None, error_string, False)
        """
        # Look up task
        task = self.get_task(task_id)
        if not task:
            return (None, f"Task with ID {task_id} not found", False)

        # Check if already complete
        if task.status:
            return (task, None, False)  # Already complete

        # Mark as complete
        task.status = True
        return (task, None, True)  # Status changed

    def mark_incomplete(
        self, task_id: int
    ) -> Tuple[Optional[Task], Optional[str], bool]:
        """
        Mark a task as incomplete.

        Args:
            task_id: ID of task to mark incomplete

        Returns:
            A tuple of (task, error_message, status_changed):
            - Success with change: (Task, None, True)
            - Success already incomplete: (Task, None, False)
            - Failure: (None, error_string, False)
        """
        # Look up task
        task = self.get_task(task_id)
        if not task:
            return (None, f"Task with ID {task_id} not found", False)

        # Check if already incomplete
        if not task.status:
            return (task, None, False)  # Already incomplete

        # Mark as incomplete
        task.status = False
        return (task, None, True)  # Status changed
