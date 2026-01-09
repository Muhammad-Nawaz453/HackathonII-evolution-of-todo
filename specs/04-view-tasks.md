# Feature Specification: View Tasks

**Feature ID**: 04
**Feature Name**: View Tasks
**Status**: Approved
**Created**: 2026-01-10
**Dependencies**: Feature 01 (Add Task)

## Purpose

Enable users to view all tasks in their todo list with complete details. This is a foundational feature that allows users to see what tasks exist, check their status, and identify task IDs for other operations (delete, update, mark complete).

## User Stories

### Primary User Story
**As a** user
**I want to** view all my tasks in a clear, organized format
**So that** I can see what I need to do and track my progress

### Secondary User Stories

**As a** user
**I want to** see all task details (ID, title, description, status, created date)
**So that** I have complete information about each task

**As a** user
**I want to** easily distinguish between complete and incomplete tasks
**So that** I can focus on what still needs to be done

**As a** user
**I want to** see a helpful message when my list is empty
**So that** I know the command worked but there are no tasks

**As a** user
**I want to** see tasks in a consistent order
**So that** I can easily find specific tasks

## Acceptance Criteria

### AC1: View All Tasks
**Given** tasks exist with IDs 1, 2, 3
**When** the user executes the view command
**Then** all tasks are displayed with complete details
**And** tasks are shown in ascending order by ID
**And** each task shows: ID, title, description (if present), status, created date

### AC2: View Empty List
**Given** no tasks exist
**When** the user executes the view command
**Then** a message is displayed: "Your todo list is empty. Use 'add' to create a task."
**And** no task details are shown

### AC3: Task Display Format
**Given** tasks exist
**When** the user executes the view command
**Then** each task is clearly separated from others
**And** the status is clearly indicated (Complete/Incomplete)
**And** the format is consistent across all tasks

### AC4: Description Handling
**Given** a task has no description (empty string)
**When** the user views tasks
**Then** the description field is not displayed for that task
**And** tasks with descriptions show the full description

### AC5: Task Count Summary
**Given** tasks exist
**When** the user views tasks
**Then** a summary is displayed showing total task count
**And** the summary shows count of complete and incomplete tasks

### AC6: Long Description Display
**Given** a task has a very long description (e.g., 500 characters)
**When** the user views tasks
**Then** the full description is displayed
**And** the description is formatted for readability

### AC7: Multiline Description Display
**Given** a task has a description with newlines
**When** the user views tasks
**Then** the newlines are preserved in the display
**And** the description is properly indented

### AC8: Special Characters Display
**Given** a task contains special characters (emoji, unicode)
**When** the user views tasks
**Then** the special characters are displayed correctly

## Input/Output Examples

### Example 1: View Multiple Tasks
```
Input:
  Command: view

Output:
  ============================================================
  YOUR TODO LIST
  ============================================================

  Task #1
  Title: Buy groceries
  Description: Milk, eggs, bread, and coffee
  Status: Incomplete
  Created: 2026-01-10T10:00:00

  ------------------------------------------------------------

  Task #2
  Title: Finish project report
  Description: Include Q4 metrics and team feedback
  Status: Complete
  Created: 2026-01-10T10:15:00

  ------------------------------------------------------------

  Task #3
  Title: Call dentist
  Status: Incomplete
  Created: 2026-01-10T10:30:00

  ============================================================
  Summary: 3 tasks (1 complete, 2 incomplete)
  ============================================================
```

### Example 2: View Empty List
```
Input:
  Command: view

Output:
  ============================================================
  YOUR TODO LIST
  ============================================================

  Your todo list is empty. Use 'add' to create a task.

  ============================================================
```

### Example 3: View Single Task
```
Input:
  Command: view

Output:
  ============================================================
  YOUR TODO LIST
  ============================================================

  Task #1
  Title: Buy groceries
  Status: Incomplete
  Created: 2026-01-10T10:00:00

  ============================================================
  Summary: 1 task (0 complete, 1 incomplete)
  ============================================================
```

