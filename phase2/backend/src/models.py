"""
SQLModel database models.
"""
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4


class Task(SQLModel, table=True):
    """
    Task model representing a todo item.

    Attributes:
        id: Unique identifier (UUID)
        title: Task title (required, max 200 chars)
        description: Detailed description (optional)
        status: Completion status (False = incomplete, True = complete)
        priority: Priority level (high, medium, low)
        category: Category/tag (optional, max 50 chars)
        due_date: Due date (optional)
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """
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
