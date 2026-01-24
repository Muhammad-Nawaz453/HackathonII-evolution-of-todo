# Backend Specification: Task CRUD API

## Feature Name
Task CRUD Operations - Backend Implementation

## Purpose
Implement the core CRUD (Create, Read, Update, Delete) operations for tasks in the FastAPI backend. This includes database operations, request validation, error handling, and response formatting.

## User Stories

1. **As a backend developer**, I need to implement task creation so the frontend can add new tasks to the database.
2. **As a backend developer**, I need to implement task retrieval so the frontend can display tasks to users.
3. **As a backend developer**, I need to implement task updates so users can modify existing tasks.
4. **As a backend developer**, I need to implement task deletion so users can remove tasks they no longer need.
5. **As a backend developer**, I need to implement status toggle operations so users can mark tasks complete/incomplete.

## Acceptance Criteria

### Create Task (POST /api/v1/tasks)
- [ ] Accepts JSON request body with task data
- [ ] Validates all fields using Pydantic schema
- [ ] Generates UUID for new task
- [ ] Sets default values (status=false, priority=medium)
- [ ] Saves task to database
- [ ] Returns 201 status with created task
- [ ] Returns 422 for validation errors with field details

### List Tasks (GET /api/v1/tasks)
- [ ] Retrieves all tasks from database
- [ ] Supports filtering by status, priority, category
- [ ] Supports search by keyword (title and description)
- [ ] Supports sorting by due_date, priority, created_at, title
- [ ] Supports pagination (page, limit)
- [ ] Returns 200 status with task array and pagination metadata
- [ ] Returns empty array if no tasks match filters

### Get Single Task (GET /api/v1/tasks/{id})
- [ ] Validates UUID format
- [ ] Retrieves task by ID from database
- [ ] Returns 200 status with task data
- [ ] Returns 404 if task not found
- [ ] Returns 400 if UUID format invalid

### Update Task - Full (PUT /api/v1/tasks/{id})
- [ ] Validates UUID format
- [ ] Validates all required fields in request body
- [ ] Updates all task fields in database
- [ ] Updates updated_at timestamp automatically (via trigger)
- [ ] Returns 200 status with updated task
- [ ] Returns 404 if task not found
- [ ] Returns 422 for validation errors

### Update Task - Partial (PATCH /api/v1/tasks/{id})
- [ ] Validates UUID format
- [ ] Validates only provided fields
- [ ] Updates only specified fields in database
- [ ] Updates updated_at timestamp automatically
- [ ] Returns 200 status with updated task
- [ ] Returns 404 if task not found
- [ ] Returns 422 for validation errors

### Delete Task (DELETE /api/v1/tasks/{id})
- [ ] Validates UUID format
- [ ] Deletes task from database
- [ ] Returns 200 status with success message
- [ ] Returns 404 if task not found

### Mark Complete (PATCH /api/v1/tasks/{id}/complete)
- [ ] Validates UUID format
- [ ] Sets status to true
- [ ] Updates updated_at timestamp
- [ ] Returns 200 status with updated task
- [ ] Returns 404 if task not found
- [ ] Idempotent (no error if already complete)

### Mark Incomplete (PATCH /api/v1/tasks/{id}/incomplete)
- [ ] Validates UUID format
- [ ] Sets status to false
- [ ] Updates updated_at timestamp
- [ ] Returns 200 status with updated task
- [ ] Returns 404 if task not found
- [ ] Idempotent (no error if already incomplete)

## Implementation Details

### File Structure
```
backend/
├── src/
│   ├── __init__.py
│   ├── main.py              # FastAPI app, CORS, error handlers
│   ├── database.py          # Database connection and session
│   ├── models.py            # SQLModel database models
│   ├── schemas.py           # Pydantic request/response schemas
│   ├── crud.py              # Database operations
│   └── routers/
│       ├── __init__.py
│       └── tasks.py         # Task endpoints
├── alembic/                 # Database migrations
├── tests/                   # Test files
├── .env.example
├── pyproject.toml
└── README.md
```

### Database Connection (database.py)

```python
from sqlmodel import create_engine, Session, SQLModel
from typing import Generator
import os

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    """Create database tables on startup."""
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    """Dependency for database sessions."""
    with Session(engine) as session:
        yield session
```

### Models (models.py)

```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from enum import Enum

class PriorityEnum(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None)
    status: bool = Field(default=False)
    priority: str = Field(default="medium", max_length=10)
    category: Optional[str] = Field(default=None, max_length=50)
    due_date: Optional[datetime] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### Schemas (schemas.py)

```python
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional
from uuid import UUID
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

