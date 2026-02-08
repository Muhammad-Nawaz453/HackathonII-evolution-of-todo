# Specification: Natural Language Flows and Conversation Patterns

**Feature ID**: PHASE3-05
**Status**: Draft
**Created**: 2026-02-03
**Dependencies**: Phase 3 Specs 01-04 (All previous specs)

## Purpose

Define comprehensive natural language conversation patterns that the AI agent must support, including intent recognition, entity extraction, multi-turn conversations, ambiguity resolution, and error recovery. This specification serves as the acceptance criteria for natural language understanding and ensures the chatbot can handle real-world user interactions.

## User Stories

**As a user**, I want to:
1. Create tasks using natural language without remembering specific syntax
2. Update tasks by describing what I want to change in plain English
3. Search for tasks using conversational queries
4. Have the AI understand dates like "tomorrow", "next Friday", "in 2 hours"
5. Get helpful responses when my request is ambiguous
6. Receive confirmation when the AI performs actions
7. Have multi-step conversations where the AI remembers context

**As a developer**, I want to:
1. Define clear patterns for each type of user intent
2. Specify how the agent should handle ambiguous requests
3. Document expected conversation flows for testing
4. Ensure consistent agent behavior across similar queries
5. Provide examples for training and validation

## Acceptance Criteria

### AC1: Task Creation Flows
- [ ] Simple creation: "Add a task to buy groceries"
- [ ] Creation with priority: "Create a high priority task to review the report"
- [ ] Creation with category: "Add a work task to prepare presentation"
- [ ] Creation with due date: "Add task to call dentist tomorrow at 2 PM"
- [ ] Creation with all details: "Create a high priority personal task to renew passport by next Friday"

### AC2: Task Retrieval Flows
- [ ] List all: "Show me my tasks" / "What do I need to do?"
- [ ] Filter by status: "Show me incomplete tasks" / "What have I completed?"
- [ ] Filter by priority: "Show me high priority tasks" / "What's urgent?"
- [ ] Filter by category: "Show me work tasks" / "What personal tasks do I have?"
- [ ] Filter by date: "What's due today?" / "Show me this week's tasks"

### AC3: Task Update Flows
- [ ] Update title: "Change the grocery task to 'Buy groceries and cook dinner'"
- [ ] Update priority: "Make the report task high priority"
- [ ] Update due date: "Reschedule the meeting to tomorrow at 3 PM"
- [ ] Update category: "Move the dentist task to personal"
- [ ] Update multiple fields: "Change the presentation task to high priority and due Monday"

### AC4: Task Completion Flows
- [ ] Mark complete: "Mark the grocery task as done" / "I finished the report"
- [ ] Mark incomplete: "Unmark the standup task" / "I didn't finish the presentation"
- [ ] Bulk complete: "Mark all my tasks from yesterday as complete"

### AC5: Task Deletion Flows
- [ ] Delete single: "Delete the grocery task" / "Remove the meeting"
- [ ] Delete with confirmation: "Delete all completed tasks" → AI asks for confirmation
- [ ] Delete by filter: "Delete all low priority tasks from last month"

### AC6: Search Flows
- [ ] Keyword search: "Find tasks about the report" / "Search for meeting tasks"
- [ ] Fuzzy search: "Show me tasks with 'grocry'" (typo handling)
- [ ] Multi-word search: "Find tasks related to client presentation"

### AC7: Date Understanding
- [ ] Relative dates: "tomorrow", "next week", "in 3 days"
- [ ] Day names: "Monday", "next Friday", "this Saturday"
- [ ] Times: "at 2 PM", "at 10:30 AM", "in the morning"
- [ ] Date ranges: "this week", "next month", "by Friday"

### AC8: Ambiguity Resolution
- [ ] Multiple matches: AI presents options when multiple tasks match
- [ ] Missing information: AI asks for required details
- [ ] Unclear intent: AI asks clarifying questions
- [ ] Confirmation for destructive actions: AI confirms before bulk deletes

