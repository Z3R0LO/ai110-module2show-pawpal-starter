# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

    My intial UML design will contain a total of 5 class, being the the Pet, Task, Owner, Scheduler, and Report classes.

    Pet -> represents an animal and owns a list of Task objects. It stores profile info (species, breed, age, weight, medical history) and is responsible for managing its own task list 

    Task -> represents a action like feeding, walk, medication, or appointment. Will manage marking itself complete, rescheduling, and reporting whether it's overdue

    Owner -> represents a person and owns a list of Pet objects. It stores contact info and is responsible for managing their pets and surfacing a unified view of upcoming tasks across all their pets

    Schdeule -> holds references to all owners and tasks system wide. It's responsible for the algorithmic work and prioritizies tasks by urgency, assembling a daily agenda for an owner, finding overdue tasks across all pets, and triggering reminders

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

    Yes, I made some changes to the design during implementation.

    A change I made was removing self.all_tasks: list as a stored list and replaced it with a property that derives the list from owners → pets → tasks. This eliminates the dual-list sync problem where Pet tasks and prevents Scheduler all_tasks from drifting out of sync. 

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

    Constraints that are considered are time, priority, and overdue status. Tasks have a due_datetime and duration_minutes. The scheduler uses both to detect overlapping windows in detect_conflicts(). Tasks have a 1–5 priority score prioritize_tasks() sorts by priority descending. Overdue tasks are always surfaced first within the same priority tier.

    Time and priority are the most actionable constraints for a pet owner knowing when something is due and how urgent it is directly determines what to do next. Overdue tasks float to the top because a missed medication or feeding needs immediate attention over a future task, even one with the same priority.


**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

    A tradeoff made is prioritize_tasks() ranks entirely by priority, then overdue status, then time. This means a lower-priority task due in 5 minutes can be ranked below a higher-priority task due in 3 hours.

    This is reasonable for pet care, a critical task generally should preempt a low priority one regardless of timing. As missing a dose is worse than being slightly late for a walk. The tradeoff accepts some time urgency loss in exchange for simpler, more predictable priority first behavior that pet owners can easily reason about.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

    For this project I used AI tools, specifically claude, for brainstorming, debugging, refactoring, implementation, and to generate tests. Claude did upwards of 90% of phase work throughout the project. Most of my prompts where based on the instructions provided in the CODEPATH project assignment. However prompts that I created that focused around asking the AI why it choose to do a certain action was insightful into understanding how the AI works. 


**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

    One moment where I did not accept a a AI suggestion as is, was when making additions to the README.md file. I often wanted to clear and precise with the langauge I was using for the descriptions, and often told the AI to rewrite certain description with modified terminology. I would evaluate what the AI suggested by reading the decriptions it provided, and comparing them to the actual implementation for the functions/code for accuracy and to verify. 

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

    Three core behaviors were tested: chronological sorting , daily recurrence, and conflict detection. Each was covered with multiple cases. For example, conflict detection was tested for overlapping tasks, tasks at an exact boundary, and completed tasks that should be ignored.

    The behaviors are important because they are the backbone of the scheduler. Sorting determines the order every user sees and if it's wrong, the entire display is misleading. Recurrence is the only stateful operation it creates new data so a bug there silently corrupts the task list over time. Conflict detection is a safety feature so that an undetected overlap means a pet owner might be scheduled to be in two places at once.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

    My confidence is about 4 out of 5. The three highest-risk behaviors, sorting, recurrence, and conflict detection, are verified by 9 passing tests, and the logic in pawpal_system.py is straightforward enough to reason about directly. The gap is that prioritize_tasks, get_daily_agenda, send_reminder, and get_upcoming_tasks have no automated tests yet, so bugs there would be seen after manual use.

    Given more time, the next edge cases to test would be create a prioritize_tasks with a mix of overdue and future tasks at the same priority tier. 
---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

    I most satisfied with the added functionality of app. Specifcally the pets list, task sorting by time, and agenda implementation. 

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

    I would want to redesign the add a task section of the app. It is functional and gets the job done, however it can be optimised and have different, and better design. Design of the UI is something I spent less time on. 

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

    I learned that it is sometimes important to ask the AI the question of why for certain actions it takes. This in turn will make the AI and even myself a bit more "kknowledgeable" about the thinking pattern and gauge the understanding of the AI, allowing for redirection or refactoring of the actions it takes.  