class TaskListResponse(BaseModel):
    data: list[TaskResponse]
    message: str
    pagination: dict

class TaskSingleResponse(BaseModel):
    data: TaskResponse
    message: str
```

### CRUD Operations (crud.py)

```python
from sqlmodel import Session, select, or_, col
from uuid import UUID
from typing import Optional
from models import Task
from schemas import TaskCreate, TaskUpdate, TaskPatch

def create_task(session: Session, task_data: TaskCreate) -> Task:
    """Create a new task in the database."""
    task = Task(**task_data.model_dump())
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

def get_tasks(
    session: Session,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    category: Optional[str] = None,
    search: Optional[str] = None,
    sort: str = "created_at",
    order: str = "desc",
    page: int = 1,
    limit: int = 20
) -> tuple[list[Task], int]:
    """Get tasks with filtering, sorting, and pagination."""
    query = select(Task)

    # Apply filters
    if status is not None:
        status_bool = status == "complete"
        query = query.where(Task.status == status_bool)

    if priority is not None:
        query = query.where(Task.priority == priority)

    if category is not None:
        query = query.where(Task.category == category)

    if search is not None:
        search_pattern = f"%{search}%"
        query = query.where(
            or_(
                Task.title.ilike(search_pattern),
                Task.description.ilike(search_pattern)
            )
        )

    # Count total before pagination
    count_query = select(func.count()).select_from(query.subquery())
    total = session.exec(count_query).one()

    # Apply sorting
    sort_column = getattr(Task, sort)
    if order == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    # Apply pagination
    offset = (page - 1) * limit
    query = query.offset(offset).limit(limit)

    tasks = session.exec(query).all()
    return tasks, total

def get_task_by_id(session: Session, task_id: UUID) -> Optional[Task]:
    """Get a single task by ID."""
    return session.get(Task, task_id)

def update_task(session: Session, task_id: UUID, task_data: TaskUpdate) -> Optional[Task]:
    """Update all fields of a task."""
    task = session.get(Task, task_id)
    if not task:
        return None

    for key, value in task_data.model_dump().items():
        setattr(task, key, value)

    session.add(task)
    session.commit()
    session.refresh(task)
    return task

def patch_task(session: Session, task_id: UUID, task_data: TaskPatch) -> Optional[Task]:
    """Update specific fields of a task."""
    task = session.get(Task, task_id)
    if not task:
        return None

    update_data = task_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(task, key, value)

    session.add(task)
    session.commit()
    session.refresh(task)
    return task

def delete_task(session: Session, task_id: UUID) -> bool:
    """Delete a task by ID."""
    task = session.get(Task, task_id)
    if not task:
        return False

    session.delete(task)
    session.commit()
    return True

def mark_task_complete(session: Session, task_id: UUID) -> Optional[Task]:
    """Mark a task as complete."""
    task = session.get(Task, task_id)
    if not task:
        return None

    task.status = True
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

def mark_task_incomplete(session: Session, task_id: UUID) -> Optional[Task]:
    """Mark a task as incomplete."""
    task = session.get(Task, task_id)
    if not task:
        return None

    task.status = False
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
```

### Router (routers/tasks.py)

```python
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from uuid import UUID
from typing import Optional
import crud
from database import get_session
from schemas import (
    TaskCreate, TaskUpdate, TaskPatch,
    TaskResponse, TaskListResponse, TaskSingleResponse
)

router = APIRouter(prefix="/api/v1/tasks", tags=["tasks"])

@router.post("", response_model=TaskSingleResponse, status_code=201)
def create_task(
    task_data: TaskCreate,
    session: Session = Depends(get_session)
):
    """Create a new task."""
    task = crud.create_task(session, task_data)
    return {
        "data": task,
        "message": "Task created successfully"
    }

@router.get("", response_model=TaskListResponse)
def list_tasks(
    status: Optional[str] = Query(None, regex="^(complete|incomplete)$"),
    priority: Optional[str] = Query(None, regex="^(high|medium|low)$"),
    category: Optional[str] = None,
    search: Optional[str] = None,
    sort: str = Query("created_at", regex="^(due_date|priority|created_at|title)$"),
    order: str = Query("desc", regex="^(asc|desc)$"),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    session: Session = Depends(get_session)
):
    """List tasks with filtering, sorting, and pagination."""
    tasks, total = crud.get_tasks(
        session, status, priority, category, search,
        sort, order, page, limit
    )

    pages = (total + limit - 1) // limit

    return {
        "data": tasks,
        "message": "Tasks retrieved successfully",
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "pages": pages
        }
    }

