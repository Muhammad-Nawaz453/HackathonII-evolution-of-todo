# Feature Specification: Update Task

**Feature ID**: 03
**Feature Name**: Update Task
**Status**: Approved
**Created**: 2026-01-10
**Dependencies**: Feature 01 (Add Task)

## Purpose

Enable users to modify the title and/or description of existing tasks. This allows users to correct mistakes, add more details, or update tasks as requirements change, without having to delete and recreate them.

## User Stories

### Primary User Story
**As a** user
**I want to** update a task's title or description
**So that** I can keep my task information accurate and current

### Secondary User Stories

**As a** user
**I want to** see the current values before updating
**So that** I know what I'm changing

**As a** user
**I want to** update only the title, only the description, or both
**So that** I have flexibility in what I change

**As a** user
**I want to** skip updating a field by pressing Enter
**So that** I can keep the current value without retyping it

**As a** user
**I want to** receive clear error messages if the task doesn't exist
**So that** I can correct my input

## Acceptance Criteria

### AC1: Update Title Only
**Given** a task exists with ID 5, title "Old Title", description "Old Description"
**When** the user updates task 5 with new title "New Title" and skips description
**Then** the task's title is changed to "New Title"
**And** the task's description remains "Old Description"
**And** a success message is displayed

### AC2: Update Description Only
**Given** a task exists with ID 5, title "My Title", description "Old Description"
**When** the user updates task 5, skips title, and provides new description "New Description"
**Then** the task's title remains "My Title"
**And** the task's description is changed to "New Description"
**And** a success message is displayed

### AC3: Update Both Title and Description
**Given** a task exists with ID 5
**When** the user updates task 5 with both new title and new description
**Then** both fields are updated
**And** a success message is displayed

### AC4: Skip Both Fields (No Changes)
**Given** a task exists with ID 5
**When** the user updates task 5 but skips both title and description
**Then** no changes are made to the task
**And** an informational message is displayed: "No changes made"

### AC5: Update Non-Existent Task
**Given** no task exists with ID 99
**When** the user attempts to update task 99
**Then** no tasks are modified
**And** an error message is displayed: "Error: Task with ID 99 not found"

### AC6: Invalid ID Format
**Given** the user provides an invalid ID (non-numeric, negative, zero)
**When** the user attempts to update
**Then** an error message is displayed (same as Delete Task feature)

### AC7: Title Validation on Update
**Given** a task exists with ID 5
**When** the user updates with an invalid title (empty, too long)
**Then** the update is rejected
**And** the original values are preserved
**And** an error message is displayed (same as Add Task validation)

### AC8: Description Validation on Update
**Given** a task exists with ID 5
**When** the user updates with an invalid description (too long)
**Then** the update is rejected
**And** the original values are preserved
**And** an error message is displayed (same as Add Task validation)

### AC9: Immutable Fields Preserved
**Given** a task exists with ID 5, created_at "2026-01-10T10:00:00"
**When** the user updates the task
**Then** the task's ID remains 5
**And** the task's created_at remains "2026-01-10T10:00:00"
**And** the task's status remains unchanged

### AC10: Whitespace Handling
**Given** a task exists with ID 5
**When** the user updates with title "  New Title  "
**Then** the title is trimmed to "New Title"
**And** the update succeeds

## Input/Output Examples

### Example 1: Update Title Only
```
Input:
  Command: update
  Task ID: 3
  Current: "Buy groceries" / "Milk and eggs"
  New Title: "Buy groceries and supplies"
  New Description: [Enter - skip]

Output:
  ✓ Task updated successfully!
  ID: 3
  Title: Buy groceries and supplies (updated)
  Description: Milk and eggs
  Status: Incomplete
```

### Example 2: Update Description Only
```
Input:
  Command: update
  Task ID: 3
  Current: "Buy groceries" / "Milk and eggs"
  New Title: [Enter - skip]
  New Description: "Milk, eggs, bread, and coffee"

Output:
  ✓ Task updated successfully!
  ID: 3
  Title: Buy groceries
  Description: Milk, eggs, bread, and coffee (updated)
  Status: Incomplete
```