### Example 4: Task with Multiline Description
```
Input:
  Command: view

Output:
  ============================================================
  YOUR TODO LIST
  ============================================================

  Task #1
  Title: Project tasks
  Description:
    - Review code
    - Write tests
    - Update documentation
  Status: Incomplete
  Created: 2026-01-10T10:00:00

  ============================================================
  Summary: 1 task (0 complete, 1 incomplete)
  ============================================================
```

### Example 5: All Tasks Complete
```
Input:
  Command: view

Output:
  ============================================================
  YOUR TODO LIST
  ============================================================

  Task #1
  Title: Buy groceries
  Status: Complete
  Created: 2026-01-10T10:00:00

  ------------------------------------------------------------

  Task #2
  Title: Call dentist
  Status: Complete
  Created: 2026-01-10T11:00:00

  ============================================================
  Summary: 2 tasks (2 complete, 0 incomplete)
  ============================================================
```

## Edge Cases and Error Handling

### Edge Case 1: Very Long Title
**Scenario**: Task has title at maximum length (200 characters)
**Handling**: Display full title, may wrap to multiple lines
**Note**: Console width varies, let terminal handle wrapping

### Edge Case 2: Very Long Description
**Scenario**: Task has description at maximum length (1000 characters)
**Handling**: Display full description, may span many lines
**Note**: No truncation - users need to see complete information

### Edge Case 3: Empty Description vs No Description
**Scenario**: Task has empty string "" as description
**Handling**: Don't display description field (same as no description)
**Rationale**: Cleaner display, no value in showing empty field

### Edge Case 4: Many Tasks
**Scenario**: User has 50+ tasks
**Handling**: Display all tasks (no pagination in Phase I)
**Note**: Output may be very long, user can scroll
**Future**: Add pagination or filtering

### Edge Case 5: Non-Sequential IDs
**Scenario**: Tasks have IDs 1, 3, 7 (gaps from deletions)
**Handling**: Display in ascending ID order, gaps are normal
**Note**: Don't renumber or hide gaps

### Edge Case 6: Special Characters in Display
**Scenario**: Task contains emoji, unicode, or special symbols
**Handling**: Display as-is, rely on terminal support
**Note**: May not render correctly on all terminals (acceptable)

### Edge Case 7: Timestamp Format
**Scenario**: Timestamps are in ISO 8601 format with microseconds
**Handling**: Display full timestamp as stored
**Future**: Consider human-readable format (e.g., "2 hours ago")

## Data Requirements

### Display Fields

| Field | Always Show? | Format | Notes |
|-------|-------------|--------|-------|
| ID | Yes | "Task #{id}" | Header for each task |
| Title | Yes | "Title: {title}" | Always present |
| Description | Conditional | "Description: {desc}" | Only if non-empty |
| Status | Yes | "Status: Complete/Incomplete" | Clear text |
| Created | Yes | "Created: {timestamp}" | ISO 8601 format |

### Sort Order

- **Primary Sort**: ID (ascending)
- **Rationale**: Predictable, matches creation order
- **Future**: Add sort options (by status, by date, by title)

### Summary Calculation

```python
total_tasks = len(all_tasks)
complete_tasks = len([t for t in all_tasks if t.status])
incomplete_tasks = total_tasks - complete_tasks
```

### Formatting Constants

```python
SEPARATOR_FULL = "=" * 60
SEPARATOR_TASK = "-" * 60
INDENT_DESC = "  "  # For multiline descriptions
```

## User Interface Specification

### Command Structure

```
Command: view
(No additional prompts - displays immediately)
```

### Display Format Structure

```
{SEPARATOR_FULL}
YOUR TODO LIST
{SEPARATOR_FULL}

[For each task:]
Task #{id}
Title: {title}
[Description: {description}]  # Only if non-empty
Status: {Complete|Incomplete}
Created: {created_at}

{SEPARATOR_TASK}  # Between tasks

{SEPARATOR_FULL}
Summary: {total} task(s) ({complete} complete, {incomplete} incomplete)
{SEPARATOR_FULL}
```

