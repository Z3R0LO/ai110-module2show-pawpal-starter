# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

---------------------------------------------------------------
## Features

### Multi-pet management

The app models a full ownership hierarchy: an `Owner` holds a list of `Pet` objects, each of which owns its own list of `Task` objects. The sidebar lets you register additional pets on the fly. Every scheduling operation — agenda, conflicts, reminders — fans out across all pets automatically.

### Task scheduling with rich metadata

Each task stores a title, type (`walk`, `feeding`, `medication`, `appointment`, `grooming`), due date and time, priority (1–5), duration in minutes, optional recurrence, and free-text notes. Duration is critical — it is used by conflict detection to compute each task's time window.

### Chronological sorting

`Scheduler.sort_by_time()` sorts any list of tasks by `due_datetime` ascending. The "All Tasks" panel always displays tasks in this order regardless of insertion order, using Python's `sorted()` with a `due_datetime` key function.

### Priority-first daily agenda

`Scheduler.prioritize_tasks()` applies a three-level sort:

1. **Priority descending** — `Critical` (5) before `High` (4), and so on down to `Very Low` (1).
2. **Overdue first within a tier** — among tasks of equal priority, those already past due surface above future tasks.
3. **Time ascending as a tiebreaker** — tasks with the same priority and overdue status are ordered by `due_datetime`.

`Scheduler.get_daily_agenda()` filters to today's incomplete tasks and then applies this sort, producing the ranked schedule shown in the "Today's Prioritized Agenda" panel.

### Conflict detection

`Scheduler.detect_conflicts()` checks every pair of incomplete tasks for time-window overlap using the standard interval-intersection condition:

```
task A starts before task B ends  AND  task B starts before task A ends
```

Each window is `due_datetime` to `due_datetime + duration_minutes`. Completed tasks are excluded. Each detected overlap produces a warning string naming both tasks, their pets, and the exact time windows. The UI renders these as `st.warning` banners, or a `st.success` confirmation when the schedule is clean.

### Overdue detection

`Task.is_overdue()` returns `True` when `datetime.now() > due_datetime` and the task is not yet complete. Overdue tasks appear at the top of the daily agenda under a red `st.error` banner, separate from the prioritized table below.

### Recurring task auto-scheduling

`Scheduler.complete_task()` marks a task done and, if `recurrence` is set, automatically creates the next occurrence on the same pet:

- `"daily"` → next task due `due_datetime + 1 day`
- `"weekly"` → next task due `due_datetime + 7 days`

The new task inherits all metadata — title, type, priority, duration, notes, and recurrence — so the chain continues indefinitely. The UI reports the next scheduled date in a `st.success` message.

### Flexible filtering

`Scheduler.filter_tasks()` accepts two independent, combinable filters:

- `completed=True / False / None` — restrict to done, incomplete, or all tasks
- `pet_name` — case-insensitive match against `task.pet.name`

The "Filter Tasks" panel exposes both as dropdowns. Results are passed through `sort_by_time()` before display.

### Reminder generation

`Scheduler.send_reminder()` walks the `owner → pets` hierarchy to resolve the owner for a given task and returns a personalized message:

```
Hi Jordan! Reminder: 'Morning walk' for Mochi is due at 08:00 [High priority].
```

If the task has no pet attached, a generic fallback message is returned instead.

------------------------------------------------------------------

## Smarter Scheduling

The `Scheduler` class goes beyond a simple task list with several algorithmic features:

- **Priority-first ordering** — tasks are ranked by priority (1–5), with overdue tasks always surfaced first within the same tier.
- **Conflict detection** — flags any two tasks whose time windows overlap, using start/end datetime comparisons.
- **Daily agenda** — filters tasks to a target date and returns them in priority order, ready to display.
- **Auto-rescheduling** — completing a recurring task (`daily` or `weekly`) automatically creates the next occurrence on the same pet.
- **Flexible filtering** — tasks can be filtered by completion status, pet name, or both.

---------------------------------------------------------------

## Testing PawPal+

### Running the tests

```bash
python -m pytest tests/test_pawpal.py -v
```

### What the tests cover

| Area | Tests | What is verified |
|---|---|---|
| Task completion | `test_task_completion` | `complete()` sets `is_completed = True` |
| Pet task management | `test_task_addition_increases_count` | `add_task()` increments `pet.tasks` |
| Sorting | `test_sort_by_time_returns_chronological_order` | Tasks come back earliest `due_datetime` first regardless of insertion order |
| Sorting | `test_sort_by_time_already_ordered_unchanged` | A pre-sorted list is not disturbed |
| Recurrence | `test_complete_daily_task_creates_next_occurrence` | Completing a `daily` task creates a new task on the same pet due exactly 1 day later, with `recurrence` preserved |
| Recurrence | `test_complete_non_recurring_task_creates_no_next_occurrence` | A task with `recurrence=None` returns `None` and creates nothing |
| Conflict detection | `test_detect_conflicts_overlapping_tasks` | Two tasks with overlapping time windows produce a warning naming both tasks |
| Conflict detection | `test_detect_conflicts_non_overlapping_tasks` | Tasks sharing an exact boundary (end == start) are not flagged |
| Conflict detection | `test_detect_conflicts_ignores_completed_tasks` | Completed tasks are excluded from conflict checks |

### Confidence Level

**4 / 5 stars**

The core scheduling behaviors — sorting, recurrence, and conflict detection — are verified and all 9 tests pass. Confidence is not a full 5 stars because the test suite does not yet cover priority-based ordering (`prioritize_tasks`), the daily agenda, reminder formatting, or the `Owner.get_upcoming_tasks` edge cases identified during review. Those paths exist in the code but remain unverified by automated tests.

------------------------------------------------------------------

### Demo 

<a href="/ai110-module2show-pawpal-starter/final_app.png" target="_blank"><img src='/ai110-module2show-pawpal-starter

### check "final_app.png" under ai110-module2show-pawpal-starter

