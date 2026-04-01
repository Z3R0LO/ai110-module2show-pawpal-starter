from __future__ import annotations
from datetime import datetime, date, timedelta


class Task:
    PRIORITY_LABELS = {1: "Very Low", 2: "Low", 3: "Medium", 4: "High", 5: "Critical"}

    def __init__(self, id: int, title: str, type: str, due_datetime: datetime,
                 priority: int, duration_minutes: int = 0, notes: str = "",
                 recurrence: str = None):
        self.id = id
        self.title = title
        self.type = type          # "feeding", "walk", "medication", "appointment"
        self.due_datetime = due_datetime
        self.priority = priority  # 1 (lowest) to 5 (highest)
        self.duration_minutes = duration_minutes
        self.is_completed = False
        self.notes = notes
        self.recurrence = recurrence  # "daily", "weekly", or None
        self.pet: Pet | None = None  # set by Pet.add_task()

    def complete(self):
        """Mark this task as done."""
        self.is_completed = True

    def reschedule(self, new_datetime: datetime):
        """Move the task to a new time and reopen it if it was marked complete."""
        self.due_datetime = new_datetime
        self.is_completed = False

    def is_overdue(self) -> bool:
        """Return True if the task is past due and not yet completed."""
        return not self.is_completed and datetime.now() > self.due_datetime

    def get_priority_label(self) -> str:
        """Return a human-readable priority label."""
        return self.PRIORITY_LABELS.get(self.priority, "Unknown")

    def __repr__(self):
        status = "done" if self.is_completed else ("OVERDUE" if self.is_overdue() else "pending")
        return f"Task({self.title!r}, {self.get_priority_label()}, {self.due_datetime:%H:%M}, {status})"


class Pet:
    def __init__(self, id: int, name: str, species: str, breed: str, age: int, weight: float):
        self.id = id
        self.name = name
        self.species = species
        self.breed = breed
        self.age = age
        self.weight = weight
        self.medical_history: list[str] = []
        self.tasks: list[Task] = []  # single source of truth for this pet's tasks

    def add_task(self, task: Task):
        """Attach a task to this pet and set the back-reference."""
        task.pet = self
        self.tasks.append(task)

    def remove_task(self, task_id: int):
        """Remove a task by its id."""
        self.tasks = [t for t in self.tasks if t.id != task_id]

    def get_tasks(self) -> list[Task]:
        """Return all tasks for this pet."""
        return list(self.tasks)

    def get_overdue_tasks(self) -> list[Task]:
        """Return tasks that are past due and incomplete."""
        return [t for t in self.tasks if t.is_overdue()]

    def update_info(self, field: str, value):
        """Update a pet attribute by name (e.g. field='weight', value=12.5)."""
        if hasattr(self, field):
            setattr(self, field, value)
        else:
            raise AttributeError(f"Pet has no attribute '{field}'")

    def __repr__(self):
        return f"Pet({self.name!r}, {self.species}, {len(self.tasks)} tasks)"


class Owner:
    def __init__(self, id: int, name: str, email: str, phone: str):
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet):
        """Register a pet under this owner."""
        self.pets.append(pet)

    def remove_pet(self, pet_id: int):
        """Remove a pet by its id."""
        self.pets = [p for p in self.pets if p.id != pet_id]

    def get_pets(self) -> list[Pet]:
        """Return all pets belonging to this owner."""
        return list(self.pets)

    def get_upcoming_tasks(self, days: int = 1) -> list[Task]:
        """Return all incomplete tasks due within the next `days` days, across all pets."""
        cutoff = datetime.now() + timedelta(days=days)
        return [
            task
            for pet in self.pets
            for task in pet.tasks
            if not task.is_completed and task.due_datetime <= cutoff
        ]

    def __repr__(self):
        return f"Owner({self.name!r}, {len(self.pets)} pets)"


