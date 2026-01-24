# Database Schema Specification

## Feature Name
Database Schema Design - Tasks and Categories

## Purpose
Define the complete database schema for the Todo Web Application, including tables, columns, data types, constraints, indexes, and relationships. This specification serves as the contract between the application layer and data layer.

## Overview

The database uses PostgreSQL 15+ hosted on Neon Serverless. The schema follows normalization principles (3NF) while maintaining query performance through strategic indexing.

## Database Configuration

### Connection Settings
- **Database**: PostgreSQL 15+
- **Hosting**: Neon Serverless
- **Connection Pooling**: Enabled (max 20 connections)
- **SSL Mode**: Required
- **Timezone**: UTC (all timestamps stored in UTC)

### Environment Variable
```
DATABASE_URL=postgresql://user:password@host:5432/database?sslmode=require
```

## Schema Design

### Tasks Table

The primary table storing all task information.

```sql
CREATE TABLE tasks (
    -- Primary Key
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Core Fields
    title VARCHAR(200) NOT NULL,
    description TEXT,
    status BOOLEAN NOT NULL DEFAULT FALSE,

    -- Enhanced Fields (Phase II)
    priority VARCHAR(10) NOT NULL DEFAULT 'medium',
    category VARCHAR(50),
    due_date TIMESTAMP WITH TIME ZONE,

    -- Audit Fields
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),

    -- Constraints
    CONSTRAINT title_not_empty CHECK (LENGTH(TRIM(title)) > 0),
    CONSTRAINT priority_valid CHECK (priority IN ('high', 'medium', 'low')),
    CONSTRAINT due_date_future CHECK (due_date IS NULL OR due_date > created_at)
);

-- Indexes for Query Performance
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_priority ON tasks(priority);
CREATE INDEX idx_tasks_category ON tasks(category) WHERE category IS NOT NULL;
CREATE INDEX idx_tasks_due_date ON tasks(due_date) WHERE due_date IS NOT NULL;
CREATE INDEX idx_tasks_created_at ON tasks(created_at DESC);
CREATE INDEX idx_tasks_updated_at ON tasks(updated_at DESC);

-- Composite Index for Common Queries
CREATE INDEX idx_tasks_status_priority ON tasks(status, priority);
CREATE INDEX idx_tasks_status_due_date ON tasks(status, due_date) WHERE due_date IS NOT NULL;

-- Full-Text Search Index (for title and description)
CREATE INDEX idx_tasks_search ON tasks USING gin(to_tsvector('english', title || ' ' || COALESCE(description, '')));

-- Trigger for Automatic updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_tasks_updated_at
    BEFORE UPDATE ON tasks
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

### Column Specifications

#### id (UUID)
- **Type**: UUID
- **Constraints**: PRIMARY KEY
- **Default**: `gen_random_uuid()`
- **Nullable**: NO
- **Purpose**: Unique identifier for each task
- **Rationale**: UUIDs prevent ID enumeration attacks and work well in distributed systems

#### title (VARCHAR)
- **Type**: VARCHAR(200)
- **Constraints**: NOT NULL, CHECK (LENGTH(TRIM(title)) > 0)
- **Nullable**: NO
- **Purpose**: Task title/summary
- **Validation**: 1-200 characters after trimming whitespace
- **Rationale**: Reasonable length for task titles, prevents empty strings

#### description (TEXT)
- **Type**: TEXT
- **Constraints**: None
- **Nullable**: YES
- **Purpose**: Detailed task description
- **Validation**: Optional, unlimited length
- **Rationale**: Some tasks need detailed descriptions, others don't

#### status (BOOLEAN)
- **Type**: BOOLEAN
- **Constraints**: NOT NULL
- **Default**: FALSE
- **Nullable**: NO
- **Purpose**: Task completion status
- **Values**: FALSE (incomplete), TRUE (complete)
- **Rationale**: Simple boolean is clearer than string enums for binary state

#### priority (VARCHAR)
- **Type**: VARCHAR(10)
- **Constraints**: NOT NULL, CHECK (priority IN ('high', 'medium', 'low'))
- **Default**: 'medium'
- **Nullable**: NO
- **Purpose**: Task priority level
- **Values**: 'high', 'medium', 'low'
- **Rationale**: Three priority levels provide sufficient granularity without overwhelming users

#### category (VARCHAR)
- **Type**: VARCHAR(50)
- **Constraints**: None
- **Nullable**: YES
- **Purpose**: Task category/tag (e.g., 'work', 'personal', 'home')
- **Validation**: Optional, max 50 characters
- **Rationale**: Free-form categories provide flexibility; can be normalized to separate table in future

#### due_date (TIMESTAMP WITH TIME ZONE)
- **Type**: TIMESTAMP WITH TIME ZONE
- **Constraints**: CHECK (due_date IS NULL OR due_date > created_at)
- **Nullable**: YES
- **Purpose**: Task deadline
- **Validation**: Optional, must be after creation time if provided
- **Rationale**: Timezone-aware timestamps prevent confusion across timezones

#### created_at (TIMESTAMP WITH TIME ZONE)
- **Type**: TIMESTAMP WITH TIME ZONE
- **Constraints**: NOT NULL
- **Default**: NOW()
- **Nullable**: NO
- **Purpose**: Record creation timestamp
- **Rationale**: Audit trail, default sort order

#### updated_at (TIMESTAMP WITH TIME ZONE)
- **Type**: TIMESTAMP WITH TIME ZONE
- **Constraints**: NOT NULL
- **Default**: NOW()
- **Nullable**: NO
- **Purpose**: Last modification timestamp
- **Rationale**: Track when tasks were last changed, automatically updated via trigger

## Indexes Strategy

### Performance Indexes

#### idx_tasks_status
```sql
CREATE INDEX idx_tasks_status ON tasks(status);
```
- **Purpose**: Filter by completion status (most common query)
- **Queries**: `WHERE status = false`, `WHERE status = true`
- **Cardinality**: Low (2 values) but high selectivity

#### idx_tasks_priority
```sql
CREATE INDEX idx_tasks_priority ON tasks(priority);
```
- **Purpose**: Filter and sort by priority
- **Queries**: `WHERE priority = 'high'`, `ORDER BY priority`
- **Cardinality**: Low (3 values) but frequently used

#### idx_tasks_category
```sql
CREATE INDEX idx_tasks_category ON tasks(category) WHERE category IS NOT NULL;
```
- **Purpose**: Filter by category
- **Queries**: `WHERE category = 'work'`
- **Partial Index**: Only indexes non-NULL categories (saves space)

#### idx_tasks_due_date
```sql
CREATE INDEX idx_tasks_due_date ON tasks(due_date) WHERE due_date IS NOT NULL;
```
- **Purpose**: Sort by due date, find overdue tasks
- **Queries**: `ORDER BY due_date`, `WHERE due_date < NOW()`
- **Partial Index**: Only indexes tasks with due dates

#### idx_tasks_created_at
```sql
CREATE INDEX idx_tasks_created_at ON tasks(created_at DESC);
```
- **Purpose**: Default sort order (newest first)
- **Queries**: `ORDER BY created_at DESC`
- **Direction**: DESC for efficient newest-first queries

### Composite Indexes

#### idx_tasks_status_priority
```sql
CREATE INDEX idx_tasks_status_priority ON tasks(status, priority);
```
- **Purpose**: Combined filter (incomplete high-priority tasks)
- **Queries**: `WHERE status = false AND priority = 'high'`
- **Rationale**: Common use case for task prioritization

#### idx_tasks_status_due_date
```sql
CREATE INDEX idx_tasks_status_due_date ON tasks(status, due_date) WHERE due_date IS NOT NULL;
```
- **Purpose**: Incomplete tasks sorted by due date
- **Queries**: `WHERE status = false ORDER BY due_date`
- **Rationale**: Most important view for users

### Full-Text Search Index

#### idx_tasks_search
```sql
CREATE INDEX idx_tasks_search ON tasks USING gin(to_tsvector('english', title || ' ' || COALESCE(description, '')));
```
- **Purpose**: Fast text search across title and description
- **Queries**: `WHERE to_tsvector('english', title || ' ' || COALESCE(description, '')) @@ to_tsquery('groceries')`
- **Type**: GIN (Generalized Inverted Index)
- **Rationale**: Enables efficient full-text search without external search engine

## Constraints

### Primary Key Constraint
- **Constraint**: `PRIMARY KEY (id)`
- **Purpose**: Ensures uniqueness and enables foreign key references
- **Enforcement**: Database level

### Check Constraints

#### title_not_empty
```sql
CONSTRAINT title_not_empty CHECK (LENGTH(TRIM(title)) > 0)
```
- **Purpose**: Prevent empty or whitespace-only titles
- **Enforcement**: Database level
- **Error**: "Title cannot be empty"

#### priority_valid
```sql
CONSTRAINT priority_valid CHECK (priority IN ('high', 'medium', 'low'))
```
- **Purpose**: Ensure priority is one of three valid values
- **Enforcement**: Database level
- **Error**: "Priority must be high, medium, or low"

#### due_date_future
```sql
CONSTRAINT due_date_future CHECK (due_date IS NULL OR due_date > created_at)
```
- **Purpose**: Prevent due dates in the past (at creation time)
- **Enforcement**: Database level
- **Error**: "Due date must be in the future"
- **Note**: Does not prevent due dates from becoming past due over time

### NOT NULL Constraints
- **id**: Always required (auto-generated)
- **title**: Always required (user input)
- **status**: Always required (defaults to FALSE)
- **priority**: Always required (defaults to 'medium')
- **created_at**: Always required (auto-generated)
- **updated_at**: Always required (auto-generated)

## Triggers

### update_tasks_updated_at
```sql
CREATE TRIGGER update_tasks_updated_at
    BEFORE UPDATE ON tasks
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```
- **Purpose**: Automatically update `updated_at` timestamp on any row modification
- **Timing**: BEFORE UPDATE
- **Scope**: FOR EACH ROW
- **Function**: Sets `NEW.updated_at = NOW()`
- **Rationale**: Ensures accurate modification tracking without application logic

## Data Types Rationale

### UUID vs SERIAL
- **Choice**: UUID
- **Rationale**:
  - No ID enumeration (security)
  - Works in distributed systems
  - Can generate client-side if needed
  - No collision risk when merging databases
- **Trade-off**: Slightly larger storage (16 bytes vs 4 bytes)

### VARCHAR vs TEXT
- **title**: VARCHAR(200) - reasonable limit, indexed
- **description**: TEXT - unlimited, not indexed
- **category**: VARCHAR(50) - reasonable limit, indexed
- **Rationale**: Bounded fields use VARCHAR for clarity and index efficiency

### TIMESTAMP WITH TIME ZONE vs TIMESTAMP
- **Choice**: TIMESTAMP WITH TIME ZONE
- **Rationale**:
  - Handles users in different timezones
  - Stores in UTC, converts on retrieval
  - Prevents timezone-related bugs
- **Trade-off**: Slightly more complex queries

### BOOLEAN vs VARCHAR for status
- **Choice**: BOOLEAN
- **Rationale**:
  - Clearer semantics (true/false vs 'complete'/'incomplete')
  - Smaller storage (1 byte vs 10+ bytes)
  - Faster comparisons
  - Type-safe in application code

## Query Patterns

### Common Queries and Index Usage

#### List all incomplete tasks (default view)
```sql
SELECT * FROM tasks
WHERE status = false
ORDER BY created_at DESC
LIMIT 20;
```
- **Indexes Used**: `idx_tasks_status`, `idx_tasks_created_at`

#### List high-priority incomplete tasks
```sql
SELECT * FROM tasks
WHERE status = false AND priority = 'high'
ORDER BY due_date ASC;
```
- **Indexes Used**: `idx_tasks_status_priority`, `idx_tasks_status_due_date`

#### Search tasks by keyword
```sql
SELECT * FROM tasks
WHERE to_tsvector('english', title || ' ' || COALESCE(description, '')) @@ to_tsquery('groceries')
ORDER BY created_at DESC;
```
- **Indexes Used**: `idx_tasks_search`, `idx_tasks_created_at`

#### Filter by category
```sql
SELECT * FROM tasks
WHERE category = 'work' AND status = false
ORDER BY priority DESC, due_date ASC;
```
- **Indexes Used**: `idx_tasks_category`, `idx_tasks_status`, `idx_tasks_priority`

#### Find overdue tasks
```sql
SELECT * FROM tasks
WHERE status = false AND due_date < NOW()
ORDER BY due_date ASC;
```
- **Indexes Used**: `idx_tasks_status_due_date`

## Migration Strategy

### Initial Migration (Alembic)

```python
# alembic/versions/001_create_tasks_table.py
"""Create tasks table

Revision ID: 001
Revises:
Create Date: 2026-01-24
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'tasks',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('status', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('priority', sa.String(10), nullable=False, server_default='medium'),
        sa.Column('category', sa.String(50), nullable=True),
        sa.Column('due_date', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),
        sa.CheckConstraint("LENGTH(TRIM(title)) > 0", name='title_not_empty'),
        sa.CheckConstraint("priority IN ('high', 'medium', 'low')", name='priority_valid'),
        sa.CheckConstraint("due_date IS NULL OR due_date > created_at", name='due_date_future'),
    )

    # Create indexes
    op.create_index('idx_tasks_status', 'tasks', ['status'])
    op.create_index('idx_tasks_priority', 'tasks', ['priority'])
    op.create_index('idx_tasks_category', 'tasks', ['category'], postgresql_where=sa.text('category IS NOT NULL'))
    op.create_index('idx_tasks_due_date', 'tasks', ['due_date'], postgresql_where=sa.text('due_date IS NOT NULL'))
    op.create_index('idx_tasks_created_at', 'tasks', [sa.text('created_at DESC')])
    op.create_index('idx_tasks_updated_at', 'tasks', [sa.text('updated_at DESC')])
    op.create_index('idx_tasks_status_priority', 'tasks', ['status', 'priority'])
    op.create_index('idx_tasks_status_due_date', 'tasks', ['status', 'due_date'], postgresql_where=sa.text('due_date IS NOT NULL'))

    # Create full-text search index
    op.execute("""
        CREATE INDEX idx_tasks_search ON tasks
        USING gin(to_tsvector('english', title || ' ' || COALESCE(description, '')))
    """)

    # Create trigger function
    op.execute("""
        CREATE OR REPLACE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = NOW();
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)

    # Create trigger
    op.execute("""
        CREATE TRIGGER update_tasks_updated_at
            BEFORE UPDATE ON tasks
            FOR EACH ROW
            EXECUTE FUNCTION update_updated_at_column();
    """)

