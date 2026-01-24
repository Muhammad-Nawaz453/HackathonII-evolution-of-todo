# Todo Backend - FastAPI

## Overview

RESTful API backend for the Todo Web Application, built with FastAPI and SQLModel, using PostgreSQL (Neon Serverless) for persistent storage.

## Features

- **RESTful API**: Standard HTTP methods and status codes
- **Data Validation**: Pydantic schemas for request/response validation
- **Database ORM**: SQLModel for type-safe database operations
- **Auto Documentation**: OpenAPI/Swagger UI at `/docs`
- **CORS Support**: Configured for Next.js frontend
- **Migrations**: Alembic for database schema versioning

## Tech Stack

- **Framework**: FastAPI 0.109+
- **Language**: Python 3.11+
- **ORM**: SQLModel 0.0.14+
- **Database**: PostgreSQL (Neon Serverless)
- **Validation**: Pydantic v2
- **Migrations**: Alembic
- **Server**: Uvicorn
- **Testing**: Pytest

## Project Structure

```
backend/
├── src/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry point
│   ├── database.py          # Database connection and session
│   ├── models.py            # SQLModel database models
│   ├── schemas.py           # Pydantic request/response schemas
│   ├── crud.py              # Database CRUD operations
│   └── routers/
│       ├── __init__.py
│       └── tasks.py         # Task endpoints
├── alembic/                 # Database migrations
│   ├── versions/
│   └── env.py
├── tests/                   # Test files
│   ├── __init__.py
│   ├── test_tasks.py
│   └── conftest.py
├── .env.example             # Environment variables template
├── .env                     # Environment variables (not committed)
├── pyproject.toml           # UV configuration
├── alembic.ini              # Alembic configuration
└── README.md                # This file
```

## Setup

### Prerequisites

- Python 3.11 or higher
- UV package manager
- Neon PostgreSQL database account

### Installation

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   uv venv
   ```

3. **Activate virtual environment**:
   ```bash
   # Linux/Mac
   source .venv/bin/activate

   # Windows
   .venv\Scripts\activate
   ```

4. **Install dependencies**:
   ```bash
   uv pip install -e ".[dev]"
   ```

5. **Set up environment variables**:
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your Neon database URL:
   ```
   DATABASE_URL=postgresql://user:password@host/database?sslmode=require
   CORS_ORIGINS=http://localhost:3000
   ENVIRONMENT=development
   ```

6. **Run database migrations**:
   ```bash
   alembic upgrade head
   ```

7. **Start development server**:
   ```bash
   uvicorn src.main:app --reload
   ```

The API will be available at `http://localhost:8000`

## API Documentation

### Interactive Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

### Endpoints

#### Tasks

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/tasks` | List all tasks (with filters, sorting, pagination) |
| POST | `/api/v1/tasks` | Create new task |
| GET | `/api/v1/tasks/{id}` | Get single task |
| PUT | `/api/v1/tasks/{id}` | Update entire task |
| PATCH | `/api/v1/tasks/{id}` | Partial update |
| DELETE | `/api/v1/tasks/{id}` | Delete task |
| PATCH | `/api/v1/tasks/{id}/complete` | Mark task complete |
| PATCH | `/api/v1/tasks/{id}/incomplete` | Mark task incomplete |

#### Health

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/health` | Health check |

### Query Parameters (GET /api/v1/tasks)

- `status`: Filter by status (`complete` or `incomplete`)
- `priority`: Filter by priority (`high`, `medium`, or `low`)
- `category`: Filter by category (string)
- `search`: Search in title and description (string)
- `sort`: Sort field (`due_date`, `priority`, `created_at`, `title`)
- `order`: Sort order (`asc` or `desc`)
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 20, max: 100)

### Example Requests

**Create Task**:
```bash
curl -X POST http://localhost:8000/api/v1/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "priority": "high",
    "category": "personal",
    "due_date": "2026-01-25T10:00:00Z"
  }'
```

**List Tasks**:
```bash
curl http://localhost:8000/api/v1/tasks?status=incomplete&priority=high&sort=due_date&order=asc
```

