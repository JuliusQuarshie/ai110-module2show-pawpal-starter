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