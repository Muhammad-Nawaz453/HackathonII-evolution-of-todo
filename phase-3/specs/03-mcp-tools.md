# Specification: MCP Tools for Task Management

**Feature ID**: PHASE3-03
**Status**: Draft
**Created**: 2026-02-03
**Dependencies**: Phase 2 (FastAPI CRUD operations), Official MCP SDK

## Purpose

Define and implement a comprehensive set of MCP (Model Context Protocol) tools that enable the AI agent to perform all task management operations. These tools serve as the bridge between the agent's natural language understanding and the database operations, providing a structured, reliable interface for task manipulation.

## User Stories

**As an AI agent**, I need to:
1. Create new tasks with all relevant parameters (title, priority, category, due date)
2. Retrieve tasks based on various filters (status, priority, category, date)
3. Search tasks using full-text search across title and description
4. Update existing tasks with new values
5. Mark tasks as complete or incomplete
6. Delete single or multiple tasks
7. Get task statistics and summaries
8. Parse natural language dates into ISO format

**As a developer**, I want to:
1. Define tools using the official MCP SDK format
2. Ensure tools have clear, unambiguous schemas
3. Validate tool inputs before execution
4. Handle errors gracefully with structured responses
5. Log tool executions for debugging and monitoring
6. Test tools independently of the agent

## Acceptance Criteria

### AC1: MCP Server Setup
- [ ] Official MCP SDK installed (`mcp` package)
- [ ] MCP server initialized at application startup
- [ ] MCP server listens on configured port (default: 3001)
- [ ] MCP server registers all tools on startup
- [ ] MCP server handles tool execution requests
- [ ] MCP server returns structured responses

### AC2: Tool Schema Definitions
- [ ] All tools have valid MCP schemas
- [ ] Schemas include name, description, input schema, output schema
- [ ] Input schemas use JSON Schema format
- [ ] Required vs optional parameters clearly defined
- [ ] Parameter types and constraints specified
- [ ] Examples provided for each tool

### AC3: Task CRUD Tools
- [ ] `add_task` tool creates new tasks
- [ ] `get_task` tool retrieves single task by ID
- [ ] `get_tasks` tool retrieves multiple tasks with filters
- [ ] `update_task` tool modifies existing tasks
- [ ] `delete_task` tool removes single task
- [ ] `bulk_delete_tasks` tool removes multiple tasks

### AC4: Task Status Tools
- [ ] `mark_task_complete` tool marks task as complete
- [ ] `mark_task_incomplete` tool marks task as incomplete
- [ ] `bulk_mark_complete` tool marks multiple tasks complete

### AC5: Search and Filter Tools
- [ ] `search_tasks` tool performs full-text search
- [ ] `filter_tasks` tool filters by priority, category, status, date
- [ ] `get_tasks_by_date` tool gets tasks for specific date/range

### AC6: Utility Tools
- [ ] `parse_date` tool converts natural language dates to ISO format
- [ ] `get_task_statistics` tool returns counts and summaries
- [ ] `validate_task_data` tool validates task parameters

### AC7: Tool Execution
- [ ] All tools validate inputs before execution
- [ ] All tools call existing CRUD functions (no duplicate logic)
- [ ] All tools return structured success/error responses
- [ ] All tools handle database errors gracefully
- [ ] All tools log execution for debugging

### AC8: Error Handling
- [ ] Validation errors return field-specific messages
- [ ] Not found errors return helpful suggestions
- [ ] Database errors return generic user-friendly messages
- [ ] All errors include error codes for programmatic handling
- [ ] All errors are logged with context

## Technical Design

### Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│              MCP Server (Port 3001)                      │
├─────────────────────────────────────────────────────────┤
│  /src/mcp_server.py                                     │
│  ├── MCPServer                                          │
│  │   ├── initialize()                                   │
│  │   ├── register_tools()                               │
│  │   ├── handle_request()                               │
│  │   └── execute_tool()                                 │
│  └── ToolExecutor                                       │
│      ├── execute(tool_name, params)                     │
│      ├── validate_params(tool_schema, params)           │
│      └── format_response(result)                        │
├─────────────────────────────────────────────────────────┤
│  /src/tools/                                            │
│  ├── task_tools.py                                      │
│  │   ├── add_task_tool                                  │
│  │   ├── get_task_tool                                  │
│  │   ├── get_tasks_tool                                 │
│  │   ├── update_task_tool                               │
│  │   ├── delete_task_tool                               │
│  │   └── bulk_delete_tasks_tool                         │
│  ├── search_tools.py                                    │
│  │   ├── search_tasks_tool                              │
│  │   ├── filter_tasks_tool                              │
│  │   └── get_tasks_by_date_tool                         │
│  └── utility_tools.py                                   │
│      ├── parse_date_tool                                │
│      ├── get_task_statistics_tool                       │
│      └── validate_task_data_tool                        │
└─────────────────────────────────────────────────────────┘
                          │
                          │ Calls
                          ▼
