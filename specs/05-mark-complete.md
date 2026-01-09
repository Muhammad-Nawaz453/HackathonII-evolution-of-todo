# Feature Specification: Mark Complete/Incomplete

**Feature ID**: 05
**Feature Name**: Mark Complete/Incomplete
**Status**: Approved
**Created**: 2026-01-10
**Dependencies**: Feature 01 (Add Task), Feature 04 (View Tasks)

## Purpose

Enable users to mark tasks as complete when finished, or mark them as incomplete if they need to work on them again. This provides task status management and allows users to track their progress.

## User Stories

### Primary User Stories

**As a** user
**I want to** mark a task as complete
**So that** I can track what I've finished

**As a** user
**I want to** mark a task as incomplete
**So that** I can reopen tasks that need more work

### Secondary User Stories

**As a** user
**I want to** receive confirmation when I change a task's status
**So that** I know the change was successful

**As a** user
**I want to** see the task's new status after marking
**So that** I can verify the change

**As a** user
**I want to** mark already-complete tasks as complete without errors
**So that** the command is forgiving (idempotent)

**As a** user
**I want to** mark already-incomplete tasks as incomplete without errors
**So that** the command is forgiving (idempotent)

## Acceptance Criteria

### AC1: Mark Incomplete Task as Complete
**Given** a task exists with ID 5 and status is incomplete
**When** the user executes the complete command with ID 5
**Then** the task's status is changed to complete
**And** a success message is displayed
**And** the task's other fields remain unchanged

### AC2: Mark Complete Task as Incomplete
**Given** a task exists with ID 5 and status is complete
**When** the user executes the incomplete command with ID 5
**Then** the task's status is changed to incomplete
**And** a success message is displayed
**And** the task's other fields remain unchanged

### AC3: Mark Already-Complete Task as Complete (Idempotent)
**Given** a task exists with ID 5 and status is already complete
**When** the user executes the complete command with ID 5
**Then** the task's status remains complete
**And** a success message is displayed (not an error)
**And** the message indicates the task was already complete

### AC4: Mark Already-Incomplete Task as Incomplete (Idempotent)
**Given** a task exists with ID 5 and status is already incomplete
**When** the user executes the incomplete command with ID 5
**Then** the task's status remains incomplete
**And** a success message is displayed (not an error)
**And** the message indicates the task was already incomplete

### AC5: Mark Non-Existent Task
**Given** no task exists with ID 99
**When** the user executes complete or incomplete command with ID 99
**Then** no tasks are modified
**And** an error message is displayed: "Error: Task with ID 99 not found"

### AC6: Invalid ID Format
**Given** the user provides an invalid ID (non-numeric, negative, zero)
**When** the user executes complete or incomplete command
**Then** an error message is displayed (same as Delete Task feature)

### AC7: Immutable Fields Preserved
**Given** a task exists with ID 5
**When** the user marks it as complete or incomplete
**Then** the task's ID, title, description, and created_at remain unchanged
**And** only the status field is modified

## Input/Output Examples

### Example 1: Mark Task as Complete
```
Input:
  Command: complete
  Task ID: 3

Output:
  ✓ Task marked as complete!
  ID: 3
  Title: Buy groceries
  Status: Complete ✓
```

### Example 2: Mark Task as Incomplete
```
Input:
  Command: incomplete
  Task ID: 3

Output:
  ✓ Task marked as incomplete!
  ID: 3
  Title: Buy groceries
  Status: Incomplete
```

### Example 3: Mark Already-Complete Task as Complete
```
Input:
  Command: complete
  Task ID: 3

Output:
  ✓ Task is already complete!
  ID: 3
  Title: Buy groceries
  Status: Complete ✓
```

### Example 4: Mark Already-Incomplete Task as Incomplete
```
Input:
  Command: incomplete
  Task ID: 3

Output:
  ✓ Task is already incomplete!
  ID: 3
  Title: Buy groceries
  Status: Incomplete
```

### Example 5: Task Not Found
```
Input:
  Command: complete
  Task ID: 99

Output:
  ✗ Error: Task with ID 99 not found
```

### Example 6: Invalid ID
```
Input:
  Command: complete
  Task ID: abc

Output:
  ✗ Error: Invalid task ID. Please provide a numeric ID
```

## Edge Cases and Error Handling

### Edge Case 1: Rapid Status Changes
**Scenario**: User marks task complete, then immediately marks it incomplete
**Handling**: Both operations succeed, final state is incomplete
**Note**: No history tracking in Phase I

### Edge Case 2: Empty Task List
**Scenario**: No tasks exist, user tries to mark task
**Handling**: Same as "task not found" error

### Edge Case 3: Whitespace in ID Input
**Scenario**: User provides "  5  " as ID
**Handling**: Strip whitespace, parse as 5, succeed
**Note**: Same as Delete/Update features

### Edge Case 4: Multiple Commands in Sequence
**Scenario**: User marks multiple tasks in a row
**Handling**: Each command is independent, all succeed
**Note**: No batch operations in Phase I

### Edge Case 5: Status Display Consistency
**Scenario**: Status must be displayed consistently across all features
**Handling**: Use "Complete" and "Incomplete" everywhere
**Note**: View Tasks feature uses same terminology

## Data Requirements

### Status Field

| Value | Meaning | Display Text | Symbol |
|-------|---------|--------------|--------|
| True | Complete | "Complete" | ✓ |
| False | Incomplete | "Incomplete" | (none) |

### State Transitions

```
Incomplete (False) --[complete command]--> Complete (True)
Complete (True) --[incomplete command]--> Incomplete (False)
Incomplete (False) --[incomplete command]--> Incomplete (False) [idempotent]
Complete (True) --[complete command]--> Complete (True) [idempotent]
```