class Scheduler:
    def __init__(self):
        self.owners: list[Owner] = []

    @property
    def all_tasks(self) -> list[Task]:
        """Derive the full task list from the owner→pet→task hierarchy (single source of truth)."""
        return [task for owner in self.owners for pet in owner.pets for task in pet.tasks]

    def add_owner(self, owner: Owner):
        """Register an owner with the scheduler."""
        self.owners.append(owner)

    def schedule_task(self, pet: Pet, task: Task):
        """Add a task to a pet. The pet sets the back-reference via add_task()."""
        pet.add_task(task)

    def detect_conflicts(self, tasks: list[Task]) -> list[str]:
        """Check for scheduling conflicts among a list of tasks.

        Two tasks conflict when their time windows overlap:
            task A starts before task B ends AND task B starts before task A ends.

        Returns a list of warning strings (empty list = no conflicts).
        """
        warnings = []
        incomplete = [t for t in tasks if not t.is_completed]

        for i, a in enumerate(incomplete):
            for b in incomplete[i + 1:]:
                a_start = a.due_datetime
                a_end   = a.due_datetime + timedelta(minutes=a.duration_minutes)
                b_start = b.due_datetime
                b_end   = b.due_datetime + timedelta(minutes=b.duration_minutes)

                if a_start < b_end and b_start < a_end:
                    a_pet = a.pet.name if a.pet else "unknown pet"
                    b_pet = b.pet.name if b.pet else "unknown pet"
                    warnings.append(
                        f"WARNING: '{a.title}' ({a_pet}, {a_start:%I:%M %p}–{a_end:%I:%M %p}) "
                        f"overlaps with '{b.title}' ({b_pet}, {b_start:%I:%M %p}–{b_end:%I:%M %p})"
                    )

        return warnings

    def complete_task(self, task: Task, next_task_id: int) -> Task | None:
        """Mark a task complete. If it recurs, schedule the next occurrence on the same pet.

        Returns the newly created Task if one was scheduled, otherwise None.
        """
        task.complete()

        if task.recurrence == "daily":
            delta = timedelta(days=1)
        elif task.recurrence == "weekly":
            delta = timedelta(weeks=1)
        else:
            return None

        next_task = Task(
            id=next_task_id,
            title=task.title,
            type=task.type,
            due_datetime=task.due_datetime + delta,
            priority=task.priority,
            duration_minutes=task.duration_minutes,
            notes=task.notes,
            recurrence=task.recurrence,
        )
        self.schedule_task(task.pet, next_task)
        return next_task

    def filter_tasks(self, tasks: list[Task], completed: bool = None, pet_name: str = None) -> list[Task]:
        """Filter tasks by completion status and/or pet name.

        - completed=True  → only completed tasks
        - completed=False → only incomplete tasks
        - completed=None  → all tasks regardless of status
        - pet_name        → only tasks belonging to a pet with that name (case-insensitive)
        """
        result = tasks
        if completed is not None:
            result = [t for t in result if t.is_completed == completed]
        if pet_name is not None:
            result = [t for t in result if t.pet and t.pet.name.lower() == pet_name.lower()]
        return result

    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        """Sort tasks by due_datetime ascending."""
        return sorted(tasks, key=lambda t: t.due_datetime)

    def prioritize_tasks(self, tasks: list[Task]) -> list[Task]:
        """Sort tasks by priority descending, then due_datetime ascending.
        Overdue tasks are always surfaced first within the same priority tier."""
        return sorted(
            tasks,
            key=lambda t: (-t.priority, t.is_overdue() is False, t.due_datetime)
        )

    def get_daily_agenda(self, owner: Owner, agenda_date: date = None) -> list[Task]:
        """Return prioritized tasks for a specific date (defaults to today) for all of the owner's pets."""
        target = agenda_date or date.today()
        day_tasks = [
            task
            for pet in owner.pets
            for task in pet.tasks
            if not task.is_completed and task.due_datetime.date() == target
        ]
        return self.prioritize_tasks(day_tasks)

    def get_overdue_tasks(self) -> list[Task]:
        """Return all overdue tasks across every pet, delegating to Pet.get_overdue_tasks()."""
        return [task for owner in self.owners for pet in owner.pets for task in pet.get_overdue_tasks()]

    def send_reminder(self, task: Task) -> str:
        """Build a reminder message. Uses task.pet back-reference to find the owner."""
        if task.pet is None:
            return f"Reminder: '{task.title}' is due at {task.due_datetime:%H:%M}."

        owner = next(
            (o for o in self.owners if task.pet in o.pets),
            None
        )
        owner_name = owner.name if owner else "Owner"
        return (
            f"Hi {owner_name}! Reminder: '{task.title}' for {task.pet.name} "
            f"is due at {task.due_datetime:%H:%M} [{task.get_priority_label()} priority]."
        )
