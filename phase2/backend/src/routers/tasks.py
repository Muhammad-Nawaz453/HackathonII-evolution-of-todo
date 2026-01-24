"""
Task API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from uuid import UUID
from typing import Optional

from .. import crud
from ..database import get_session
from ..schemas import (
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