@router.get("/{task_id}", response_model=TaskSingleResponse)
def get_task(
    task_id: UUID,
    session: Session = Depends(get_session)
):
    """Get a single task by ID."""
    task = crud.get_task_by_id(session, task_id)
    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return {
        "data": task,
        "message": "Task retrieved successfully"
    }

@router.put("/{task_id}", response_model=TaskSingleResponse)
def update_task(
    task_id: UUID,
    task_data: TaskUpdate,
    session: Session = Depends(get_session)
):
    """Update all fields of a task."""
    task = crud.update_task(session, task_id, task_data)
    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return {
        "data": task,
        "message": "Task updated successfully"
    }

@router.patch("/{task_id}", response_model=TaskSingleResponse)
def patch_task(
    task_id: UUID,
    task_data: TaskPatch,
    session: Session = Depends(get_session)
):
    """Update specific fields of a task."""
    task = crud.patch_task(session, task_id, task_data)
    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return {
        "data": task,
        "message": "Task updated successfully"
    }

@router.delete("/{task_id}")
def delete_task(
    task_id: UUID,
    session: Session = Depends(get_session)
):
    """Delete a task."""
    success = crud.delete_task(session, task_id)
    if not success:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return {
        "data": None,
        "message": "Task deleted successfully"
    }

@router.patch("/{task_id}/complete", response_model=TaskSingleResponse)
def mark_complete(
    task_id: UUID,
    session: Session = Depends(get_session)
):
    """Mark a task as complete."""
    task = crud.mark_task_complete(session, task_id)
    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return {
        "data": task,
        "message": "Task marked as complete"
    }

@router.patch("/{task_id}/incomplete", response_model=TaskSingleResponse)
def mark_incomplete(
    task_id: UUID,
    session: Session = Depends(get_session)
):
    """Mark a task as incomplete."""
    task = crud.mark_task_incomplete(session, task_id)
    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return {
        "data": task,
        "message": "Task marked as incomplete"
    }
```

### Main Application (main.py)

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import create_db_and_tables
from routers import tasks
import os

app = FastAPI(
    title="Todo API",
    description="RESTful API for Todo Web Application",
    version="1.0.0"
)

# CORS configuration
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(tasks.router)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/api/v1/health")
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "database": "connected",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/")
def root():
    """Root endpoint."""
    return {
        "message": "Todo API",
        "docs": "/docs",
        "version": "1.0.0"
    }
```

## Testing Strategy

### Manual Testing with Swagger UI
1. Start backend: `uvicorn src.main:app --reload`
2. Open browser: `http://localhost:8000/docs`
3. Test each endpoint with various inputs
4. Verify responses match specification

### Test Cases

#### Create Task
- Valid task with all fields → 201
- Valid task with only title → 201 (defaults applied)
- Empty title → 422
- Invalid priority → 422
- Past due date → 422

#### List Tasks
- No filters → All tasks
- Filter by status=incomplete → Only incomplete tasks
- Filter by priority=high → Only high priority tasks
- Search "groceries" → Tasks matching keyword
- Sort by due_date asc → Ordered by due date
- Page 2, limit 10 → Second page of results

#### Get Task
- Valid UUID → 200 with task
- Non-existent UUID → 404
- Invalid UUID format → 400

#### Update Task
- Valid data → 200 with updated task
- Non-existent task → 404
- Invalid data → 422

#### Delete Task
- Existing task → 200
- Non-existent task → 404

## Edge Cases

1. **Empty Database**: List tasks returns empty array with pagination
2. **Duplicate Titles**: Allowed (no uniqueness constraint)
3. **Null Category**: Allowed (optional field)
4. **Whitespace Title**: Trimmed and validated
5. **Already Complete**: Mark complete is idempotent
6. **Concurrent Updates**: Last write wins (no optimistic locking)

## Dependencies
- `architecture/00-system-architecture.md`
- `architecture/01-database-schema.md`
- `architecture/02-api-design.md`

## Related Specifications
- `backend/02-search-filter-api.md` - Advanced search features
- `frontend/01-task-list-ui.md` - Frontend consuming this API

---

**Version**: 1.0.0
**Created**: 2026-01-24
**Status**: Draft
**Author**: Backend Developer
