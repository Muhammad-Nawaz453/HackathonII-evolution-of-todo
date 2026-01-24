# Todo Web App Constitution - Phase II

## Project Vision

Build a production-ready, full-stack web application that demonstrates excellence in modern web development, clean architecture, and spec-driven development. Transform the Phase I console application into a scalable, maintainable web platform with persistent storage, intuitive UI, and robust API design.

**Phase II Goals:**
- Deliver a responsive, user-friendly web interface
- Implement persistent database storage with PostgreSQL
- Create a RESTful API following industry best practices
- Deploy a production-ready application to cloud platforms
- Maintain spec-driven development discipline across frontend and backend
- Demonstrate clean separation between presentation, business logic, and data layers

## Core Principles

### I. Spec-Driven Development (NON-NEGOTIABLE)

**All code is generated from specifications - now across the full stack.**

- Every feature begins with a complete specification document
- Specifications must include: purpose, user stories, acceptance criteria, API contracts, UI mockups, data models, and error scenarios
- Backend specs define API endpoints, request/response schemas, validation rules, and database operations
- Frontend specs define component hierarchy, user interactions, state management, and API integration
- No code is written until the specification is reviewed and approved
- Implementation must match the specification exactly
- Changes to behavior require specification updates first

**Rationale**: In full-stack development, specifications serve as contracts between frontend and backend teams, ensuring API compatibility, reducing integration issues, and enabling parallel development.

### II. Clean Architecture & Separation of Concerns

**Each layer has a single, well-defined responsibility with clear boundaries.**

#### Backend Architecture (FastAPI)
- **Models Layer** (`models.py`): SQLModel database models, schema definitions, relationships
- **Database Layer** (`database.py`): Connection management, session handling, migrations
- **CRUD Layer** (`crud.py`): Database operations, queries, transactions
- **Schemas Layer** (`schemas.py`): Pydantic request/response models, validation
- **Routers Layer** (`routers/`): HTTP endpoints, request handling, response formatting
- **Main Application** (`main.py`): App initialization, middleware, CORS, error handlers

#### Frontend Architecture (Next.js)
- **Pages/Routes** (`app/`): Next.js App Router pages, layouts, routing
- **Components** (`components/`): Reusable UI components, presentational logic
- **API Client** (`lib/api.ts`): Backend communication, request/response handling
- **Types** (`types/`): TypeScript interfaces, type definitions
- **Utilities** (`lib/utils.ts`): Helper functions, formatters, validators

#### Architectural Rules
- No circular dependencies between layers
- Upper layers depend on lower layers, never the reverse
- Each layer has clear interfaces and contracts
- Business logic stays in the backend (CRUD layer)
- Frontend components are presentational and stateless where possible
- API client abstracts all backend communication

**Rationale**: Clean architecture enables independent testing, parallel development, technology swaps, and long-term maintainability.

### III. API Design Standards

**RESTful APIs must be consistent, predictable, and well-documented.**

#### HTTP Methods & Semantics
- `GET`: Retrieve resources (idempotent, no side effects)
- `POST`: Create new resources (non-idempotent)
- `PUT`: Update entire resource (idempotent)
- `PATCH`: Partial update (idempotent)
- `DELETE`: Remove resource (idempotent)

#### URL Structure
- Resource-based URLs: `/api/tasks`, `/api/tasks/{id}`, `/api/categories`
- Use plural nouns for collections: `/tasks` not `/task`
- Hierarchical relationships: `/tasks/{id}/subtasks`
- Query parameters for filtering: `/tasks?status=incomplete&priority=high`
- Query parameters for sorting: `/tasks?sort=due_date&order=asc`
- Query parameters for pagination: `/tasks?page=1&limit=20`

#### Status Codes
- `200 OK`: Successful GET, PUT, PATCH, DELETE
- `201 Created`: Successful POST with resource creation
- `204 No Content`: Successful DELETE with no response body
- `400 Bad Request`: Invalid input, validation errors
- `404 Not Found`: Resource doesn't exist
- `422 Unprocessable Entity`: Semantic validation errors
- `500 Internal Server Error`: Server-side failures

#### Response Format
```json
{
  "data": { /* resource or array */ },
  "message": "Success message",
  "errors": [ /* validation errors if any */ ]
}
```