### AC9: Multi-Turn Conversations
- [ ] Context retention: AI remembers previous messages in conversation
- [ ] Follow-up questions: User can reference "that task" or "the meeting"
- [ ] Refinement: User can clarify or correct previous requests
- [ ] Chained operations: Multiple operations in sequence

### AC10: Error Handling
- [ ] Task not found: AI suggests search or list alternatives
- [ ] Invalid date: AI asks for clarification
- [ ] Missing required info: AI prompts for details
- [ ] Tool failure: AI explains issue and suggests retry

## Conversation Flow Patterns

### Pattern 1: Simple Task Creation

**User Intent**: Create a basic task

**Example Conversations**:

```
User: "Add a task to buy groceries"
Agent: [Calls add_task(title="Buy groceries")]
Agent: "✓ I've added 'Buy groceries' to your task list."

User: "Create a task for team meeting"
Agent: [Calls add_task(title="Team meeting")]
Agent: "✓ I've created 'Team meeting' as a task."

User: "Remind me to call mom"
Agent: [Calls add_task(title="Call mom")]
Agent: "✓ I've added 'Call mom' to your tasks."
```

**Intent Patterns**:
- "add [a] task [to] {title}"
- "create [a] task [for] {title}"
- "remind me to {title}"
- "I need to {title}"

**Entity Extraction**:
- `title`: Everything after trigger words (add/create/remind)

### Pattern 2: Task Creation with Details

**User Intent**: Create task with priority, category, or due date

**Example Conversations**:

```
User: "Add a high priority task to review the Q1 report by Friday"
Agent: [Calls parse_date("Friday")]
Agent: [Calls add_task(title="Review the Q1 report", priority="high", due_date="2026-02-07T23:59:59Z")]
Agent: "✓ I've created a high priority task: 'Review the Q1 report' due Friday, February 7th."

User: "Create a work task to prepare client presentation for next Monday at 2 PM"
Agent: [Calls parse_date("next Monday at 2 PM")]
Agent: [Calls add_task(title="Prepare client presentation", category="work", due_date="2026-02-10T14:00:00Z")]
Agent: "✓ I've created a work task: 'Prepare client presentation' due Monday, February 10th at 2:00 PM."

User: "Add a low priority personal task to renew passport"
Agent: [Calls add_task(title="Renew passport", priority="low", category="personal")]
Agent: "✓ I've added a low priority personal task: 'Renew passport'."
```

**Intent Patterns**:
- "{priority} priority task [to] {title}"
- "{category} task [to] {title}"
- "task [to] {title} [by/on] {date}"
- "{priority} {category} task [to] {title} [by] {date}"

**Entity Extraction**:
- `priority`: "high", "medium", "low", "urgent", "important"
- `category`: "work", "personal", "shopping", "health", etc.
- `due_date`: Natural language date expressions
- `title`: Main task description

### Pattern 3: Task Retrieval with Filters

**User Intent**: View tasks with specific criteria

**Example Conversations**:

```
User: "Show me my tasks"
Agent: [Calls get_tasks()]
Agent: "You have 5 tasks:
1. ☐ Buy groceries (medium priority)
2. ☐ Review Q1 report (high priority, due Friday)
3. ☑ Team standup (completed)
4. ☐ Prepare presentation (work, due Monday)
5. ☐ Call mom (low priority)"

User: "What are my high priority tasks?"
Agent: [Calls get_tasks(priority="high")]
Agent: "You have 2 high priority tasks:
1. ☐ Review Q1 report (due Friday)
2. ☐ Client meeting (due tomorrow)"

User: "Show me incomplete work tasks"
Agent: [Calls get_tasks(status="incomplete", category="work")]
Agent: "You have 3 incomplete work tasks:
1. ☐ Prepare presentation (due Monday)
2. ☐ Review budget (due next week)
3. ☐ Update documentation"

User: "What's due today?"
Agent: [Calls get_tasks_by_date(date="today")]
Agent: "You have 2 tasks due today:
1. ☐ Team standup (9:00 AM)
2. ☐ Submit timesheet (5:00 PM)"
```

