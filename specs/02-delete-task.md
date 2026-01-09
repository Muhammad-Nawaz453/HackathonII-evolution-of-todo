# Feature Specification: Delete Task

**Feature ID**: 02
**Feature Name**: Delete Task
**Status**: Approved
**Created**: 2026-01-10
**Dependencies**: Feature 01 (Add Task)

## Purpose

Enable users to permanently remove tasks from their todo list by specifying the task ID. This allows users to clean up completed tasks or remove tasks that are no longer relevant.

## User Stories

### Primary User Story
**As a** user
**I want to** delete a task by its ID
**So that** I can remove tasks I no longer need to track

### Secondary User Stories

**As a** user
**I want to** receive confirmation when a task is deleted
**So that** I know the deletion was successful

**As a** user
**I want to** see clear error messages if I try to delete a non-existent task
**So that** I understand what went wrong and can correct my input

**As a** user
**I want to** be prevented from accidentally deleting tasks
**So that** I don't lose important information (future enhancement: confirmation prompt)

## Acceptance Criteria

### AC1: Successful Task Deletion
**Given** a task exists with ID 5
**When** the user executes the delete command with ID 5
**Then** the task is permanently removed from the todo list
**And** the user receives a confirmation message with the deleted task's title
**And** the task cannot be retrieved afterward

### AC2: Delete Non-Existent Task
**Given** no task exists with ID 99
**When** the user executes the delete command with ID 99
**Then** no tasks are deleted
**And** an error message is displayed: "Error: Task with ID 99 not found"

### AC3: Invalid ID Format - Non-Numeric
**Given** the user provides a non-numeric ID (e.g., "abc")
**When** the user executes the delete command
**Then** no tasks are deleted
**And** an error message is displayed: "Error: Invalid task ID. Please provide a numeric ID"

### AC4: Invalid ID Format - Negative Number
**Given** the user provides a negative ID (e.g., -5)
**When** the user executes the delete command
**Then** no tasks are deleted
**And** an error message is displayed: "Error: Invalid task ID. Please provide a positive number"

### AC5: Invalid ID Format - Zero
**Given** the user provides ID 0
**When** the user executes the delete command
**Then** no tasks are deleted
**And** an error message is displayed: "Error: Invalid task ID. Please provide a positive number"

### AC6: Delete from Empty List
**Given** the todo list is empty
**When** the user executes the delete command with any ID
**Then** no tasks are deleted
**And** an error message is displayed: "Error: Task with ID X not found"

### AC7: ID Not Reused After Deletion
**Given** tasks with IDs 1, 2, 3 exist
**When** task with ID 2 is deleted
**And** a new task is added
**Then** the new task receives ID 4 (not ID 2)

## Input/Output Examples

### Example 1: Successful Deletion
```
Input:
  Command: delete
  Task ID: 3

Output:
  ✓ Task deleted successfully!
  Deleted: "Buy groceries" (ID: 3)
```

### Example 2: Task Not Found
```
Input:
  Command: delete
  Task ID: 99

Output:
  ✗ Error: Task with ID 99 not found
```

### Example 3: Non-Numeric ID
```
Input:
  Command: delete
  Task ID: abc

Output:
  ✗ Error: Invalid task ID. Please provide a numeric ID
```

### Example 4: Negative ID
```
Input:
  Command: delete
  Task ID: -5

Output:
  ✗ Error: Invalid task ID. Please provide a positive number
```

### Example 5: Zero ID
```
Input:
  Command: delete
  Task ID: 0

Output:
  ✗ Error: Invalid task ID. Please provide a positive number
```

### Example 6: Empty List
```
Input:
  Command: delete
  Task ID: 1

Output:
  ✗ Error: Task with ID 1 not found
```

### Example 7: Whitespace in ID Input
```
Input:
  Command: delete
  Task ID: "  5  "

Output:
  ✓ Task deleted successfully!
  Deleted: "Finish report" (ID: 5)

Note: Leading/trailing whitespace should be stripped before parsing
```

## Edge Cases and Error Handling

### Edge Case 1: Decimal Numbers
**Scenario**: User provides a decimal number (e.g., 3.5)
**Handling**: Reject as invalid - only integers are valid task IDs
**Error**: "Error: Invalid task ID. Please provide a numeric ID"

### Edge Case 2: Very Large Numbers
**Scenario**: User provides a very large number (e.g., 999999999999)
**Handling**: Accept as valid input, but will result in "not found" error
**Error**: "Error: Task with ID 999999999999 not found"

### Edge Case 3: Empty Input
**Scenario**: User presses Enter without providing an ID
**Handling**: Treat as invalid input
**Error**: "Error: Invalid task ID. Please provide a numeric ID"

### Edge Case 4: Multiple Numbers
**Scenario**: User provides multiple numbers (e.g., "1 2 3")
**Handling**: Reject as invalid - only one ID at a time
**Error**: "Error: Invalid task ID. Please provide a numeric ID"