#### Error Response Format
```json
{
  "detail": "Human-readable error message",
  "errors": [
    {
      "field": "title",
      "message": "Title is required"
    }
  ]
}
```

#### API Versioning
- Version in URL path: `/api/v1/tasks`
- Start with v1, increment for breaking changes
- Maintain backward compatibility within versions

**Rationale**: Consistent API design reduces cognitive load, improves developer experience, and enables automatic client generation.

### IV. Database Design Principles

**Data integrity, normalization, and performance are paramount.**

#### Schema Design
- Use UUIDs for primary keys (better for distributed systems)
- Include `created_at` and `updated_at` timestamps on all tables
- Use appropriate data types (ENUM for status/priority, TIMESTAMP for dates)
- Define foreign key constraints for referential integrity
- Add indexes on frequently queried columns (status, priority, due_date)
- Use NOT NULL constraints where appropriate

#### Normalization
- Follow 3NF (Third Normal Form) for data integrity
- Separate concerns: tasks, categories, tags in separate tables
- Use junction tables for many-to-many relationships
- Avoid data duplication

#### Migrations
- All schema changes through migrations (Alembic)
- Migrations are versioned and reversible
- Never modify existing migrations
- Test migrations on development database first

#### Query Optimization
- Use indexes for WHERE, ORDER BY, JOIN columns
- Avoid N+1 queries (use eager loading)
- Paginate large result sets
- Use database-level constraints and defaults

**Rationale**: Proper database design ensures data integrity, query performance, and scalability as the application grows.

### V. Frontend UX Guidelines

**The interface must be intuitive, responsive, and accessible.**

#### User Experience
- Immediate feedback for all user actions (loading states, success/error messages)
- Optimistic UI updates where appropriate
- Clear error messages with recovery suggestions
- Keyboard navigation support
- Mobile-first responsive design
- Consistent visual hierarchy and spacing

#### Component Design
- Single Responsibility: Each component does one thing well
- Composability: Build complex UIs from simple components
- Reusability: Extract common patterns into shared components
- Props over state: Prefer controlled components
- Accessibility: ARIA labels, semantic HTML, keyboard support

#### State Management
- Server state managed by API calls (React Query or SWR recommended)
- UI state kept local to components when possible
- Form state managed by form libraries (React Hook Form)
- Avoid prop drilling (use Context for deeply nested state)

#### Performance
- Code splitting for large components
- Lazy loading for routes and heavy components
- Debounce search inputs
- Virtualize long lists
- Optimize images (Next.js Image component)

**Rationale**: Great UX drives user adoption and satisfaction. Performance and accessibility are not optional.

### VI. Data Integrity & Validation

**Validate at every layer - defense in depth.**

#### Frontend Validation
- Immediate feedback on form inputs
- Client-side validation for UX (required fields, format, length)
- Clear error messages next to form fields
- Disable submit until form is valid

#### Backend Validation
- Pydantic schemas validate all incoming requests
- Business logic validation in CRUD layer
- Database constraints as final safety net
- Return detailed validation errors (field-level)

#### Validation Rules (Tasks)
- `title`: Required, 1-200 characters, non-empty after trim
- `description`: Optional, max 1000 characters
- `status`: Boolean only
- `priority`: Enum (high, medium, low)
- `category`: Optional string, max 50 characters
- `due_date`: Optional ISO 8601 datetime, must be future date
- `id`: UUID format, must exist for updates/deletes

**Rationale**: Multi-layer validation prevents bad data, improves security, and provides better user experience.

### VII. Security Standards

**Security is built-in, not bolted-on.**

#### API Security
- CORS configured for specific origins (not wildcard in production)
- Input validation and sanitization on all endpoints
- SQL injection prevention (use parameterized queries via SQLModel)
- Rate limiting on API endpoints (prevent abuse)
- HTTPS only in production
- Environment variables for secrets (never commit credentials)

#### Database Security
- Use connection pooling with proper limits
- Principle of least privilege for database users
- Encrypted connections to database (SSL/TLS)
- Regular backups (Neon handles this)
- No raw SQL queries (use ORM)

