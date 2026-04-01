import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

# Check the session_state "vault" before creating new objects.
# Streamlit reruns the entire script on every interaction, so without
# this guard a fresh Owner/Scheduler would be created on every click.
if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler()

if "owner" not in st.session_state:
    st.session_state.owner = Owner(id=1, name=owner_name, email="", phone="")
    st.session_state.scheduler.add_owner(st.session_state.owner)

if "pet" not in st.session_state:
    st.session_state.pet = Pet(id=1, name=pet_name, species=species, breed="", age=0, weight=0.0)
    st.session_state.owner.add_pet(st.session_state.pet)

st.markdown("### Tasks")

if "task_id_counter" not in st.session_state:
    st.session_state.task_id_counter = 1

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority_label = st.selectbox("Priority", ["Very Low", "Low", "Medium", "High", "Critical"], index=3)

priority_map = {"Very Low": 1, "Low": 2, "Medium": 3, "High": 4, "Critical": 5}

if st.button("Add task"):
    from datetime import datetime, date
    # Schedule the task for today at the current time
    due = datetime.combine(date.today(), datetime.now().time())
    task = Task(
        id=st.session_state.task_id_counter,
        title=task_title,
        type="general",
        due_datetime=due,
        priority=priority_map[priority_label],
        duration_minutes=int(duration),
    )
    # Call scheduler.schedule_task() to attach the task to the pet
    st.session_state.scheduler.schedule_task(st.session_state.pet, task)
    st.session_state.task_id_counter += 1
    st.success(f"Added '{task_title}' to {st.session_state.pet.name}'s tasks.")

# Display tasks currently on the pet using pet.get_tasks()
current_tasks = st.session_state.pet.get_tasks()
if current_tasks:
    st.write("Current tasks:")
    st.table([
        {
            "Title": t.title,
            "Priority": t.get_priority_label(),
            "Duration (min)": t.duration_minutes,
            "Completed": t.is_completed,
        }
        for t in current_tasks
    ])
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")

if st.button("Generate schedule"):
    from datetime import date
    agenda = st.session_state.scheduler.get_daily_agenda(st.session_state.owner, date.today())
    if not agenda:
        st.info("No tasks scheduled for today.")
    else:
        st.success(f"Today's schedule for {st.session_state.owner.name}:")
        st.table([
            {
                "Time": t.due_datetime.strftime("%I:%M %p"),
                "Task": t.title,
                "Pet": t.pet.name if t.pet else "?",
                "Priority": t.get_priority_label(),
                "Duration (min)": t.duration_minutes,
                "Overdue": t.is_overdue(),
            }
            for t in agenda
        ])

    overdue = st.session_state.scheduler.get_overdue_tasks()
    if overdue:
        st.warning(f"{len(overdue)} overdue task(s):")
        for t in overdue:
            st.write(f"- {t.title} ({t.pet.name}) — due {t.due_datetime.strftime('%I:%M %p')}")
