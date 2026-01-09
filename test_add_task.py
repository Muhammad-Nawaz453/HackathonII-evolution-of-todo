"""
Manual test script for the Add Task feature.

This script tests the core functionality without requiring interactive input.
"""

import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from models import Task, ValidationError
from todo_manager import TodoManager


def test_task_creation():
    """Test basic task creation."""
    print("Test 1: Basic task creation with title only")
    task = Task.create(task_id=1, title="Buy groceries")
    assert task.id == 1
    assert task.title == "Buy groceries"
    assert task.description == ""
    assert task.status is False
    assert task.created_at is not None
    print("[PASS]\n")


def test_task_with_description():
    """Test task creation with description."""
    print("Test 2: Task creation with title and description")
    task = Task.create(
        task_id=2, title="Finish report", description="Include Q4 metrics"
    )
    assert task.id == 2
    assert task.title == "Finish report"
    assert task.description == "Include Q4 metrics"
    assert task.status is False
    print("[PASS]\n")


def test_empty_title():
    """Test that empty title raises ValidationError."""
    print("Test 3: Empty title validation")
    try:
        Task.create(task_id=3, title="")
        assert False, "Should have raised ValidationError"
    except ValidationError as e:
        assert str(e) == "Title cannot be empty"
        print(f"[PASS] - Error message: {e}\n")


def test_whitespace_only_title():
    """Test that whitespace-only title raises ValidationError."""
    print("Test 4: Whitespace-only title validation")
    try:
        Task.create(task_id=4, title="   ")
        assert False, "Should have raised ValidationError"
    except ValidationError as e:
        assert str(e) == "Title cannot be empty"
        print(f"[PASS] - Error message: {e}\n")


def test_title_too_long():
    """Test that title exceeding 200 characters raises ValidationError."""
    print("Test 5: Title length validation (>200 chars)")
    long_title = "A" * 250
    try:
        Task.create(task_id=5, title=long_title)
        assert False, "Should have raised ValidationError"
    except ValidationError as e:
        assert "cannot exceed 200 characters" in str(e)
        assert "250 characters" in str(e)
        print(f"[PASS] - Error message: {e}\n")


def test_description_too_long():
    """Test that description exceeding 1000 characters raises ValidationError."""
    print("Test 6: Description length validation (>1000 chars)")
    long_desc = "A" * 1500
    try:
        Task.create(task_id=6, title="Valid title", description=long_desc)
        assert False, "Should have raised ValidationError"
    except ValidationError as e:
        assert "cannot exceed 1000 characters" in str(e)
        assert "1500 characters" in str(e)
        print(f"[PASS] - Error message: {e}\n")


def test_whitespace_trimming():
    """Test that leading/trailing whitespace is trimmed from title."""
    print("Test 7: Whitespace trimming")
    task = Task.create(task_id=7, title="  Buy milk  ")
    assert task.title == "Buy milk"
    print("[PASS]\n")


def test_newlines_in_title():
    """Test that newlines in title are converted to spaces."""
    print("Test 8: Newlines in title")
    task = Task.create(task_id=8, title="Buy\nmilk")
    assert task.title == "Buy milk"
    print("[PASS]\n")


def test_newlines_in_description():
    """Test that newlines in description are preserved."""
    print("Test 9: Newlines in description")
    task = Task.create(task_id=9, title="Task", description="Line 1\nLine 2")
    assert task.description == "Line 1\nLine 2"
    print("[PASS]\n")


def test_todo_manager_add():
    """Test TodoManager add_task functionality."""
    print("Test 10: TodoManager add_task")
    manager = TodoManager()

    # Add first task
    task1, error1 = manager.add_task("First task")
    assert task1 is not None
    assert error1 is None
    assert task1.id == 1

    # Add second task
    task2, error2 = manager.add_task("Second task", "With description")
    assert task2 is not None
    assert error2 is None
    assert task2.id == 2

    # Verify task count
    assert manager.task_count() == 2
    print("[PASS]\n")


def test_todo_manager_validation():
    """Test that TodoManager properly handles validation errors."""
    print("Test 11: TodoManager validation error handling")
    manager = TodoManager()

    # Try to add task with empty title
    task, error = manager.add_task("")
    assert task is None
    assert error == "Title cannot be empty"
    assert manager.task_count() == 0
    print("[PASS]\n")


def test_unique_id_generation():
    """Test that IDs are unique and sequential."""
    print("Test 12: Unique ID generation")
    manager = TodoManager()

    task1, _ = manager.add_task("Task 1")
    task2, _ = manager.add_task("Task 2")
    task3, _ = manager.add_task("Task 3")

    assert task1.id == 1
    assert task2.id == 2
    assert task3.id == 3
    print("[PASS]\n")


def test_special_characters():
    """Test that special characters are handled correctly."""
    print("Test 13: Special characters in title")
    task = Task.create(task_id=10, title="📝 Review code")
    assert task.title == "📝 Review code"
    assert len(task.title) == 13  # Character count, not bytes
    print("[PASS]\n")


def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("RUNNING ADD TASK FEATURE TESTS")
    print("=" * 60)
    print()

    tests = [
        test_task_creation,
        test_task_with_description,
        test_empty_title,
        test_whitespace_only_title,
        test_title_too_long,
        test_description_too_long,
        test_whitespace_trimming,
        test_newlines_in_title,
        test_newlines_in_description,
        test_todo_manager_add,
        test_todo_manager_validation,
        test_unique_id_generation,
        test_special_characters,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"[FAIL] - {e}\n")
            failed += 1

    print("=" * 60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("=" * 60)

    if failed == 0:
        print("\n[SUCCESS] All tests passed! The Add Task feature is working correctly.")
    else:
        print(f"\n[FAILURE] {failed} test(s) failed. Please review the implementation.")


if __name__ == "__main__":
    run_all_tests()
