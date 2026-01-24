# API Design Specification

## Feature Name
RESTful API Design - Complete Endpoint Specifications

## Purpose
Define all API endpoints, request/response schemas, validation rules, error handling, and HTTP semantics for the Todo Web Application backend. This specification serves as the contract between frontend and backend teams.

## Overview

The API follows RESTful principles with resource-based URLs, standard HTTP methods, and consistent response formats. All endpoints are versioned under `/api/v1/` and return JSON.

## Base Configuration

### Base URL
- **Development**: `http://localhost:8000/api/v1`
- **Production**: `https://your-backend.railway.app/api/v1`

### Content Type
- **Request**: `application/json`
- **Response**: `application/json`

### CORS Configuration
```python
origins = [
    "http://localhost:3000",  # Development frontend
    "https://your-app.vercel.app",  # Production frontend
]
```

## Global Response Format

### Success Response
```json
{
  "data": { /* resource or array */ },
  "message": "Operation successful"
}
```

### Error Response
```json
{
  "detail": "Human-readable error message",
  "errors": [
    {
      "field": "field_name",
      "message": "Specific validation error"
    }
  ]
}
```

## HTTP Status Codes

### Success Codes
- `200 OK` - Successful GET, PUT, PATCH
- `201 Created` - Successful POST with resource creation
- `204 No Content` - Successful DELETE

### Client Error Codes
- `400 Bad Request` - Malformed request, invalid JSON
- `404 Not Found` - Resource doesn't exist
- `422 Unprocessable Entity` - Validation errors

### Server Error Codes
- `500 Internal Server Error` - Unexpected server failure

## API Endpoints

### 1. List Tasks

**Endpoint**: `GET /api/v1/tasks`

**Purpose**: Retrieve a list of tasks with optional filtering, sorting, and pagination.

**Query Parameters**:
```
?status=incomplete          # Filter by status (complete/incomplete)
?priority=high              # Filter by priority (high/medium/low)
?category=work              # Filter by category
?search=groceries           # Search in title and description
?sort=due_date              # Sort field (due_date, priority, created_at, title)
?order=asc                  # Sort order (asc/desc)
?page=1                     # Page number (default: 1)
?limit=20                   # Items per page (default: 20, max: 100)
```

**Request Example**:
```http
GET /api/v1/tasks?status=incomplete&priority=high&sort=due_date&order=asc
```

**Response (200 OK)**:
```json
{
  "data": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Buy groceries",
      "description": "Milk, eggs, bread",
      "status": false,
      "priority": "high",
      "category": "personal",
      "due_date": "2026-01-25T10:00:00Z",
      "created_at": "2026-01-24T15:30:00Z",
      "updated_at": "2026-01-24T15:30:00Z"
    },
    {
      "id": "660e8400-e29b-41d4-a716-446655440001",
      "title": "Finish project report",
      "description": "Complete Q4 analysis",
      "status": false,
      "priority": "high",
      "category": "work",
      "due_date": "2026-01-26T17:00:00Z",
      "created_at": "2026-01-24T14:00:00Z",
      "updated_at": "2026-01-24T14:00:00Z"
    }
  ],
  "message": "Tasks retrieved successfully",
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 2,
    "pages": 1
  }
}
```

**Validation Rules**:
- `status`: Must be "complete" or "incomplete" if provided
- `priority`: Must be "high", "medium", or "low" if provided
- `sort`: Must be valid field name (due_date, priority, created_at, title)
- `order`: Must be "asc" or "desc"
- `page`: Must be positive integer
- `limit`: Must be 1-100

**Error Response (422)**:
```json
{
  "detail": "Invalid query parameters",
  "errors": [
    {
      "field": "priority",
      "message": "Priority must be high, medium, or low"
    }
  ]
}
```

---

### 2. Create Task

**Endpoint**: `POST /api/v1/tasks`

**Purpose**: Create a new task.

