import streamlit as st
from datetime import datetime, date, time
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="wide")
st.title("🐾 PawPal+")
st.caption("Pet care scheduling — powered by priority, conflict detection, and smart sorting.")

# ── Session state init ────────────────────────────────────────────────────────
if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler()
if "owner" not in st.session_state:
    st.session_state.owner = Owner(id=1, name="Jordan", email="", phone="")
    st.session_state.scheduler.add_owner(st.session_state.owner)
if "pets" not in st.session_state:
    default_pet = Pet(id=1, name="Mochi", species="dog", breed="", age=0, weight=0.0)
    st.session_state.owner.add_pet(default_pet)
    st.session_state.pets = [default_pet]
if "task_id_counter" not in st.session_state:
    st.session_state.task_id_counter = 1

scheduler: Scheduler = st.session_state.scheduler
owner: Owner = st.session_state.owner

# ── Sidebar — owner & pet setup ───────────────────────────────────────────────
with st.sidebar:
    st.header("Setup")

    owner.name = st.text_input("Owner name", value=owner.name)

    st.subheader("Pets")
    for pet in st.session_state.pets:
        st.markdown(f"- **{pet.name}** ({pet.species})")

    with st.expander("Add a pet"):
        new_pet_name    = st.text_input("Pet name",  key="new_pet_name")
        new_pet_species = st.selectbox("Species", ["dog", "cat", "other"], key="new_pet_species")
        new_pet_breed   = st.text_input("Breed (optional)", key="new_pet_breed")
        if st.button("Add pet"):
            if new_pet_name.strip():
                new_id  = len(st.session_state.pets) + 1
                new_pet = Pet(id=new_id, name=new_pet_name.strip(),
                              species=new_pet_species, breed=new_pet_breed,
                              age=0, weight=0.0)
                owner.add_pet(new_pet)
                st.session_state.pets.append(new_pet)
                st.success(f"Added {new_pet_name}!")
                st.rerun()
            else:
                st.error("Enter a pet name.")

# ── Add task ──────────────────────────────────────────────────────────────────
st.subheader("Add a Task")

TASK_TYPES    = ["walk", "feeding", "medication", "appointment", "grooming", "other"]
PRIORITY_MAP  = {"Very Low": 1, "Low": 2, "Medium": 3, "High": 4, "Critical": 5}
RECURRENCE_MAP = {"None": None, "Daily": "daily", "Weekly": "weekly"}

col1, col2, col3 = st.columns(3)
with col1:
    task_title    = st.text_input("Task title", value="Morning walk")
    task_type     = st.selectbox("Type", TASK_TYPES)
with col2:
    task_time     = st.time_input("Due time", value=time(8, 0))
    task_duration = st.number_input("Duration (min)", min_value=0, max_value=480, value=30)
with col3:
    priority_label = st.selectbox("Priority", list(PRIORITY_MAP.keys()), index=3)
    recurrence_label = st.selectbox("Recurrence", list(RECURRENCE_MAP.keys()))

pet_names = [p.name for p in st.session_state.pets]
assign_to = st.selectbox("Assign to pet", pet_names)

if st.button("Add task", type="primary"):
    due = datetime.combine(date.today(), task_time)
    task = Task(
        id=st.session_state.task_id_counter,
        title=task_title,
        type=task_type,
        due_datetime=due,
        priority=PRIORITY_MAP[priority_label],
        duration_minutes=int(task_duration),
        recurrence=RECURRENCE_MAP[recurrence_label],
    )
    target_pet = next(p for p in st.session_state.pets if p.name == assign_to)
    scheduler.schedule_task(target_pet, task)
    st.session_state.task_id_counter += 1
    st.success(f"Added **{task_title}** to {assign_to}'s tasks.")

st.divider()

# ── All tasks — sorted by time ────────────────────────────────────────────────
st.subheader("All Tasks — Sorted by Time")

all_tasks = scheduler.all_tasks
if not all_tasks:
    st.info("No tasks yet. Add one above.")
