import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from datetime import datetime, timedelta
from pawpal_system import Task, Pet, Owner, Scheduler


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


def test_sort_by_time_returns_chronological_order():
    """sort_by_time() should return tasks ordered earliest due_datetime first."""
    scheduler = Scheduler()
    t1 = Task(id=1, title="Evening walk",   type="walk",    due_datetime=datetime(2026, 3, 31, 18, 0), priority=3)
    t2 = Task(id=2, title="Morning feeding",type="feeding", due_datetime=datetime(2026, 3, 31, 8, 0),  priority=4)
    t3 = Task(id=3, title="Noon medication",type="medication", due_datetime=datetime(2026, 3, 31, 12, 0), priority=5)

    sorted_tasks = scheduler.sort_by_time([t1, t2, t3])

    assert sorted_tasks[0].title == "Morning feeding"
    assert sorted_tasks[1].title == "Noon medication"
    assert sorted_tasks[2].title == "Evening walk"


def test_sort_by_time_already_ordered_unchanged():
    """sort_by_time() on an already-sorted list should return the same order."""
    scheduler = Scheduler()
    t1 = Task(id=1, title="Task A", type="walk",    due_datetime=datetime(2026, 3, 31, 7, 0),  priority=3)
    t2 = Task(id=2, title="Task B", type="feeding", due_datetime=datetime(2026, 3, 31, 9, 0),  priority=3)
    t3 = Task(id=3, title="Task C", type="feeding", due_datetime=datetime(2026, 3, 31, 11, 0), priority=3)

    sorted_tasks = scheduler.sort_by_time([t1, t2, t3])

    assert [t.id for t in sorted_tasks] == [1, 2, 3]


def test_complete_daily_task_creates_next_occurrence():
    """Completing a daily recurring task should create a new task due one day later."""
    scheduler = Scheduler()
    owner = Owner(id=1, name="Jordan", email="jordan@email.com", phone="555-0000")
    pet = Pet(id=1, name="Mochi", species="dog", breed="Shiba Inu", age=3, weight=10.5)
    owner.add_pet(pet)
    scheduler.add_owner(owner)

    due = datetime(2026, 3, 31, 8, 0)
    task = Task(id=1, title="Morning feeding", type="feeding",
                due_datetime=due, priority=4, recurrence="daily")
    scheduler.schedule_task(pet, task)

    next_task = scheduler.complete_task(task, next_task_id=2)

    assert task.is_completed is True
    assert next_task is not None
    assert next_task.due_datetime == due + timedelta(days=1)
    assert next_task.recurrence == "daily"
    assert next_task in pet.tasks


def test_complete_non_recurring_task_creates_no_next_occurrence():
    """Completing a task with no recurrence should return None."""
    scheduler = Scheduler()
    owner = Owner(id=1, name="Jordan", email="jordan@email.com", phone="555-0000")
    pet = Pet(id=1, name="Mochi", species="dog", breed="Shiba Inu", age=3, weight=10.5)
    owner.add_pet(pet)
    scheduler.add_owner(owner)

    task = Task(id=1, title="Vet appointment", type="appointment",
                due_datetime=datetime(2026, 3, 31, 15, 0), priority=5, recurrence=None)
    scheduler.schedule_task(pet, task)

    next_task = scheduler.complete_task(task, next_task_id=2)

    assert task.is_completed is True
    assert next_task is None


def test_detect_conflicts_overlapping_tasks():
    """Two tasks whose time windows overlap should produce a conflict warning."""
    scheduler = Scheduler()
    owner = Owner(id=1, name="Jordan", email="jordan@email.com", phone="555-0000")
    pet = Pet(id=1, name="Mochi", species="dog", breed="Shiba Inu", age=3, weight=10.5)
    owner.add_pet(pet)
    scheduler.add_owner(owner)

    # Morning walk: 7:30–8:00, Bath time: 7:45–8:05 — overlap
    t1 = Task(id=1, title="Morning walk", type="walk",
              due_datetime=datetime(2026, 3, 31, 7, 30), priority=3, duration_minutes=30)
    t2 = Task(id=2, title="Bath time", type="walk",
              due_datetime=datetime(2026, 3, 31, 7, 45), priority=2, duration_minutes=20)
    scheduler.schedule_task(pet, t1)
    scheduler.schedule_task(pet, t2)

    warnings = scheduler.detect_conflicts([t1, t2])

    assert len(warnings) == 1
    assert "Morning walk" in warnings[0]
    assert "Bath time" in warnings[0]


def test_detect_conflicts_non_overlapping_tasks():
    """Tasks that do not overlap should produce no warnings."""
    scheduler = Scheduler()
    owner = Owner(id=1, name="Jordan", email="jordan@email.com", phone="555-0000")
    pet = Pet(id=1, name="Mochi", species="dog", breed="Shiba Inu", age=3, weight=10.5)
    owner.add_pet(pet)
    scheduler.add_owner(owner)

    # Walk ends at 8:00, feeding starts at 8:00 — exact boundary, no overlap
    t1 = Task(id=1, title="Morning walk",    type="walk",    due_datetime=datetime(2026, 3, 31, 7, 30), priority=3, duration_minutes=30)
    t2 = Task(id=2, title="Breakfast feeding", type="feeding", due_datetime=datetime(2026, 3, 31, 8, 0),  priority=4, duration_minutes=10)
    scheduler.schedule_task(pet, t1)
    scheduler.schedule_task(pet, t2)

    warnings = scheduler.detect_conflicts([t1, t2])

    assert warnings == []


def test_detect_conflicts_ignores_completed_tasks():
    """A completed task should not be flagged as a conflict even if its window overlaps."""
    scheduler = Scheduler()
    owner = Owner(id=1, name="Jordan", email="jordan@email.com", phone="555-0000")
    pet = Pet(id=1, name="Mochi", species="dog", breed="Shiba Inu", age=3, weight=10.5)
    owner.add_pet(pet)
    scheduler.add_owner(owner)

    t1 = Task(id=1, title="Morning walk", type="walk",
              due_datetime=datetime(2026, 3, 31, 7, 30), priority=3, duration_minutes=30)
    t2 = Task(id=2, title="Bath time", type="walk",
              due_datetime=datetime(2026, 3, 31, 7, 45), priority=2, duration_minutes=20)
    t1.complete()
    scheduler.schedule_task(pet, t1)
    scheduler.schedule_task(pet, t2)

    warnings = scheduler.detect_conflicts([t1, t2])

    assert warnings == []