**Intent Patterns**:
- "show [me] [my] tasks"
- "what [do I need to do / am I working on / is due]"
- "list [my] {filter} tasks"
- "what's {filter}"

**Filter Extraction**:
- Status: "incomplete", "complete", "done", "finished"
- Priority: "high", "medium", "low", "urgent", "important"
- Category: "work", "personal", "shopping", etc.
- Date: "today", "tomorrow", "this week", "overdue"

### Pattern 4: Task Search

**User Intent**: Find tasks by keyword

**Example Conversations**:

```
User: "Find tasks about the report"
Agent: [Calls search_tasks(query="report")]
Agent: "I found 2 tasks matching 'report':
1. ☐ Review Q1 report (high priority, due Friday)
2. ☐ Submit expense report (due next week)"

User: "Search for meeting tasks"
Agent: [Calls search_tasks(query="meeting")]
Agent: "I found 3 tasks with 'meeting':
1. ☐ Team standup meeting (due today)
2. ☐ Client meeting (due tomorrow)
3. ☑ Project kickoff meeting (completed)"

User: "Do I have any tasks about groceries?"
Agent: [Calls search_tasks(query="groceries")]
Agent: "Yes, I found 1 task:
1. ☐ Buy groceries (medium priority)"
```

**Intent Patterns**:
- "find tasks [about/with/containing] {query}"
- "search [for] {query} [tasks]"
- "do I have [any] tasks [about] {query}"
- "show me tasks [related to] {query}"

### Pattern 5: Task Update

**User Intent**: Modify existing task

**Example Conversations**:

```
User: "Change the grocery task to 'Buy groceries and cook dinner'"
Agent: [Calls search_tasks(query="grocery")]
Agent: [Calls update_task(task_id="123", title="Buy groceries and cook dinner")]
Agent: "✓ I've updated the task to 'Buy groceries and cook dinner'."

User: "Make the report task high priority"
Agent: [Calls search_tasks(query="report")]
Agent: "I found 2 tasks with 'report'. Which one?
1. Review Q1 report
2. Submit expense report"
User: "The first one"
Agent: [Calls update_task(task_id="456", priority="high")]
Agent: "✓ I've set 'Review Q1 report' to high priority."

User: "Reschedule the client meeting to tomorrow at 3 PM"
Agent: [Calls search_tasks(query="client meeting")]
Agent: [Calls parse_date("tomorrow at 3 PM")]
Agent: [Calls update_task(task_id="789", due_date="2026-02-04T15:00:00Z")]
Agent: "✓ I've rescheduled 'Client meeting' to tomorrow at 3:00 PM."
```

**Intent Patterns**:
- "change {task_identifier} to {new_value}"
- "update {task_identifier} [to] {new_value}"
- "make {task_identifier} {new_value}"
- "reschedule {task_identifier} [to] {new_date}"
- "move {task_identifier} to {new_category}"

**Task Identification**:
- By keyword: "the grocery task", "report task"
- By position: "the first one", "task #2"
- By ID: "task 123" (if user knows ID)

### Pattern 6: Task Completion

**User Intent**: Mark task as complete or incomplete

**Example Conversations**:

