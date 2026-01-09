# Feature Specification: Add Task

**Feature ID**: 01
**Feature Name**: Add Task
**Status**: Approved
**Created**: 2026-01-10
**Dependencies**: None (foundational feature)

## Purpose

Enable users to create new todo tasks with a title and optional description. This is the foundational feature that establishes the Task data model and provides the primary method for populating the todo list.

## User Stories

### Primary User Story
**As a** user
**I want to** add a new task to my todo list
**So that** I can track things I need to do

### Secondary User Stories

**As a** user
**I want to** provide a descriptive title for my task
**So that** I can quickly identify what needs to be done

**As a** user
**I want to** optionally add a detailed description
**So that** I can capture additional context or notes about the task

**As a** user
**I want to** receive immediate confirmation when a task is added
**So that** I know my task was saved successfully

**As a** user
**I want to** see clear error messages if my input is invalid
**So that** I can correct my mistakes and successfully add the task

## Acceptance Criteria

### AC1: Successful Task Creation
**Given** the user provides a valid title
**When** the add task command is executed
**Then** a new task is created with:
- A unique, auto-generated ID
- The provided title
- An empty description (if not provided)
- Status set to incomplete (False)
- A timestamp of creation
**And** the user receives confirmation with the task ID

### AC2: Task with Description
**Given** the user provides a valid title and description
**When** the add task command is executed
**Then** a new task is created with both title and description
**And** the user receives confirmation

### AC3: Title Validation - Empty Title
**Given** the user provides an empty title or only whitespace
**When** the add task command is executed
**Then** the task is NOT created
**And** an error message is displayed: "Error: Title cannot be empty"

### AC4: Title Validation - Length Limit
**Given** the user provides a title longer than 200 characters
**When** the add task command is executed
**Then** the task is NOT created
**And** an error message is displayed: "Error: Title cannot exceed 200 characters (provided: X characters)"

### AC5: Description Length Limit
**Given** the user provides a description longer than 1000 characters
**When** the add task command is executed
**Then** the task is NOT created
**And** an error message is displayed: "Error: Description cannot exceed 1000 characters (provided: X characters)"

### AC6: Unique ID Generation
**Given** multiple tasks are created
**When** each add task command is executed
**Then** each task receives a unique, sequential ID starting from 1
**And** IDs are never reused

### AC7: Whitespace Handling
**Given** the user provides a title with leading/trailing whitespace
**When** the add task command is executed
**Then** the whitespace is stripped before validation
**And** if the resulting title is non-empty, the task is created

## Input/Output Examples

### Example 1: Basic Task (Title Only)
```
Input:
  Command: add
  Title: "Buy groceries"
  Description: (empty)

Output:
  ✓ Task added successfully!
  ID: 1
  Title: Buy groceries
  Status: Incomplete
  Created: 2026-01-10T14:30:00
```

### Example 2: Task with Description
```
Input:
  Command: add
  Title: "Finish project report"
  Description: "Include Q4 metrics and team feedback. Due Friday."

Output:
  ✓ Task added successfully!
  ID: 2
  Title: Finish project report
  Description: Include Q4 metrics and team feedback. Due Friday.
  Status: Incomplete
  Created: 2026-01-10T14:35:00
```

### Example 3: Empty Title Error
```
Input:
  Command: add
  Title: ""
  Description: (empty)

Output:
  ✗ Error: Title cannot be empty
```

### Example 4: Whitespace-Only Title Error
```
Input:
  Command: add
  Title: "   "
  Description: (empty)

Output:
  ✗ Error: Title cannot be empty
```

### Example 5: Title Too Long Error
```
Input:
  Command: add
  Title: "A" * 250
  Description: (empty)

Output:
  ✗ Error: Title cannot exceed 200 characters (provided: 250 characters)
```

### Example 6: Description Too Long Error
```
Input:
  Command: add
  Title: "Valid title"
  Description: "A" * 1500

Output:
  ✗ Error: Description cannot exceed 1000 characters (provided: 1500 characters)
```

### Example 7: Whitespace Trimming
```
Input:
  Command: add
  Title: "  Buy milk  "
  Description: (empty)

Output:
  ✓ Task added successfully!
  ID: 3
  Title: Buy milk
  Status: Incomplete
  Created: 2026-01-10T14:40:00
```

## Edge Cases and Error Handling

### Edge Case 1: Special Characters in Title
**Scenario**: User includes special characters (emoji, unicode, punctuation)
**Handling**: Accept all valid UTF-8 characters, count by character length not bytes
**Example**: "📝 Review code" is valid (13 characters)

### Edge Case 2: Newlines in Title
**Scenario**: User includes newline characters in title
**Handling**: Replace newlines with spaces, then trim and validate
**Example**: "Buy\nmilk" becomes "Buy milk"

### Edge Case 3: Newlines in Description
**Scenario**: User includes newline characters in description
**Handling**: Preserve newlines in description (multiline descriptions allowed)
**Example**: "Line 1\nLine 2" is stored as-is

