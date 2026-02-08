# MCP Tool Reference - Phase 3

This document provides detailed reference for all MCP (Model Context Protocol) tools available to the AI agent.

## Overview

The backend provides 12 MCP tools organized into three categories:
- **Task CRUD Tools** (6 tools): Create, read, update, delete tasks
- **Search Tools** (3 tools): Search and filter tasks
- **Utility Tools** (3 tools): Helper functions

## Tool Categories

### Task CRUD Tools

#### 1. add_task

**Purpose**: Create a new task with specified parameters

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "title": {
      "type": "string",
      "description": "Task title (required, 1-200 characters)",
      "minLength": 1,
      "maxLength": 200
    },
    "description": {
      "type": "string",
      "description": "Task description (optional, max 1000 characters)",
      "maxLength": 1000
    },
    "priority": {
      "type": "string",
      "enum": ["high", "medium", "low"],
      "description": "Task priority (default: medium)"
    },
    "category": {
      "type": "string",
      "description": "Task category (e.g., work, personal, shopping)",
      "maxLength": 50
    },
    "due_date": {
      "type": "string",
      "format": "date-time",
      "description": "Due date in ISO 8601 format"
    }
  },
  "required": ["title"]
}
```

**Output Schema**:
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "title": "string",
    "priority": "string",
    "due_date": "string"
  },
  "message": "Task 'Title' created successfully",
  "affected_count": 1
}
```

**Example Usage**:
```json
// Input
{
  "title": "Review quarterly report",
  "priority": "high",
  "category": "work",
  "due_date": "2026-02-07T23:59:59Z"
}

// Output
{
  "success": true,
  "data": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "title": "Review quarterly report",
    "priority": "high",
    "due_date": "2026-02-07T23:59:59Z"
  },
  "message": "Task 'Review quarterly report' created successfully",
  "affected_count": 1
}
```

**Error Codes**:
- `MISSING_TITLE`: Title is required
- `VALIDATION_ERROR`: Invalid input parameters
- `DATABASE_ERROR`: Database operation failed

---

#### 2. get_task

**Purpose**: Retrieve a single task by ID

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "task_id": {
      "type": "string",
      "format": "uuid",
      "description": "ID of the task to retrieve"
    }
  },
  "required": ["task_id"]
}
```

**Output Schema**:
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "title": "string",
    "description": "string",
    "priority": "string",
    "category": "string",
    "due_date": "string",
    "complete": boolean,
    "created_at": "string",
    "updated_at": "string"
  },
  "message": "Task retrieved successfully"
}
```

**Error Codes**:
- `TASK_NOT_FOUND`: Task with specified ID does not exist
- `INVALID_UUID`: Task ID is not a valid UUID

---

#### 3. get_tasks

**Purpose**: Retrieve multiple tasks with optional filters

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "status": {
      "type": "string",
      "enum": ["complete", "incomplete", "all"],
      "description": "Filter by completion status (default: all)"
    },
    "priority": {
      "type": "string",
      "enum": ["high", "medium", "low"],
      "description": "Filter by priority"
    },
    "category": {
      "type": "string",
      "description": "Filter by category"
    },
    "due_date_from": {
      "type": "string",
      "format": "date-time",
      "description": "Filter tasks due after this date"
    },
    "due_date_to": {
      "type": "string",
      "format": "date-time",
      "description": "Filter tasks due before this date"
    },
    "limit": {
      "type": "integer",
      "description": "Maximum number of tasks to return (default: 50)",
      "minimum": 1,
      "maximum": 100
    }
  }
}
```

**Output Schema**:
```json
{
  "success": true,
  "data": {
    "tasks": [
      {
        "id": "uuid",
        "title": "string",
        "description": "string",
        "priority": "string",
        "category": "string",
        "due_date": "string",
        "complete": boolean,
        "created_at": "string"
      }
    ],
    "count": number
  },
  "message": "Retrieved N tasks",
  "affected_count": number
}
```

**Example Usage**:
```json
// Get all high priority incomplete tasks
{
  "status": "incomplete",
  "priority": "high"
}

// Get all work tasks due this week
{
  "category": "work",
  "due_date_from": "2026-02-03T00:00:00Z",
  "due_date_to": "2026-02-09T23:59:59Z"
}
```

---

#### 4. update_task

**Purpose**: Update an existing task's fields

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "task_id": {
      "type": "string",
      "format": "uuid",
      "description": "ID of the task to update (required)"
    },
    "title": {
      "type": "string",
      "description": "New task title",
      "minLength": 1,
      "maxLength": 200
    },
    "description": {
      "type": "string",
      "description": "New task description",
      "maxLength": 1000
    },
    "priority": {
      "type": "string",
      "enum": ["high", "medium", "low"],
      "description": "New priority"
    },
    "category": {
      "type": "string",
      "description": "New category",
      "maxLength": 50
    },
    "due_date": {
      "type": "string",
      "format": "date-time",
      "description": "New due date in ISO 8601 format"
    }
  },
  "required": ["task_id"]
}
```