┌─────────────────────────────────────────────────────────┐
│         Phase 2 CRUD Operations (Existing)               │
│         /src/crud.py                                     │
│  ├── create_task()                                      │
│  ├── get_task()                                         │
│  ├── get_tasks()                                        │
│  ├── update_task()                                      │
│  ├── delete_task()                                      │
│  └── search_tasks()                                     │
└─────────────────────────────────────────────────────────┘
```

### MCP Tool Schema Format

Each tool follows this structure:

```python
{
    "name": "tool_name",
    "description": "Clear description of what the tool does",
    "inputSchema": {
        "type": "object",
        "properties": {
            "param1": {
                "type": "string",
                "description": "Parameter description"
            },
            "param2": {
                "type": "integer",
                "description": "Parameter description",
                "minimum": 1
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

### Tool Definitions

#### 1. add_task

**Purpose**: Create a new task with specified parameters

**Schema**:
```python
{
    "name": "add_task",
    "description": "Create a new task with title, priority, category, due date, and description",
    "inputSchema": {
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
                "description": "Due date in ISO 8601 format (e.g., 2026-02-10T14:00:00Z)"
            }
        },
        "required": ["title"]
    }
}
```

**Implementation**:
```python
async def add_task_tool(params: dict, db_session) -> dict:
    """Execute add_task tool."""
    try:
        # Validate required fields
        if not params.get("title"):
            return {
                "success": False,
                "error": "Title is required",
                "error_code": "MISSING_TITLE"
            }

        # Call existing CRUD function
        task = await crud.create_task(
            db_session,
            title=params["title"],
            description=params.get("description"),
            priority=params.get("priority", "medium"),
            category=params.get("category"),
            due_date=params.get("due_date")
        )

        return {
            "success": True,
            "data": {
                "id": task.id,
                "title": task.title,
                "priority": task.priority,
                "due_date": task.due_date
            },
            "message": f"Task '{task.title}' created successfully",
            "affected_count": 1
        }

    except ValidationError as e:
        return {
            "success": False,
            "error": str(e),
            "error_code": "VALIDATION_ERROR"
        }
    except Exception as e:
        logger.error(f"add_task error: {e}", exc_info=True)
        return {
            "success": False,
            "error": "Failed to create task",
            "error_code": "DATABASE_ERROR"
        }
```

#### 2. get_tasks

**Purpose**: Retrieve multiple tasks with optional filters

**Schema**:
```python
{
    "name": "get_tasks",
    "description": "Retrieve tasks with optional filters for status, priority, category, and date range",
    "inputSchema": {
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
}
```

**Implementation**:
```python
async def get_tasks_tool(params: dict, db_session) -> dict:
    """Execute get_tasks tool."""
    try:
        # Build filters
        filters = {}
        if params.get("status") and params["status"] != "all":
            filters["complete"] = (params["status"] == "complete")
        if params.get("priority"):
            filters["priority"] = params["priority"]
        if params.get("category"):
            filters["category"] = params["category"]

        # Call existing CRUD function
        tasks = await crud.get_tasks(
            db_session,
            filters=filters,
            limit=params.get("limit", 50)
        )

        return {
            "success": True,
            "data": {
                "tasks": [
                    {
                        "id": task.id,
                        "title": task.title,
                        "description": task.description,
                        "priority": task.priority,
                        "category": task.category,
                        "due_date": task.due_date,
                        "complete": task.complete,
                        "created_at": task.created_at
                    }
                    for task in tasks
                ],
                "count": len(tasks)
            },
            "message": f"Retrieved {len(tasks)} tasks",
            "affected_count": len(tasks)
        }

    except Exception as e:
        logger.error(f"get_tasks error: {e}", exc_info=True)
        return {
            "success": False,
            "error": "Failed to retrieve tasks",
            "error_code": "DATABASE_ERROR"
        }
```

#### 3. update_task

**Purpose**: Update an existing task's fields

**Schema**:
```python
{
    "name": "update_task",
    "description": "Update an existing task's title, priority, category, due date, or description",
    "inputSchema": {
        "type": "object",
        "properties": {
            "task_id": {
                "type": "string",
                "description": "ID of the task to update (required)",
                "format": "uuid"
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
}
```

#### 4. search_tasks

**Purpose**: Full-text search across task titles and descriptions

**Schema**:
```python
{
    "name": "search_tasks",
    "description": "Search tasks by keyword in title or description",
    "inputSchema": {
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
}
```

#### 5. mark_task_complete

**Purpose**: Mark a task as complete

**Schema**:
```python
{
    "name": "mark_task_complete",
    "description": "Mark a task as complete",
    "inputSchema": {
        "type": "object",
        "properties": {
            "task_id": {
                "type": "string",
                "description": "ID of the task to mark complete",
                "format": "uuid"
            }
        },
        "required": ["task_id"]
    }
}
```

#### 6. delete_task

**Purpose**: Delete a single task

**Schema**:
```python
{
    "name": "delete_task",
    "description": "Delete a single task by ID",
    "inputSchema": {
        "type": "object",
        "properties": {
            "task_id": {
                "type": "string",
                "description": "ID of the task to delete",
                "format": "uuid"
            }
        },
        "required": ["task_id"]
    }
}
```

#### 7. parse_date

**Purpose**: Convert natural language dates to ISO format

**Schema**:
```python
{
    "name": "parse_date",
    "description": "Convert natural language date (e.g., 'tomorrow', 'next Friday', '2 PM') to ISO 8601 format",
    "inputSchema": {
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
}
```

**Implementation**:
```python
from dateutil import parser
from datetime import datetime, timedelta
import re

async def parse_date_tool(params: dict) -> dict:
    """Parse natural language dates."""
    try:
        date_string = params["date_string"].lower()
        reference = datetime.now()

        # Handle common patterns
        if date_string in ["today", "now"]:
            result = reference
        elif date_string == "tomorrow":
            result = reference + timedelta(days=1)
        elif date_string == "yesterday":
            result = reference - timedelta(days=1)
        elif "next week" in date_string:
            result = reference + timedelta(weeks=1)
        elif "next month" in date_string:
            result = reference + timedelta(days=30)
        elif match := re.match(r"in (\d+) (day|week|month)s?", date_string):
            count = int(match.group(1))
            unit = match.group(2)
            if unit == "day":
                result = reference + timedelta(days=count)
            elif unit == "week":
                result = reference + timedelta(weeks=count)
            elif unit == "month":
                result = reference + timedelta(days=count * 30)
        else:
            # Try dateutil parser
            result = parser.parse(date_string, fuzzy=True)

        return {
            "success": True,
            "data": {
                "iso_date": result.isoformat(),
                "original": date_string
            },
            "message": f"Parsed '{date_string}' to {result.strftime('%Y-%m-%d %H:%M')}"
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Could not parse date: {date_string}",
            "error_code": "PARSE_ERROR"
        }
```

#### 8. get_task_statistics

**Purpose**: Get summary statistics about tasks

**Schema**:
```python
{
    "name": "get_task_statistics",
    "description": "Get statistics about tasks (total, complete, incomplete, by priority, by category)",
    "inputSchema": {
        "type": "object",
        "properties": {}
    }
}
```

**Implementation**:
```python
async def get_task_statistics_tool(db_session) -> dict:
    """Get task statistics."""
    try:
        all_tasks = await crud.get_tasks(db_session)

        stats = {
            "total": len(all_tasks),
            "complete": sum(1 for t in all_tasks if t.complete),
            "incomplete": sum(1 for t in all_tasks if not t.complete),
            "by_priority": {
                "high": sum(1 for t in all_tasks if t.priority == "high"),
                "medium": sum(1 for t in all_tasks if t.priority == "medium"),
                "low": sum(1 for t in all_tasks if t.priority == "low")
            },
            "overdue": sum(
                1 for t in all_tasks
                if t.due_date and t.due_date < datetime.now() and not t.complete
            )
        }

        return {
            "success": True,
            "data": stats,
            "message": f"Retrieved statistics for {stats['total']} tasks"
        }

    except Exception as e:
        logger.error(f"get_task_statistics error: {e}", exc_info=True)
        return {
            "success": False,
            "error": "Failed to get statistics",
            "error_code": "DATABASE_ERROR"
        }
```

### MCP Server Implementation

**File**: `backend/src/mcp_server.py`

```python
from mcp import MCPServer, Tool
from typing import Dict, Any, List
import logging

from .tools.task_tools import (
    add_task_tool,
    get_task_tool,
    get_tasks_tool,
    update_task_tool,
    delete_task_tool,
    bulk_delete_tasks_tool
)
from .tools.search_tools import (
    search_tasks_tool,
    filter_tasks_tool,
    get_tasks_by_date_tool
)
from .tools.utility_tools import (
    parse_date_tool,
    get_task_statistics_tool,
    validate_task_data_tool
)

logger = logging.getLogger(__name__)


class TodoMCPServer:
    """MCP Server for todo task management tools."""

    def __init__(self):
        self.server = MCPServer(name="todo-mcp-server")
        self.tools: Dict[str, Tool] = {}
        self.tool_executors: Dict[str, callable] = {}

    def register_tools(self):
        """Register all MCP tools."""

        # Import tool schemas
        from .tools.task_tools import TASK_TOOL_SCHEMAS
        from .tools.search_tools import SEARCH_TOOL_SCHEMAS
        from .tools.utility_tools import UTILITY_TOOL_SCHEMAS

        all_schemas = {
            **TASK_TOOL_SCHEMAS,
            **SEARCH_TOOL_SCHEMAS,
            **UTILITY_TOOL_SCHEMAS
        }

        # Register each tool
        for tool_name, schema in all_schemas.items():
            tool = Tool(
                name=schema["name"],
                description=schema["description"],
                input_schema=schema["inputSchema"],
                output_schema=schema.get("outputSchema")
            )
            self.server.register_tool(tool)
            self.tools[tool_name] = tool

            # Map to executor function
            self.tool_executors[tool_name] = self._get_executor(tool_name)

        logger.info(f"Registered {len(self.tools)} MCP tools")

    def _get_executor(self, tool_name: str) -> callable:
        """Get executor function for a tool."""
        executor_map = {
            "add_task": add_task_tool,
            "get_task": get_task_tool,
            "get_tasks": get_tasks_tool,
            "update_task": update_task_tool,
            "delete_task": delete_task_tool,
            "bulk_delete_tasks": bulk_delete_tasks_tool,
            "search_tasks": search_tasks_tool,
            "filter_tasks": filter_tasks_tool,
            "get_tasks_by_date": get_tasks_by_date_tool,
            "parse_date": parse_date_tool,
            "get_task_statistics": get_task_statistics_tool,
            "validate_task_data": validate_task_data_tool
        }
        return executor_map.get(tool_name)

    async def execute_tool(
        self,
        tool_name: str,
        params: Dict[str, Any],
        db_session: Any
    ) -> Dict[str, Any]:
        """Execute a tool by name.

        Args:
            tool_name: Name of the tool to execute
            params: Tool parameters
            db_session: Database session

        Returns:
            Tool execution result
        """
        if tool_name not in self.tool_executors:
            return {
                "success": False,
                "error": f"Unknown tool: {tool_name}",
                "error_code": "UNKNOWN_TOOL"
            }

        executor = self.tool_executors[tool_name]

        try:
            # Validate parameters against schema
            tool = self.tools[tool_name]
            self._validate_params(tool.input_schema, params)

            # Execute tool
            logger.info(f"Executing tool: {tool_name} with params: {params}")
            result = await executor(params, db_session)

            logger.info(f"Tool {tool_name} completed: {result.get('success')}")
            return result

        except ValidationError as e:
            logger.error(f"Validation error in {tool_name}: {e}")
            return {
                "success": False,
                "error": str(e),
                "error_code": "VALIDATION_ERROR"
            }
        except Exception as e:
            logger.error(f"Error executing {tool_name}: {e}", exc_info=True)
            return {
                "success": False,
                "error": "Tool execution failed",
                "error_code": "EXECUTION_ERROR"
            }

    def _validate_params(self, schema: dict, params: dict):
        """Validate parameters against JSON schema."""
        # Use jsonschema library for validation
        from jsonschema import validate, ValidationError as JSONValidationError

        try:
            validate(instance=params, schema=schema)
        except JSONValidationError as e:
            raise ValidationError(f"Invalid parameters: {e.message}")

    def get_tool_schemas_for_openai(self) -> List[Dict[str, Any]]:
        """Get tool schemas in OpenAI function calling format.

        Returns:
            List of tool schemas formatted for OpenAI API
        """
        openai_tools = []

        for tool_name, tool in self.tools.items():
            openai_tools.append({
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.input_schema
                }
            })

        return openai_tools


# Global MCP server instance
mcp_server = TodoMCPServer()


def initialize_mcp_server():
    """Initialize MCP server at application startup."""
    mcp_server.register_tools()
    logger.info("MCP server initialized")


def get_mcp_server() -> TodoMCPServer:
    """Get the global MCP server instance."""
    return mcp_server


def get_tool_executor():
    """Get tool executor for agent integration."""
    return mcp_server
```

## Edge Cases and Error Handling

### Edge Case 1: Invalid Task ID
**Scenario**: Tool called with non-existent task ID
**Handling**:
- Return `success: false` with error code `TASK_NOT_FOUND`
- Include helpful message: "Task with ID {id} not found"
- Suggest using search_tasks to find the right task

### Edge Case 2: Missing Required Parameters
**Scenario**: Tool called without required parameters
**Handling**:
- Validate parameters before execution
- Return validation error with field-specific messages
- Error code: `VALIDATION_ERROR`

### Edge Case 3: Invalid Date Format
**Scenario**: Due date provided in invalid format
**Handling**:
- Try to parse with dateutil
- If fails, return parse error
- Suggest using parse_date tool first

### Edge Case 4: Database Connection Error
**Scenario**: Database is unavailable
**Handling**:
- Catch database exceptions
- Return generic error (don't expose internals)
- Error code: `DATABASE_ERROR`
- Log full error for debugging

### Edge Case 5: Bulk Operation on Empty Set
**Scenario**: bulk_delete_tasks matches no tasks
**Handling**:
- Return success with affected_count: 0
- Message: "No tasks matched the criteria"
- Don't treat as error

### Edge Case 6: Ambiguous Natural Language Date
**Scenario**: parse_date receives ambiguous input like "Friday"
**Handling**:
- Assume next occurrence (next Friday)
- Include interpretation in response message
- Agent can confirm with user if needed

## Dependencies

### External Dependencies
- `mcp` (Official MCP SDK)
- `jsonschema` (Parameter validation)
- `python-dateutil` (Date parsing)
- Phase 2 CRUD operations (existing)

### Internal Dependencies
- Phase 2: FastAPI backend, database models, CRUD operations
- Phase 3 Spec 02: Agent SDK (will call these tools)

## Testing Requirements

### Unit Tests
- [ ] Each tool schema is valid MCP format
- [ ] Each tool validates parameters correctly
- [ ] Each tool handles missing parameters
- [ ] Each tool handles invalid parameters
- [ ] Each tool returns structured responses
- [ ] Date parsing handles common patterns

### Integration Tests
- [ ] Tools execute with real database
- [ ] Tools call CRUD functions correctly
- [ ] Tools handle database errors
- [ ] Tools return correct data formats
- [ ] MCP server registers all tools
- [ ] MCP server executes tools correctly

### Error Tests
- [ ] Invalid task ID returns TASK_NOT_FOUND
- [ ] Missing parameters return VALIDATION_ERROR
- [ ] Database errors return DATABASE_ERROR
- [ ] Invalid dates return PARSE_ERROR
- [ ] Unknown tools return UNKNOWN_TOOL

## Performance Requirements

- **Tool Execution**: < 500ms per tool call
- **Parameter Validation**: < 10ms
- **Date Parsing**: < 50ms
- **Statistics Calculation**: < 200ms (even with 1000+ tasks)
- **Search**: < 300ms (full-text search)

## Security Considerations

- **Input Validation**: All parameters validated against schema
- **SQL Injection**: Use ORM (SQLModel) - no raw SQL
- **Authorization**: Verify user owns tasks (future: multi-user)
- **Rate Limiting**: Limit tool calls per user per minute
- **Logging**: Log tool executions but not sensitive data

## Documentation Requirements

- [ ] README with MCP server setup instructions
- [ ] Tool schema documentation (auto-generated from schemas)
- [ ] Example tool calls for each tool
- [ ] Error code reference
- [ ] Integration guide for agent developers

## Success Metrics

- All tools have valid MCP schemas
- All tools execute successfully with valid inputs
- All tools return structured responses
- All tools handle errors gracefully
- Tool execution time < 500ms
- No SQL injection vulnerabilities
- 100% test coverage for tool execution logic

## Future Enhancements (Out of Scope for Phase 3)

- Batch tool execution (execute multiple tools in one call)
- Tool versioning (v1, v2 schemas)
- Tool analytics (track usage, performance)
- Custom tool plugins (user-defined tools)
- Tool caching (cache frequent queries)

---

**Specification Status**: Ready for Implementation
**Estimated Complexity**: High
**Implementation Order**: 2 of 5 (implement alongside Agent SDK)
