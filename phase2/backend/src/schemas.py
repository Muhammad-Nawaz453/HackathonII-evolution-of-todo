"""
Pydantic schemas for request/response validation.
"""
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional
from uuid import UUID
from enum import Enum


class PriorityEnum(str, Enum):
    """Priority levels for tasks."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class TaskCreate(BaseModel):
    """Schema for creating a new task."""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    priority: PriorityEnum = Field(default=PriorityEnum.MEDIUM)
    category: Optional[str] = Field(None, max_length=50)
    due_date: Optional[datetime] = None

    @field_validator('title')
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        """Validate title is not empty or whitespace."""
        if not v.strip():
            raise ValueError('Title cannot be empty or whitespace')
        return v.strip()

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


class TaskUpdate(BaseModel):
    """Schema for full task update (PUT)."""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    status: bool
    priority: PriorityEnum
    category: Optional[str] = Field(None, max_length=50)
    due_date: Optional[datetime] = None

    @field_validator('title')
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        """Validate title is not empty or whitespace."""
        if not v.strip():
            raise ValueError('Title cannot be empty or whitespace')
        return v.strip()


class TaskPatch(BaseModel):
    """Schema for partial task update (PATCH)."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    status: Optional[bool] = None
    priority: Optional[PriorityEnum] = None
    category: Optional[str] = Field(None, max_length=50)
    due_date: Optional[datetime] = None

    @field_validator('title')
    @classmethod
    def title_not_empty(cls, v: Optional[str]) -> Optional[str]:
        """Validate title is not empty or whitespace if provided."""
        if v is not None and not v.strip():
            raise ValueError('Title cannot be empty or whitespace')
        return v.strip() if v else None


class TaskResponse(BaseModel):
    """Schema for task response."""
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


class PaginationInfo(BaseModel):
    """Pagination metadata."""
    page: int
    limit: int
    total: int
    pages: int


class TaskListResponse(BaseModel):
    """Schema for task list response."""
    data: list[TaskResponse]
    message: str
    pagination: PaginationInfo


class TaskSingleResponse(BaseModel):
    """Schema for single task response."""
    data: TaskResponse
    message: str


class ErrorField(BaseModel):
    """Schema for field-level error."""
    field: str
    message: str


class ErrorResponse(BaseModel):
    """Schema for error response."""
    detail: str
    errors: list[ErrorField] = []
