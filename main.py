from datetime import datetime, date
from pawpal_system import Owner, Pet, Task, Scheduler

# --- Setup ---
scheduler = Scheduler()

owner = Owner(id=1, name="Jordan", email="jordan@email.com", phone="555-1234")
scheduler.add_owner(owner)

mochi = Pet(id=1, name="Mochi", species="dog", breed="Shiba Inu", age=3, weight=10.5)
luna  = Pet(id=2, name="Luna",  species="cat", breed="Siamese",   age=5, weight=4.2)

owner.add_pet(mochi)
owner.add_pet(luna)

# --- Tasks ---
today = date.today()

def dt(hour: int, minute: int = 0) -> datetime:
    return datetime(today.year, today.month, today.day, hour, minute)

tasks = [
    Task(id=1, title="Morning walk",      type="walk",        due_datetime=dt(7, 30), priority=3, duration_minutes=30),
    Task(id=2, title="Breakfast feeding", type="feeding",     due_datetime=dt(8, 0),  priority=4, duration_minutes=10),
    Task(id=3, title="Flea medication",   type="medication",  due_datetime=dt(9, 0),  priority=5, duration_minutes=5,  notes="Apply to back of neck"),
    Task(id=4, title="Lunchtime feeding", type="feeding",     due_datetime=dt(12, 0), priority=4, duration_minutes=10),
    Task(id=5, title="Vet appointment",   type="appointment", due_datetime=dt(15, 0), priority=5, duration_minutes=60, notes="Annual checkup"),
    Task(id=6, title="Evening walk",      type="walk",        due_datetime=dt(18, 0), priority=3, duration_minutes=45),
]

scheduler.schedule_task(mochi, tasks[0])  # morning walk   -> Mochi
scheduler.schedule_task(mochi, tasks[1])  # breakfast      -> Mochi
scheduler.schedule_task(luna,  tasks[2])  # flea med       -> Luna
scheduler.schedule_task(mochi, tasks[3])  # lunch          -> Mochi
scheduler.schedule_task(luna,  tasks[4])  # vet appt       -> Luna
scheduler.schedule_task(mochi, tasks[5])  # evening walk   -> Mochi

# --- Print Today's Schedule ---
print("=" * 52)
print(f"  PawPal+ | Today's Schedule for {owner.name}")
print(f"  {today.strftime('%A, %B %d %Y')}")
print("=" * 52)

agenda = scheduler.get_daily_agenda(owner)

if not agenda:
    print("  No tasks scheduled for today.")
else:
    for task in agenda:
        overdue_flag = "  *** OVERDUE ***" if task.is_overdue() else ""
        pet_name     = task.pet.name if task.pet else "?"
        print(
            f"  {task.due_datetime:%I:%M %p}  [{task.get_priority_label():9}]  "
            f"{task.title} ({pet_name}, {task.duration_minutes} min){overdue_flag}"
        )

print("=" * 52)

overdue = scheduler.get_overdue_tasks()
if overdue:
    print(f"\n  !! {len(overdue)} overdue task(s) need attention:")
    for task in overdue:
        print(f"     - {task.title} ({task.pet.name}) was due at {task.due_datetime:%I:%M %p}")
    print()

print("  Reminders:")
for task in agenda[:2]:
    print(f"     {scheduler.send_reminder(task)}")

print("=" * 52)