### Immutable Fields

When marking complete/incomplete:
- ID: Never changes
- Title: Never changes
- Description: Never changes
- Created_at: Never changes
- Status: Only field that changes

### State Changes

**Before Mark Complete**:
```
Task 3: {
  id: 3,
  title: "Buy groceries",
  description: "Milk and eggs",
  status: False,  # Incomplete
  created_at: "2026-01-10T10:00:00"
}
```

**After Mark Complete**:
```
Task 3: {
  id: 3,
  title: "Buy groceries",
  description: "Milk and eggs",
  status: True,  # Complete
  created_at: "2026-01-10T10:00:00"
}
```

## User Interface Specification

### Command Structure

```
Command: complete
Prompt: "Enter task ID to mark as complete: "

Command: incomplete
Prompt: "Enter task ID to mark as incomplete: "
```

### Success Output Format (Status Changed)

```
✓ Task marked as {complete|incomplete}!
ID: {id}
Title: {title}
Status: {Complete ✓|Incomplete}
```

### Success Output Format (Already in Target State)

```
✓ Task is already {complete|incomplete}!
ID: {id}
Title: {title}
Status: {Complete ✓|Incomplete}
```

### Error Output Format

```
✗ Error: {error_message}
```

### User Flow

1. User selects "complete" or "incomplete" command from main menu
2. System prompts for task ID
3. User enters task ID
4. System validates ID format
5. If invalid: Display error, return to main menu
6. System looks up task by ID
7. If not found: Display error, return to main menu
8. System checks current status
9. If already in target state: Display "already" message
10. If not in target state: Update status, display success message
11. Return to main menu

## Implementation Notes

### Module Responsibilities

**models.py**:
- No changes required
- Status field already exists as boolean

**todo_manager.py**:
- Implement `mark_complete(task_id)` method
- Implement `mark_incomplete(task_id)` method
- Return tuple: (task, error_message, status_changed)
- Handle task lookup and status update

**main.py**:
- Implement `handle_complete_command()` function
- Implement `handle_incomplete_command()` function
- Reuse ID parsing logic from Delete Task
- Display appropriate message based on result
- Update main menu to include both commands

### Mark Complete Logic

```python
def mark_complete(self, task_id: int) -> tuple[Optional[Task], Optional[str], bool]:
    """
    Mark a task as complete.

    Args:
        task_id: ID of task to mark complete

    Returns:
        (task, error_message, status_changed)
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
```

### Mark Incomplete Logic

```python
def mark_incomplete(self, task_id: int) -> tuple[Optional[Task], Optional[str], bool]:
    """
    Mark a task as incomplete.

    Args:
        task_id: ID of task to mark incomplete

    Returns:
        (task, error_message, status_changed)
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
```

### Display Logic

```python
def display_mark_result(task: Task, command: str, status_changed: bool) -> None:
    """
    Display result of marking task complete/incomplete.

    Args:
        task: The task that was marked
        command: "complete" or "incomplete"
        status_changed: Whether status actually changed
    """
    if status_changed:
        print(f"\n✓ Task marked as {command}!")
    else:
        print(f"\n✓ Task is already {command}!")

    print(f"ID: {task.id}")
    print(f"Title: {task.title}")

    status_text = "Complete ✓" if task.status else "Incomplete"
    print(f"Status: {status_text}")
```

### Error Handling Strategy

- ID validation errors: Return before lookup (reuse Delete logic)
- Task not found: Return after lookup
- No validation errors for status (boolean field, always valid)
- Idempotent operations: Not an error, just different message
- All errors communicated via return values

### Testing Checklist

- [ ] Mark incomplete task as complete
- [ ] Mark complete task as incomplete
- [ ] Mark already-complete task as complete (idempotent)
- [ ] Mark already-incomplete task as incomplete (idempotent)
- [ ] Mark non-existent task
- [ ] Invalid ID (non-numeric, negative, zero)
- [ ] Empty task list
- [ ] Whitespace in ID input
- [ ] Verify only status field changes
- [ ] Verify ID unchanged
- [ ] Verify title unchanged
- [ ] Verify description unchanged
- [ ] Verify created_at unchanged
- [ ] Mark multiple tasks in sequence
- [ ] Toggle task status back and forth

## Dependencies

**Depends On**:
- Feature 01 (Add Task): Must have tasks to mark
- Feature 04 (View Tasks): Users need to see task IDs and current status

**Enables**:
- Complete task lifecycle management
- Progress tracking
- Task filtering (future: view only complete/incomplete)

## Future Considerations

- **Toggle Command**: Single command that switches status automatically
- **Completion Timestamp**: Track when task was completed
- **Completion History**: Track all status changes over time
- **Bulk Operations**: Mark multiple tasks at once
- **Mark by Criteria**: Complete all tasks matching a pattern
- **Undo**: Revert status change
- **Statistics**: Show completion rate, average time to complete
- **Recurring Tasks**: Auto-recreate task when marked complete
- **Subtasks**: Mark parent complete only when all subtasks complete

## Approval

**Specification Status**: ✓ Approved for Implementation
**Approved By**: Development Team
**Approval Date**: 2026-01-10

---

**Next Steps**:
1. Implement TodoManager.mark_complete() in todo_manager.py
2. Implement TodoManager.mark_incomplete() in todo_manager.py
3. Implement handle_complete_command() in main.py
4. Implement handle_incomplete_command() in main.py
5. Update main menu to include complete and incomplete commands
6. Test all acceptance criteria
7. Verify all edge cases
8. Update README.md with complete/incomplete command documentation