def downgrade():
    op.drop_table('tasks')
    op.execute("DROP FUNCTION IF EXISTS update_updated_at_column() CASCADE")
```

## SQLModel Definition

```python
# backend/src/models.py
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
    title: str = Field(max_length=200, min_length=1)
    description: Optional[str] = Field(default=None)
    status: bool = Field(default=False)
    priority: PriorityEnum = Field(default=PriorityEnum.MEDIUM)
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
```

## Acceptance Criteria

### Schema Design
- [ ] Tasks table created with all required columns
- [ ] All constraints defined (PRIMARY KEY, NOT NULL, CHECK)
- [ ] All indexes created for query optimization
- [ ] Trigger created for automatic updated_at
- [ ] Full-text search index created

### Data Integrity
- [ ] UUID primary key prevents ID enumeration
- [ ] Title cannot be empty or whitespace-only
- [ ] Priority must be high, medium, or low
- [ ] Due date must be in future at creation time
- [ ] Timestamps stored in UTC with timezone

### Performance
- [ ] Indexes cover common query patterns
- [ ] Partial indexes used where appropriate
- [ ] Composite indexes for combined filters
- [ ] Full-text search performs efficiently

### Migration
- [ ] Alembic migration creates schema correctly
- [ ] Migration is reversible (downgrade works)
- [ ] SQLModel definition matches database schema

## Dependencies
- `00-system-architecture.md` - Overall system design

## Related Specifications
- `02-api-design.md` - API endpoints using this schema
- `backend/01-task-crud-api.md` - CRUD operations on tasks table

## Future Enhancements
- **Categories Table**: Normalize categories into separate table with foreign key
- **Tags Table**: Many-to-many relationship for multiple tags per task
- **Users Table**: Add user authentication and task ownership
- **Audit Log**: Track all changes to tasks for history

---

**Version**: 1.0.0
**Created**: 2026-01-24
**Status**: Draft
**Author**: Database Architect
