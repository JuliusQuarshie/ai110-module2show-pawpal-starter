
# PawPal+ (Module 2 Project)

PawPal+ is a smart pet care management application built with Python and Streamlit. It helps pet owners organize daily care activities, manage tasks, and generate schedules based on priorities and available time.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, medication, enrichment, grooming, etc.).
- Consider constraints such as available time, task priority, and preferred scheduling times.
- Produce a daily plan and explain how tasks were prioritized.

The system uses object-oriented programming (OOP) and scheduling algorithms to manage these responsibilities.

## What You Will Build

PawPal+ allows users to:

- Register and manage multiple pets.
- Create care tasks with duration, priority, preferred time, and recurrence.
- Mark tasks as completed.
- Generate daily schedules based on available time and priority.
- Filter tasks by pet, completion status, or date.
- Automatically generate the next occurrence of recurring tasks.
- Detect overlapping preferred task times.

## Getting Started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Run the CLI Demo

```bash
python3 main.py
```

### Run the Streamlit Application

```bash
python3 -m streamlit run app.py
```

## 🖥️ Sample Output

Example output from running `python3 main.py`:

```text
=== 1. Tasks Sorted by Time ===
08:00 | Bro: Morning Walk
08:15 | Luna: Breakfast
09:00 | Luna: Medication
11:00 | Bro: Grooming

=== 2. Filter Tasks for Bro ===
Bro: Grooming
Bro: Morning Walk

=== 3. Today's Schedule ===
08:00 - 08:30 | Bro: Morning Walk
08:30 - 08:45 | Luna: Breakfast
08:45 - 08:55 | Luna: Medication
08:55 - 09:15 | Bro: Grooming

=== 4. Conflict Detection ===
WARNING: Overlapping tasks at 08:15
  - Bro: Morning Walk
  - Luna: Breakfast

=== 5. Recurring Task Test ===
Before completion: False
After completion: True
Next occurrence: Morning Walk on 2026-10-12
Expected date: 2026-10-11 + 1 day

=== 6. Completed Task Filtering ===
Bro: Morning Walk [Completed]
```

*Note: Recurring task dates depend on the day the demo is executed.*

## 🧪 Testing PawPal+

PawPal+ uses pytest to verify that its core features and scheduling algorithms work correctly. The test suite includes both normal scenarios and edge cases.

### Run Tests

```bash
python3 -m pytest
```

### Run Tests with Coverage

```bash
python3 -m pytest --cov=pawpal_system
```

Coverage reporting requires `pytest-cov`.

### Sample Test Output

```text
collected 10 items

tests/test_pawpal.py ..........              [100%]

10 passed
```

### Tested Features

1. **Task Completion:** Verifies that completing a task updates its status.
2. **Task Addition:** Confirms that adding a task increases a pet's task count.
3. **Sorting Correctness:** Ensures tasks are arranged chronologically by preferred time.
4. **Filtering:** Confirms that tasks can be retrieved for a specific pet.
5. **Daily Recurrence:** Verifies that completing a daily task generates another task for the following day without duplication.
6. **Overlapping Task Detection:** Checks whether tasks with overlapping preferred times are flagged.
7. **Empty Task Lists:** Ensures the scheduler handles pets without tasks without crashing.
8. **Identical Task Times:** Verifies that tasks scheduled for exactly the same time produce a conflict warning.
9. **Insufficient Available Time:** Confirms that tasks exceeding the owner's time budget are excluded from the schedule.
10. **Weekly Recurrence:** Verifies that completing a weekly task schedules its next occurrence seven days later.

### Confidence Level: ⭐⭐⭐⭐☆ (4/5)

I am confident in PawPal+'s core functionality because all 10 automated tests passed. The tests cover normal operations and important edge cases involving sorting, recurrence, scheduling constraints, and conflict detection.

However, the system still has limitations. User data is stored temporarily in Streamlit session state, and preferred task times are not enforced as fixed appointments. Additional testing and improvements would be necessary before using the application as a fully reliable pet care management system.

## 📐 Smarter Scheduling

PawPal+ uses several algorithms to organize pet care tasks efficiently.

| Feature | Method(s) | Description |
|---------|-----------|-------------|
| Task Sorting | `sort_by_time()`, `sort_tasks()` | Orders tasks chronologically or by priority and preferred time. |
| Filtering | `filter_tasks()` | Filters tasks by pet name, completion status, or date. |
| Conflict Detection | `detect_conflicts()` | Identifies tasks with overlapping preferred-time intervals. |
| Recurring Tasks | `next_occurrence()`, `mark_task_complete()` | Automatically generates the next daily or weekly task after completion. |
| Daily Scheduling | `generate_schedule()` | Creates a daily plan and skips tasks that exceed the owner's available time. |

### Scheduling Logic

The Scheduler class retrieves tasks from all pets registered under an Owner.

It prioritizes high-priority tasks, followed by medium- and low-priority tasks. Within the same priority level, preferred times determine the order.

Tasks that exceed the owner's remaining available time are skipped.

Completed tasks and tasks scheduled for another date are excluded from today's generated schedule.

### Conflict Detection

The scheduler compares preferred start times and task durations to identify overlapping intervals.

For example, if a dog has a 30-minute walk beginning at 08:00 and a cat has a 15-minute feeding beginning at 08:15, the system reports a conflict.

These conflicts produce warnings rather than stopping the application.

### Recurring Tasks

Tasks can be configured to repeat daily or weekly.

When a recurring task is completed through the Scheduler, the system:

1. Marks the current task as completed.
2. Calculates the next due date using `timedelta`.
3. Creates a new task for the next occurrence.
4. Prevents duplicate occurrences from repeated completion of the same task.

### Scheduling Tradeoffs

PawPal+ prioritizes important tasks over strictly enforcing their preferred times.

For example, a high-priority medication task may be scheduled before a lower-priority grooming task, even if grooming has an earlier preferred time.

The scheduler currently uses preferred times for ordering rather than reserving fixed appointment slots. Conflict warnings are calculated separately.

## 🏗️ System Architecture

The application follows an object-oriented design using four main classes:

- **Owner:** Stores owner information, preferences, available time, and registered pets.
- **Pet:** Stores pet details and manages care tasks.
- **Task:** Represents a care activity, including duration, priority, preferred time, due date, recurrence, and completion status.
- **Scheduler:** Handles sorting, filtering, daily scheduling, recurring tasks, and conflict detection.

The backend implementation is located in `pawpal_system.py`.

The Streamlit interface in `app.py` uses these classes to provide an interactive experience.

The initial UML diagram is saved in `diagrams/uml_draft.mmd`.

## 📸 Demo Walkthrough

1. Launch the Streamlit application using `python3 -m streamlit run app.py`.
2. Enter the owner's name and daily available time.
3. Register pets by entering their names, species, and ages.
4. Add care tasks with duration, priority, preferred time, and recurrence settings.
5. Generate a daily schedule and review the planned activities, available time, and conflict warnings.
6. Mark a task as completed and generate the schedule again to see the updated plan.

## Current Limitations

- Data is stored in Streamlit session state and is not permanently saved.
- Preferred task times are not enforced as fixed appointments.
- Weekly recurring tasks repeat every seven days after their stored due date.
- Owner preferences are stored but not yet fully incorporated into scheduling decisions.

## Technologies Used

- Python
- Object-Oriented Programming (OOP)
- Python Dataclasses
- Streamlit
- pytest
- Mermaid.js
- Git and GitHub
