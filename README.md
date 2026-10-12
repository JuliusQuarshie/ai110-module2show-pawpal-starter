# 🐾 PawPal+ | Smart Pet Care Management

PawPal+ is a smart pet care management application built with Python and Streamlit. It helps pet owners organize daily care activities, manage responsibilities, and generate schedules based on task priorities and available time.

This project was developed as part of CodePath's AI110 Module 2, focusing on object-oriented programming (OOP), algorithmic thinking, system design, testing, and AI-assisted software development.

## 📖 Project Overview

Managing pet care can be challenging, especially for owners with busy schedules or multiple pets. Activities such as feeding, walking, medication, and grooming need to be organized consistently.

PawPal+ provides an interactive application where pet owners can register pets, create care tasks, track their completion, detect scheduling conflicts, and generate personalized daily care plans.

The application follows a CLI-first development approach, where backend functionality is implemented and tested before connecting it to the Streamlit user interface.

## ✨ Features

### Pet Management
- Register multiple pets with their names, species, and ages.
- View registered pets and their assigned tasks.
- Manage care activities for different pets.

### Task Management
- Create tasks with duration, priority, preferred time, and due date.
- Assign tasks to specific pets.
- Configure daily or weekly recurrence.
- Mark tasks as completed.
- Filter tasks by pet name or completion status.

### Smart Scheduling
- Sort tasks chronologically or by priority.
- Generate schedules based on daily available time.
- Prioritize high-priority activities.
- Skip tasks exceeding the available time budget.
- Automatically create future occurrences of completed recurring tasks.
- Detect overlapping preferred-time intervals.
- Display warnings for scheduling conflicts.

### Streamlit Interface
- Manage owner information and daily availability.
- Register and view multiple pets.
- Add and complete care tasks.
- Sort and filter tasks.
- Check conflicts for selected dates.
- Generate daily schedules.
- View scheduling explanations and available-time summaries.

### 🎨 Professional UI Enhancements (Optional Challenge 4)

I improved the Streamlit interface to make PawPal+ more visually appealing and easier to use.

The enhancements include:

- **Dashboard Metrics:** Displays the number of registered pets, total tasks, completed tasks, and pending tasks using `st.metric()`.
- **Progress Tracking:** Uses `st.progress()` to show overall task completion and individual pet progress.
- **Color-Coded Priorities:** Uses 🔴 High, 🟡 Medium, and 🟢 Low indicators to make task urgency easier to recognize.
- **Pet Cards:** Uses `st.container(border=True)` and `st.columns()` to organize pet information.
- **Improved Task Display:** Shows tasks in structured panels with completion status, due dates, duration, and recurrence.
- **Professional Schedule Tables:** Uses `st.dataframe()` to display schedules clearly.
- **Conflict Alerts:** Uses `st.warning()`, `st.error()`, and `st.success()` to communicate scheduling issues and results.

These improvements make the application's existing scheduling features easier to understand without modifying the backend algorithms.

## 🚀 Getting Started

### Requirements

- Python 3.10 or later
- pip
- Git

### Installation

Clone the repository:

```bash
git clone https://github.com/JuliusQuarshie/ai110-module2show-pawpal-starter.git
cd ai110-module2show-pawpal-starter
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

For Windows:

```powershell
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### Run the Streamlit App

```bash
python3 -m streamlit run app.py
```

Open the local URL displayed in your terminal.

### Run the CLI Demo

```bash
python3 main.py
```

This runs the backend demonstration without requiring the Streamlit interface.

## 🏗️ System Architecture

PawPal+ uses four main Python classes.

| Class | Responsibility |
|---|---|
| `Owner` | Stores owner information, available time, preferences, and registered pets. |
| `Pet` | Represents individual pets and manages their care tasks. |
| `Task` | Represents activities with duration, priority, preferred time, recurrence, due date, and completion status. |
| `Scheduler` | Organizes tasks, generates daily schedules, manages recurrence, filters activities, and detects conflicts. |

### Class Relationships

An Owner can register multiple Pets. Each Pet maintains its own collection of Tasks.

The Scheduler receives an Owner object and retrieves tasks from all registered pets.