**Request Body**:
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "priority": "high",
  "category": "personal",
  "due_date": "2026-01-25T10:00:00Z"
}
```

**Required Fields**:
- `title` (string, 1-200 characters)

**Optional Fields**:
- `description` (string, max 1000 characters)
- `priority` (enum: "high", "medium", "low", default: "medium")
- `category` (string, max 50 characters)
- `due_date` (ISO 8601 datetime)

**Response (201 Created)**:
```json
{
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "status": false,
    "priority": "high",
    "category": "personal",
    "due_date": "2026-01-25T10:00:00Z",
    "created_at": "2026-01-24T15:30:00Z",
    "updated_at": "2026-01-24T15:30:00Z"
  },
  "message": "Task created successfully"
}
```

**Validation Rules**:
- `title`: Required, non-empty after trim, 1-200 characters
- `description`: Optional, max 1000 characters
- `priority`: Must be "high", "medium", or "low"
- `category`: Optional, max 50 characters
- `due_date`: Optional, must be valid ISO 8601 datetime, must be future date

**Error Response (422)**:
```json
{
  "detail": "Validation error",
  "errors": [
    {
      "field": "title",
      "message": "Title is required and cannot be empty"
    },
    {
      "field": "priority",
      "message": "Priority must be high, medium, or low"
    }
  ]
}
```

---

### 3. Get Single Task

**Endpoint**: `GET /api/v1/tasks/{id}`

**Purpose**: Retrieve a single task by ID.

**Path Parameters**:
- `id` (UUID): Task identifier

**Request Example**:
```http
GET /api/v1/tasks/550e8400-e29b-41d4-a716-446655440000
```

**Response (200 OK)**:
```json
{
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "status": false,
    "priority": "high",
    "category": "personal",
    "due_date": "2026-01-25T10:00:00Z",
    "created_at": "2026-01-24T15:30:00Z",
    "updated_at": "2026-01-24T15:30:00Z"
  },
  "message": "Task retrieved successfully"
}
```

**Error Response (404)**:
```json
{
  "detail": "Task not found",
  "errors": [
    {
      "field": "id",
      "message": "Task with ID 550e8400-e29b-41d4-a716-446655440000 does not exist"
    }
  ]
}
```

**Error Response (400)** - Invalid UUID:
```json
{
  "detail": "Invalid task ID format",
  "errors": [
    {
      "field": "id",
      "message": "ID must be a valid UUID"
    }
  ]
}
```

---

### 4. Update Task (Full Update)

**Endpoint**: `PUT /api/v1/tasks/{id}`

**Purpose**: Replace entire task with new data (all fields required).

**Path Parameters**:
- `id` (UUID): Task identifier

**Request Body**:
```json
{
  "title": "Buy groceries and cook dinner",
  "description": "Milk, eggs, bread, chicken",
  "status": false,
  "priority": "high",
  "category": "personal",
  "due_date": "2026-01-25T18:00:00Z"
}
```

**Required Fields** (all fields):
- `title` (string, 1-200 characters)
- `status` (boolean)
- `priority` (enum: "high", "medium", "low")

**Optional Fields**:
- `description` (string, max 1000 characters)
- `category` (string, max 50 characters)
- `due_date` (ISO 8601 datetime)

**Response (200 OK)**:
```json
{
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Buy groceries and cook dinner",
    "description": "Milk, eggs, bread, chicken",
    "status": false,
    "priority": "high",
    "category": "personal",
    "due_date": "2026-01-25T18:00:00Z",
    "created_at": "2026-01-24T15:30:00Z",
    "updated_at": "2026-01-24T16:45:00Z"
  },
  "message": "Task updated successfully"
}
```

**Error Response (404)**:
```json
{
  "detail": "Task not found",
  "errors": [
    {
      "field": "id",
      "message": "Task with ID 550e8400-e29b-41d4-a716-446655440000 does not exist"
    }
  ]
}
```

---

### 5. Update Task (Partial Update)

**Endpoint**: `PATCH /api/v1/tasks/{id}`

**Purpose**: Update specific fields of a task (only provided fields are updated).

**Path Parameters**:
- `id` (UUID): Task identifier

**Request Body** (any combination of fields):
```json
{
  "title": "Buy groceries and cook dinner",
  "priority": "medium"
}
```

**Allowed Fields**:
- `title` (string, 1-200 characters)
- `description` (string, max 1000 characters)
- `status` (boolean)
- `priority` (enum: "high", "medium", "low")
- `category` (string, max 50 characters)
- `due_date` (ISO 8601 datetime or null)

**Response (200 OK)**:
```json
{
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Buy groceries and cook dinner",
    "description": "Milk, eggs, bread",
    "status": false,
    "priority": "medium",
    "category": "personal",
    "due_date": "2026-01-25T10:00:00Z",
    "created_at": "2026-01-24T15:30:00Z",
    "updated_at": "2026-01-24T16:50:00Z"
  },
  "message": "Task updated successfully"
}
```

**Error Response (422)**:
```json
{
  "detail": "Validation error",
  "errors": [
    {
      "field": "title",
      "message": "Title cannot be empty"
    }
  ]
}
```

---

### 6. Delete Task

**Endpoint**: `DELETE /api/v1/tasks/{id}`

**Purpose**: Permanently delete a task.

**Path Parameters**:
- `id` (UUID): Task identifier

**Request Example**:
```http
DELETE /api/v1/tasks/550e8400-e29b-41d4-a716-446655440000
```

**Response (200 OK)**:
```json
{
  "data": null,
  "message": "Task deleted successfully"
}
```

**Alternative Response (204 No Content)**:
```
(empty body)
```

**Error Response (404)**:
```json
{
  "detail": "Task not found",
  "errors": [
    {
      "field": "id",
      "message": "Task with ID 550e8400-e29b-41d4-a716-446655440000 does not exist"
    }
  ]
}
```

**Note**: DELETE is idempotent - deleting a non-existent task returns 404, not 200.

---

### 7. Mark Task Complete

**Endpoint**: `PATCH /api/v1/tasks/{id}/complete`

**Purpose**: Mark a task as complete (convenience endpoint).

**Path Parameters**:
- `id` (UUID): Task identifier

**Request Body**: None

**Request Example**:
```http
PATCH /api/v1/tasks/550e8400-e29b-41d4-a716-446655440000/complete
```

**Response (200 OK)**:
```json
{
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "status": true,
    "priority": "high",
    "category": "personal",
    "due_date": "2026-01-25T10:00:00Z",
    "created_at": "2026-01-24T15:30:00Z",
    "updated_at": "2026-01-24T17:00:00Z"
  },
  "message": "Task marked as complete"
}
```

**Error Response (404)**:
```json
{
  "detail": "Task not found",
  "errors": [
    {
      "field": "id",
      "message": "Task with ID 550e8400-e29b-41d4-a716-446655440000 does not exist"
    }
  ]
}
```

**Note**: Idempotent - marking an already complete task returns 200 with no changes.

---

### 8. Mark Task Incomplete

**Endpoint**: `PATCH /api/v1/tasks/{id}/incomplete`

**Purpose**: Mark a task as incomplete (convenience endpoint).

**Path Parameters**:
- `id` (UUID): Task identifier

**Request Body**: None

**Request Example**:
```http
PATCH /api/v1/tasks/550e8400-e29b-41d4-a716-446655440000/incomplete
```

**Response (200 OK)**:
```json
{
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "status": false,
    "priority": "high",
    "category": "personal",
    "due_date": "2026-01-25T10:00:00Z",
    "created_at": "2026-01-24T15:30:00Z",
    "updated_at": "2026-01-24T17:05:00Z"
  },
  "message": "Task marked as incomplete"
}
```

**Error Response (404)**:
```json
{
  "detail": "Task not found",
  "errors": [
    {
      "field": "id",
      "message": "Task with ID 550e8400-e29b-41d4-a716-446655440000 does not exist"
    }
  ]
}
```

**Note**: Idempotent - marking an already incomplete task returns 200 with no changes.

---

### 9. Health Check

**Endpoint**: `GET /api/v1/health`

**Purpose**: Check API and database health.

**Request Example**:
```http
GET /api/v1/health
```

**Response (200 OK)**:
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2026-01-24T17:10:00Z"
}
```

