# Todo App - In-Memory Task Manager

A clean, simple command-line todo application built with spec-driven development principles. All tasks are stored in memory and cleared when the application exits.

## Project Status

**Phase I - COMPLETE ✅**

All Phase I features implemented and tested:
- ✅ Add Task
- ✅ View Tasks
- ✅ Delete Task
- ✅ Update Task
- ✅ Mark Complete/Incomplete

## Features

### 1. Add Task
Create new todo tasks with a title and optional description. Each task receives:
- Unique auto-generated ID
- Title (required, 1-200 characters)
- Description (optional, up to 1000 characters)
- Status (incomplete by default)
- Creation timestamp

### 2. View Tasks
Display all tasks with complete details including ID, title, description, status, and creation date. Shows a summary with task counts (total, complete, incomplete).

### 3. Delete Task
Permanently remove tasks by ID. Deleted task IDs are never reused.

### 4. Update Task
Modify the title and/or description of existing tasks. Press Enter to keep current values unchanged.

### 5. Mark Complete/Incomplete
Change task status to track progress. Mark tasks as complete when finished, or mark them incomplete to reopen them.

## Requirements

- **Python**: 3.13 or higher
- **Package Manager**: UV (recommended) or pip
- **Operating System**: Windows, macOS, or Linux

## Installation

### Option 1: Using UV (Recommended)

1. Install UV if you haven't already:
   ```bash
   # macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Windows
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

2. Clone or download this repository:
   ```bash
   cd todo_app
   ```

3. Run the application directly with UV:
   ```bash
   uv run python src/main.py
   ```

### Option 2: Using Standard Python

1. Ensure Python 3.13+ is installed:
   ```bash
   python --version
   ```

2. Navigate to the project directory:
   ```bash
   cd todo_app
   ```

3. Run the application:
   ```bash
   python src/main.py
   ```

## Usage

### Starting the Application

```bash
# With UV
uv run python src/main.py

# With standard Python
python src/main.py
```

### Available Commands

Once the application is running, you'll see a menu with available commands:

#### 1. Add Task
```
Command: add

Prompts:
1. Enter task title: [your title here]
2. Enter task description (optional, press Enter to skip): [your description]

Example:
  Enter task title: Buy groceries
  Enter task description: Milk, eggs, bread, and coffee

Output:
  Success: Task added successfully!
  ID: 1
  Title: Buy groceries
  Description: Milk, eggs, bread, and coffee
  Status: Incomplete
  Created: 2026-01-10T14:30:00.123456
```

#### 2. View Tasks
```
Command: view

Displays all tasks with complete details and summary statistics.

Example Output:
  ============================================================
  YOUR TODO LIST
  ============================================================

  Task #1
  Title: Buy groceries
  Description: Milk, eggs, bread, and coffee
  Status: Incomplete
  Created: 2026-01-10T10:00:00

  ------------------------------------------------------------

  Task #2
  Title: Finish project report
  Status: Complete
  Created: 2026-01-10T10:15:00

  ============================================================
  Summary: 2 tasks (1 complete, 1 incomplete)
  ============================================================
```

#### 3. Delete Task
```
Command: delete

Prompts:
1. Enter task ID to delete: [task ID]

Example:
  Enter task ID to delete: 3

Output:
  Success: Task deleted successfully!
  Deleted: "Buy groceries" (ID: 3)
```

#### 4. Update Task
```
Command: update

Prompts:
1. Enter task ID to update: [task ID]
2. Displays current task details
3. Enter new title (or press Enter to keep current): [new title or Enter]
4. Enter new description (or press Enter to keep current): [new description or Enter]

Example:
  Enter task ID to update: 1

  Current task:
  Task #1
  Title: Buy groceries
  Description: Milk and eggs
  Status: Incomplete

  Enter new title (or press Enter to keep current): Shopping list
  Enter new description (or press Enter to keep current): [Enter]

Output:
  Success: Task updated successfully!
  ID: 1
  Title: Shopping list
  Description: Milk and eggs
  Status: Incomplete
```

#### 5. Mark Complete
```
Command: complete

Prompts:
1. Enter task ID to mark as complete: [task ID]

Example:
  Enter task ID to mark as complete: 1

Output:
  Success: Task marked as complete!
  ID: 1
  Title: Buy groceries
  Status: Complete
```

#### 6. Mark Incomplete
```
Command: incomplete

Prompts:
1. Enter task ID to mark as incomplete: [task ID]

Example:
  Enter task ID to mark as incomplete: 1

Output:
  Success: Task marked as incomplete!
  ID: 1
  Title: Buy groceries
  Status: Incomplete
```

#### 7. Quit
```
Command: quit (or exit)