```
User: "Mark the grocery task as done"
Agent: [Calls search_tasks(query="grocery")]
Agent: [Calls mark_task_complete(task_id="123")]
Agent: "✓ I've marked 'Buy groceries' as complete. Great job!"

User: "I finished the report"
Agent: [Calls search_tasks(query="report")]
Agent: [Calls mark_task_complete(task_id="456")]
Agent: "✓ I've marked 'Review Q1 report' as complete. Well done!"

User: "Unmark the standup task"
Agent: [Calls search_tasks(query="standup")]
Agent: [Calls mark_task_incomplete(task_id="789")]
Agent: "✓ I've marked 'Team standup' as incomplete."

User: "Mark all my tasks from yesterday as complete"
Agent: [Calls get_tasks_by_date(date="yesterday")]
Agent: "I found 3 tasks from yesterday. Mark all as complete?"
User: "Yes"
Agent: [Calls bulk_mark_complete(task_ids=["123", "456", "789"])]
Agent: "✓ I've marked 3 tasks as complete."
```

**Intent Patterns**:
- "mark {task_identifier} [as] {status}"
- "I finished {task_identifier}"
- "I completed {task_identifier}"
- "unmark {task_identifier}"
- "mark all {filter} [as] {status}"

**Status Keywords**:
- Complete: "done", "complete", "finished", "completed"
- Incomplete: "incomplete", "not done", "unfinished"

### Pattern 7: Task Deletion

**User Intent**: Delete one or more tasks

**Example Conversations**:

```
User: "Delete the grocery task"
Agent: [Calls search_tasks(query="grocery")]
Agent: [Calls delete_task(task_id="123")]
Agent: "✓ I've deleted 'Buy groceries'."

User: "Remove the meeting"
Agent: [Calls search_tasks(query="meeting")]
Agent: "I found 3 tasks with 'meeting'. Which one would you like to delete?
1. Team standup meeting
2. Client meeting
3. Project kickoff meeting"
User: "The third one"
Agent: [Calls delete_task(task_id="789")]
Agent: "✓ I've deleted 'Project kickoff meeting'."

User: "Delete all completed tasks"
Agent: [Calls get_tasks(status="complete")]
Agent: "⚠️ This will delete 5 completed tasks. Are you sure?"
User: "Yes, delete them"
Agent: [Calls bulk_delete_tasks(filter={status: "complete"})]
Agent: "✓ I've deleted 5 completed tasks."

User: "Clear all low priority tasks from last month"
Agent: [Calls get_tasks(priority="low", date_range="last_month")]
Agent: "⚠️ This will delete 8 low priority tasks from last month. Confirm?"
User: "Yes"
Agent: [Calls bulk_delete_tasks(filter={priority: "low", date_range: "last_month"})]
Agent: "✓ I've deleted 8 tasks."
```

**Intent Patterns**:
- "delete {task_identifier}"
- "remove {task_identifier}"
- "clear {filter} tasks"
- "delete all {filter}"

**Confirmation Rules**:
- Single task: No confirmation needed
- Multiple tasks (2-5): Show count, ask for confirmation
- Bulk operation (>5): Show count, require explicit confirmation

### Pattern 8: Multi-Turn Conversations

**User Intent**: Have contextual conversation with follow-ups

**Example Conversations**:

```
Conversation 1: Task Refinement
User: "Add a task to prepare presentation"
Agent: "✓ I've added 'Prepare presentation' to your tasks."
User: "Make it high priority"
Agent: [Remembers "Prepare presentation" from context]
Agent: [Calls update_task(task_id="123", priority="high")]
Agent: "✓ I've set 'Prepare presentation' to high priority."
User: "And due Monday at 2 PM"
Agent: [Calls update_task(task_id="123", due_date="2026-02-10T14:00:00Z")]
Agent: "✓ I've set the due date to Monday, February 10th at 2:00 PM."

Conversation 2: Clarification
User: "Show me my tasks"
Agent: [Shows 10 tasks]
User: "Which ones are high priority?"
Agent: [Filters previous results by priority=high]
Agent: "Of those tasks, 3 are high priority:
1. Review Q1 report
2. Client meeting
3. Prepare presentation"

Conversation 3: Correction
User: "Add a task to buy groceries tomorrow"
Agent: "✓ I've added 'Buy groceries' due tomorrow."
User: "Actually, make it today"
Agent: [Calls update_task(task_id="123", due_date="today")]
Agent: "✓ I've changed the due date to today."
```

