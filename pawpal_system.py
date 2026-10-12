
from dataclasses import dataclass, field, replace
from datetime import datetime, timedelta, date


@dataclass
class Owner:
    name: str
    available_minutes: int
    preferences: dict = field(default_factory=dict)
    pets: list = field(default_factory=list)

    def add_pet(self, pet):
        """Register a pet under the owner."""
        self.pets.append(pet)

    def remove_pet(self, pet):
        """Remove an existing pet."""
        if pet in self.pets:
            self.pets.remove(pet)

    def get_all_tasks(self):
        """Collect tasks from every registered pet."""
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
        """Assign a care task to this pet."""
        self.tasks.append(task)

    def remove_task(self, task):
        """Remove a care task from this pet."""
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
    due_date: date = field(default_factory=date.today)

    def mark_complete(self):
        """Mark this task as completed."""
        self.completed = True

    def is_recurring(self):
        """Check whether the task repeats daily or weekly."""
        return self.recurrence.lower() in ("daily", "weekly")

    def next_occurrence(self):
        """Create the next occurrence of a recurring task."""
        if not self.is_recurring():
            return None

        days = 1 if self.recurrence.lower() == "daily" else 7

        return replace(
            self,
            due_date=self.due_date + timedelta(days=days),
            completed=False
        )


class Scheduler:
    def __init__(self, owner, start_time="08:00"):
        """Initialize scheduling for an owner's pets."""
        self.owner = owner
        self.start_time = start_time

    def filter_tasks(self, pet_name=None, completed=None, on_date=None):
        """Filter tasks by pet name, status, or due date."""
        tasks = self.owner.get_all_tasks()

        if pet_name is not None:
            tasks = [
                (pet, task)
                for pet, task in tasks
                if pet.name.lower() == pet_name.lower()
            ]

        if completed is not None:
            tasks = [
                (pet, task)
                for pet, task in tasks
                if task.completed == completed
            ]

        if on_date is not None:
            tasks = [
                (pet, task)
                for pet, task in tasks
                if task.due_date == on_date
            ]

        return tasks

    def sort_by_time(self, on_date=None):
        """Sort incomplete tasks by preferred time."""
        if on_date is None:
            on_date = date.today()

        tasks = self.filter_tasks(
            completed=False,
            on_date=on_date
        )

        return sorted(
            tasks,
            key=lambda item: item[1].due_time or "23:59"
        )

    def sort_tasks(self, on_date=None):
        """Sort incomplete tasks by priority and preferred time."""
        if on_date is None:
            on_date = date.today()

        priority_order = {
            "high": 0,
            "medium": 1,
            "low": 2
        }

        tasks = self.filter_tasks(
            completed=False,
            on_date=on_date
        )

        return sorted(
            tasks,
            key=lambda item: (
                priority_order.get(item[1].priority.lower(), 3),
                item[1].due_time or "23:59"
            )
        )

    def generate_schedule(self, on_date=None):
        """Build a daily plan within available time."""
        if on_date is None:
            on_date = date.today()

        current_time = datetime.strptime(
            self.start_time, "%H:%M"
        )

        remaining_minutes = self.owner.available_minutes
        schedule = []

        for pet, task in self.sort_tasks(on_date):
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

    def mark_task_complete(self, pet, task):
        """Complete a task and schedule its next occurrence."""
        if not any(
            registered_pet is pet
            for registered_pet in self.owner.pets
        ):
            raise ValueError("Pet is not registered to this owner.")

        if not any(existing is task for existing in pet.tasks):
            raise ValueError("Task does not belong to this pet.")

        if task.completed:
            return None

        task.mark_complete()

        next_task = task.next_occurrence()

        if next_task is not None:
            pet.add_task(next_task)

        return next_task

    def get_recurring_tasks(self):
        """Retrieve recurring tasks belonging to all pets."""
        return [
            (pet, task)
            for pet, task in self.owner.get_all_tasks()
            if task.is_recurring()
        ]

    def detect_conflicts(self, on_date=None):
        """Find overlapping preferred-time intervals."""
        if on_date is None:
            on_date = date.today()

        intervals = []

        for pet, task in self.filter_tasks(
            completed=False,
            on_date=on_date
        ):
            if not task.due_time or task.duration_minutes <= 0:
                continue

            start = datetime.strptime(
                task.due_time, "%H:%M"
            )
            end = start + timedelta(
                minutes=task.duration_minutes
            )

            intervals.append((start, end, pet, task))

        intervals.sort(key=lambda item: item[0])
        conflicts = []

        for i, (start1, end1, pet1, task1) in enumerate(intervals):
            for start2, end2, pet2, task2 in intervals[i + 1:]:
                if start2 >= end1:
                    break

                if start1 < end2 and start2 < end1:
                    conflicts.append({
                        "time": start2.strftime("%H:%M"),
                        "tasks": [
                            (pet1.name, task1.title),
                            (pet2.name, task2.title)
                        ]
                    })

        return conflicts
