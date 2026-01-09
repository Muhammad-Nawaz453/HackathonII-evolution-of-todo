# Todo App Constitution

## Project Vision

Build a clean, maintainable, and user-friendly command-line todo application that demonstrates excellence in spec-driven development. Every line of code must be traceable to a specification, and every feature must be designed before implementation.

## Core Principles

### I. Spec-Driven Development (NON-NEGOTIABLE)

**All code is generated from specifications.**

- Every feature begins with a complete specification document
- Specifications must include: purpose, user stories, acceptance criteria, input/output examples, edge cases, and data requirements
- No code is written until the specification is reviewed and approved
- Implementation must match the specification exactly
- Changes to behavior require specification updates first

**Rationale**: Specifications serve as contracts between intent and implementation, ensuring clarity, reducing rework, and creating living documentation.

### II. Clean Code & Simplicity

**Code must be readable, maintainable, and minimal.**

- Functions do one thing well
- Variable and function names are descriptive and unambiguous
- No premature optimization or over-engineering
- YAGNI (You Aren't Gonna Need It) - implement only what's specified
- DRY (Don't Repeat Yourself) - extract common patterns
- Maximum function length: 25 lines
- Maximum file length: 300 lines

**Rationale**: Simple code is easier to understand, test, and modify. Complexity is a liability.

### III. Modularity & Separation of Concerns

**Each module has a single, well-defined responsibility.**

- `models.py`: Data structures and validation only
- `todo_manager.py`: Business logic and state management
- `main.py`: User interface and command routing
- No circular dependencies
- Clear interfaces between modules
- Each module is independently testable

**Rationale**: Modular design enables parallel development, easier testing, and flexible refactoring.

### IV. Data Integrity & Validation

**All inputs are validated; all operations are safe.**

- Validate all user inputs before processing
- Provide clear, actionable error messages
- Handle edge cases explicitly (empty strings, invalid IDs, etc.)
- No silent failures - every error is communicated
- Defensive programming: assume inputs are malicious
- Immutable data where possible

**Rationale**: Robust validation prevents bugs, improves user experience, and builds trust.

### V. User Experience First

**The interface must be intuitive and forgiving.**

- Clear prompts and instructions
- Immediate feedback for all operations
- Graceful error handling with recovery suggestions
- Consistent command structure and output format
- Help text available for all commands
- No cryptic error codes or technical jargon

**Rationale**: A great CLI tool feels natural and helps users succeed without reading documentation.

### VI. In-Memory Constraints

**No persistence layer - embrace the limitations.**

- All data stored in memory (Python data structures)
- Data is lost when the program exits
- No file I/O, no databases, no external storage
- Clear communication to users about data volatility
- Focus on runtime performance and simplicity

**Rationale**: Constraints drive creativity and keep the codebase minimal. This is a learning project, not production software.

## Code Quality Standards

### Python Standards

- **Version**: Python 3.13+ required
- **Package Manager**: UV exclusively
- **Style Guide**: PEP 8 compliance mandatory
- **Type Hints**: Required for all function signatures
- **Docstrings**: Required for all public functions and classes
- **Format**: Use `black` for formatting (line length: 88)
- **Linting**: Use `ruff` for linting

### Documentation Requirements

- Every module has a module-level docstring explaining its purpose
- Every public function has a docstring with:
  - Brief description
  - Args with types
  - Returns with type
  - Raises (if applicable)
- Complex logic includes inline comments explaining "why", not "what"

### Error Handling

- Use custom exception classes for domain errors
- Never use bare `except:` clauses
- Log errors with context (what operation failed, what inputs caused it)
- Provide recovery paths where possible

## Non-Negotiable Constraints

### Technical Constraints

1. **No External Dependencies**: Only Python standard library (except for development tools like black, ruff)
2. **No Persistence**: Data exists only in memory during runtime
3. **Single Process**: No threading, no multiprocessing, no async
4. **Console Only**: No GUI, no web interface, no REST API
5. **Python 3.13+**: Use modern Python features

### Development Constraints

1. **Specification First**: No code without a spec
2. **One Feature at a Time**: Complete each feature fully before starting the next
3. **No Scope Creep**: Implement exactly what's specified, nothing more
4. **Test Manually**: Run the application and verify each feature works
5. **Version Control**: Commit after each completed feature

## Development Workflow

### Feature Development Cycle

1. **Specify**: Write complete specification in `specs/XX-feature-name.md`
2. **Review**: Verify specification is complete and unambiguous
3. **Design**: Plan data structures and module interactions
4. **Implement**: Write code that matches the specification exactly
5. **Verify**: Test all acceptance criteria and edge cases
6. **Document**: Update README if user-facing changes
7. **Commit**: Create atomic commit with clear message

### Specification Template

Each specification must include:

- **Feature Name**: Clear, descriptive title
- **Purpose**: Why this feature exists
- **User Stories**: Who needs this and why
- **Acceptance Criteria**: Testable conditions for success
- **Input/Output Examples**: Concrete examples with expected results
- **Edge Cases**: Boundary conditions and error scenarios
- **Data Requirements**: What data is needed and how it's structured
- **Dependencies**: What other features this relies on

### Code Review Checklist

Before considering a feature complete:

- [ ] Specification exists and is complete
- [ ] Implementation matches specification exactly
- [ ] All acceptance criteria are met
- [ ] All edge cases are handled
- [ ] Error messages are clear and helpful
- [ ] Code follows style guide (PEP 8)
- [ ] Type hints are present
- [ ] Docstrings are complete
- [ ] No hardcoded values (use constants)
- [ ] Manual testing completed successfully

## Data Model Standards

### Task Structure

Every task must have:

- `id`: Unique integer, auto-generated, immutable
- `title`: Non-empty string, required, max 200 characters
- `description`: Optional string, max 1000 characters
- `status`: Boolean (True = complete, False = incomplete), default False
- `created_at`: ISO 8601 timestamp, auto-generated, immutable

### ID Generation

- Sequential integers starting from 1
- Never reuse IDs, even after deletion
- IDs are assigned at creation time
- IDs are immutable

### Validation Rules

- Title: Required, non-empty after stripping whitespace, max 200 chars
- Description: Optional, max 1000 chars if provided
- Status: Boolean only, no other values accepted
- ID: Positive integer, must exist for update/delete operations

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

## Success Metrics

A feature is successful when:

1. Specification is complete and unambiguous
2. Implementation matches specification exactly
3. All acceptance criteria pass
4. All edge cases are handled gracefully
5. Code is clean, documented, and maintainable
6. User experience is intuitive and helpful
7. No regressions in existing features

## Project Constraints Summary

**DO:**
- Write specifications before code
- Keep code simple and readable
- Validate all inputs
- Provide clear error messages
- Follow Python best practices
- Document everything
- Test thoroughly

**DON'T:**
- Write code without a specification
- Add features not in the spec
- Use external dependencies (except dev tools)
- Persist data to disk or database
- Over-engineer or optimize prematurely
- Ignore edge cases
- Write cryptic code

---

**Version**: 1.0.0
**Ratified**: 2026-01-10
**Last Amended**: 2026-01-10
**Next Review**: After Phase I completion
