"""
Console interface for the Todo application.

This module provides the command-line user interface and handles user interaction.
"""

from typing import Optional
from todo_manager import TodoManager
from models import Task


# ============================================================
# SHARED UTILITY FUNCTIONS
# ============================================================


def parse_task_id(id_string: str) -> tuple[Optional[int], Optional[str]]:
    """
    Parse and validate a task ID from user input.

    Args:
        id_string: The user input string to parse

    Returns:
        A tuple of (task_id, error_message):
        - Success: (int, None)
        - Failure: (None, error_string)
    """
    # Strip whitespace
    id_string = id_string.strip()

    # Check if empty
    if not id_string:
        return (None, "Invalid task ID. Please provide a numeric ID")

    # Try to parse as integer
    try:
        task_id = int(id_string)
    except ValueError:
        return (None, "Invalid task ID. Please provide a numeric ID")

    # Check if positive
    if task_id <= 0:
        return (None, "Invalid task ID. Please provide a positive number")

    return (task_id, None)


def format_status(status: bool) -> str:
    """
    Format task status for display.

    Args:
        status: The task status (True=complete, False=incomplete)

    Returns:
        Formatted status string
    """
    return "Complete" if status else "Incomplete"


# ============================================================
# DISPLAY FUNCTIONS
# ============================================================


def display_menu() -> None:
    """Display the main menu options."""
    print("\n" + "=" * 50)
    print("TODO APP - In-Memory Task Manager")
    print("=" * 50)
    print("\nAvailable Commands:")
    print("  add        - Add a new task")
    print("  view       - View all tasks")
    print("  update     - Update a task")
    print("  delete     - Delete a task")
    print("  complete   - Mark a task as complete")
    print("  incomplete - Mark a task as incomplete")
    print("  quit       - Exit the application")
    print()


def display_task_success(task: Task) -> None:
    """
    Display a success message after adding a task.

    Args:
        task: The task that was successfully created
    """
    print("\n✓ Task added successfully!")
    print(f"ID: {task.id}")
    print(f"Title: {task.title}")
    if task.description:
        print(f"Description: {task.description}")
    print(f"Status: {'Complete' if task.status else 'Incomplete'}")
    print(f"Created: {task.created_at}")


def display_error(error_message: str) -> None:
    """
    Display an error message.

    Args:
        error_message: The error message to display
    """
    print(f"\nError: {error_message}")


def display_task(task: Task) -> None:
    """
    Display a single task with all details.

    Args:
        task: The task to display
    """
    print(f"\nTask #{task.id}")
    print(f"Title: {task.title}")

    if task.description:
        # Handle multiline descriptions
        if "\n" in task.description:
            print("Description:")
            for line in task.description.split("\n"):
                print(f"  {line}")
        else:
            print(f"Description: {task.description}")

    print(f"Status: {format_status(task.status)}")
    print(f"Created: {task.created_at}")


def display_task_list(tasks: list[Task]) -> None:
    """
    Display all tasks with summary.

    Args:
        tasks: List of tasks to display
    """
    print("\n" + "=" * 60)
    print("YOUR TODO LIST")
    print("=" * 60)

    if not tasks:
        print("\nYour todo list is empty. Use 'add' to create a task.")
    else:
        for i, task in enumerate(tasks):
            display_task(task)
            # Add separator between tasks (but not after last)
            if i < len(tasks) - 1:
                print("\n" + "-" * 60)

        # Display summary
        total = len(tasks)
        complete = sum(1 for t in tasks if t.status)
        incomplete = total - complete

        print("\n" + "=" * 60)
        print(f"Summary: {total} task(s) ({complete} complete, {incomplete} incomplete)")

    print("=" * 60)


# ============================================================
# COMMAND HANDLERS
# ============================================================


def handle_add_command(manager: TodoManager) -> None:
    """
    Handle the 'add' command to create a new task.

    Args:
        manager: The TodoManager instance
    """
    print("\n--- Add New Task ---")

    # Prompt for title
    title = input("Enter task title: ")

    # Prompt for description
    description = input("Enter task description (optional, press Enter to skip): ")

    # Convert empty description to None
    if not description:
        description = None

    # Add task
    task, error = manager.add_task(title, description)

    # Display result
    if task:
        display_task_success(task)
    else:
        display_error(error)


def handle_view_command(manager: TodoManager) -> None:
    """
    Handle the 'view' command to display all tasks.

    Args:
        manager: The TodoManager instance
    """
    tasks = manager.get_all_tasks()
    display_task_list(tasks)


