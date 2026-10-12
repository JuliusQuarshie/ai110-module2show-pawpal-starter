
import streamlit as st
from datetime import date, time
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(
    page_title="PawPal+ | Pet Care Dashboard",
    page_icon="🐾",
    layout="wide"
)

if "owner" not in st.session_state:
    st.session_state.owner = Owner(
        name="Jordan",
        available_minutes=120
    )

owner = st.session_state.owner
scheduler = Scheduler(owner)

PRIORITY_ICONS = {
    "high": "🔴",
    "medium": "🟡",
    "low": "🟢"
}

SPECIES_ICONS = {
    "dog": "🐶",
    "cat": "🐱",
    "other": "🐾"
}


def priority_label(priority):
    """Return a visual priority indicator."""
    return (
        f"{PRIORITY_ICONS.get(priority.lower(), '⚪')} "
        f"{priority.capitalize()}"
    )


def pet_icon(species):
    """Return an emoji representing a pet species."""
    return SPECIES_ICONS.get(species.lower(), "🐾")


# HEADER
st.title("🐾 PawPal+")
st.markdown("#### Your Pet Care Dashboard")
st.caption(
    "One place to manage your pets, track care routines, "
    "and plan your day."
)

st.divider()

# SIDEBAR SETTINGS
with st.sidebar:
    st.header("⚙️ Settings")

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
    st.info(
        "🐾 PawPal+ keeps your pet information "
        "available during this browser session."
    )

# DASHBOARD METRICS
st.subheader(f"👋 Welcome, {owner.name}!")

all_tasks = owner.get_all_tasks()
total_tasks = len(all_tasks)
completed_tasks = sum(
    1 for _, task in all_tasks if task.completed
)
pending_tasks = total_tasks - completed_tasks

completion_rate = (
    completed_tasks / total_tasks
    if total_tasks else 0
)

metric1, metric2, metric3, metric4 = st.columns(4)

metric1.metric("🐾 My Pets", len(owner.pets))
metric2.metric("📋 Total Tasks", total_tasks)
metric3.metric("✅ Completed", completed_tasks)
metric4.metric("⏳ Pending", pending_tasks)

st.markdown("##### Overall Task Progress")
st.progress(completion_rate)
st.caption(
    f"{completion_rate:.0%} of all recorded tasks completed"
)

st.divider()

# PET MANAGEMENT
st.header("🐶 My Pets")

with st.expander("➕ Register a New Pet", expanded=not owner.pets):
    with st.form("add_pet_form", clear_on_submit=True):
        name = st.text_input("Pet Name")

        col1, col2 = st.columns(2)

        with col1:
            species = st.selectbox(
                "Species",
                ["Dog", "Cat", "Other"]
            )

        with col2:
            age = st.number_input(
                "Age",
                min_value=0,
                max_value=40
            )

        if st.form_submit_button("Add Pet", type="primary"):
            if name.strip():
                owner.add_pet(
                    Pet(name.strip(), species, int(age))
                )
                st.rerun()
            else:
                st.error("Please enter a pet name.")

if owner.pets:
    columns = st.columns(3)

    for index, pet in enumerate(owner.pets):
        with columns[index % 3]:
            with st.container(border=True):
                st.markdown(
                    f"### {pet_icon(pet.species)} {pet.name}"
                )
                st.write(f"**Species:** {pet.species}")
                st.write(f"**Age:** {pet.age} years")
                st.write(f"**Care Tasks:** {len(pet.tasks)}")

                pet_completed = sum(
                    1 for task in pet.tasks if task.completed
                )

                pet_progress = (
                    pet_completed / len(pet.tasks)
                    if pet.tasks else 0
                )

                st.progress(pet_progress)
                st.caption(
                    f"{pet_completed}/{len(pet.tasks)} "
                    "tasks completed"
                )
else:
    st.info("No pets registered yet. Add your first pet above!")

st.divider()

# ADD CARE TASKS
st.header("📝 Care Task Manager")

