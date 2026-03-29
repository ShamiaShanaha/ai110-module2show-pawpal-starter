from pawpal_system import Owner, Pet, Task, Priority, Scheduler, TimeSlot, Frequency  # Phase 4 Step 1

# Create Owner
jordan = Owner(name="Jordan", available_minutes=120)

# Create Pets
buddy = Pet(name="Buddy", species="dog", age=3)
whiskers = Pet(name="Whiskers", species="cat", age=5)

# Add pets to owner
jordan.add_pet(buddy)
jordan.add_pet(whiskers)

# Phase 4 Step 2: tasks added intentionally out of time order to test sort_by_time()
buddy.add_task(Task(name="Enrichment Play", category="enrichment", duration_minutes=20, priority=Priority.LOW, time_slot=TimeSlot.AFTERNOON, frequency=Frequency.AS_NEEDED))
buddy.add_task(Task(name="Morning Walk", category="walk", duration_minutes=30, priority=Priority.HIGH, species_filter="dog", time_slot=TimeSlot.MORNING, frequency=Frequency.DAILY))
buddy.add_task(Task(name="Evening Brush", category="grooming", duration_minutes=10, priority=Priority.MEDIUM, species_filter="dog", time_slot=TimeSlot.EVENING, frequency=Frequency.AS_NEEDED))
buddy.add_task(Task(name="Feeding", category="feeding", duration_minutes=10, priority=Priority.HIGH, time_slot=TimeSlot.MORNING, frequency=Frequency.DAILY))

# Phase 4 Step 4: Whiskers also has a MORNING task — creates a time conflict with Buddy's morning tasks
whiskers.add_task(Task(name="Medication", category="meds", duration_minutes=15, priority=Priority.MEDIUM, species_filter="cat", time_slot=TimeSlot.EVENING, frequency=Frequency.DAILY))
whiskers.add_task(Task(name="Feeding", category="feeding", duration_minutes=10, priority=Priority.HIGH, time_slot=TimeSlot.MORNING, frequency=Frequency.DAILY))
whiskers.add_task(Task(name="Morning Grooming", category="grooming", duration_minutes=20, priority=Priority.MEDIUM, time_slot=TimeSlot.MORNING, frequency=Frequency.AS_NEEDED))  # Phase 4 Step 4: intentional conflict — same slot as Buddy's morning tasks
whiskers.add_task(Task(name="Afternoon Play", category="enrichment", duration_minutes=15, priority=Priority.LOW, time_slot=TimeSlot.AFTERNOON, frequency=Frequency.AS_NEEDED))

# Run scheduler
scheduler = Scheduler(owner=jordan)

# --- Today's full schedule (includes conflict warnings) ---
print("=== Today's Schedule ===")
print(scheduler.explain_reasoning())

# Phase 4 Step 2: sort all tasks by time slot to verify ordering
print("\n=== All Tasks Sorted by Time of Day ===")
for task in scheduler.sort_by_time():
    print(f"  {task}")

# Phase 4 Step 2: filter by pet name only
print("\n=== Buddy's Tasks Only ===")
for task in scheduler.filter_tasks(pet_name="Buddy"):
    print(f"  {task}")

# Phase 4 Step 2: filter by status only (all pending)
print("\n=== All Pending Tasks (Every Pet) ===")
for task in scheduler.filter_tasks(completed=False):
    print(f"  {task}")

# Phase 4 Step 2: filter by both pet name and status
print("\n=== Whiskers' Pending Tasks Only ===")
for task in scheduler.filter_tasks(pet_name="Whiskers", completed=False):
    print(f"  {task}")
