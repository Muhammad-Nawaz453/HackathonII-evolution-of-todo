# Example Conversations - Phase 3

This document provides example conversations for testing the AI-powered todo chatbot. Use these to verify natural language understanding and tool execution.

## Simple Task Creation

### Example 1: Basic Task

```
User: Add a task to buy groceries
Agent: ✓ I've added 'Buy groceries' to your task list.

Expected Tool Call: add_task(title="Buy groceries")
Expected Result: Task created with default priority (medium)
```

### Example 2: Task with Priority

```
User: Create a high priority task to review the quarterly report
Agent: ✓ I've created a high priority task: 'Review the quarterly report'.

Expected Tool Call: add_task(title="Review the quarterly report", priority="high")
Expected Result: Task created with high priority
```

### Example 3: Task with Due Date

```
User: Add a task to call the dentist tomorrow at 2 PM
Agent: ✓ I've added 'Call the dentist' due tomorrow at 2:00 PM.

Expected Tool Calls:
1. parse_date("tomorrow at 2 PM")
2. add_task(title="Call the dentist", due_date="2026-02-04T14:00:00Z")
Expected Result: Task created with correct due date
```

### Example 4: Task with All Details

```
User: Create a high priority work task to prepare client presentation by next Friday
Agent: ✓ I've created a high priority work task: 'Prepare client presentation' due Friday, February 7th.

Expected Tool Calls:
1. parse_date("next Friday")
2. add_task(title="Prepare client presentation", priority="high", category="work", due_date="2026-02-07T23:59:59Z")
Expected Result: Task created with all specified attributes
```

## Task Retrieval

### Example 5: List All Tasks

```
User: Show me my tasks
Agent: You have 5 tasks:
1. ☐ Buy groceries (medium priority)
2. ☐ Review quarterly report (high priority, due Friday)
3. ☑ Team standup (completed)
4. ☐ Prepare presentation (work, due Monday)
5. ☐ Call dentist (due tomorrow at 2:00 PM)

Expected Tool Call: get_tasks()
Expected Result: All tasks displayed with details
```

### Example 6: Filter by Priority

```
User: What are my high priority tasks?
Agent: You have 2 high priority tasks:
1. ☐ Review quarterly report (due Friday)
2. ☐ Client meeting (due tomorrow)

Expected Tool Call: get_tasks(priority="high")
Expected Result: Only high priority tasks shown
```

### Example 7: Filter by Status

```
User: Show me incomplete tasks
Agent: You have 4 incomplete tasks:
1. ☐ Buy groceries
2. ☐ Review quarterly report (due Friday)
3. ☐ Prepare presentation (due Monday)
4. ☐ Call dentist (due tomorrow)

Expected Tool Call: get_tasks(status="incomplete")
Expected Result: Only incomplete tasks shown
```

### Example 8: Filter by Date

```
User: What's due today?
Agent: You have 2 tasks due today:
1. ☐ Team standup (9:00 AM)
2. ☐ Submit timesheet (5:00 PM)

Expected Tool Call: get_tasks_by_date(date="today")
Expected Result: Only today's tasks shown
```

## Task Search

### Example 9: Keyword Search

```
User: Find tasks about the report
Agent: I found 2 tasks matching 'report':
1. ☐ Review quarterly report (high priority, due Friday)
2. ☐ Submit expense report (due next week)

Expected Tool Call: search_tasks(query="report")
Expected Result: Tasks containing "report" in title or description
```

### Example 10: Search with No Results

```
User: Search for tasks about vacation
Agent: I didn't find any tasks matching 'vacation'. Would you like to create one?

Expected Tool Call: search_tasks(query="vacation")
Expected Result: Empty results, helpful suggestion
```

## Task Updates

### Example 11: Update Title

```
User: Change the grocery task to 'Buy groceries and cook dinner'
Agent: ✓ I've updated the task to 'Buy groceries and cook dinner'.

Expected Tool Calls:
1. search_tasks(query="grocery")
2. update_task(task_id="123", title="Buy groceries and cook dinner")
Expected Result: Task title updated
```

### Example 12: Update Priority

```
User: Make the report task high priority
Agent: ✓ I've set 'Review quarterly report' to high priority.

Expected Tool Calls:
1. search_tasks(query="report")
2. update_task(task_id="456", priority="high")
Expected Result: Task priority updated
```

### Example 13: Reschedule Task

```
User: Reschedule the dentist appointment to next Monday at 10 AM
Agent: ✓ I've rescheduled 'Call dentist' to Monday, February 10th at 10:00 AM.

Expected Tool Calls:
1. search_tasks(query="dentist")
2. parse_date("next Monday at 10 AM")
3. update_task(task_id="789", due_date="2026-02-10T10:00:00Z")
Expected Result: Task due date updated
```

## Task Completion

### Example 14: Mark Complete

```
User: Mark the grocery task as done
Agent: ✓ I've marked 'Buy groceries' as complete. Great job!

Expected Tool Calls:
1. search_tasks(query="grocery")
2. mark_task_complete(task_id="123")
Expected Result: Task marked complete
```

### Example 15: Mark Incomplete

```
User: Unmark the standup task
Agent: ✓ I've marked 'Team standup' as incomplete.

Expected Tool Calls:
1. search_tasks(query="standup")
2. mark_task_incomplete(task_id="456")
Expected Result: Task marked incomplete
```

## Task Deletion

### Example 16: Delete Single Task

```
User: Delete the grocery task
Agent: ✓ I've deleted 'Buy groceries'.

Expected Tool Calls:
1. search_tasks(query="grocery")
2. delete_task(task_id="123")
Expected Result: Task deleted
```

### Example 17: Bulk Delete with Confirmation