#### Frontend Security
- Sanitize user inputs before rendering
- XSS prevention (React escapes by default)
- CSRF protection (SameSite cookies if using auth)
- Secure environment variable handling (NEXT_PUBLIC_ prefix)
- No sensitive data in client-side code

**Rationale**: Security breaches destroy trust and can have legal consequences. Build security in from day one.

### VIII. Code Quality Standards

#### Backend (Python/FastAPI)
- **Version**: Python 3.11+ required
- **Package Manager**: UV exclusively
- **Style Guide**: PEP 8 compliance mandatory
- **Type Hints**: Required for all function signatures
- **Docstrings**: Required for all public functions and classes
- **Format**: Use `black` for formatting (line length: 88)
- **Linting**: Use `ruff` for linting
- **Testing**: Pytest for unit and integration tests

#### Frontend (TypeScript/Next.js)
- **Version**: Node.js 18+, Next.js 14+
- **Package Manager**: npm or pnpm
- **Language**: TypeScript strict mode
- **Style Guide**: ESLint with Next.js config
- **Format**: Prettier (line length: 100)
- **Component Style**: Functional components with hooks
- **CSS**: Tailwind CSS utility classes
- **Testing**: Jest + React Testing Library

#### Documentation Requirements
- Every module has a module-level docstring/comment explaining its purpose
- Every public function/component has documentation
- Complex logic includes inline comments explaining "why", not "what"
- API endpoints documented with OpenAPI/Swagger (FastAPI auto-generates)
- README files in backend/ and frontend/ directories

### IX. Error Handling

**Errors must be caught, logged, and communicated clearly.**

#### Backend Error Handling
- Use FastAPI exception handlers for consistent error responses
- Log all errors with context (endpoint, user input, stack trace)
- Return appropriate HTTP status codes
- Provide actionable error messages
- Never expose internal implementation details in errors

#### Frontend Error Handling
- Catch API errors and display user-friendly messages
- Use error boundaries for React component errors
- Provide retry mechanisms for transient failures
- Log errors to console in development
- Consider error tracking service (Sentry) for production

#### Error Categories
- **Validation Errors**: User input issues (400/422)
- **Not Found Errors**: Resource doesn't exist (404)
- **Server Errors**: Unexpected failures (500)
- **Network Errors**: Connection issues (timeout, offline)

**Rationale**: Good error handling improves debugging, user experience, and system reliability.

### X. Testing Strategy

**Test at every layer with appropriate test types.**

#### Backend Testing
- **Unit Tests**: Test CRUD functions, validation logic
- **Integration Tests**: Test API endpoints with test database
- **Schema Tests**: Verify Pydantic models validate correctly
- **Database Tests**: Test queries, transactions, constraints

#### Frontend Testing
- **Component Tests**: Test UI components in isolation
- **Integration Tests**: Test component interactions
- **API Tests**: Mock API calls, test error handling
- **E2E Tests**: Test critical user flows (optional for Phase II)

#### Test Coverage Goals
- Backend: 80%+ coverage for business logic
- Frontend: 70%+ coverage for components
- All edge cases covered
- All error paths tested

**Rationale**: Automated tests catch regressions, enable refactoring, and serve as living documentation.

## Technology Stack

### Backend
- **Framework**: FastAPI 0.109+
- **ORM**: SQLModel 0.0.14+
- **Database**: PostgreSQL (Neon Serverless)
- **Validation**: Pydantic v2
- **Migrations**: Alembic
- **Testing**: Pytest
- **ASGI Server**: Uvicorn

### Frontend
- **Framework**: Next.js 14+ (App Router)
- **Language**: TypeScript 5+
- **Styling**: Tailwind CSS 3+
- **HTTP Client**: Fetch API or Axios
- **Forms**: React Hook Form (optional)
- **Date Picker**: react-datepicker or similar
- **Icons**: Lucide React or Heroicons

### Infrastructure
- **Frontend Hosting**: Vercel
- **Backend Hosting**: Railway, Render, or local
- **Database**: Neon Serverless PostgreSQL
- **Version Control**: Git + GitHub

## Non-Negotiable Constraints