**Response (500)** - Database connection failed:
```json
{
  "status": "unhealthy",
  "database": "disconnected",
  "timestamp": "2026-01-24T17:10:00Z"
}
```

---

## Pydantic Schemas

### Request Schemas

#### TaskCreate
```python
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional
from enum import Enum

class PriorityEnum(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    priority: PriorityEnum = Field(default=PriorityEnum.MEDIUM)
    category: Optional[str] = Field(None, max_length=50)
    due_date: Optional[datetime] = None

    @field_validator('title')
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('Title cannot be empty or whitespace')
        return v.strip()

    @field_validator('due_date')
    @classmethod
    def due_date_future(cls, v: Optional[datetime]) -> Optional[datetime]:
        if v and v < datetime.utcnow():
            raise ValueError('Due date must be in the future')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
                "priority": "high",
                "category": "personal",
                "due_date": "2026-01-25T10:00:00Z"
            }
        }
```

#### TaskUpdate (Full)
```python
class TaskUpdate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    status: bool
    priority: PriorityEnum
    category: Optional[str] = Field(None, max_length=50)
    due_date: Optional[datetime] = None

    @field_validator('title')
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('Title cannot be empty or whitespace')
        return v.strip()
```

#### TaskPatch (Partial)
```python
class TaskPatch(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    status: Optional[bool] = None
    priority: Optional[PriorityEnum] = None
    category: Optional[str] = Field(None, max_length=50)
    due_date: Optional[datetime] = None

    @field_validator('title')
    @classmethod
    def title_not_empty(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError('Title cannot be empty or whitespace')
        return v.strip() if v else None
```

