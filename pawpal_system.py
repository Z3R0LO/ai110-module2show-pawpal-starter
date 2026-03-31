from datetime import datetime


class Task:
    def __init__(self, id: int, title: str, type: str, due_datetime: datetime, priority: int, notes: str = ""):
        self.id = id
        self.title = title
        self.type = type          # "feeding", "walk", "medication", "appointment"
        self.due_datetime = due_datetime
        self.priority = priority  # 1 (lowest) to 5 (highest)
        self.is_completed = False
        self.notes = notes

    def complete(self):
        pass

    def reschedule(self, new_datetime: datetime):
        pass

    def is_overdue(self) -> bool:
        pass

    def get_priority_label(self) -> str:
        pass


class Pet:
    def __init__(self, id: int, name: str, species: str, breed: str, age: int, weight: float):
        self.id = id
        self.name = name
        self.species = species
        self.breed = breed
        self.age = age
        self.weight = weight
        self.medical_history: list[str] = []
        self.tasks: list[Task] = []

    def add_task(self, task: Task):
        pass

    def remove_task(self, task_id: int):
        pass

    def get_tasks(self) -> list[Task]:
        pass

    def get_overdue_tasks(self) -> list[Task]:
        pass

    def update_info(self, field: str, value):
        pass


class Owner:
    def __init__(self, id: int, name: str, email: str, phone: str):
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet):
        pass

    def remove_pet(self, pet_id: int):
        pass

    def get_pets(self) -> list[Pet]:
        pass

    def get_upcoming_tasks(self) -> list[Task]:
        pass


class Scheduler:
    def __init__(self):
        self.all_tasks: list[Task] = []
        self.owners: list[Owner] = []

    def add_owner(self, owner: Owner):
        pass

    def schedule_task(self, pet: Pet, task: Task):
        pass

    def prioritize_tasks(self, tasks: list[Task]) -> list[Task]:
        pass

    def get_daily_agenda(self, owner: Owner) -> list[Task]:
        pass

    def get_overdue_tasks(self) -> list[Task]:
        pass

    def send_reminder(self, task: Task):
        pass