**Context Retention**:
- Remember last mentioned task (for "it", "that task")
- Remember last query results (for "those", "them")
- Remember last operation (for "undo", "change that")
- Maintain context for 10 messages or 5 minutes

### Pattern 9: Ambiguity Resolution

**User Intent**: Handle unclear or ambiguous requests

**Example Conversations**:

```
Scenario 1: Multiple Matches
User: "Update the meeting"
Agent: [Calls search_tasks(query="meeting")]
Agent: "I found 3 tasks with 'meeting'. Which one would you like to update?
1. Team standup meeting (due today)
2. Client meeting (due tomorrow)
3. Project review meeting (due Friday)"
User: "The client one"
Agent: "Got it. What would you like to update about 'Client meeting'?"
User: "Change it to 3 PM"
Agent: [Calls update_task(task_id="456", due_date="...T15:00:00Z")]
Agent: "✓ I've rescheduled 'Client meeting' to 3:00 PM."

Scenario 2: Missing Information
User: "Add a task"
Agent: "Sure! What should the task be about?"
User: "Prepare quarterly report"
Agent: [Calls add_task(title="Prepare quarterly report")]
Agent: "✓ I've added 'Prepare quarterly report'. Would you like to set a priority or due date?"
User: "High priority, due Friday"
Agent: [Calls update_task(task_id="789", priority="high", due_date="Friday")]
Agent: "✓ Updated to high priority, due Friday."

Scenario 3: Unclear Intent
User: "The report thing"
Agent: "I'm not sure what you'd like me to do. Would you like to:
1. Create a new task about a report
2. Find existing tasks about reports
3. Update a report task
4. Something else?"
User: "Find existing ones"
Agent: [Calls search_tasks(query="report")]
Agent: "I found 2 tasks about reports: ..."
```

**Clarification Strategies**:
- Present options when multiple matches
- Ask for missing required information
- Suggest possible interpretations
- Provide examples of valid commands

### Pattern 10: Error Recovery

**User Intent**: Handle errors gracefully

**Example Conversations**:

```
Scenario 1: Task Not Found
User: "Delete task 999"
Agent: [Calls delete_task(task_id="999")]
Agent: [Receives error: TASK_NOT_FOUND]
Agent: "I couldn't find a task with ID 999. Would you like me to show you your current tasks?"
User: "Yes"
Agent: [Calls get_tasks()]
Agent: [Shows task list]

Scenario 2: Invalid Date
User: "Add a task due on Blursday"
Agent: [Calls parse_date("Blursday")]
Agent: [Receives error: PARSE_ERROR]
Agent: "I couldn't understand the date 'Blursday'. Could you specify the date in a different way? For example: 'tomorrow', 'next Friday', or '2026-02-10'."
User: "Next Friday"
Agent: [Continues with valid date]

Scenario 3: Tool Failure
User: "Show me my tasks"
Agent: [Calls get_tasks()]
Agent: [Receives error: DATABASE_ERROR]
Agent: "I'm having trouble retrieving your tasks right now. This might be a temporary issue. Would you like me to try again?"
User: "Yes"
Agent: [Retries and succeeds]
Agent: [Shows tasks]
```

**Error Handling Principles**:
- Never show technical error messages to users
- Provide actionable suggestions for recovery
- Offer to retry transient failures
- Explain what went wrong in simple terms

## Natural Language Understanding Requirements

### Intent Classification

The agent must correctly classify user intent into these categories:

1. **CREATE**: Add new task
2. **READ**: View/list/search tasks
3. **UPDATE**: Modify existing task
4. **DELETE**: Remove task(s)
5. **COMPLETE**: Mark task status
6. **SEARCH**: Find tasks by keyword
7. **STATS**: Get statistics/summaries
8. **HELP**: Request assistance
9. **CLARIFY**: Respond to clarification questions