### Response Schemas

#### TaskResponse
```python
from uuid import UUID

class TaskResponse(BaseModel):
    id: UUID
    title: str
    description: Optional[str]
    status: bool
    priority: str
    category: Optional[str]
    due_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```

#### TaskListResponse
```python
class PaginationInfo(BaseModel):
    page: int
    limit: int
    total: int
    pages: int

class TaskListResponse(BaseModel):
    data: list[TaskResponse]
    message: str
    pagination: PaginationInfo
```

#### ErrorDetail
```python
class ErrorField(BaseModel):
    field: str
    message: str

class ErrorResponse(BaseModel):
    detail: str
    errors: list[ErrorField] = []
```

---

## Query Parameter Validation

### TaskQueryParams
```python
from typing import Optional, Literal

class TaskQueryParams(BaseModel):
    status: Optional[Literal["complete", "incomplete"]] = None
    priority: Optional[PriorityEnum] = None
    category: Optional[str] = None
    search: Optional[str] = None
    sort: Optional[Literal["due_date", "priority", "created_at", "title"]] = "created_at"
    order: Optional[Literal["asc", "desc"]] = "desc"
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=20, ge=1, le=100)
```

---

## Error Handling

### Validation Errors (422)
```python
from fastapi import HTTPException
from pydantic import ValidationError

try:
    task = TaskCreate(**request_data)
except ValidationError as e:
    errors = [
        {"field": err["loc"][0], "message": err["msg"]}
        for err in e.errors()
    ]
    raise HTTPException(
        status_code=422,
        detail="Validation error",
        errors=errors
    )
```

### Not Found Errors (404)
```python
task = db.query(Task).filter(Task.id == task_id).first()
if not task:
    raise HTTPException(
        status_code=404,
        detail="Task not found",
        errors=[{
            "field": "id",
            "message": f"Task with ID {task_id} does not exist"
        }]
    )
```

### Server Errors (500)
```python
try:
    # Database operation
    db.commit()
except Exception as e:
    db.rollback()
    logger.error(f"Database error: {str(e)}")
    raise HTTPException(
        status_code=500,
        detail="Internal server error",
        errors=[{
            "field": "server",
            "message": "An unexpected error occurred"
        }]
    )
```

---

## CORS Configuration

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://your-app.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["*"],
)
```

---

## OpenAPI Documentation

FastAPI automatically generates OpenAPI documentation at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`

---

## Acceptance Criteria

### Endpoint Implementation
- [ ] All 9 endpoints implemented and functional
- [ ] Request/response schemas match specification
- [ ] Validation rules enforced on all inputs
- [ ] Error responses follow consistent format
- [ ] HTTP status codes used correctly

### Data Validation
- [ ] Title validation (required, non-empty, max 200 chars)
- [ ] Priority validation (high/medium/low only)
- [ ] Due date validation (future dates only)
- [ ] UUID validation for task IDs
- [ ] Query parameter validation

### Error Handling
- [ ] 404 for non-existent resources
- [ ] 422 for validation errors with field details
- [ ] 500 for server errors (logged, not exposed)
- [ ] Clear, actionable error messages

### API Features
- [ ] Filtering by status, priority, category
- [ ] Search by keyword (title and description)
- [ ] Sorting by multiple fields
- [ ] Pagination with metadata
- [ ] CORS configured for frontend

### Documentation
- [ ] OpenAPI/Swagger documentation auto-generated
- [ ] All endpoints documented with examples
- [ ] Request/response schemas documented
- [ ] Error responses documented

## Dependencies
- `00-system-architecture.md` - Overall system design
- `01-database-schema.md` - Database schema

## Related Specifications
- `backend/01-task-crud-api.md` - Backend implementation details
- `frontend/01-task-list-ui.md` - Frontend API consumption

---

**Version**: 1.0.0
**Created**: 2026-01-24
**Status**: Draft
**Author**: API Architect
