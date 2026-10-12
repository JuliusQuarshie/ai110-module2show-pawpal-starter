
from datetime import date
from pawpal_system import Owner, Pet, Task, Scheduler


def main():
    owner = Owner("Jordan", 120)

    dog = Pet("Bro", "Dog", 3)
    cat = Pet("Luna", "Cat", 2)

    owner.add_pet(dog)
    owner.add_pet(cat)

    # Intentionally add tasks out of chronological order
    grooming = Task("Grooming", 20, "low", "11:00", "weekly")
    walk = Task("Morning Walk", 30, "high", "08:00", "daily")
    feeding = Task("Breakfast", 15, "high", "08:15", "daily")
    medication = Task("Medication", 10, "high", "09:00")

    dog.add_task(grooming)
    dog.add_task(walk)
    cat.add_task(feeding)
    cat.add_task(medication)

    scheduler = Scheduler(owner)

    print("\n=== 1. Tasks Sorted by Time ===")
    for pet, task in scheduler.sort_by_time():
        print(f"{task.due_time} | {pet.name}: {task.title}")

    print("\n=== 2. Filter Tasks for Bro ===")
    for pet, task in scheduler.filter_tasks(pet_name="Bro"):
        print(f"{pet.name}: {task.title}")

    print("\n=== 3. Today's Schedule ===")
    for item in scheduler.generate_schedule():
        print(
            f"{item['start']} - {item['end']} | "
            f"{item['pet']}: {item['task']}"
        )

    print("\n=== 4. Conflict Detection ===")
    conflicts = scheduler.detect_conflicts()

    if conflicts:
        for conflict in conflicts:
            print(
                f"WARNING: Overlapping tasks at {conflict['time']}"
            )
            for pet_name, title in conflict["tasks"]:
                print(f"  - {pet_name}: {title}")
    else:
        print("No conflicts detected.")

    print("\n=== 5. Recurring Task Test ===")
    print("Before completion:", walk.completed)

    next_task = scheduler.mark_task_complete(dog, walk)

    print("After completion:", walk.completed)

    if next_task:
        print(
            f"Next occurrence: {next_task.title} "
            f"on {next_task.due_date}"
        )
        print(
            f"Expected date: {date.today().isoformat()} + 1 day"
        )

    print("\n=== 6. Completed Task Filtering ===")
    for pet, task in scheduler.filter_tasks(completed=True):
        print(f"{pet.name}: {task.title} [Completed]")


if __name__ == "__main__":
    main()