```
User: Delete all completed tasks
Agent: ⚠️ This will delete 5 completed tasks. Are you sure?
User: Yes
Agent: ✓ I've deleted 5 completed tasks.

Expected Tool Calls:
1. get_tasks(status="complete")
2. [Wait for confirmation]
3. bulk_delete_tasks(filter={status: "complete"})
Expected Result: Multiple tasks deleted after confirmation
```

## Multi-Turn Conversations

### Example 18: Task Refinement

```
User: Add a task to prepare presentation
Agent: ✓ I've added 'Prepare presentation' to your tasks.

User: Make it high priority
Agent: ✓ I've set 'Prepare presentation' to high priority.

User: And due Monday at 2 PM
Agent: ✓ I've set the due date to Monday, February 10th at 2:00 PM.

Expected Behavior: Agent remembers "Prepare presentation" from context
```

### Example 19: Clarification Flow

```
User: Update the meeting
Agent: I found 3 tasks with 'meeting'. Which one would you like to update?
1. Team standup meeting (due today)
2. Client meeting (due tomorrow)
3. Project review meeting (due Friday)

User: The client one
Agent: Got it. What would you like to update about 'Client meeting'?

User: Change it to 3 PM
Agent: ✓ I've rescheduled 'Client meeting' to 3:00 PM.

Expected Behavior: Agent handles ambiguity by asking clarifying questions
```

### Example 20: Context Switching

```
User: Show me my tasks
Agent: [Shows 5 tasks]

User: Which ones are high priority?
Agent: Of those tasks, 3 are high priority:
1. Review quarterly report
2. Client meeting
3. Prepare presentation

User: Mark the first one as done
Agent: ✓ I've marked 'Review quarterly report' as complete.

Expected Behavior: Agent maintains context across multiple turns
```

## Error Handling

### Example 21: Task Not Found

```
User: Delete task 999
Agent: I couldn't find a task with ID 999. Would you like me to show you your current tasks?

User: Yes
Agent: [Shows task list]

Expected Behavior: Graceful error handling with helpful suggestion
```

### Example 22: Invalid Date

```
User: Add a task due on Blursday
Agent: I couldn't understand the date 'Blursday'. Could you specify the date in a different way? For example: 'tomorrow', 'next Friday', or '2026-02-10'.

User: Next Friday
Agent: ✓ I've added the task due Friday, February 7th.

Expected Behavior: Agent asks for clarification on invalid input
```

### Example 23: Missing Information

```
User: Add a task
Agent: Sure! What should the task be about?

User: Prepare quarterly report
Agent: ✓ I've added 'Prepare quarterly report'. Would you like to set a priority or due date?

User: High priority, due Friday
Agent: ✓ Updated to high priority, due Friday.

Expected Behavior: Agent prompts for missing required information
```

## Complex Scenarios

### Example 24: Multiple Operations

```
User: Show me all my work tasks that are incomplete and high priority
Agent: You have 2 incomplete high priority work tasks:
1. ☐ Review quarterly report (due Friday)
2. ☐ Prepare client presentation (due Monday)

Expected Tool Call: get_tasks(status="incomplete", priority="high", category="work")
Expected Result: Filtered task list
```

### Example 25: Natural Language Date Range

```
User: What tasks do I have this week?
Agent: You have 4 tasks this week:
1. ☐ Team standup (today at 9:00 AM)
2. ☐ Client meeting (tomorrow at 3:00 PM)
3. ☐ Review quarterly report (Friday)
4. ☐ Submit timesheet (Friday at 5:00 PM)

Expected Tool Calls:
1. parse_date("this week") → date range
2. get_tasks_by_date(date_from="2026-02-03", date_to="2026-02-09")
Expected Result: Tasks within the week
```

### Example 26: Bulk Update

```
User: Move all my personal tasks to low priority
Agent: I found 3 personal tasks. Change all to low priority?
User: Yes
Agent: ✓ I've updated 3 tasks to low priority.

Expected Tool Calls:
1. get_tasks(category="personal")
2. [For each task] update_task(task_id=X, priority="low")
Expected Result: Multiple tasks updated
```

## Testing Checklist

Use this checklist to verify all conversation patterns work:

- [ ] Simple task creation
- [ ] Task with priority
- [ ] Task with due date
- [ ] Task with category
- [ ] Task with all details
- [ ] List all tasks
- [ ] Filter by priority
- [ ] Filter by status
- [ ] Filter by category
- [ ] Filter by date
- [ ] Keyword search
- [ ] Update title
- [ ] Update priority
- [ ] Update due date
- [ ] Update category
- [ ] Mark complete
- [ ] Mark incomplete
- [ ] Delete single task
- [ ] Bulk delete with confirmation
- [ ] Multi-turn conversation
- [ ] Context retention
- [ ] Clarification questions
- [ ] Error handling (not found)
- [ ] Error handling (invalid date)
- [ ] Error handling (missing info)
- [ ] Complex filters
- [ ] Natural language dates
- [ ] Bulk operations

## Notes for Testing

1. **Test in Order**: Start with simple patterns, then move to complex ones
2. **Verify Tool Calls**: Check that correct tools are called with correct parameters
3. **Check UI Updates**: Verify task list updates in real-time
4. **Test Edge Cases**: Try typos, ambiguous queries, invalid inputs
5. **Test Context**: Verify multi-turn conversations maintain context
6. **Test Mobile**: Verify all patterns work on mobile devices

## Expected Accuracy

- **Intent Recognition**: >90% accuracy
- **Entity Extraction**: >85% accuracy
- **Date Parsing**: >95% accuracy
- **Tool Selection**: >95% accuracy

If accuracy is below targets, refine the system prompt in `backend/src/agent_setup.py`.