**Update Task**:
```bash
curl -X PATCH http://localhost:8000/api/v1/tasks/{id} \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Buy groceries and cook dinner"
  }'
```

**Delete Task**:
```bash
curl -X DELETE http://localhost:8000/api/v1/tasks/{id}
```

## Database

### Schema

The database uses PostgreSQL with the following schema:

**tasks** table:
- `id` (UUID, primary key)
- `title` (VARCHAR(200), required)
- `description` (TEXT, optional)
- `status` (BOOLEAN, default: false)
- `priority` (VARCHAR(10), default: 'medium')
- `category` (VARCHAR(50), optional)
- `due_date` (TIMESTAMP WITH TIME ZONE, optional)
- `created_at` (TIMESTAMP WITH TIME ZONE, auto)
- `updated_at` (TIMESTAMP WITH TIME ZONE, auto)

### Migrations

**Create new migration**:
```bash
alembic revision --autogenerate -m "Description of changes"
```

**Apply migrations**:
```bash
alembic upgrade head
```

**Rollback migration**:
```bash
alembic downgrade -1
```

**View migration history**:
```bash
alembic history
```

## Development

### Code Style

- **PEP 8**: Follow Python style guide
- **Type Hints**: Required for all function signatures
- **Docstrings**: Required for all public functions
- **Line Length**: 88 characters (Black default)

### Formatting

```bash
black src/ tests/
```

### Linting

```bash
ruff check src/ tests/
```

### Testing

**Run all tests**:
```bash
pytest
```

**Run with coverage**:
```bash
pytest --cov=src tests/
```

**Run specific test file**:
```bash
pytest tests/test_tasks.py
```

## Deployment

### Railway

1. Create new project in Railway
2. Connect GitHub repository
3. Add environment variables:
   - `DATABASE_URL`: Neon connection string
   - `CORS_ORIGINS`: Frontend URL (e.g., https://your-app.vercel.app)
4. Set start command: `uvicorn src.main:app --host 0.0.0.0 --port $PORT`
5. Deploy

### Render

1. Create new Web Service in Render
2. Connect GitHub repository
3. Set build command: `uv pip install -e .`
4. Set start command: `uvicorn src.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables (same as Railway)
6. Deploy

### Environment Variables (Production)

```
DATABASE_URL=postgresql://user:password@host/database?sslmode=require
CORS_ORIGINS=https://your-app.vercel.app
ENVIRONMENT=production
LOG_LEVEL=INFO
```

## Troubleshooting

### Database Connection Issues

**Error**: `could not connect to server`
- Verify `DATABASE_URL` is correct
- Check Neon database is running
- Ensure SSL mode is enabled (`?sslmode=require`)

**Error**: `password authentication failed`
- Verify username and password in connection string
- Check Neon database credentials

### CORS Issues

**Error**: `CORS policy: No 'Access-Control-Allow-Origin' header`
- Verify `CORS_ORIGINS` includes frontend URL
- Ensure URL matches exactly (no trailing slash)
- Check frontend is making requests to correct backend URL

### Migration Issues

**Error**: `Target database is not up to date`
- Run `alembic upgrade head`

**Error**: `Can't locate revision identified by`
- Delete `alembic/versions/` files and recreate: `alembic revision --autogenerate -m "Initial"`

## API Response Format

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

## Security

- **Input Validation**: All inputs validated with Pydantic
- **SQL Injection**: Prevented by SQLModel parameterized queries
- **CORS**: Restricted to specific origins
- **HTTPS**: Required in production
- **Environment Variables**: Secrets never committed to repository

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [Neon Documentation](https://neon.tech/docs)
- [Pydantic Documentation](https://docs.pydantic.dev/)

## Support

For issues or questions:
1. Check API documentation at `/docs`
2. Review specifications in `../specs/backend/`
3. Check troubleshooting section above
4. Review constitution in `../constitution.md`

---

**Version**: 1.0.0
**Created**: 2026-01-24
**Status**: Ready for Implementation