Exits the application and clears all tasks from memory.
```

### Input Validation

The application validates all inputs and provides clear error messages:

**Task Title:**
- **Empty Title**: "Error: Title cannot be empty"
- **Title Too Long**: "Error: Title cannot exceed 200 characters (provided: X characters)"

**Task Description:**
- **Description Too Long**: "Error: Description cannot exceed 1000 characters (provided: X characters)"

**Task ID:**
- **Non-Numeric**: "Error: Invalid task ID. Please provide a numeric ID"
- **Non-Positive**: "Error: Invalid task ID. Please provide a positive number"
- **Not Found**: "Error: Task with ID X not found"

### Data Persistence

**Important**: This application stores all data in memory only. When you exit the application, all tasks are permanently lost. This is by design for Phase I.

## Project Structure

```
todo_app/
├── constitution.md          # Project principles and development rules
├── specs/                   # Feature specifications
│   └── 01-add-task.md      # Add Task feature specification
├── src/                     # Python source code
│   ├── __init__.py         # Package initialization
│   ├── main.py             # Console interface and user interaction
│   ├── todo_manager.py     # Business logic and state management
│   └── models.py           # Task data model and validation
├── pyproject.toml          # Project configuration and dependencies
├── README.md               # This file
└── CLAUDE.md               # Instructions for Claude Code
```

## Development

### Philosophy

This project follows **Spec-Driven Development (SDD)**:
1. Every feature starts with a complete specification
2. Specifications define requirements, acceptance criteria, and edge cases
3. Code is generated from specifications
4. Implementation must match the specification exactly

See `constitution.md` for complete development principles.

### Code Quality Standards

- **Style Guide**: PEP 8 compliance
- **Type Hints**: Required for all function signatures
- **Docstrings**: Required for all public functions and classes
- **Formatting**: Black (line length: 88)
- **Linting**: Ruff

### Running Code Quality Tools

```bash
# Format code with Black
uv run black src/

# Lint code with Ruff
uv run ruff check src/

# Type check with mypy (if installed)
uv run mypy src/
```

### Adding New Features

1. Read `constitution.md` to understand project principles
2. Create a specification in `specs/XX-feature-name.md`
3. Review and approve the specification
4. Implement the feature according to the spec
5. Test all acceptance criteria and edge cases
6. Update this README if user-facing changes
7. Commit with clear message

## Architecture

### Module Responsibilities

**models.py**
- Defines the Task data structure
- Implements validation logic
- Handles data normalization (whitespace trimming, etc.)
- Generates timestamps

**todo_manager.py**
- Manages task storage (in-memory dictionary)
- Generates unique task IDs
- Coordinates task operations
- Provides business logic layer

**main.py**
- Displays user interface
- Captures user input
- Routes commands to appropriate handlers
- Displays success/error messages
- Manages application flow

### Data Flow

```
User Input → main.py → todo_manager.py → models.py
                ↓            ↓              ↓
            Display ← Result ← Validation ← Task Creation
```

## Examples

### Example Session

```
Welcome to Todo App!
Note: All data is stored in memory and will be lost when you exit.

==================================================
TODO APP - In-Memory Task Manager
==================================================

Available Commands:
  add    - Add a new task
  quit   - Exit the application

Enter command: add

--- Add New Task ---
Enter task title: Complete project documentation
Enter task description: Write README, update specs, and create examples

✓ Task added successfully!
ID: 1
Title: Complete project documentation
Description: Write README, update specs, and create examples
Status: Incomplete
Created: 2026-01-10T15:45:30.123456

==================================================
TODO APP - In-Memory Task Manager
==================================================

Available Commands:
  add    - Add a new task
  quit   - Exit the application

Enter command: quit

Goodbye! All tasks have been cleared from memory.
```

## Troubleshooting

### "Command not found" or "Module not found"

Make sure you're running the command from the project root directory:
```bash
cd todo_app
python src/main.py
```

### Python version issues

Verify you have Python 3.13+:
```bash
python --version
```

If you have multiple Python versions, you may need to use `python3` or `python3.13`:
```bash
python3.13 src/main.py
```

### UV not found

Install UV following the instructions at: https://docs.astral.sh/uv/

## Contributing

This is a learning project demonstrating spec-driven development. Contributions should:
1. Start with a specification document
2. Follow the constitution principles
3. Include clear documentation
4. Pass all validation checks

## License

This project is for educational purposes.

## Roadmap

### Phase I (Current)
- [x] Project setup and constitution
- [x] Add Task feature
- [ ] Delete Task feature
- [ ] Update Task feature
- [ ] View Tasks feature
- [ ] Mark Complete/Incomplete feature

### Phase II (Future)
- Task filtering and search
- Task sorting options
- Export/import functionality
- Configuration options

### Phase III (Future)
- File-based persistence
- Task categories/tags
- Due dates and reminders
- Priority levels

## Contact

For questions or feedback about this project, please refer to the project documentation or create an issue in the repository.

---

**Built with Spec-Driven Development** | **Python 3.13+** | **UV Package Manager**