if owner.pets:
    with st.expander("➕ Create a Care Task", expanded=True):
        with st.form("add_task_form", clear_on_submit=True):
            pet_index = st.selectbox(
                "Assign to Pet",
                range(len(owner.pets)),
                format_func=lambda i: (
                    f"{pet_icon(owner.pets[i].species)} "
                    f"{owner.pets[i].name}"
                )
            )

            task_title = st.text_input(
                "Task Name",
                placeholder="e.g. Morning Walk"
            )

            col1, col2, col3 = st.columns(3)

            with col1:
                duration = st.number_input(
                    "Duration (minutes)",
                    min_value=1,
                    max_value=240,
                    value=20
                )

            with col2:
                priority = st.selectbox(
                    "Priority",
                    ["high", "medium", "low"],
                    format_func=priority_label
                )

            with col3:
                recurrence = st.selectbox(
                    "Frequency",
                    ["none", "daily", "weekly"]
                )

            col4, col5 = st.columns(2)

            with col4:
                due_time = st.time_input(
                    "Preferred Time",
                    value=time(8, 0)
                )

            with col5:
                due_date = st.date_input(
                    "Due Date",
                    value=date.today()
                )

            if st.form_submit_button(
                "Add Care Task",
                type="primary"
            ):
                if task_title.strip():
                    task = Task(
                        title=task_title.strip(),
                        duration_minutes=int(duration),
                        priority=priority,
                        due_time=due_time.strftime("%H:%M"),
                        recurrence=recurrence,
                        due_date=due_date
                    )

                    owner.pets[pet_index].add_task(task)
                    st.rerun()
                else:
                    st.error("Please enter a task name.")

    # TASK BROWSER
    st.subheader("📋 All Care Tasks")

    filter1, filter2, filter3 = st.columns(3)

    with filter1:
        selected_pet = st.selectbox(
            "Filter by Pet",
            ["All Pets"] + [
                pet.name for pet in owner.pets
            ]
        )

    with filter2:
        selected_status = st.selectbox(
            "Status",
            ["All", "Pending", "Completed"]
        )

    with filter3:
        sort_choice = st.selectbox(
            "Sort By",
            ["Preferred Time", "Priority"]
        )

    completed_filter = None

    if selected_status == "Pending":
        completed_filter = False
    elif selected_status == "Completed":
        completed_filter = True

    filtered_tasks = scheduler.filter_tasks(
        pet_name=(
            None if selected_pet == "All Pets"
            else selected_pet
        ),
        completed=completed_filter
    )

    if sort_choice == "Preferred Time":
        filtered_tasks.sort(
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

        filtered_tasks.sort(
            key=lambda item: (
                priority_order.get(item[1].priority, 3),
                item[1].due_date,
                item[1].due_time or "23:59"
            )
        )

    st.caption(f"Showing {len(filtered_tasks)} care task(s)")

    for pet, task in filtered_tasks:
        with st.container(border=True):
            info_col, action_col = st.columns([5, 1])

            with info_col:
                st.markdown(
                    f"**{pet_icon(pet.species)} "
                    f"{pet.name} — {task.title}**"
                )

                status = (
                    "✅ Completed" if task.completed
                    else "⏳ Pending"
                )

                st.caption(
                    f"{status}  |  "
                    f"{priority_label(task.priority)}  |  "
                    f"🕒 {task.due_time or 'Any time'}  |  "
                    f"📅 {task.due_date}  |  "
                    f"⏱️ {task.duration_minutes} min  |  "
                    f"🔁 {task.recurrence.capitalize()}"
                )

            with action_col:
                if not task.completed:
                    if st.button(
                        "✅ Complete",
                        key=f"complete_{id(task)}"
                    ):
                        scheduler.mark_task_complete(pet, task)
                        st.rerun()

    if not filtered_tasks:
        st.info("No tasks match your current filters.")
else:
    st.info("Register a pet before creating care tasks.")

st.divider()

# CONFLICT DETECTION
st.header("⚠️ Schedule Conflict Monitor")

conflict_date = st.date_input(
    "Check Date",
    value=date.today(),
    key="conflict_check"
)

conflicts = scheduler.detect_conflicts(
    on_date=conflict_date
)

if conflicts:
    st.warning(
        f"{len(conflicts)} scheduling conflict(s) detected."
    )

    for conflict in conflicts:
        task_names = [
            f"{pet_name}: {title}"
            for pet_name, title in conflict["tasks"]
        ]

        st.error(
            f"🕒 {conflict['time']} — "
            + " overlaps with ".join(task_names)
        )

    st.info(
        "💡 Tip: Adjust the preferred times "
        "of conflicting tasks."
    )
else:
    st.success(
        "✅ No preferred-time conflicts detected "
        "for this date."
    )

st.divider()

# DAILY SCHEDULE
st.header("📅 Daily Care Planner")

col1, col2 = st.columns(2)

with col1:
    schedule_date = st.date_input(
        "Plan for Date",
        value=date.today(),
        key="daily_date"
    )

with col2:
    start_time = st.time_input(
        "Starting Time",
        value=time(8, 0),
        key="daily_start"
    )

if st.button("🚀 Generate My Schedule", type="primary"):
    daily_scheduler = Scheduler(
        owner,
        start_time=start_time.strftime("%H:%M")
    )

    schedule = daily_scheduler.generate_schedule(
        on_date=schedule_date
    )

    if schedule:
        st.success("Your daily care plan is ready! 🐾")

        schedule_data = []

        for item in schedule:
            schedule_data.append({
                "Start": item["start"],
                "End": item["end"],
                "Pet": item["pet"],
                "Activity": item["task"],
                "Duration": f"{item['duration']} min",
                "Priority": priority_label(
                    item["priority"]
                )
            })

        st.dataframe(
            schedule_data,
            use_container_width=True,
            hide_index=True
        )

        used_minutes = sum(
            item["duration"]
            for item in schedule
        )

        stat1, stat2, stat3 = st.columns(3)

        stat1.metric("Activities", len(schedule))
        stat2.metric("Time Planned", f"{used_minutes} min")
        stat3.metric(
            "Time Left",
            f"{owner.available_minutes - used_minutes} min"
        )

        st.info(
            "🧠 **How PawPal+ planned your day:** "
            "High-priority tasks were considered first, "
            "followed by medium- and low-priority tasks. "
            "Tasks with the same priority were ordered "
            "by preferred time. Activities exceeding your "
            "available time budget were skipped."
        )
    else:
        st.warning(
            "No pending tasks could fit into the "
            "schedule for this date."
        )

    st.caption(
        "Preferred times are used for ordering. "
        "They are not enforced as fixed appointments."
    )

st.divider()

# FOOTER
st.caption(
    "🐾 PawPal+ | Smart Pet Care Management"
)
