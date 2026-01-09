"""
Comprehensive test script for all Phase I features.

Tests all five features: Add, View, Delete, Update, Mark Complete/Incomplete
"""

import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from models import Task, ValidationError
from todo_manager import TodoManager
from main import parse_task_id, format_status


def test_parse_task_id():
    """Test ID parsing utility."""
    print("=" * 60)
    print("TEST: parse_task_id()")
    print("=" * 60)

    # Valid IDs
    assert parse_task_id("5") == (5, None)
    assert parse_task_id("  10  ") == (10, None)
    assert parse_task_id("1") == (1, None)

    # Invalid IDs
    assert parse_task_id("")[1] is not None
    assert parse_task_id("abc")[1] is not None
    assert parse_task_id("0")[1] is not None
    assert parse_task_id("-5")[1] is not None
    assert parse_task_id("3.5")[1] is not None

    print("[PASS] All ID parsing tests passed\n")


def test_format_status():
    """Test status formatting utility."""
    print("=" * 60)
    print("TEST: format_status()")
    print("=" * 60)

    assert format_status(True) == "Complete"
    assert format_status(False) == "Incomplete"

    print("[PASS] All status formatting tests passed\n")


def test_view_empty_list():
    """Test viewing empty task list."""
    print("=" * 60)
    print("TEST: View Empty List")
    print("=" * 60)

    manager = TodoManager()
    tasks = manager.get_all_tasks()
    assert len(tasks) == 0
    print("[PASS] Empty list test passed\n")


def test_add_and_view():
    """Test adding tasks and viewing them."""
    print("=" * 60)
    print("TEST: Add and View Tasks")
    print("=" * 60)

    manager = TodoManager()

    # Add task 1
    task1, error1 = manager.add_task("Buy groceries", "Milk and eggs")
    assert task1 is not None
    assert error1 is None
    assert task1.id == 1
    assert task1.title == "Buy groceries"
    assert task1.description == "Milk and eggs"
    assert task1.status is False

    # Add task 2
    task2, error2 = manager.add_task("Call dentist")
    assert task2 is not None
    assert task2.id == 2
    assert task2.description == ""

    # Add task 3
    task3, error3 = manager.add_task("Finish report", "Include Q4 metrics")
    assert task3 is not None
    assert task3.id == 3

    # View all tasks
    tasks = manager.get_all_tasks()
    assert len(tasks) == 3
    assert tasks[0].id == 1
    assert tasks[1].id == 2
    assert tasks[2].id == 3

    print("[PASS] Add and view tests passed\n")
    return manager


def test_delete():
    """Test deleting tasks."""
    print("=" * 60)
    print("TEST: Delete Tasks")
    print("=" * 60)

    manager = TodoManager()
    manager.add_task("Task 1")
    manager.add_task("Task 2")
    manager.add_task("Task 3")

    # Delete task 2
    deleted, error = manager.delete_task(2)
    assert deleted is not None
    assert deleted.id == 2
    assert error is None

    # Verify task 2 is gone
    tasks = manager.get_all_tasks()
    assert len(tasks) == 2
    assert tasks[0].id == 1
    assert tasks[1].id == 3

    # Try to delete non-existent task
    deleted, error = manager.delete_task(99)
    assert deleted is None
    assert "not found" in error

    # Verify ID not reused
    task4, _ = manager.add_task("Task 4")
    assert task4.id == 4  # Not 2

    print("[PASS] Delete tests passed\n")


def test_update():
    """Test updating tasks."""
    print("=" * 60)
    print("TEST: Update Tasks")
    print("=" * 60)

    manager = TodoManager()
    task, _ = manager.add_task("Old Title", "Old Description")

    # Update title only
    updated, error, changed = manager.update_task(1, "New Title", None)
    assert updated is not None
    assert error is None
    assert changed is True
    assert updated.title == "New Title"
    assert updated.description == "Old Description"

    # Update description only
    updated, error, changed = manager.update_task(1, None, "New Description")
    assert updated is not None
    assert changed is True
    assert updated.title == "New Title"
    assert updated.description == "New Description"

    # Update both
    updated, error, changed = manager.update_task(1, "Final Title", "Final Desc")
    assert updated is not None
    assert changed is True
    assert updated.title == "Final Title"
    assert updated.description == "Final Desc"

    # No changes
    updated, error, changed = manager.update_task(1, None, None)
    assert updated is not None
    assert changed is False

    # Invalid title
    updated, error, changed = manager.update_task(1, "", None)
    assert updated is None
    assert "cannot be empty" in error
    assert changed is False

    # Non-existent task
    updated, error, changed = manager.update_task(99, "Title", None)
    assert updated is None
    assert "not found" in error

    print("[PASS] Update tests passed\n")


