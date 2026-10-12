
import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(
    page_title="PawPal+",
    page_icon="🐾",
    layout="wide"
)

# Keep owner data available across Streamlit reruns
if "owner" not in st.session_state:
    st.session_state.owner = Owner(
        name="Jordan",
        available_minutes=120
    )

owner = st.session_state.owner

st.title("🐾 PawPal+")
st.write("Your smart pet care management assistant.")
st.divider()

# OWNER SETTINGS
st.header("👤 Owner Information")

owner.name = st.text_input("Owner Name", value=owner.name)

owner.available_minutes = st.number_input(
    "Daily Available Time (minutes)",
    min_value=1,
    max_value=1440,
    value=owner.available_minutes
)

st.divider()

# PET MANAGEMENT
st.header("🐶 Manage Your Pets")

with st.form("add_pet_form", clear_on_submit=True):
    pet_name = st.text_input("Pet Name")
    species = st.selectbox("Species", ["Dog", "Cat", "Other"])
    age = st.number_input("Age", min_value=0, max_value=40)

    add_pet = st.form_submit_button("Add Pet")

    if add_pet:
        if pet_name.strip():
            owner.add_pet(Pet(pet_name.strip(), species, int(age)))
            st.success(f"{pet_name} added successfully!")
        else:
            st.error("Please enter a pet name.")

if owner.pets:
    st.subheader("Registered Pets")

    for pet in owner.pets:
        st.write(
            f"🐾 **{pet.name}** — {pet.species}, "
            f"{pet.age} years old ({len(pet.tasks)} tasks)"
        )
else:
    st.info("No pets registered yet.")

st.divider()

# TASK MANAGEMENT
st.header("📋 Manage Care Tasks")

if owner.pets:
    with st.form("add_task_form", clear_on_submit=True):
        selected_pet = st.selectbox(
            "Select Pet",
            options=range(len(owner.pets)),
            format_func=lambda i: (
                f"{owner.pets[i].name} ({owner.pets[i].species})"
            )
        )

        task_title = st.text_input("Task Name")

        col1, col2 = st.columns(2)

        with col1:
            duration = st.number_input(
                "Duration (minutes)",
                min_value=1,
                max_value=240,
                value=20
            )

            priority = st.selectbox(
                "Priority",
                ["high", "medium", "low"]
            )

        with col2:
            due_time = st.time_input("Preferred Time")

            recurrence = st.selectbox(
                "Frequency",
                ["none", "daily", "weekly"]
            )

        add_task = st.form_submit_button("Add Task")

        if add_task:
            if task_title.strip():
                task = Task(
                    title=task_title.strip(),
                    duration_minutes=int(duration),
                    priority=priority,
                    due_time=due_time.strftime("%H:%M"),
                    recurrence=recurrence
                )

                owner.pets[selected_pet].add_task(task)
                st.success(f"{task_title} added successfully!")
            else:
                st.error("Please enter a task name.")

    st.subheader("Current Tasks")

    for pet in owner.pets:
        for task_index, task in enumerate(pet.tasks):
            col1, col2 = st.columns([4, 1])

            with col1:
                status = "✅" if task.completed else "⏳"
                st.write(
                    f"{status} **{pet.name}: {task.title}** "
                    f"— {task.duration_minutes} min | "
                    f"{task.priority} | {task.due_time} | "
                    f"{task.recurrence}"
                )

            with col2:
                if not task.completed:
                    if st.button(
                        "Complete",
                        key=f"complete_{id(pet)}_{task_index}"
                    ):
                        Scheduler(owner).mark_task_complete(pet, task)
                        st.rerun()
else:
    st.info("Add a pet before creating care tasks.")

st.divider()

# SCHEDULE GENERATION
st.header("📅 Daily Care Schedule")

start_time = st.time_input(
    "Schedule Start Time",
    value=__import__("datetime").time(8, 0),
    key="schedule_start"
)

if st.button("Generate Schedule", type="primary"):
    scheduler = Scheduler(
        owner,
        start_time=start_time.strftime("%H:%M")
    )

    schedule = scheduler.generate_schedule()

    if schedule:
        st.success("Your daily schedule is ready!")

        st.table([
            {
                "Start": item["start"],
                "End": item["end"],
                "Pet": item["pet"],
                "Activity": item["task"],
                "Duration": f'{item["duration"]} min',
                "Priority": item["priority"]
            }
            for item in schedule
        ])

        used_minutes = sum(
            item["duration"] for item in schedule
        )

        col1, col2, col3 = st.columns(3)

        col1.metric("Scheduled Tasks", len(schedule))
        col2.metric("Time Used", f"{used_minutes} min")
        col3.metric(
            "Time Remaining",
            f"{owner.available_minutes - used_minutes} min"
        )

        st.caption(
            "Tasks are ordered by priority and preferred time. "
            "Activities that exceed the available time are skipped. "
            "Preferred times are used for ordering, not as fixed "
            "appointment times."
        )

    else:
        st.warning(
            "No tasks could be scheduled. Check your tasks "
            "and available time."
        )

    conflicts = scheduler.detect_conflicts()

    if conflicts:
        st.warning("⚠️ Potential Scheduling Conflicts")

        for conflict in conflicts:
            names = [
                f"{pet}: {title}"
                for pet, title in conflict["tasks"]
            ]

            st.write(
                f"Tasks sharing {conflict['time']}: "
                + ", ".join(names)
            )

st.divider()
st.caption("PawPal+ | Smart Pet Care Management")