### Empty List Format

```
{SEPARATOR_FULL}
YOUR TODO LIST
{SEPARATOR_FULL}

Your todo list is empty. Use 'add' to create a task.

{SEPARATOR_FULL}
```

### User Flow

1. User selects "view" command from main menu
2. System retrieves all tasks from TodoManager
3. If no tasks: Display empty list message
4. If tasks exist:
   - Display header
   - For each task (sorted by ID):
     - Display task details
     - Add separator between tasks
   - Display summary
5. Return to main menu

## Implementation Notes

### Module Responsibilities

**models.py**:
- No changes required
- Task model already has all needed fields

**todo_manager.py**:
- `get_all_tasks()` method already exists
- Returns list of tasks sorted by ID
- No additional methods needed

**main.py**:
- Implement `handle_view_command()` function
- Implement `display_task(task)` helper function
- Implement `display_task_list(tasks)` helper function
- Calculate and display summary statistics

### Display Helper Functions

```python
def display_task(task: Task) -> None:
    """Display a single task with all details."""
    print(f"\nTask #{task.id}")
    print(f"Title: {task.title}")

    if task.description:
        # Handle multiline descriptions
        if '\n' in task.description:
            print("Description:")
            for line in task.description.split('\n'):
                print(f"  {line}")
        else:
            print(f"Description: {task.description}")

    status_text = "Complete" if task.status else "Incomplete"
    print(f"Status: {status_text}")
    print(f"Created: {task.created_at}")


def display_task_list(tasks: list[Task]) -> None:
    """Display all tasks with summary."""
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
```

### Error Handling Strategy

- No user input validation needed (no parameters)
- No error cases (viewing always succeeds)
- Empty list is not an error, just a different display

### Testing Checklist

- [ ] View empty list
- [ ] View single task
- [ ] View multiple tasks
- [ ] View tasks with and without descriptions
- [ ] View tasks with multiline descriptions
- [ ] View all complete tasks
- [ ] View all incomplete tasks
- [ ] View mix of complete and incomplete
- [ ] Verify tasks sorted by ID
- [ ] Verify summary counts are correct
- [ ] View task with maximum length title
- [ ] View task with maximum length description
- [ ] View tasks with special characters
- [ ] View tasks with emoji
- [ ] Verify description field hidden when empty
- [ ] View tasks with non-sequential IDs (after deletions)

## Dependencies

**Depends On**:
- Feature 01 (Add Task): Must have tasks to view

**Enables**:
- Feature 02 (Delete Task): Users need to see IDs to delete
- Feature 03 (Update Task): Users need to see IDs to update
- Feature 05 (Mark Complete): Users need to see IDs to mark
- Essential for all task management operations

## Future Considerations

- **Filtering**: View only complete, only incomplete, by date range
- **Sorting**: Sort by status, date, title (alphabetical)
- **Pagination**: Display 10 tasks at a time for large lists
- **Search**: Find tasks by title or description keywords
- **Compact View**: Show only ID and title for quick scanning
- **Detailed View**: Show one task at a time with full details
- **Export**: Save task list to file
- **Human-Readable Dates**: "2 hours ago" instead of ISO timestamp
- **Color Coding**: Green for complete, red for incomplete (terminal colors)
- **Table Format**: Display tasks in a formatted table

## Approval

**Specification Status**: ✓ Approved for Implementation
**Approved By**: Development Team
**Approval Date**: 2026-01-10

---

**Next Steps**:
1. Implement display_task() helper in main.py
2. Implement display_task_list() helper in main.py
3. Implement handle_view_command() in main.py
4. Update main menu to include view command
5. Test all acceptance criteria
6. Verify all edge cases
7. Update README.md with view command documentation