**Accuracy Target**: >90% intent classification accuracy

### Entity Extraction

The agent must extract these entities from user messages:

- **Task Title**: Main task description
- **Priority**: high, medium, low
- **Category**: work, personal, shopping, health, etc.
- **Due Date**: Natural language date/time
- **Status**: complete, incomplete
- **Task Identifier**: Keywords, position, ID
- **Quantity**: Numbers for bulk operations
- **Filters**: Criteria for filtering tasks

**Accuracy Target**: >85% entity extraction accuracy

### Date Parsing

The agent must understand these date formats:

**Relative Dates**:
- "today", "tomorrow", "yesterday"
- "next week", "next month", "next year"
- "in 3 days", "in 2 weeks", "in 1 month"

**Day Names**:
- "Monday", "Tuesday", etc.
- "next Friday", "this Saturday"
- "Monday next week"

**Times**:
- "at 2 PM", "at 14:00", "at 10:30 AM"
- "in the morning", "in the afternoon", "in the evening"
- "at noon", "at midnight"

**Date Ranges**:
- "this week", "next week", "last week"
- "this month", "next month", "last month"
- "by Friday", "before Monday", "after tomorrow"

**Accuracy Target**: >95% date parsing accuracy

## Testing Requirements

### Conversation Tests

For each pattern, test:
- [ ] Happy path (expected input)
- [ ] Variations (different phrasings)
- [ ] Edge cases (unusual but valid input)
- [ ] Error cases (invalid input)
- [ ] Multi-turn scenarios

### Intent Classification Tests

Test intent recognition for:
- [ ] 50+ create task variations
- [ ] 50+ read task variations
- [ ] 50+ update task variations
- [ ] 30+ delete task variations
- [ ] 30+ complete task variations
- [ ] 30+ search task variations

### Entity Extraction Tests

Test entity extraction for:
- [ ] Task titles with special characters
- [ ] Priority keywords in different positions
- [ ] Category names (common and custom)
- [ ] Complex date expressions
- [ ] Multiple entities in one message

### Date Parsing Tests

Test date parsing for:
- [ ] All relative date formats
- [ ] All day name formats
- [ ] All time formats
- [ ] Date ranges
- [ ] Ambiguous dates (with clarification)

### Multi-Turn Tests

Test conversation context for:
- [ ] Follow-up questions
- [ ] Pronoun resolution ("it", "that", "them")
- [ ] Context retention across 5+ turns
- [ ] Context switching (new topic)

### Error Handling Tests

Test error recovery for:
- [ ] Task not found
- [ ] Invalid dates
- [ ] Missing required information
- [ ] Ambiguous requests
- [ ] Tool failures

## Performance Requirements

- **Intent Classification**: < 100ms
- **Entity Extraction**: < 150ms
- **Date Parsing**: < 50ms
- **Full Response Generation**: < 3 seconds (including tool execution)
- **Context Retrieval**: < 50ms

## Documentation Requirements

- [ ] Conversation pattern reference
- [ ] Intent classification guide
- [ ] Entity extraction guide
- [ ] Date parsing examples
- [ ] Error handling guide
- [ ] Testing conversation scripts

## Success Metrics

- Intent classification accuracy >90%
- Entity extraction accuracy >85%
- Date parsing accuracy >95%
- User satisfaction with natural language understanding
- Successful completion of all conversation patterns
- Graceful handling of all error scenarios

## Future Enhancements (Out of Scope for Phase 3)

- Multi-language support (Urdu, Spanish, etc.)
- Voice input/output
- Sentiment analysis (detect urgency, frustration)
- Personalization (learn user preferences)
- Proactive suggestions ("You have 3 tasks due today")
- Natural language task templates
- Conversation history search

---

**Specification Status**: Ready for Implementation
**Estimated Complexity**: High
**Implementation Order**: 5 of 5 (implement last, after all infrastructure is ready)
**Testing Priority**: Critical (defines user experience)
