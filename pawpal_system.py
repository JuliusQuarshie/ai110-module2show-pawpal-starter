
from dataclasses import dataclass, field
from datetime import datetime, timedelta


@dataclass
class Owner:
    name: str
    available_minutes: int
    preferences: dict = field(default_factory=dict)
    pets: list = field(default_factory=list)

    def add_pet(self, pet):
        """Add a pet to the owner."""
        self.pets.append(pet)

    def remove_pet(self, pet):
        """Remove a pet from the owner."""
        if pet in self.pets:
            self.pets.remove(pet)

    def get_all_tasks(self):
        """Retrieve tasks from all owned pets."""
        return [
            (pet, task)
            for pet in self.pets
            for task in pet.tasks
        ]


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: list = field(default_factory=list)

    def add_task(self, task):
        """Add a care task to the pet."""
        self.tasks.append(task)

    def remove_task(self, task):
        """Remove a care task from the pet."""
        if task in self.tasks:
            self.tasks.remove(task)


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str
    due_time: str = ""
    recurrence: str = "none"
    completed: bool = False

    def mark_complete(self):
        """Mark the task as completed."""
        self.completed = True

    def is_recurring(self):
        """Check whether the task repeats."""
        return self.recurrence.lower() in ["daily", "weekly"]


class Scheduler:
    def __init__(self, owner, start_time="08:00"):
        """Initialize scheduler using an owner's pets and available time."""
        self.owner = owner
        self.start_time = start_time

    def sort_tasks(self):
        """Sort incomplete tasks by priority, then preferred time."""
        priority_order = {"high": 0, "medium": 1, "low": 2}

        tasks = [
            (pet, task)
            for pet, task in self.owner.get_all_tasks()
            if not task.completed
        ]

        return sorted(
            tasks,
            key=lambda item: (
                priority_order.get(item[1].priority.lower(), 3),
                item[1].due_time or "23:59"
            )
        )

    def generate_schedule(self):
        """Generate a daily schedule within the owner's available time."""
        current_time = datetime.strptime(self.start_time, "%H:%M")
        remaining_minutes = self.owner.available_minutes
        schedule = []

        for pet, task in self.sort_tasks():
            if task.duration_minutes <= 0:
                continue

            if task.duration_minutes > remaining_minutes:
                continue

            end_time = current_time + timedelta(
                minutes=task.duration_minutes
            )

            schedule.append({
                "pet": pet.name,
                "task": task.title,
                "start": current_time.strftime("%H:%M"),
                "end": end_time.strftime("%H:%M"),
                "duration": task.duration_minutes,
                "priority": task.priority
            })

            current_time = end_time
            remaining_minutes -= task.duration_minutes

        return schedule

    def detect_conflicts(self):
        """Find tasks assigned the same preferred due time."""
        tasks_by_time = {}
        conflicts = []

        for pet, task in self.owner.get_all_tasks():
            if task.completed or not task.due_time:
                continue

            tasks_by_time.setdefault(task.due_time, []).append(
                (pet.name, task.title)
            )

        for due_time, tasks in tasks_by_time.items():
            if len(tasks) > 1:
                conflicts.append({
                    "time": due_time,
                    "tasks": tasks
                })

        return conflicts

    def get_recurring_tasks(self):
        """Retrieve recurring tasks from all pets."""
        return [
            (pet, task)
            for pet, task in self.owner.get_all_tasks()
            if task.is_recurring()
        ]