### Example 3: Update Both Fields
```
Input:
  Command: update
  Task ID: 3
  Current: "Buy groceries" / "Milk and eggs"
  New Title: "Shopping list"
  New Description: "Weekly grocery shopping"

Output:
  ✓ Task updated successfully!
  ID: 3
  Title: Shopping list (updated)
  Description: Weekly grocery shopping (updated)
  Status: Incomplete
```

### Example 4: No Changes Made
```
Input:
  Command: update
  Task ID: 3
  Current: "Buy groceries" / "Milk and eggs"
  New Title: [Enter - skip]
  New Description: [Enter - skip]

Output:
  ℹ No changes made to task 3
```

### Example 5: Task Not Found
```
Input:
  Command: update
  Task ID: 99

Output:
  ✗ Error: Task with ID 99 not found
```

### Example 6: Invalid Title (Empty)
```
Input:
  Command: update
  Task ID: 3
  Current: "Buy groceries" / "Milk and eggs"
  New Title: "   "
  New Description: [Enter - skip]

Output:
  ✗ Error: Title cannot be empty
  Task not updated.
```

### Example 7: Invalid Title (Too Long)
```
Input:
  Command: update
  Task ID: 3
  Current: "Buy groceries" / "Milk and eggs"
  New Title: [250 characters]
  New Description: [Enter - skip]

Output:
  ✗ Error: Title cannot exceed 200 characters (provided: 250 characters)
  Task not updated.
```

### Example 8: Invalid Description (Too Long)
```
Input:
  Command: update
  Task ID: 3
  Current: "Buy groceries" / "Milk and eggs"
  New Title: [Enter - skip]
  New Description: [1500 characters]

Output:
  ✗ Error: Description cannot exceed 1000 characters (provided: 1500 characters)
  Task not updated.
```

## Edge Cases and Error Handling