else:
    sorted_tasks = scheduler.sort_by_time(all_tasks)
    st.table([
        {
            "Time":          t.due_datetime.strftime("%I:%M %p"),
            "Pet":           t.pet.name if t.pet else "—",
            "Task":          t.title,
            "Type":          t.type,
            "Priority":      t.get_priority_label(),
            "Duration (min)": t.duration_minutes,
            "Recurrence":    t.recurrence or "—",
            "Status":        "Done" if t.is_completed else ("OVERDUE" if t.is_overdue() else "Pending"),
        }
        for t in sorted_tasks
    ])

st.divider()

# ── Conflict warnings ─────────────────────────────────────────────────────────
st.subheader("Conflict Detection")

if not all_tasks:
    st.info("Add tasks to check for conflicts.")
else:
    conflicts = scheduler.detect_conflicts(all_tasks)
    if conflicts:
        for warning in conflicts:
            st.warning(warning)
    else:
        st.success("No scheduling conflicts detected.")

st.divider()

# ── Daily agenda ──────────────────────────────────────────────────────────────
st.subheader("Today's Prioritized Agenda")

agenda = scheduler.get_daily_agenda(owner, date.today())
overdue = scheduler.get_overdue_tasks()

if overdue:
    st.error(f"{len(overdue)} overdue task(s) need attention:")
    for t in overdue:
        st.markdown(
            f"- **{t.title}** ({t.pet.name if t.pet else '?'}) — "
            f"was due at {t.due_datetime.strftime('%I:%M %p')}"
        )

if not agenda:
    st.info("No incomplete tasks scheduled for today.")
else:
    st.success(f"Showing {len(agenda)} task(s) for {owner.name}, ranked by priority:")
    st.table([
        {
            "Priority":       t.get_priority_label(),
            "Time":           t.due_datetime.strftime("%I:%M %p"),
            "Task":           t.title,
            "Pet":            t.pet.name if t.pet else "—",
            "Duration (min)": t.duration_minutes,
            "Overdue":        "Yes" if t.is_overdue() else "No",
        }
        for t in agenda
    ])

st.divider()

# ── Complete a task ───────────────────────────────────────────────────────────
st.subheader("Complete a Task")

incomplete = [t for t in all_tasks if not t.is_completed]
if not incomplete:
    st.info("No incomplete tasks.")
else:
    task_options = {f"{t.title} ({t.pet.name if t.pet else '?'}, {t.due_datetime.strftime('%I:%M %p')})": t
                   for t in scheduler.sort_by_time(incomplete)}
    selected_label = st.selectbox("Select task to complete", list(task_options.keys()))

    if st.button("Mark as complete"):
        selected_task = task_options[selected_label]
        next_task = scheduler.complete_task(selected_task, next_task_id=st.session_state.task_id_counter)
        st.session_state.task_id_counter += 1
        if next_task:
            st.success(
                f"**{selected_task.title}** marked complete. "
                f"Next {selected_task.recurrence} occurrence scheduled for "
                f"{next_task.due_datetime.strftime('%b %d at %I:%M %p')}."
            )
        else:
            st.success(f"**{selected_task.title}** marked complete.")
        st.rerun()

st.divider()

# ── Filter tasks ──────────────────────────────────────────────────────────────
st.subheader("Filter Tasks")

col_a, col_b = st.columns(2)
with col_a:
    filter_status = st.selectbox("Completion status", ["All", "Incomplete", "Completed"])
with col_b:
    filter_pet = st.selectbox("Pet", ["All pets"] + pet_names)

status_map = {"All": None, "Incomplete": False, "Completed": True}
filtered = scheduler.filter_tasks(
    all_tasks,
    completed=status_map[filter_status],
    pet_name=None if filter_pet == "All pets" else filter_pet,
)

if not filtered:
    st.info("No tasks match the selected filters.")
else:
    st.write(f"**{len(filtered)} task(s)** matching filters:")
    st.table([
        {
            "Time":     t.due_datetime.strftime("%I:%M %p"),
            "Pet":      t.pet.name if t.pet else "—",
            "Task":     t.title,
            "Priority": t.get_priority_label(),
            "Status":   "Done" if t.is_completed else ("OVERDUE" if t.is_overdue() else "Pending"),
        }
        for t in scheduler.sort_by_time(filtered)
    ])
