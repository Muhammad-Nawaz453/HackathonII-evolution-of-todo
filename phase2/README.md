# Todo Web Application - Phase II

## Overview

A full-stack web application for managing tasks with persistent database storage, built with modern technologies and following spec-driven development principles.

**Phase II** transforms the Phase I console application into a production-ready web platform with:
- **Frontend**: Next.js 14+ with TypeScript and Tailwind CSS
- **Backend**: FastAPI with SQLModel ORM
- **Database**: PostgreSQL (Neon Serverless)
- **Deployment**: Vercel (frontend), Railway/Render (backend)

## Features

### Basic Features (from Phase I)
1. ✅ Add Task - Create new tasks with title and description
2. ✅ Delete Task - Remove tasks permanently
3. ✅ Update Task - Edit task details
4. ✅ View Tasks - Display all tasks in a list
5. ✅ Mark Complete/Incomplete - Toggle task status

### Intermediate Features (Phase II)
1. 🎯 **Due Dates** - Set deadlines with date picker
2. 🎯 **Priorities & Categories** - Organize with priority levels (high/medium/low) and categories
3. 🎯 **Search & Filter** - Find tasks by keyword, filter by status/priority/category
4. 🎯 **Sort Tasks** - Sort by due date, priority, created date, or alphabetically

## Project Structure

```
phase2/
├── constitution.md                    # Phase II development principles
├── specs/                             # Feature specifications
│   ├── architecture/
│   │   ├── 00-system-architecture.md  # Overall system design
│   │   ├── 01-database-schema.md      # Database design
│   │   └── 02-api-design.md           # API endpoints
│   ├── backend/
│   │   └── 01-task-crud-api.md        # Backend implementation
│   └── frontend/
│       ├── 01-task-list-ui.md         # Task list component
│       ├── 02-task-form.md            # Task form component
│       └── 03-filters-sorting.md      # Filter/sort controls
├── backend/                           # FastAPI backend (to be created)
│   ├── src/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── database.py
│   │   ├── schemas.py
│   │   ├── crud.py
│   │   └── routers/
│   ├── alembic/
│   ├── tests/
│   ├── .env.example
│   ├── pyproject.toml
│   └── README.md
└── frontend/                          # Next.js frontend (to be created)
    ├── src/
    │   ├── app/
    │   ├── components/
    │   ├── lib/
    │   └── types/
    ├── public/
    ├── .env.local.example
    ├── package.json
    ├── tailwind.config.ts
    ├── tsconfig.json
    └── README.md
```

## Technology Stack

### Frontend
- **Framework**: Next.js 14+ (App Router)
- **Language**: TypeScript 5+
- **Styling**: Tailwind CSS 3+
- **HTTP Client**: Fetch API
- **Date Picker**: react-datepicker
- **Icons**: Lucide React
- **Deployment**: Vercel

### Backend
- **Framework**: FastAPI 0.109+
- **Language**: Python 3.11+
- **ORM**: SQLModel 0.0.14+
- **Database**: PostgreSQL (Neon Serverless)
- **Validation**: Pydantic v2
- **Migrations**: Alembic
- **Server**: Uvicorn
- **Deployment**: Railway or Render

### Development Tools
- **Backend**: UV (package manager), Black, Ruff, Pytest
- **Frontend**: npm/pnpm, ESLint, Prettier, Jest
- **Version Control**: Git + GitHub

## Getting Started

### Prerequisites
- **Node.js**: 18+ (for frontend)
- **Python**: 3.11+ (for backend)
- **UV**: Python package manager
- **Neon Account**: For PostgreSQL database
- **Vercel Account**: For frontend deployment

### Quick Start

#### 1. Clone Repository
```bash
cd phase2
```

#### 2. Set Up Backend
```bash
cd backend
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
cp .env.example .env
# Edit .env with your Neon database URL
alembic upgrade head
uvicorn src.main:app --reload
```

Backend runs at: `http://localhost:8000`
API docs at: `http://localhost:8000/docs`

#### 3. Set Up Frontend
```bash
cd frontend
npm install
cp .env.local.example .env.local
# Edit .env.local with backend API URL
npm run dev
```

Frontend runs at: `http://localhost:3000`

### Database Setup (Neon)