### Edge Case 1: Update to Same Values
**Scenario**: User provides the exact same title and description
**Handling**: Accept as valid update (no-op, but not an error)
**Output**: Success message (don't indicate "no changes")

### Edge Case 2: Clear Description
**Scenario**: User wants to remove description entirely
**Handling**: Not supported in this version - skipping keeps current value
**Workaround**: User must delete and recreate task
**Future**: Add explicit "clear" option

### Edge Case 3: Partial Validation Failure
**Scenario**: User updates both fields, but only one is invalid
**Handling**: Reject entire update, preserve all original values
**Rationale**: Atomic updates - all or nothing

### Edge Case 4: Empty Task List
**Scenario**: No tasks exist, user tries to update
**Handling**: Same as "task not found" error

### Edge Case 5: Special Characters in Updated Values
**Scenario**: User includes emoji, unicode, newlines
**Handling**: Same validation as Add Task feature

### Edge Case 6: Very Long Current Values
**Scenario**: Current title/description are at max length
**Handling**: Display truncated in prompt, but allow full update

## Data Requirements

### Update Rules

| Field | Updatable? | Validation | Default on Skip |
|-------|-----------|------------|-----------------|
| id | No | N/A | Unchanged |
| title | Yes | Same as Add Task | Keep current |
| description | Yes | Same as Add Task | Keep current |
| status | No | N/A | Unchanged |
| created_at | No | N/A | Unchanged |

### Validation Reuse

- Title validation: Use `Task.validate_title()` from models.py
- Description validation: Use `Task.validate_description()` from models.py
- ID validation: Use same logic as Delete Task feature

### Update Behavior

- **Atomic**: All validations pass or no changes made
- **Selective**: Only specified fields are updated
- **Preserving**: Skipped fields retain current values
- **Immutable Fields**: ID, created_at, status never change

### State Changes

**Before Update**:
```
Task 3: {
  id: 3,
  title: "Buy groceries",
  description: "Milk and eggs",
  status: False,
  created_at: "2026-01-10T10:00:00"
}
```

**After Update (title only)**:
```
Task 3: {
  id: 3,
  title: "Shopping list",  # Changed
  description: "Milk and eggs",  # Unchanged
  status: False,  # Unchanged
  created_at: "2026-01-10T10:00:00"  # Unchanged
}
```

## User Interface Specification

### Command Structure

```
Command: update
Prompts:
  1. "Enter task ID to update: "
  2. Display current values
  3. "Enter new title (or press Enter to keep current): "
  4. "Enter new description (or press Enter to keep current): "
```

### Current Values Display Format

```
Current task:
  ID: {id}
  Title: {title}
  Description: {description}
  Status: {status}
```

### Success Output Format

```
✓ Task updated successfully!
ID: {id}
Title: {title} [(updated)]
Description: {description} [(updated)]
Status: {status}

Note: "(updated)" indicator only shown for fields that changed
```

### No Changes Output Format

```
ℹ No changes made to task {id}
```

### Error Output Format

```
✗ Error: {error_message}
Task not updated.
```

### User Flow

1. User selects "update" command from main menu
2. System prompts for task ID
3. User enters task ID
4. System validates ID format
5. If invalid: Display error, return to main menu
6. System looks up task by ID
7. If not found: Display error, return to main menu
8. System displays current task values
9. System prompts for new title
10. User enters new title or presses Enter to skip
11. System prompts for new description
12. User enters new description or presses Enter to skip
13. System validates new values (if provided)
14. If validation fails: Display error, return to main menu (no changes)
15. If no changes: Display "no changes" message
16. If changes valid: Update task, display success message
17. Return to main menu

## Implementation Notes

### Module Responsibilities

**models.py**:
- No new methods required
- Reuse existing validation methods
- Consider adding `update()` method to Task class (optional)

**todo_manager.py**:
- Implement `update_task(task_id, new_title, new_description)` method
- Parameters: task_id (int), new_title (Optional[str]), new_description (Optional[str])
- Return tuple: (updated_task, error_message, changes_made)
- Handle task lookup, validation, and update

**main.py**:
- Implement `handle_update_command()` function
- Reuse ID parsing logic from Delete Task
- Display current task values
- Prompt for new values
- Handle "skip" logic (empty input = keep current)
- Call `todo_manager.update_task()`
- Display appropriate message based on result

### Update Logic

```python
def update_task(
    task_id: int,
    new_title: Optional[str] = None,
    new_description: Optional[str] = None
) -> tuple[Optional[Task], Optional[str], bool]:
    """
    Update a task's title and/or description.

    Args:
        task_id: ID of task to update
        new_title: New title (None = keep current)
        new_description: New description (None = keep current)

    Returns:
        (task, error_message, changes_made)
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
```

### Skip Detection

- Empty string after strip() = skip (keep current value)
- None parameter = skip (not provided)
- Non-empty string = update attempt

### Error Handling Strategy

- ID validation errors: Return before lookup
- Task not found: Return after lookup
- Validation errors: Catch and return, preserve original task
- No exceptions thrown to user interface
- All errors communicated via return values

### Testing Checklist

- [ ] Update title only
- [ ] Update description only
- [ ] Update both title and description
- [ ] Skip both fields (no changes)
- [ ] Update non-existent task
- [ ] Invalid ID (non-numeric, negative, zero)
- [ ] Invalid title (empty, too long)
- [ ] Invalid description (too long)
- [ ] Update to same values
- [ ] Whitespace trimming in new title
- [ ] Newlines in new title (convert to spaces)
- [ ] Newlines in new description (preserve)
- [ ] Verify ID unchanged after update
- [ ] Verify created_at unchanged after update
- [ ] Verify status unchanged after update
- [ ] Empty input treated as skip
- [ ] Special characters handled correctly

## Dependencies

**Depends On**:
- Feature 01 (Add Task): Reuses validation logic
- Feature 02 (Delete Task): Reuses ID parsing logic

**Enables**:
- Complete task lifecycle management
- Users can refine tasks without recreating them

## Future Considerations

- **Explicit Clear Option**: Allow clearing description with special keyword
- **Update History**: Track changes over time (requires new data structure)
- **Undo Update**: Revert to previous values
- **Bulk Update**: Update multiple tasks at once
- **Update Status**: Move to Feature 05 (Mark Complete)
- **Confirmation Prompt**: Show changes and ask "Apply these changes?"

## Approval

**Specification Status**: ✓ Approved for Implementation
**Approved By**: Development Team
**Approval Date**: 2026-01-10

---

**Next Steps**:
1. Implement TodoManager.update_task() in todo_manager.py
2. Implement handle_update_command() in main.py
3. Update main menu to include update command
4. Test all acceptance criteria
5. Verify all edge cases
6. Update README.md with update command documentation
