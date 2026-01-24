"""
CRUD operations for tasks.
"""
from sqlmodel import Session, select, or_, func, col
from uuid import UUID
from typing import Optional
from datetime import datetime

from .models import Task
from .schemas import TaskCreate, TaskUpdate, TaskPatch


def create_task(session: Session, task_data: TaskCreate) -> Task:
    """
    Create a new task in the database.

    Args:
        session: Database session
        task_data: Task creation data

    Returns:
        Created task
    """
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
    """
    Get tasks with filtering, sorting, and pagination.

    Args:
        session: Database session
        status: Filter by status (complete/incomplete)
        priority: Filter by priority (high/medium/low)
        category: Filter by category
        search: Search in title and description
        sort: Sort field
        order: Sort order (asc/desc)
        page: Page number
        limit: Items per page

    Returns:
        Tuple of (tasks list, total count)
    """
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
    """
    Get a single task by ID.

    Args:
        session: Database session
        task_id: Task UUID

    Returns:
        Task if found, None otherwise
    """
    return session.get(Task, task_id)


def update_task(session: Session, task_id: UUID, task_data: TaskUpdate) -> Optional[Task]:
    """
    Update all fields of a task.

    Args:
        session: Database session
        task_id: Task UUID
        task_data: Updated task data

    Returns:
        Updated task if found, None otherwise
    """
    task = session.get(Task, task_id)
    if not task:
        return None

    for key, value in task_data.model_dump().items():
        setattr(task, key, value)

    task.updated_at = datetime.utcnow()
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def patch_task(session: Session, task_id: UUID, task_data: TaskPatch) -> Optional[Task]:
    """
    Update specific fields of a task.

    Args:
        session: Database session
        task_id: Task UUID
        task_data: Partial task data

    Returns:
        Updated task if found, None otherwise
    """
    task = session.get(Task, task_id)
    if not task:
        return None

    update_data = task_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(task, key, value)

    task.updated_at = datetime.utcnow()
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def delete_task(session: Session, task_id: UUID) -> bool:
    """
    Delete a task by ID.

    Args:
        session: Database session
        task_id: Task UUID

    Returns:
        True if deleted, False if not found
    """
    task = session.get(Task, task_id)
    if not task:
        return False

    session.delete(task)
    session.commit()
    return True


def mark_task_complete(session: Session, task_id: UUID) -> Optional[Task]:
    """
    Mark a task as complete.

    Args:
        session: Database session
        task_id: Task UUID

    Returns:
        Updated task if found, None otherwise
    """
    task = session.get(Task, task_id)
    if not task:
        return None

    task.status = True
    task.updated_at = datetime.utcnow()
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def mark_task_incomplete(session: Session, task_id: UUID) -> Optional[Task]:
    """
    Mark a task as incomplete.

    Args:
        session: Database session
        task_id: Task UUID

    Returns:
        Updated task if found, None otherwise
    """
    task = session.get(Task, task_id)
    if not task:
        return None

    task.status = False
    task.updated_at = datetime.utcnow()
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
