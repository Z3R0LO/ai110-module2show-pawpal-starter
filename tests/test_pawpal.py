import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from datetime import datetime
from pawpal_system import Task, Pet


def test_task_completion():
    """Calling complete() should mark the task as completed."""
    task = Task(id=1, title="Morning walk", type="walk",
                due_datetime=datetime(2026, 3, 31, 7, 30), priority=3)

    assert task.is_completed is False

    task.complete()

    assert task.is_completed is True


def test_task_addition_increases_count():
    """Adding a task to a Pet should increase its task count by one."""
    pet = Pet(id=1, name="Mochi", species="dog", breed="Shiba Inu", age=3, weight=10.5)
    task = Task(id=2, title="Flea medication", type="medication",
                due_datetime=datetime(2026, 3, 31, 9, 0), priority=5)

    assert len(pet.tasks) == 0

    pet.add_task(task)

    assert len(pet.tasks) == 1