**Output Schema**:
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "title": "string",
    "updated_fields": ["field1", "field2"]
  },
  "message": "Task updated successfully",
  "affected_count": 1
}
```

**Error Codes**:
- `TASK_NOT_FOUND`: Task does not exist
- `VALIDATION_ERROR`: Invalid field values
- `NO_CHANGES`: No fields provided to update

---

#### 5. delete_task

**Purpose**: Delete a single task by ID

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "task_id": {
      "type": "string",
      "format": "uuid",
      "description": "ID of the task to delete"
    }
  },
  "required": ["task_id"]
}
```

**Output Schema**:
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "title": "string"
  },
  "message": "Task 'Title' deleted successfully",
  "affected_count": 1
}
```

**Error Codes**:
- `TASK_NOT_FOUND`: Task does not exist

---

#### 6. bulk_delete_tasks

**Purpose**: Delete multiple tasks matching filter criteria

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "filter": {
      "type": "object",
      "properties": {
        "status": {
          "type": "string",
          "enum": ["complete", "incomplete"]
        },
        "priority": {
          "type": "string",
          "enum": ["high", "medium", "low"]
        },
        "category": {
          "type": "string"
        },
        "older_than_days": {
          "type": "integer",
          "description": "Delete tasks older than N days"
        }
      }
    },
    "confirm": {
      "type": "boolean",
      "description": "Must be true to execute deletion"
    }
  },
  "required": ["filter", "confirm"]
}
```

**Output Schema**:
```json
{
  "success": true,
  "data": {
    "deleted_count": number,
    "deleted_ids": ["uuid1", "uuid2"]
  },
  "message": "Deleted N tasks",
  "affected_count": number
}
```

**Error Codes**:
- `CONFIRMATION_REQUIRED`: confirm parameter must be true
- `NO_MATCHES`: No tasks match the filter criteria

---

### Search Tools

#### 7. search_tasks

**Purpose**: Full-text search across task titles and descriptions

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "query": {
      "type": "string",
      "description": "Search query (required)",
      "minLength": 1
    },
    "limit": {
      "type": "integer",
      "description": "Maximum results (default: 20)",
      "minimum": 1,
      "maximum": 50
    }
  },
  "required": ["query"]
}
```

**Output Schema**:
```json
{
  "success": true,
  "data": {
    "tasks": [
      {
        "id": "uuid",
        "title": "string",
        "description": "string",
        "priority": "string",
        "relevance_score": number
      }
    ],
    "count": number,
    "query": "string"
  },
  "message": "Found N tasks matching 'query'",
  "affected_count": number
}
```

**Example Usage**:
```json
// Search for tasks about reports
{
  "query": "report",
  "limit": 10
}

// Output includes tasks with "report" in title or description
```

---

#### 8. filter_tasks

**Purpose**: Filter tasks by multiple criteria

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "priority": {
      "type": "array",
      "items": {"type": "string", "enum": ["high", "medium", "low"]},
      "description": "Filter by one or more priorities"
    },
    "category": {
      "type": "array",
      "items": {"type": "string"},
      "description": "Filter by one or more categories"
    },
    "status": {
      "type": "string",
      "enum": ["complete", "incomplete", "all"]
    },
    "overdue": {
      "type": "boolean",
      "description": "Filter for overdue tasks only"
    }
  }
}
```

**Output Schema**: Same as `get_tasks`

---

#### 9. get_tasks_by_date

**Purpose**: Get tasks for a specific date or date range

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "date": {
      "type": "string",
      "description": "Specific date or keyword (today, tomorrow, this_week)"
    },
    "date_from": {
      "type": "string",
      "format": "date-time",
      "description": "Start of date range"
    },
    "date_to": {
      "type": "string",
      "format": "date-time",
      "description": "End of date range"
    }
  }
}
```

**Output Schema**: Same as `get_tasks`

**Example Usage**:
```json
// Get tasks due today
{"date": "today"}

// Get tasks due this week
{"date": "this_week"}

// Get tasks in custom range
{
  "date_from": "2026-02-03T00:00:00Z",
  "date_to": "2026-02-10T23:59:59Z"
}
```

---

### Utility Tools

#### 10. parse_date

**Purpose**: Convert natural language dates to ISO 8601 format

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "date_string": {
      "type": "string",
      "description": "Natural language date string"
    },
    "reference_date": {
      "type": "string",
      "format": "date-time",
      "description": "Reference date for relative dates (default: now)"
    }
  },
  "required": ["date_string"]
}
```

**Output Schema**:
```json
{
  "success": true,
  "data": {
    "iso_date": "2026-02-04T14:00:00Z",
    "original": "tomorrow at 2 PM",
    "parsed_components": {
      "date": "2026-02-04",
      "time": "14:00:00",
      "timezone": "UTC"
    }
  },
  "message": "Parsed 'tomorrow at 2 PM' to 2026-02-04 14:00"
}
```