### Edge Case 5: Special Characters
**Scenario**: User includes special characters (e.g., "#5", "ID:5")
**Handling**: Reject as invalid
**Error**: "Error: Invalid task ID. Please provide a numeric ID"

### Edge Case 6: Delete Last Remaining Task
**Scenario**: Only one task exists, user deletes it
**Handling**: Delete successfully, list becomes empty
**Success**: Normal deletion confirmation

## Data Requirements

### ID Validation Rules

| Input Type | Valid? | Action |
|------------|--------|--------|
| Positive integer (1, 2, 3...) | Yes | Attempt deletion |
| Zero | No | Error: positive number required |
| Negative integer | No | Error: positive number required |
| Decimal/float | No | Error: numeric ID required |
| Non-numeric string | No | Error: numeric ID required |
| Empty string | No | Error: numeric ID required |
| Whitespace only | No | Error: numeric ID required |

### Deletion Behavior

- **Permanent**: Deleted tasks cannot be recovered
- **Immediate**: Deletion takes effect immediately
- **ID Preservation**: Deleted task IDs are never reused
- **Counter Unchanged**: The next_id counter continues incrementing

### State Changes

**Before Deletion**:
```
Tasks: {1: Task(...), 2: Task(...), 3: Task(...)}
Next ID: 4
```

**After Deleting Task 2**:
```
Tasks: {1: Task(...), 3: Task(...)}
Next ID: 4 (unchanged)
```

**After Adding New Task**:
```
Tasks: {1: Task(...), 3: Task(...), 4: Task(...)}
Next ID: 5
```

## User Interface Specification

### Command Structure

```
Command: delete
Prompt: "Enter task ID to delete: "
```

### Success Output Format

```
✓ Task deleted successfully!
Deleted: "{title}" (ID: {id})
```

### Error Output Format

```
✗ Error: {error_message}
```

### User Flow

1. User selects "delete" command from main menu
2. System prompts for task ID
3. User enters task ID and presses Enter
4. System validates input format
5. If format invalid: Display error, return to main menu
6. If format valid: Attempt to find and delete task
7. If task found: Delete task, display success message
8. If task not found: Display error message
9. Return to main menu

## Implementation Notes

### Module Responsibilities

**models.py**:
- No changes required (Task model remains unchanged)
- Validation logic already exists

**todo_manager.py**:
- Implement `delete_task(task_id: int)` method
- Return tuple: (deleted_task, error_message)
- Handle task lookup and removal
- Preserve next_id counter

**main.py**:
- Implement `handle_delete_command()` function
- Prompt user for task ID
- Validate ID format (parse string to int)
- Call `todo_manager.delete_task()`
- Display success or error message

### ID Parsing Strategy

```python
def parse_task_id(id_string: str) -> tuple[Optional[int], Optional[str]]:
    """
    Parse a task ID from user input.

    Returns:
        (task_id, error_message)
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
```

### Error Handling Strategy

- Input validation errors: Return immediately with error message
- Task not found errors: Return after lookup attempt
- No exceptions thrown to user interface
- All errors communicated via return values

### Testing Checklist

- [ ] Delete existing task successfully
- [ ] Attempt to delete non-existent task
- [ ] Provide non-numeric ID (letters, symbols)
- [ ] Provide negative ID
- [ ] Provide zero as ID
- [ ] Provide decimal number as ID
- [ ] Provide empty input
- [ ] Provide whitespace-only input
- [ ] Delete from empty list
- [ ] Delete last remaining task
- [ ] Verify ID is not reused after deletion
- [ ] Verify next_id counter continues incrementing
- [ ] Strip whitespace from ID input
- [ ] Handle very large numbers gracefully

## Dependencies

**Depends On**:
- Feature 01 (Add Task): Must have tasks to delete

**Enables**:
- Feature 04 (View Tasks): Users need to see task IDs to delete them
- Complete task lifecycle management

## Future Considerations

- **Confirmation Prompt**: Add "Are you sure?" confirmation before deletion
- **Undo Deletion**: Implement undo functionality (requires history tracking)
- **Bulk Delete**: Delete multiple tasks at once
- **Delete by Criteria**: Delete all completed tasks, delete by title pattern
- **Soft Delete**: Mark as deleted instead of removing (requires status field)

## Approval

**Specification Status**: ✓ Approved for Implementation
**Approved By**: Development Team
**Approval Date**: 2026-01-10

---

**Next Steps**:
1. Implement ID parsing utility in main.py
2. Implement TodoManager.delete_task() in todo_manager.py
3. Implement handle_delete_command() in main.py
4. Update main menu to include delete command
5. Test all acceptance criteria
6. Verify all edge cases
7. Update README.md with delete command documentation
