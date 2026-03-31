```mermaid


classDiagram
    class Owner {
        +int id
        +String name
        +String email
        +String phone
        +List~Pet~ pets
        +addPet(pet: Pet) void
        +removePet(petId: int) void
        +getPets() List~Pet~
        +getUpcomingTasks() List~Task~
    }

    class Pet {
        +int id
        +String name
        +String species
        +String breed
        +int age
        +float weight
        +List~String~ medicalHistory
        +List~Task~ tasks
        +addTask(task: Task) void
        +removeTask(taskId: int) void
        +getTasks() List~Task~
        +getOverdueTasks() List~Task~
        +updateInfo(field: String, value: String) void
    }

    class Task {
        +int id
        +String title
        +String type
        +DateTime dueDateTime
        +int priority
        +boolean isCompleted
        +String notes
        +complete() void
        +reschedule(newDateTime: DateTime) void
        +isOverdue() boolean
        +getPriorityLabel() String
    }

    class Scheduler {
        +List~Task~ allTasks
        +List~Owner~ owners
        +addOwner(owner: Owner) void
        +scheduleTask(pet: Pet, task: Task) void
        +prioritizeTasks(tasks: List~Task~) List~Task~
        +getDailyAgenda(owner: Owner) List~Task~
        +getOverdueTasks() List~Task~
        +sendReminder(task: Task) void
    }

    Owner "1" --> "0..*" Pet : owns
    Pet "1" --> "0..*" Task : has
    Scheduler "1" --> "0..*" Task : manages
    Scheduler "1" --> "0..*" Owner : tracks