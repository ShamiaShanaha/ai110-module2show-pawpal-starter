import streamlit as st
from pawpal_system import Owner, Pet, Task, Priority, Scheduler  # new code

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

# --- Owner & Pet Setup --- # new code 2
st.subheader("Owner & Pet Setup")  # new code 2
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
available_minutes = st.number_input("Available minutes today", min_value=10, max_value=480, value=60)  # new code 2

if st.button("Set up owner & pet"):  # new code 2
    st.session_state.owner = Owner(name=owner_name, available_minutes=available_minutes)  # new code 2
    st.session_state.pet = Pet(name=pet_name, species=species, age=1)  # new code 2
    st.session_state.owner.add_pet(st.session_state.pet)  # new code 2: attach pet to owner
    st.success(f"Owner '{owner_name}' and pet '{pet_name}' ({species}) set up.")  # new code 2

st.divider()

# --- Task Management --- # new code 2
st.markdown("### Tasks")
st.caption("Add tasks below. Each task is added directly to your pet using add_task().")  # new code 2

if "tasks" not in st.session_state:
    st.session_state.tasks = []

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):  # new code 2
    if "pet" not in st.session_state:  # new code 2: guard — pet must exist before adding tasks
        st.warning("Please set up your owner & pet first.")  # new code 2
    else:
        new_task = Task(  # new code 2: create a real Task object
            name=task_title,
            category="general",
            duration_minutes=int(duration),
            priority=Priority[priority.upper()]
        )
        st.session_state.pet.add_task(new_task)  # new code 2: call add_task() directly on Pet
        st.session_state.tasks.append(  # new code 2: keep UI table in sync
            {"title": task_title, "duration_minutes": int(duration), "priority": priority}
        )

if st.session_state.tasks:
    st.write("Current tasks:")
    st.table(st.session_state.tasks)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

# --- Schedule Generation --- # new code 2
st.subheader("Build Schedule")
st.caption("Generates a prioritized daily plan from your pet's tasks within your available time.")  # new code 2

if st.button("Generate schedule"):  # new code
    if "owner" not in st.session_state:  # new code: only create Owner if not already in session
        st.warning("Please set up your owner & pet before generating a schedule.")  # new code 2
    else:
        scheduler = Scheduler(owner=st.session_state.owner)  # new code

        # --- phase 6 step 1: Conflict Warnings ---
        st.markdown("#### Conflict Warnings")
        conflicts = scheduler.safe_detect_conflicts()  # phase 6 step 1: run safe conflict check
        for msg in conflicts:
            if "No conflicts" in msg:
                st.success(msg)  # phase 6 step 1: green banner for a clean schedule
            else:
                st.warning(f"⚠️ {msg}")  # phase 6 step 1: yellow banner per conflict — clear for pet owner

        st.divider()

        # --- phase 6 step 1: Scheduled Tasks Table ---
        st.markdown("#### Today's Scheduled Tasks")
        plan = scheduler.generate_plan()  # phase 6 step 1: get ordered task list
        if plan:
            plan_data = [  # phase 6 step 1: build table rows from scheduled tasks
                {
                    "Task": task.name,
                    "Category": task.category,
                    "Duration (min)": task.duration_minutes,
                    "Priority": task.priority.name,
                    "Status": "Done" if task.is_completed else "Pending"
                }
                for task in plan
            ]
            st.table(plan_data)  # phase 6 step 1: display as clean table
            total = sum(t.duration_minutes for t in plan)
            budget = st.session_state.owner.get_available_time()
            st.caption(f"Total time used: {total} / {budget} min")  # phase 6 step 1: time summary

        else:
            st.warning("No tasks could be scheduled. Add tasks or increase available minutes.")  # phase 6 step 1

        st.divider()

        # --- phase 6 step 1: Tasks Sorted by Time of Day ---
        st.markdown("#### All Tasks by Time of Day")
        sorted_tasks = scheduler.sort_by_time()  # phase 6 step 1: use sort_by_time() method
        if sorted_tasks:
            sorted_data = [  # phase 6 step 1: build table rows sorted by time slot
                {
                    "Task": task.name,
                    "Time Slot": task.time_slot.name.capitalize(),
                    "Duration (min)": task.duration_minutes,
                    "Priority": task.priority.name,
                    "Frequency": task.frequency.value
                }
                for task in sorted_tasks
            ]
            st.table(sorted_data)  # phase 6 step 1
        else:
            st.info("No tasks to display.")  # phase 6 step 1