**Supported Formats**:
- Relative: "today", "tomorrow", "yesterday", "next week", "in 3 days"
- Day names: "Monday", "next Friday", "this Saturday"
- Times: "at 2 PM", "at 10:30 AM", "in the morning"
- Ranges: "this week", "next month", "by Friday"

**Error Codes**:
- `PARSE_ERROR`: Could not parse date string

---

#### 11. get_task_statistics

**Purpose**: Get summary statistics about tasks

**Input Schema**:
```json
{
  "type": "object",
  "properties": {}
}
```

**Output Schema**:
```json
{
  "success": true,
  "data": {
    "total": number,
    "complete": number,
    "incomplete": number,
    "by_priority": {
      "high": number,
      "medium": number,
      "low": number
    },
    "by_category": {
      "work": number,
      "personal": number,
      "shopping": number
    },
    "overdue": number,
    "due_today": number,
    "due_this_week": number
  },
  "message": "Retrieved statistics for N tasks"
}
```

**Example Usage**:
```json
// No input required
{}

// Output provides comprehensive statistics
```

---

#### 12. validate_task_data

**Purpose**: Validate task parameters before creation/update

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "title": {"type": "string"},
    "description": {"type": "string"},
    "priority": {"type": "string"},
    "category": {"type": "string"},
    "due_date": {"type": "string"}
  }
}
```

**Output Schema**:
```json
{
  "success": true,
  "data": {
    "valid": boolean,
    "errors": [
      {
        "field": "string",
        "message": "string"
      }
    ]
  },
  "message": "Validation complete"
}
```

---

## Tool Execution Flow

### Typical Flow for Task Creation

1. User: "Add a high priority task to review report by Friday"
2. Agent calls `parse_date("Friday")` → Returns ISO date
3. Agent calls `add_task(title="Review report", priority="high", due_date="...")`
4. Tool executes → Returns success with task ID
5. Agent responds: "✓ I've created a high priority task..."

### Typical Flow for Task Search

1. User: "Find tasks about the report"
2. Agent calls `search_tasks(query="report")`
3. Tool executes → Returns matching tasks
4. Agent formats results and responds

### Typical Flow for Ambiguous Request

1. User: "Update the meeting"
2. Agent calls `search_tasks(query="meeting")`
3. Tool returns multiple matches
4. Agent asks: "I found 3 tasks with 'meeting'. Which one?"
5. User clarifies
6. Agent calls `update_task(task_id="...", ...)`

## Error Handling

### Common Error Codes

- `TASK_NOT_FOUND`: Task with specified ID does not exist
- `VALIDATION_ERROR`: Invalid input parameters
- `DATABASE_ERROR`: Database operation failed
- `PARSE_ERROR`: Could not parse date string
- `CONFIRMATION_REQUIRED`: User confirmation needed
- `NO_MATCHES`: No tasks match filter criteria
- `UNKNOWN_TOOL`: Tool name not recognized

### Error Response Format

```json
{
  "success": false,
  "error": "Human-readable error message",
  "error_code": "ERROR_CODE",
  "details": {
    "field": "additional context"
  }
}
```

## Performance Considerations

- **Tool Execution Time**: < 500ms per tool call
- **Search Performance**: Indexed for fast full-text search
- **Batch Operations**: Use `bulk_delete_tasks` for multiple deletions
- **Caching**: Conversation context cached for performance

## Testing Tools

### Using curl

```bash
# Test via chat endpoint
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Show me my tasks"}'
```

### Using Python

```python
import requests

response = requests.post(
    "http://localhost:8000/api/chat",
    json={"message": "Add a task to test tools"}
)
print(response.json())
```

## Tool Development

### Adding New Tools

1. Define tool schema in `src/tools/your_tools.py`
2. Implement execution function
3. Register in `src/mcp_server.py`
4. Add tests in `tests/test_your_tools.py`
5. Update this documentation

### Tool Schema Template

```python
TOOL_SCHEMA = {
    "name": "tool_name",
    "description": "Clear description of what the tool does",
    "inputSchema": {
        "type": "object",
        "properties": {
            "param1": {
                "type": "string",
                "description": "Parameter description"
            }
        },
        "required": ["param1"]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "success": {"type": "boolean"},
            "data": {"type": "object"},
            "message": {"type": "string"}
        }
    }
}
```

## Best Practices

1. **Always validate inputs** before execution
2. **Return structured responses** with success/error indicators
3. **Include helpful error messages** for users
4. **Log tool executions** for debugging
5. **Keep tools atomic** (single responsibility)
6. **Make tools idempotent** where possible
7. **Handle edge cases** gracefully

## Support

For issues with tools:
1. Check tool schema is valid MCP format
2. Verify tool is registered in MCP server
3. Test tool independently before agent integration
4. Check logs for detailed error messages

---

**Last Updated**: 2026-02-03
**Version**: 3.0.0