def test_mark_complete_incomplete():
    """Test marking tasks complete and incomplete."""
    print("=" * 60)
    print("TEST: Mark Complete/Incomplete")
    print("=" * 60)

    manager = TodoManager()
    task, _ = manager.add_task("Test Task")

    # Initially incomplete
    assert task.status is False

    # Mark complete
    marked, error, changed = manager.mark_complete(1)
    assert marked is not None
    assert error is None
    assert changed is True
    assert marked.status is True

    # Mark complete again (idempotent)
    marked, error, changed = manager.mark_complete(1)
    assert marked is not None
    assert changed is False
    assert marked.status is True

    # Mark incomplete
    marked, error, changed = manager.mark_incomplete(1)
    assert marked is not None
    assert changed is True
    assert marked.status is False

    # Mark incomplete again (idempotent)
    marked, error, changed = manager.mark_incomplete(1)
    assert marked is not None
    assert changed is False
    assert marked.status is False

    # Non-existent task
    marked, error, changed = manager.mark_complete(99)
    assert marked is None
    assert "not found" in error

    print("[PASS] Mark complete/incomplete tests passed\n")


def test_integration():
    """Test complete workflow integration."""
    print("=" * 60)
    print("TEST: Integration - Complete Workflow")
    print("=" * 60)

    manager = TodoManager()

    # Add multiple tasks
    manager.add_task("Task 1", "Description 1")
    manager.add_task("Task 2", "Description 2")
    manager.add_task("Task 3", "Description 3")
    manager.add_task("Task 4", "Description 4")

    # View all
    tasks = manager.get_all_tasks()
    assert len(tasks) == 4

    # Mark some complete
    manager.mark_complete(1)
    manager.mark_complete(3)

    # Verify status
    assert manager.get_task(1).status is True
    assert manager.get_task(2).status is False
    assert manager.get_task(3).status is True
    assert manager.get_task(4).status is False

    # Update a task
    manager.update_task(2, "Updated Task 2", None)
    assert manager.get_task(2).title == "Updated Task 2"

    # Delete a task
    manager.delete_task(3)
    tasks = manager.get_all_tasks()
    assert len(tasks) == 3
    assert manager.get_task(3) is None

    # Add new task (ID should be 5, not 3)
    task5, _ = manager.add_task("Task 5")
    assert task5.id == 5

    # Final verification
    tasks = manager.get_all_tasks()
    assert len(tasks) == 4
    assert [t.id for t in tasks] == [1, 2, 4, 5]

    print("[PASS] Integration tests passed\n")


def test_immutability():
    """Test that immutable fields remain unchanged."""
    print("=" * 60)
    print("TEST: Immutable Fields")
    print("=" * 60)

    manager = TodoManager()
    task, _ = manager.add_task("Original Title", "Original Description")

    original_id = task.id
    original_created_at = task.created_at

    # Update task
    manager.update_task(1, "New Title", "New Description")
    updated_task = manager.get_task(1)
    assert updated_task.id == original_id
    assert updated_task.created_at == original_created_at

    # Mark complete
    manager.mark_complete(1)
    marked_task = manager.get_task(1)
    assert marked_task.id == original_id
    assert marked_task.created_at == original_created_at

    print("[PASS] Immutability tests passed\n")


def run_all_tests():
    """Run all Phase I tests."""
    print("\n" + "=" * 60)
    print("RUNNING PHASE I COMPREHENSIVE TESTS")
    print("=" * 60)
    print()

    tests = [
        test_parse_task_id,
        test_format_status,
        test_view_empty_list,
        test_add_and_view,
        test_delete,
        test_update,
        test_mark_complete_incomplete,
        test_integration,
        test_immutability,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"[FAIL] {test.__name__}: {e}\n")
            failed += 1
        except Exception as e:
            print(f"[ERROR] {test.__name__}: {e}\n")
            failed += 1

    print("=" * 60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("=" * 60)

    if failed == 0:
        print("\n[SUCCESS] All Phase I features are working correctly!")
        print("All 5 features implemented and tested:")
        print("  1. Add Task")
        print("  2. Delete Task")
        print("  3. Update Task")
        print("  4. View Tasks")
        print("  5. Mark Complete/Incomplete")
    else:
        print(f"\n[FAILURE] {failed} test(s) failed. Please review the implementation.")

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
