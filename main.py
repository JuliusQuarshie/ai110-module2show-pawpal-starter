from pawpal_system import Owner, Pet, Task, Scheduler


def main():
    owner = Owner("Jordan", 120)

    dog = Pet("Max", "Dog", 3)
    cat = Pet("Luna", "Cat", 2)

    owner.add_pet(dog)
    owner.add_pet(cat)

    dog.add_task(Task("Morning Walk", 30, "high", "08:00", "daily"))
    dog.add_task(Task("Grooming", 20, "medium", "10:00", "weekly"))
    cat.add_task(Task("Breakfast", 15, "high", "09:00", "daily"))

    scheduler = Scheduler(owner)

    print("=== PawPal+ Today's Schedule ===")

    for item in scheduler.generate_schedule():
        print(
            f"{item['start']} - {item['end']} | "
            f"{item['pet']}: {item['task']} "
            f"({item['duration']} min, {item['priority']})"
        )


if __name__ == "__main__":
    main()