### Edge Case 4: Maximum ID Reached
**Scenario**: Theoretical - ID counter reaches maximum integer value
**Handling**: Not applicable for in-memory app (would require billions of tasks)
**Note**: Document this limitation but don't implement special handling

### Edge Case 5: Concurrent ID Generation
**Scenario**: Multiple tasks created in rapid succession
**Handling**: Not applicable - single-threaded application, no concurrency
**Note**: IDs are assigned sequentially in order of creation

### Edge Case 6: Empty Description vs No Description
**Scenario**: User provides empty string "" vs not providing description at all
**Handling**: Treat both as "no description" - store as empty string ""
**Display**: Don't show description field if empty

## Data Requirements

### Task Data Model

```python
class Task:
    """
    Represents a single todo task.

    Attributes:
        id (int): Unique identifier, auto-generated, immutable
        title (str): Task title, required, 1-200 characters
        description (str): Optional details, 0-1000 characters
        status (bool): Completion status, False=incomplete, True=complete
        created_at (str): ISO 8601 timestamp, auto-generated, immutable
    """
    id: int
    title: str
    description: str
    status: bool
    created_at: str
```

### Validation Rules

| Field | Required | Type | Min Length | Max Length | Default | Mutable |
|-------|----------|------|------------|------------|---------|---------|
| id | Auto | int | N/A | N/A | Auto-increment | No |
| title | Yes | str | 1 (after trim) | 200 chars | None | Yes* |
| description | No | str | 0 | 1000 chars | "" | Yes* |
| status | Auto | bool | N/A | N/A | False | Yes* |
| created_at | Auto | str | N/A | N/A | Now (ISO 8601) | No |

*Mutable via Update Task feature (not implemented yet)

### ID Generation Strategy

- **Starting Value**: 1
- **Increment**: Sequential (+1 for each new task)
- **Persistence**: Counter maintained in TodoManager instance
- **Reuse**: Never reuse IDs, even after deletion
- **Type**: Positive integer (1, 2, 3, ...)

### Timestamp Format

- **Format**: ISO 8601 with timezone
- **Example**: "2026-01-10T14:30:00.123456"
- **Precision**: Microseconds
- **Timezone**: Local system timezone
- **Generation**: Use `datetime.now().isoformat()`

## User Interface Specification

### Command Structure

```
Command: add
Prompts:
  1. "Enter task title: "
  2. "Enter task description (optional, press Enter to skip): "
```

### Success Output Format

```
✓ Task added successfully!
ID: {id}
Title: {title}
[Description: {description}]  # Only shown if non-empty
Status: Incomplete
Created: {created_at}
```

### Error Output Format

```
✗ Error: {error_message}
```

### User Flow

1. User selects "add" command from main menu
2. System prompts for title
3. User enters title and presses Enter
4. System prompts for description
5. User enters description (or presses Enter to skip)
6. System validates inputs
7. If valid: Create task, display success message
8. If invalid: Display error message, return to main menu (do not re-prompt)

## Implementation Notes

### Module Responsibilities

**models.py**:
- Define Task class with validation
- Implement title validation (length, emptiness)
- Implement description validation (length)
- Handle whitespace trimming
- Generate timestamps

**todo_manager.py**:
- Maintain ID counter
- Store tasks in memory (list or dict)
- Implement add_task() method
- Handle ID generation
- Coordinate validation and storage

**main.py**:
- Display prompts to user
- Capture user input
- Call todo_manager.add_task()
- Display success/error messages
- Handle user flow

### Error Handling Strategy

- Validation errors raise custom `ValidationError` exception
- TodoManager catches validation errors and returns error message
- Main UI displays error message to user
- No stack traces shown to user (log internally if needed)

### Testing Checklist

- [ ] Create task with valid title only
- [ ] Create task with title and description
- [ ] Reject empty title
- [ ] Reject whitespace-only title
- [ ] Reject title > 200 characters
- [ ] Reject description > 1000 characters
- [ ] Trim leading/trailing whitespace from title
- [ ] Handle special characters in title
- [ ] Handle newlines in title (convert to spaces)
- [ ] Preserve newlines in description
- [ ] Generate unique sequential IDs
- [ ] Generate valid ISO 8601 timestamps
- [ ] Display success message with all task details
- [ ] Display clear error messages for each validation failure

## Dependencies

**None** - This is the foundational feature.

## Future Considerations

- This feature establishes the Task data model used by all other features
- ID generation strategy must be consistent across all features
- Validation rules defined here apply to Update Task feature
- Consider adding task priority or tags in future phases (not Phase I)

## Approval

**Specification Status**: ✓ Approved for Implementation
**Approved By**: Development Team
**Approval Date**: 2026-01-10

---

**Next Steps**:
1. Implement Task model in models.py
2. Implement TodoManager.add_task() in todo_manager.py
3. Implement add command UI in main.py
4. Test all acceptance criteria
5. Verify all edge cases
6. Proceed to Feature 02: Delete Task