### Technical Constraints
1. **Database Required**: PostgreSQL via Neon (no in-memory storage)
2. **RESTful API**: Follow REST principles strictly
3. **Type Safety**: TypeScript on frontend, type hints on backend
4. **Responsive Design**: Mobile-first, works on all screen sizes
5. **Production Ready**: Deployable to cloud platforms

### Development Constraints
1. **Specification First**: No code without a spec (frontend AND backend)
2. **API Contract First**: Define API before implementing either side
3. **One Feature at a Time**: Complete each feature fully before starting the next
4. **No Scope Creep**: Implement exactly what's specified
5. **Version Control**: Commit after each completed feature with clear messages

### Deployment Constraints
1. **Frontend**: Must deploy to Vercel
2. **Database**: Must use Neon Serverless PostgreSQL
3. **Environment Variables**: All secrets in .env files (never committed)
4. **HTTPS**: Production must use HTTPS
5. **CORS**: Properly configured for frontend domain

## Development Workflow

### Feature Development Cycle

1. **Specify**: Write complete specification in `specs/` directory
   - Architecture specs for system-wide decisions
   - Backend specs for API endpoints and database operations
   - Frontend specs for UI components and user interactions

2. **API Contract**: Define API endpoints, request/response schemas
   - Document in architecture spec or backend spec
   - Review and approve before implementation

3. **Backend First**: Implement and test API endpoints
   - Write models, CRUD operations, routers
   - Test with Swagger UI or Postman
   - Verify all acceptance criteria

4. **Frontend Second**: Implement UI components
   - Create components, integrate with API
   - Test user interactions
   - Verify responsive design

5. **Integration**: Test full stack together
   - Verify data flow from UI to database
   - Test error handling end-to-end
   - Check edge cases

6. **Document**: Update README files
   - Backend API documentation
   - Frontend component documentation
   - Deployment instructions

7. **Commit**: Create atomic commits with clear messages
   - Separate commits for backend and frontend when appropriate
   - Reference specification in commit message

### Specification Template

Each specification must include:

- **Feature Name**: Clear, descriptive title
- **Purpose**: Why this feature exists
- **User Stories**: Who needs this and why
- **Acceptance Criteria**: Testable conditions for success
- **API Endpoints** (Backend specs): HTTP method, URL, request/response schemas
- **UI Components** (Frontend specs): Component hierarchy, props, state
- **Data Model**: Database schema, relationships, constraints
- **Validation Rules**: Input validation, error messages
- **Edge Cases**: Boundary conditions and error scenarios
- **Dependencies**: What other features/specs this relies on

## Success Metrics

A feature is successful when:

1. Specification is complete and unambiguous
2. API contract is defined and documented
3. Backend implementation matches specification exactly
4. Frontend implementation matches specification exactly
5. All acceptance criteria pass
6. All edge cases are handled gracefully
7. Code is clean, typed, and documented
8. User experience is intuitive and responsive
9. No regressions in existing features
10. Feature is deployed and accessible

## Project Constraints Summary

**DO:**
- Write specifications before code (frontend AND backend)
- Define API contracts first
- Keep code simple, typed, and readable
- Validate at every layer (frontend, backend, database)
- Provide clear error messages
- Follow REST principles
- Test thoroughly at each layer
- Document APIs and components
- Use environment variables for configuration
- Deploy early and often

**DON'T:**
- Write code without a specification
- Add features not in the spec
- Skip validation on any layer
- Expose internal errors to users
- Hardcode configuration values
- Ignore responsive design
- Skip error handling
- Commit secrets or credentials
- Deploy without testing
- Ignore security best practices

## Governance

### Constitution Authority
- This constitution supersedes all other development practices
- When in doubt, refer to this document
- Deviations require explicit justification and documentation
- All code reviews must verify constitutional compliance

### Amendment Process
1. Propose amendment with rationale
2. Document impact on existing code
3. Update constitution with version increment
4. Update all affected specifications
5. Refactor code to comply with new rules

### Enforcement
- Every pull request must pass constitutional review
- Violations must be fixed before merge
- Repeated violations indicate specification gaps
- Constitution is living document - update as needed

---

**Version**: 2.0.0
**Ratified**: 2026-01-24
**Last Amended**: 2026-01-24
**Next Review**: After Phase II completion
**Supersedes**: Constitution v1.0.0 (Phase I)
