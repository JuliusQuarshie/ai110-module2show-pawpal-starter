
import streamlit as st
from datetime import date, time
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(
    page_title="PawPal+",
    page_icon="🐾",
    layout="wide"
)

# SESSION STATE
if "owner" not in st.session_state:
    st.session_state.owner = Owner(
        name="Jordan",
        available_minutes=120
    )

owner = st.session_state.owner
scheduler = Scheduler(owner)

# HEADER
st.title("🐾 PawPal+")
st.write("Your smart pet care management assistant.")
st.caption("Manage pets, organize care routines, and plan your day.")
st.divider()

# OWNER INFORMATION
st.header("👤 Owner Information")

owner.name = st.text_input(
    "Owner Name",
    value=owner.name
)

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

    if st.form_submit_button("Add Pet"):
        if pet_name.strip():
            owner.add_pet(
                Pet(pet_name.strip(), species, int(age))
            )
            st.success(f"{pet_name.strip()} added successfully!")
        else:
            st.error("Please enter a pet name.")

if owner.pets:
    st.subheader("Registered Pets")

    for pet in owner.pets:
        st.write(
            f"🐾 **{pet.name}** — {pet.species}, "
            f"{pet.age} years old | {len(pet.tasks)} tasks"
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
            due_time = st.time_input(
                "Preferred Time",
                value=time(8, 0)
            )

            recurrence = st.selectbox(
                "Frequency",
                ["none", "daily", "weekly"]
            )

        # Today's date is the default due date.
        task_date = st.date_input(
            "Task Due Date",
            value=date.today()
        )

        if st.form_submit_button("Add Task"):
            if task_title.strip():
                task = Task(
                    title=task_title.strip(),
                    duration_minutes=int(duration),
                    priority=priority,
                    due_time=due_time.strftime("%H:%M"),
                    recurrence=recurrence,
                    due_date=task_date
                )

                owner.pets[selected_pet].add_task(task)
                st.success(
                    f"{task_title.strip()} added successfully!"
                )
            else:
                st.error("Please enter a task name.")

    st.subheader("🔎 Browse & Filter Tasks")

    filter_col1, filter_col2, filter_col3 = st.columns(3)

    with filter_col1:
        pet_filter = st.selectbox(
            "Filter by Pet",
            ["All Pets"] + [
                pet.name for pet in owner.pets
            ]
        )

    with filter_col2:
        status_filter = st.selectbox(
            "Task Status",
            ["All", "Pending", "Completed"]
        )

    with filter_col3:
        sort_option = st.selectbox(
            "Sort Tasks",
            ["Preferred Time", "Priority"]
        )

    completed_filter = None

    if status_filter == "Pending":
        completed_filter = False
    elif status_filter == "Completed":
        completed_filter = True

    filtered_tasks = scheduler.filter_tasks(
        pet_name=None if pet_filter == "All Pets" else pet_filter,
        completed=completed_filter
    )

    if sort_option == "Preferred Time":
        filtered_tasks = sorted(
            filtered_tasks,
            key=lambda item: (
                item[1].due_date,
                item[1].due_time or "23:59"
            )
        )
    else:
        priority_order = {
            "high": 0,
            "medium": 1,
            "low": 2
        }

        filtered_tasks = sorted(
            filtered_tasks,
            key=lambda item: (
                priority_order.get(item[1].priority.lower(), 3),
                item[1].due_date,
                item[1].due_time or "23:59"
            )
        )

    st.caption(f"Showing {len(filtered_tasks)} task(s)")

    if filtered_tasks:
        for pet, task in filtered_tasks:
            col1, col2 = st.columns([5, 1])

            with col1:
                status = "✅ Completed" if task.completed else "⏳ Pending"

                st.write(
                    f"**{pet.name}: {task.title}**"
                )
                st.caption(
                    f"{status} | {task.due_date} at "
                    f"{task.due_time or 'Unspecified'} | "
                    f"{task.duration_minutes} min | "
                    f"{task.priority.capitalize()} priority | "
                    f"{task.recurrence.capitalize()}"
                )

            with col2:
                if not task.completed:
                    if st.button(
                        "Complete",
                        key=f"complete_{id(task)}"
                    ):
                        scheduler.mark_task_complete(pet, task)
                        st.rerun()

            st.divider()
    else:
        st.info("No tasks match your selected filters.")

else:
    st.info("Add a pet before creating care tasks.")

# CONFLICT DETECTION
st.header("⚠️ Scheduling Conflict Check")

check_date = st.date_input(
    "Check conflicts for",
    value=date.today(),
    key="conflict_date"
)

conflicts = scheduler.detect_conflicts(on_date=check_date)

if conflicts:
    st.warning(
        f"{len(conflicts)} potential scheduling "
        f"conflict(s) detected."
    )

    for conflict in conflicts:
        task_names = [
            f"{pet_name}: {title}"
            for pet_name, title in conflict["tasks"]
        ]

        st.error(
            f"Overlap around {conflict['time']}: "
            + " and ".join(task_names)
        )

    st.info(
        "Consider adjusting the preferred times of these "
        "tasks to avoid overlapping care activities."
    )
else:
    st.success(
        "No overlapping preferred-time tasks found "
        "for this date."
    )

st.divider()

# DAILY SCHEDULE
st.header("📅 Daily Care Schedule")

schedule_col1, schedule_col2 = st.columns(2)

with schedule_col1:
    schedule_date = st.date_input(
        "Schedule Date",
        value=date.today(),
        key="schedule_date"
    )

with schedule_col2:
    start_time = st.time_input(
        "Schedule Start Time",
        value=time(8, 0),
        key="schedule_start"
    )

if st.button("Generate Schedule", type="primary"):
    daily_scheduler = Scheduler(
        owner,
        start_time=start_time.strftime("%H:%M")
    )

    schedule = daily_scheduler.generate_schedule(
        on_date=schedule_date
    )

    if schedule:
        st.success("Your daily care schedule is ready!")

        rows = []

        for item in schedule:
            rows.append({
                "Start": item["start"],
                "End": item["end"],
                "Pet": item["pet"],
                "Activity": item["task"],
                "Duration": f"{item['duration']} min",
                "Priority": item["priority"].capitalize()
            })

        st.table(rows)

        used_minutes = sum(
            item["duration"]
            for item in schedule
        )

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Scheduled Tasks",
            len(schedule)
        )

        col2.metric(
            "Time Used",
            f"{used_minutes} min"
        )

        col3.metric(
            "Time Remaining",
            f"{owner.available_minutes - used_minutes} min"
        )

        st.info(
            "How this plan was created: high-priority tasks "
            "are considered first. Tasks with the same priority "
            "are ordered by preferred time. Activities that "
            "exceed the remaining daily time budget are skipped."
        )
    else:
        st.warning(
            "No pending tasks could be scheduled for this date. "
            "Try adding tasks or increasing your available time."
        )

    daily_conflicts = daily_scheduler.detect_conflicts(
        on_date=schedule_date
    )

    if daily_conflicts:
        st.warning(
            f"This date also has "
            f"{len(daily_conflicts)} preferred-time "
            f"conflict(s). See the Conflict Check section."
        )

    st.caption(
        "Preferred times guide task ordering but are not "
        "treated as fixed appointment times."
    )

st.divider()
st.caption(
    "PawPal+ | Smart Pet Care Management | Built with Python & Streamlit"
)
