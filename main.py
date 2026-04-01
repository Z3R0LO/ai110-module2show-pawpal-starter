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

# --- Tasks added OUT OF ORDER intentionally ---
today = date.today()

def dt(hour: int, minute: int = 0) -> datetime:
    return datetime(today.year, today.month, today.day, hour, minute)

tasks = [
    Task(id=1, title="Evening walk",      type="walk",        due_datetime=dt(18, 0),  priority=3, duration_minutes=45),
    Task(id=2, title="Vet appointment",   type="appointment", due_datetime=dt(15, 0),  priority=5, duration_minutes=60, notes="Annual checkup"),
    Task(id=3, title="Flea medication",   type="medication",  due_datetime=dt(9, 0),   priority=5, duration_minutes=5,  notes="Apply to back of neck"),
    Task(id=4, title="Lunchtime feeding", type="feeding",     due_datetime=dt(12, 0),  priority=4, duration_minutes=10),
    Task(id=5, title="Morning walk",      type="walk",        due_datetime=dt(7, 30),  priority=3, duration_minutes=30),
    Task(id=6, title="Breakfast feeding", type="feeding",     due_datetime=dt(8, 0),   priority=4, duration_minutes=10),
    # Intentional conflicts:
    Task(id=7, title="Bath time",         type="walk",        due_datetime=dt(7, 45),  priority=2, duration_minutes=20),  # same-pet: overlaps Morning walk (7:30–8:00)
    Task(id=8, title="Luna feeding",      type="feeding",     due_datetime=dt(15, 30), priority=4, duration_minutes=15),  # cross-pet: overlaps Vet appointment (15:00–16:00)
]

scheduler.schedule_task(mochi, tasks[0])  # evening walk    -> Mochi
scheduler.schedule_task(luna,  tasks[1])  # vet appt        -> Luna
scheduler.schedule_task(luna,  tasks[2])  # flea med        -> Luna
scheduler.schedule_task(mochi, tasks[3])  # lunch           -> Mochi
scheduler.schedule_task(mochi, tasks[4])  # morning walk    -> Mochi
scheduler.schedule_task(mochi, tasks[5])  # breakfast       -> Mochi
scheduler.schedule_task(mochi, tasks[6])  # bath time       -> Mochi (conflicts with morning walk)
scheduler.schedule_task(luna,  tasks[7])  # luna feeding    -> Luna  (conflicts with vet appointment)

all_tasks = scheduler.all_tasks

# --- sort_by_time ---
print("=" * 56)
print("  sort_by_time() — all tasks sorted earliest to latest")
print("=" * 56)
for t in scheduler.sort_by_time(all_tasks):
    print(f"  {t.due_datetime:%I:%M %p}  {t.title:22}  ({t.pet.name})")

# --- filter_tasks: incomplete only ---
print()
print("=" * 56)
print("  filter_tasks(completed=False) — incomplete tasks only")
print("=" * 56)
incomplete = scheduler.filter_tasks(all_tasks, completed=False)
for t in scheduler.sort_by_time(incomplete):
    print(f"  {t.due_datetime:%I:%M %p}  {t.title:22}  ({t.pet.name})")

# --- filter_tasks: by pet name ---
print()
print("=" * 56)
print("  filter_tasks(pet_name='Mochi') — Mochi's tasks only")
print("=" * 56)
mochi_tasks = scheduler.filter_tasks(all_tasks, pet_name="Mochi")
for t in scheduler.sort_by_time(mochi_tasks):
    print(f"  {t.due_datetime:%I:%M %p}  {t.title:22}  ({t.pet.name})")

# --- filter_tasks: completed tasks for Luna ---
print()
print("=" * 56)
print("  filter_tasks(completed=True, pet_name='Luna') — Luna's completed tasks")
print("=" * 56)
tasks[2].complete()  # mark flea medication as done
luna_done = scheduler.filter_tasks(all_tasks, completed=True, pet_name="Luna")
if luna_done:
    for t in scheduler.sort_by_time(luna_done):
        print(f"  {t.due_datetime:%I:%M %p}  {t.title:22}  ({t.pet.name})  [completed]")
else:
    print("  No completed tasks for Luna.")

# --- detect_conflicts ---
print()
print("=" * 56)
print("  detect_conflicts() — all tasks")
print("=" * 56)
conflicts = scheduler.detect_conflicts(scheduler.all_tasks)
if conflicts:
    for w in conflicts:
        print(f"  {w}")
else:
    print("  No conflicts found.")

print("=" * 56)