1. Create account at [neon.tech](https://neon.tech)
2. Create new project
3. Copy connection string
4. Add to backend `.env` file:
   ```
   DATABASE_URL=postgresql://user:password@host/database?sslmode=require
   ```
5. Run migrations: `alembic upgrade head`

## Development Workflow

### Spec-Driven Development

All features follow this workflow:

1. **Specify**: Write complete specification in `specs/` directory
2. **Review**: Verify specification is complete and unambiguous
3. **Backend First**: Implement API endpoints, test with Swagger UI
4. **Frontend Second**: Implement UI components, integrate with API
5. **Integration**: Test full stack together
6. **Document**: Update README files
7. **Commit**: Create atomic commits with clear messages

### Feature Development Example

To add a new feature:

1. Create specification: `specs/backend/XX-feature-name.md`
2. Implement backend: Update models, CRUD, routers
3. Test backend: Use Swagger UI at `/docs`
4. Create frontend spec: `specs/frontend/XX-feature-name.md`
5. Implement frontend: Create components, integrate API
6. Test integration: Verify end-to-end functionality
7. Commit changes: `git commit -m "feat: add feature-name"`

## API Documentation

### Base URL
- **Development**: `http://localhost:8000/api/v1`
- **Production**: `https://your-backend.railway.app/api/v1`

### Key Endpoints

#### Tasks
- `GET /tasks` - List all tasks (with filters, sorting, pagination)
- `POST /tasks` - Create new task
- `GET /tasks/{id}` - Get single task
- `PUT /tasks/{id}` - Update entire task
- `PATCH /tasks/{id}` - Partial update
- `DELETE /tasks/{id}` - Delete task
- `PATCH /tasks/{id}/complete` - Mark complete
- `PATCH /tasks/{id}/incomplete` - Mark incomplete

#### Health
- `GET /health` - Health check

Full API documentation available at `/docs` when backend is running.

## Deployment

### 🚀 Quick Deploy to Vercel

Both backend and frontend are deployed to Vercel from the same GitHub repository.

**📖 Complete Deployment Guide**: See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed step-by-step instructions.

### Live Demo

- **Frontend**: [https://your-frontend.vercel.app](https://your-frontend.vercel.app) _(Update after deployment)_
- **Backend API**: [https://your-backend.vercel.app](https://your-backend.vercel.app) _(Update after deployment)_
- **API Docs**: [https://your-backend.vercel.app/docs](https://your-backend.vercel.app/docs) _(Update after deployment)_

### Environment Variables Required

**Backend** (Vercel Project 1):
```env
DATABASE_URL=postgresql://user:password@host/database?sslmode=require
CORS_ORIGINS=https://your-frontend.vercel.app
ENVIRONMENT=production
```

**Frontend** (Vercel Project 2):
```env
NEXT_PUBLIC_API_URL=https://your-backend.vercel.app/api/v1
```

### Deployment Summary

1. **Backend**: Deploy from `phase2/backend/` directory
   - Framework: Other
   - Root Directory: `phase2/backend`
   - Install: `pip install -r requirements.txt`

2. **Frontend**: Deploy from `phase2/frontend/` directory
   - Framework: Next.js (auto-detected)
   - Root Directory: `phase2/frontend`
   - Install: `npm install`

3. **Database**: Neon PostgreSQL (already hosted)
   - No deployment needed
   - Add connection string to backend env vars

**📋 Detailed Instructions**: See [DEPLOYMENT.md](./DEPLOYMENT.md)

## Testing

### Backend Testing
```bash
cd backend
pytest tests/
```

### Frontend Testing
```bash
cd frontend
npm test
```

### Manual Testing
1. Start backend: `uvicorn src.main:app --reload`
2. Start frontend: `npm run dev`
3. Test all features in browser
4. Test on mobile devices
5. Test with screen reader (accessibility)

## Project Principles

### From Constitution (v2.0.0)

1. **Spec-Driven Development**: No code without specification
2. **Clean Architecture**: Clear separation of concerns
3. **API Design Standards**: RESTful, consistent, well-documented
4. **Data Integrity**: Validate at every layer
5. **Security First**: Built-in, not bolted-on
6. **User Experience**: Intuitive, responsive, accessible
7. **Code Quality**: Typed, tested, documented

See `constitution.md` for complete principles.

## Contributing

### Code Style

**Backend (Python)**:
- PEP 8 compliance
- Type hints required
- Docstrings for all public functions
- Format with Black (line length: 88)
- Lint with Ruff

**Frontend (TypeScript)**:
- ESLint with Next.js config
- TypeScript strict mode
- Format with Prettier (line length: 100)
- Functional components with hooks

### Commit Messages

Follow conventional commits:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting)
- `refactor:` Code refactoring
- `test:` Test changes
- `chore:` Build/tooling changes

Example: `feat(backend): implement task search endpoint`

## Troubleshooting

### Backend Issues

**Database connection failed**:
- Verify `DATABASE_URL` in `.env`
- Check Neon database is running
- Ensure SSL mode is enabled

**CORS errors**:
- Verify `CORS_ORIGINS` includes frontend URL
- Check frontend URL matches exactly (no trailing slash)

### Frontend Issues

**API calls failing**:
- Verify `NEXT_PUBLIC_API_URL` in `.env.local`
- Check backend is running
- Inspect network tab in browser DevTools

**Build errors**:
- Delete `.next` folder and rebuild
- Clear npm cache: `npm cache clean --force`
- Reinstall dependencies: `rm -rf node_modules && npm install`

## Resources

### Documentation
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Next.js Docs](https://nextjs.org/docs)
- [SQLModel Docs](https://sqlmodel.tiangolo.com/)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [Neon Docs](https://neon.tech/docs)

### Specifications
- All specifications in `specs/` directory
- Architecture specs: System design, database, API
- Backend specs: Implementation details
- Frontend specs: Component design, UI/UX

## License

This project is for educational purposes as part of a hackathon.

## Support

For issues or questions:
1. Check specifications in `specs/` directory
2. Review constitution for principles
3. Check API documentation at `/docs`
4. Review troubleshooting section above

---

**Version**: 2.0.0 (Phase II)
**Created**: 2026-01-24
**Status**: Foundation Complete - Ready for Implementation
**Next Steps**: Implement backend, then frontend, following specifications
