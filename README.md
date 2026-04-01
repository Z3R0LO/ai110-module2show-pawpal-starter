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

## Smarter Scheduling

The `Scheduler` class goes beyond a simple task list with several algorithmic features:

- **Priority-first ordering** — tasks are ranked by priority (1–5), with overdue tasks always surfaced first within the same tier.
- **Conflict detection** — flags any two tasks whose time windows overlap, using start/end datetime comparisons.
- **Daily agenda** — filters tasks to a target date and returns them in priority order, ready to display.
- **Auto-rescheduling** — completing a recurring task (`daily` or `weekly`) automatically creates the next occurrence on the same pet.
- **Flexible filtering** — tasks can be filtered by completion status, pet name, or both.

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

---

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