def handle_delete_command(manager: TodoManager) -> None:
    """
    Handle the 'delete' command to remove a task.

    Args:
        manager: The TodoManager instance
    """
    print("\n--- Delete Task ---")

    # Prompt for task ID
    id_input = input("Enter task ID to delete: ")

    # Parse and validate ID
    task_id, error = parse_task_id(id_input)
    if error:
        display_error(error)
        return

    # Delete task
    deleted_task, error = manager.delete_task(task_id)

    # Display result
    if deleted_task:
        print(f"\nSuccess: Task deleted successfully!")
        print(f'Deleted: "{deleted_task.title}" (ID: {deleted_task.id})')
    else:
        display_error(error)


def handle_update_command(manager: TodoManager) -> None:
    """
    Handle the 'update' command to modify a task.

    Args:
        manager: The TodoManager instance
    """
    print("\n--- Update Task ---")

    # Prompt for task ID
    id_input = input("Enter task ID to update: ")

    # Parse and validate ID
    task_id, error = parse_task_id(id_input)
    if error:
        display_error(error)
        return

    # Get current task
    current_task = manager.get_task(task_id)
    if not current_task:
        display_error(f"Task with ID {task_id} not found")
        return

    # Display current task
    print("\nCurrent task:")
    display_task(current_task)

    # Prompt for new values
    print("\n--- Enter New Values (or press Enter to keep current) ---")
    new_title = input("Enter new title (or press Enter to keep current): ")
    new_description = input("Enter new description (or press Enter to keep current): ")

    # Convert empty inputs to None (keep current)
    new_title = new_title if new_title else None
    new_description = new_description if new_description else None

    # Update task
    updated_task, error, changes_made = manager.update_task(
        task_id, new_title, new_description
    )

    # Display result
    if error:
        display_error(error)
        print("Task not updated.")
    elif not changes_made:
        print(f"\nInfo: No changes made to task {task_id}")
    else:
        print(f"\nSuccess: Task updated successfully!")
        print(f"ID: {updated_task.id}")
        print(f"Title: {updated_task.title}")
        if updated_task.description:
            print(f"Description: {updated_task.description}")
        print(f"Status: {format_status(updated_task.status)}")


def handle_complete_command(manager: TodoManager) -> None:
    """
    Handle the 'complete' command to mark a task as complete.

    Args:
        manager: The TodoManager instance
    """
    print("\n--- Mark Task as Complete ---")

    # Prompt for task ID
    id_input = input("Enter task ID to mark as complete: ")

    # Parse and validate ID
    task_id, error = parse_task_id(id_input)
    if error:
        display_error(error)
        return

    # Mark task as complete
    task, error, status_changed = manager.mark_complete(task_id)

    # Display result
    if error:
        display_error(error)
    elif status_changed:
        print(f"\nSuccess: Task marked as complete!")
        print(f"ID: {task.id}")
        print(f"Title: {task.title}")
        print(f"Status: {format_status(task.status)}")
    else:
        print(f"\nSuccess: Task is already complete!")
        print(f"ID: {task.id}")
        print(f"Title: {task.title}")
        print(f"Status: {format_status(task.status)}")


def handle_incomplete_command(manager: TodoManager) -> None:
    """
    Handle the 'incomplete' command to mark a task as incomplete.

    Args:
        manager: The TodoManager instance
    """
    print("\n--- Mark Task as Incomplete ---")

    # Prompt for task ID
    id_input = input("Enter task ID to mark as incomplete: ")

    # Parse and validate ID
    task_id, error = parse_task_id(id_input)
    if error:
        display_error(error)
        return

    # Mark task as incomplete
    task, error, status_changed = manager.mark_incomplete(task_id)

    # Display result
    if error:
        display_error(error)
    elif status_changed:
        print(f"\nSuccess: Task marked as incomplete!")
        print(f"ID: {task.id}")
        print(f"Title: {task.title}")
        print(f"Status: {format_status(task.status)}")
    else:
        print(f"\nSuccess: Task is already incomplete!")
        print(f"ID: {task.id}")
        print(f"Title: {task.title}")
        print(f"Status: {format_status(task.status)}")


def main() -> None:
    """
    Main application loop.

    Displays menu, processes commands, and manages application flow.
    """
    # Initialize todo manager
    manager = TodoManager()

    print("\nWelcome to Todo App!")
    print("Note: All data is stored in memory and will be lost when you exit.")

    # Main loop
    while True:
        display_menu()

        # Get user command
        command = input("Enter command: ").strip().lower()

        # Route command
        if command == "add":
            handle_add_command(manager)
        elif command == "view":
            handle_view_command(manager)
        elif command == "update":
            handle_update_command(manager)
        elif command == "delete":
            handle_delete_command(manager)
        elif command == "complete":
            handle_complete_command(manager)
        elif command == "incomplete":
            handle_incomplete_command(manager)
        elif command == "quit" or command == "exit":
            print("\nGoodbye! All tasks have been cleared from memory.")
            break
        elif command == "":
            # Empty input, just show menu again
            continue
        else:
            print(f"\nError: Unknown command: '{command}'")
            print("Type 'view' to see available commands.")


if __name__ == "__main__":
    main()