Separating these responsibilities helps keep the application modular and makes the scheduling algorithms easier to test independently.

### UML Diagrams

The system architecture was designed using Mermaid.js UML class diagrams.

**Initial UML Design:** [View uml_draft.mmd](diagrams/uml_draft.mmd)

**Final UML Design:** [View uml_final.mmd](diagrams/uml_final.mmd)

The initial UML represents the original architecture before implementation. The final UML includes the additional methods and relationships introduced during development, including filtering, recurring task management, and conflict detection.

Both files can be visualized using the [Mermaid Live Editor](https://mermaid.live/).

## 🧠 Smarter Scheduling Algorithms

| Feature | Methods | Description |
|---|---|---|
| Chronological Sorting | `sort_by_time()` | Sorts incomplete tasks by preferred time. |
| Priority Sorting | `sort_tasks()` | Sorts tasks by priority and then preferred time. |
| Task Filtering | `filter_tasks()` | Filters tasks by pet, completion status, or date. |
| Daily Scheduling | `generate_schedule()` | Creates schedules within the owner's available time budget. |
| Conflict Detection | `detect_conflicts()` | Identifies overlapping preferred-time intervals. |
| Recurring Tasks | `next_occurrence()`, `mark_task_complete()` | Creates future occurrences of completed daily or weekly tasks. |

### Scheduling Logic

The Scheduler retrieves tasks from every pet registered under an Owner.

Tasks are prioritized in the following order:

1. High priority
2. Medium priority
3. Low priority

Tasks with identical priorities are ordered by their preferred times.

The scheduler skips activities that exceed the owner's remaining available time. Completed tasks and tasks belonging to other dates are excluded from the selected day's schedule.

### Conflict Detection

The scheduler compares the preferred start times and durations of care tasks.

For example, if Bro has a 30-minute walk scheduled for 08:00 and Luna has a 15-minute feeding scheduled for 08:15, their preferred-time intervals overlap.

PawPal+ displays a warning identifying both tasks rather than crashing or automatically changing their times.

### Recurring Task Management

PawPal+ supports daily and weekly recurring activities.

When a recurring task is completed through the Scheduler:

1. The original task is marked completed.
2. The next due date is calculated using Python's `timedelta`.
3. A new task instance is created for the next occurrence.
4. The system prevents duplicate future tasks if the original completion action is repeated.

Daily tasks recur after one day, while weekly tasks recur after seven days.

## 🖥️ CLI Demo Output

The `main.py` script demonstrates the backend algorithms without Streamlit.

Example output:

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

*Note: Recurring task dates change depending on when the script is executed.*

## 📸 Demo Walkthrough

This walkthrough demonstrates the main features of the PawPal+ Streamlit application.

### Step 1: Launch PawPal+

Run:

```bash
python3 -m streamlit run app.py
```

The application opens in a browser and displays the PawPal+ dashboard.

### Step 2: Configure Owner Information

Enter the owner's name and specify how much time is available for pet care each day.

For example, Jordan has 120 minutes available daily.

This information is used by the scheduling algorithm when generating plans.

### Step 3: Register Pets

Navigate to the Manage Your Pets section.

Enter a pet's name, species, and age, then click **Add Pet**.

For example, register:

- Bro — Dog, 3 years old
- Luna — Cat, 2 years old

Both pets appear under Registered Pets.

### Step 4: Create Care Tasks

Navigate to Manage Care Tasks.

Select a registered pet and create a task by specifying its name, duration, priority, preferred time, due date, and recurrence frequency.

Example tasks:

| Pet | Task | Preferred Time | Duration | Priority |
|---|---|---|---|---|
| Bro | Morning Walk | 08:00 | 30 min | High |
| Luna | Breakfast | 08:15 | 15 min | High |
| Luna | Medication | 09:00 | 10 min | High |
| Bro | Grooming | 11:00 | 20 min | Low |

### Step 5: Sort and Filter Tasks

Use the task browser to filter activities by pet or completion status.

For example, selecting Bro displays only Bro's care tasks.

Users can also sort tasks by preferred time or priority.

### Step 6: Review Scheduling Conflicts

Select a date in the Scheduling Conflict Check section.

If two tasks have overlapping preferred-time intervals, PawPal+ displays a warning identifying the affected activities.

For example, Bro's morning walk and Luna's breakfast overlap between 08:15 and 08:30.

The application recommends reviewing the preferred times.

### Step 7: Generate a Daily Schedule

Select the desired schedule date and starting time.

Click **Generate Schedule**.

PawPal+ displays a table containing the scheduled activities, start times, end times, durations, and priorities.

It also displays:

- Number of scheduled tasks
- Total minutes used
- Remaining available minutes

The application explains how task priorities and available time influenced the plan.

### Step 8: Complete a Task

Click **Complete** beside an unfinished task.

PawPal+ updates the task's completion status.

Completed tasks are excluded from future generated schedules.

If the activity repeats daily or weekly, the next occurrence is automatically created.

## 🧪 Testing PawPal+

PawPal+ uses pytest to verify the correctness of its classes and scheduling algorithms.

### Run Tests

```bash
python3 -m pytest
```

### Run Tests with Coverage

Install the coverage extension:

```bash
pip install pytest-cov
```

Then run:

```bash
python3 -m pytest --cov=pawpal_system
```

### Sample Test Results

```text
collected 10 items

tests/test_pawpal.py ..........              [100%]

10 passed
```

### Tested Behaviors

1. Task completion updates the completion status.
2. Adding a task increases a pet's task count.
3. Sorting returns tasks in chronological order.
4. Filtering retrieves tasks belonging to a specific pet.
5. Daily recurrence creates the next task without duplication.
6. Overlapping preferred times trigger conflict detection.
7. Pets without tasks are handled correctly.
8. Identical task times generate conflict warnings.
9. Tasks exceeding available time are skipped.
10. Weekly recurrence creates a task seven days later.

### Confidence Level: ⭐⭐⭐⭐☆ (4/5)

I am confident in PawPal+'s core functionality because all 10 automated tests passed. The tests verify both regular functionality and edge cases involving sorting, filtering, recurrence, scheduling constraints, and conflicts.

However, the system requires additional improvements before being considered production-ready, particularly permanent data storage and more advanced appointment scheduling.

## ⚖️ Scheduling Tradeoffs

PawPal+ prioritizes important tasks rather than strictly enforcing preferred times.

For example, medication may be placed before grooming even if grooming has an earlier preferred time.

This approach helps owners focus on important care activities when they have limited time.

However, it can generate schedules that differ from the preferred task times.

The system favors straightforward, predictable scheduling behavior over more complex optimization algorithms.

## ⚠️ Current Limitations

- Application data is stored temporarily in Streamlit session state instead of a database.
- Preferred times guide task ordering but are not enforced as fixed appointments.
- Conflicts are detected but not automatically resolved.
- Recurring tasks are generated when completed, rather than by a background scheduling service.
- Owner preferences are stored but not fully incorporated into the scheduler.
- Existing tasks cannot currently be edited directly through the UI.

## 🔮 Future Improvements

Future iterations could include:

- Permanent database storage.
- User authentication and individual accounts.
- Fixed appointment scheduling.
- Automatic conflict resolution.
- Notifications for feeding and medications.
- Calendar integration.
- Task editing functionality.
- Mobile-friendly improvements.

## 🛠️ Technologies Used

- Python
- Object-Oriented Programming (OOP)
- Python Dataclasses
- Streamlit
- pytest
- Mermaid.js
- Git and GitHub

## 🤖 AI-Assisted Development

AI assistance was used during system design, UML diagram development, Python class implementation, scheduling algorithm development, debugging, automated test creation, and documentation.

Each major component was reviewed and verified through CLI execution, pytest tests, or Streamlit interactions.

Working with AI helped accelerate development while allowing me to remain responsible for architecture decisions, algorithmic tradeoffs, testing, and the final implementation.

## 🔗 Repository

**GitHub:** https://github.com/JuliusQuarshie/ai110-module2show-pawpal-starter

The repository contains the Python backend, Streamlit interface, CLI demo, pytest test suite, UML diagrams, and project reflection.