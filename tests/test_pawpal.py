from pawpal_system import Pet, Task


def test_task_completion():
    task = Task("Morning Walk", 30, "high")

    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_task_addition():
    pet = Pet("Max", "Dog", 3)
    task = Task("Morning Walk", 30, "high")

    assert len(pet.tasks) == 0

    pet.add_task(task)

    assert len(pet.tasks) == 1
    assert pet.tasks[0] == task

from datetime import date, timedelta
from pawpal_system import Owner, Scheduler


def test_sort_by_time():
    owner = Owner("Jordan", 120)
    pet = Pet("Bro", "Dog", 3)
    owner.add_pet(pet)

    pet.add_task(Task("Grooming", 20, "low", "11:00"))
    pet.add_task(Task("Walk", 30, "high", "08:00"))

    scheduler = Scheduler(owner)

    sorted_tasks = scheduler.sort_by_time()

    assert sorted_tasks[0][1].title == "Walk"
    assert sorted_tasks[1][1].title == "Grooming"


def test_filter_by_pet():
    owner = Owner("Jordan", 120)
    dog = Pet("Bro", "Dog", 3)
    cat = Pet("Luna", "Cat", 2)

    owner.add_pet(dog)
    owner.add_pet(cat)

    dog.add_task(Task("Walk", 30, "high"))
    cat.add_task(Task("Feeding", 15, "medium"))

    results = Scheduler(owner).filter_tasks(pet_name="Bro")

    assert len(results) == 1
    assert results[0][1].title == "Walk"


def test_daily_recurrence():
    owner = Owner("Jordan", 120)
    pet = Pet("Bro", "Dog", 3)
    owner.add_pet(pet)

    task = Task("Walk", 30, "high", recurrence="daily")
    pet.add_task(task)

    next_task = Scheduler(owner).mark_task_complete(pet, task)

    assert task.completed is True
    assert next_task.due_date == date.today() + timedelta(days=1)
    assert next_task.completed is False
    assert len(pet.tasks) == 2

    # Completing the same task again must not duplicate it.
    Scheduler(owner).mark_task_complete(pet, task)
    assert len(pet.tasks) == 2


def test_overlapping_tasks():
    owner = Owner("Jordan", 120)
    pet = Pet("Bro", "Dog", 3)
    owner.add_pet(pet)

    pet.add_task(Task("Walk", 30, "high", "08:00"))
    pet.add_task(Task("Feeding", 15, "high", "08:15"))

    conflicts = Scheduler(owner).detect_conflicts()

    assert len(conflicts) == 1
    assert conflicts[0]["time"] == "08:15"


def test_pet_with_no_tasks():
    owner = Owner("Jordan", 120)
    owner.add_pet(Pet("Bro", "Dog", 3))

    scheduler = Scheduler(owner)

    assert scheduler.generate_schedule() == []
    assert scheduler.detect_conflicts() == []


def test_same_time_conflict():
    owner = Owner("Jordan", 120)
    pet = Pet("Bro", "Dog", 3)
    owner.add_pet(pet)

    pet.add_task(Task("Walk", 30, "high", "08:00"))
    pet.add_task(Task("Feeding", 15, "high", "08:00"))

    conflicts = Scheduler(owner).detect_conflicts()

    assert len(conflicts) == 1
    assert conflicts[0]["time"] == "08:00"


def test_insufficient_available_time():
    owner = Owner("Jordan", 20)
    pet = Pet("Bro", "Dog", 3)
    owner.add_pet(pet)

    pet.add_task(Task("Morning Walk", 30, "high", "08:00"))

    schedule = Scheduler(owner).generate_schedule()

    assert schedule == []


def test_weekly_recurrence():
    owner = Owner("Jordan", 120)
    pet = Pet("Bro", "Dog", 3)
    owner.add_pet(pet)

    task = Task("Grooming", 20, "medium", recurrence="weekly")
    pet.add_task(task)

    next_task = Scheduler(owner).mark_task_complete(pet, task)

    assert next_task is not None
    assert next_task.due_date == date.today() + timedelta(days=7)
    assert next_task.completed is False