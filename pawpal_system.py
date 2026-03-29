from dataclasses import dataclass, field
from datetime import date, timedelta  # Phase 4 Step 3
from enum import Enum
from typing import List, Optional


# new edit
class Priority(Enum):
    HIGH = 1
    MEDIUM = 2
    LOW = 3


# Phase 4 Step 1
class TimeSlot(Enum):
    MORNING = 1
    AFTERNOON = 2
    EVENING = 3
    ANY = 4


# Phase 4 Step 1
class Frequency(Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    AS_NEEDED = "as_needed"


@dataclass
class Task:
    name: str
    category: str
    duration_minutes: int
    priority: Priority
    species_filter: Optional[str] = None  # new edit: e.g. "dog" — None means applies to any pet
    is_completed: bool = False
    time_slot: TimeSlot = TimeSlot.ANY          # Phase 4 Step 1: preferred time of day
    frequency: Frequency = Frequency.AS_NEEDED  # Phase 4 Step 1: how often this task recurs
    due_date: Optional[date] = None             # Phase 4 Step 3: when this task is next due

    def mark_complete(self) -> Optional["Task"]:  # Phase 4 Step 3: returns next occurrence if recurring
        """Mark this task as completed and return a new instance for the next occurrence if recurring."""
        self.is_completed = True

        if self.frequency == Frequency.DAILY:  # Phase 4 Step 3: reschedule tomorrow
            next_due = date.today() + timedelta(days=1)
        elif self.frequency == Frequency.WEEKLY:  # Phase 4 Step 3: reschedule next week
            next_due = date.today() + timedelta(weeks=1)
        else:
            return None  # Phase 4 Step 3: AS_NEEDED tasks don't auto-reschedule

        # Phase 4 Step 3: return a fresh copy of this task with the new due date
        return Task(
            name=self.name,
            category=self.category,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            species_filter=self.species_filter,
            is_completed=False,
            time_slot=self.time_slot,
            frequency=self.frequency,
            due_date=next_due
        )

    def edit(self, name: str, duration: int, priority: Priority) -> None:  # newcode 2
        """Update the task's name, duration, and priority in place."""
        self.name = name
        self.duration_minutes = duration
        self.priority = priority

    def __repr__(self) -> str:  # newcode 2
        """Return a readable string showing priority, name, duration, and status."""
        status = "Done" if self.is_completed else "Pending"
        return f"[{self.priority.name}] {self.name} ({self.duration_minutes} min) — {status}"


@dataclass
class Pet:
    name: str
    species: str  # e.g. "dog", "cat", "rabbit"
    age: int
    special_needs: str = ""
    tasks: List[Task] = field(default_factory=list)  # newcode 2

    def get_profile(self) -> str:  # newcode 2
        """Return a formatted summary string of the pet's details."""
        needs = f", Special needs: {self.special_needs}" if self.special_needs else ""
        return f"{self.name} ({self.species}, age {self.age}{needs})"

    def add_task(self, task: Task) -> None:  # newcode 2
        """Append a task to this pet's task list."""
        self.tasks.append(task)

    def get_pending_tasks(self) -> List[Task]:  # newcode 2
        """Return all tasks that have not yet been completed."""
        return [t for t in self.tasks if not t.is_completed]


class Owner:
    def __init__(self, name: str, available_minutes: int, preferences: str = ""):
        self.name = name
        self.available_minutes = available_minutes
        self.preferences = preferences
        self.pets: List[Pet] = []  # newcode 2: supports multiple pets

    def add_pet(self, pet: Pet) -> None:  # new edit
        """Add a pet to the owner's list of pets."""
        self.pets.append(pet)  # newcode 2: append instead of overwrite

    def get_available_time(self) -> int:  # newcode 2
        """Return the owner's total available minutes for the day."""
        return self.available_minutes

    def update_preferences(self, preferences: str) -> None:  # newcode 2
        """Update the owner's scheduling preferences."""
        self.preferences = preferences

    def get_all_tasks(self) -> List[Task]:  # newcode 2
        """Return a flat list of all tasks across every pet."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    def _get_plan_with_pets(self) -> List[tuple]:  # new code 3: helper that pairs each task with its pet
        """Filter, sort, and return scheduled (pet, task) pairs within the time budget."""
        budget = self.owner.get_available_time()
        candidates = []
        for pet in self.owner.pets:
            for task in pet.get_pending_tasks():
                if task.species_filter is None or task.species_filter == pet.species:
                    candidates.append((pet, task))

        # Phase 4 Step 1: daily tasks always come first, then by priority, then time slot, then duration
        slot_order = {TimeSlot.MORNING: 1, TimeSlot.AFTERNOON: 2, TimeSlot.EVENING: 3, TimeSlot.ANY: 4}
        candidates.sort(key=lambda pt: (
            0 if pt[1].frequency == Frequency.DAILY else 1,  # Phase 4 Step 1: daily tasks first
            pt[1].priority.value,
            slot_order[pt[1].time_slot],                     # Phase 4 Step 1: sort by time slot
            pt[1].duration_minutes
        ))

        plan = []
        time_used = 0
        for pet, task in candidates:
            if time_used + task.duration_minutes <= budget:
                plan.append((pet, task))
                time_used += task.duration_minutes

        return plan

    def generate_plan(self) -> List[Task]:  # newcode 2
        """Return the ordered list of tasks scheduled within the owner's time budget."""
        # new edit: Read available_minutes live from owner (not a snapshot)
        # new edit: Filter tasks by pet species, then sort by priority then duration as tie-breaker
        return [task for _, task in self._get_plan_with_pets()]

    def sort_by_time(self) -> List[Task]:  # Phase 4 Step 2
        """Return all tasks across all pets sorted by time_slot (MORNING first, ANY last).

        Does not filter by completion status — returns all tasks regardless.
        Useful for displaying a time-ordered view of the full task list.
        """
        slot_order = {TimeSlot.MORNING: 1, TimeSlot.AFTERNOON: 2, TimeSlot.EVENING: 3, TimeSlot.ANY: 4}
        all_pending = self.owner.get_all_tasks()
        return sorted(all_pending, key=lambda t: slot_order[t.time_slot])

    def get_tasks_by_pet(self, pet_name: str) -> List[Task]:  # Phase 4 Step 1
        """Return all tasks belonging to the pet with the given name."""
        for pet in self.owner.pets:
            if pet.name.lower() == pet_name.lower():
                return pet.tasks
        return []

    def get_tasks_by_status(self, completed: bool) -> List[Task]:  # Phase 4 Step 1
        """Return all tasks across pets that match the given completion status."""
        return [t for t in self.owner.get_all_tasks() if t.is_completed == completed]

    def complete_and_reschedule(self, pet: Pet, task: Task) -> Optional[Task]:  # Phase 4 Step 3
        """Mark a task complete and automatically add the next occurrence to the pet if recurring.

        Args:
            pet: The pet that owns the task being completed.
            task: The task to mark as done.
        Returns:
            The newly created next Task if the frequency is DAILY or WEEKLY, otherwise None.
        """
        next_task = task.mark_complete()  # Phase 4 Step 3: mark done and get next occurrence
        if next_task is not None:
            pet.add_task(next_task)  # Phase 4 Step 3: add rescheduled task back to the pet
        return next_task

    def filter_tasks(self, pet_name: Optional[str] = None, completed: Optional[bool] = None) -> List[Task]:  # Phase 4 Step 2
        """Filter tasks by pet name, completion status, or both combined.

        Args:
            pet_name: If provided, only returns tasks belonging to that pet (case-insensitive).
            completed: If True, returns only completed tasks. If False, returns only pending tasks.
                       If None, returns tasks regardless of status.
        Returns:
            A list of Task objects matching the given filters.
        """
        results = self.owner.get_all_tasks()

        if pet_name is not None:  # Phase 4 Step 2: narrow by pet name if provided
            results = [
                task for pet in self.owner.pets
                if pet.name.lower() == pet_name.lower()
                for task in pet.tasks
            ]

        if completed is not None:  # Phase 4 Step 2: narrow by completion status if provided
            results = [t for t in results if t.is_completed == completed]

        return results

    def detect_time_conflicts(self) -> List[str]:  # Phase 4 Step 4
        """Detect overlapping tasks by simulating sequential start times within each slot.

        Assigns each slot a simulated start minute (MORNING=0, AFTERNOON=120, EVENING=240)
        and checks if any two tasks within the same slot have overlapping time windows.
        Returns:
            A list of conflict warning strings, empty if no overlaps are found.
        """
        warnings = []

        # Phase 4 Step 4: group scheduled (pet, task) pairs by time slot
        slot_buckets: dict = {slot: [] for slot in TimeSlot}
        for pet, task in self._get_plan_with_pets():
            slot_buckets[task.time_slot].append((pet, task))

        for slot, entries in slot_buckets.items():
            if len(entries) < 2:
                continue  # Phase 4 Step 4: need at least 2 tasks in a slot to have a conflict

            # Phase 4 Step 4: flag when tasks from different pets share the same slot
            # owner cannot be with two pets simultaneously
            for i in range(len(entries)):
                for j in range(i + 1, len(entries)):
                    pet_a, task_a = entries[i]
                    pet_b, task_b = entries[j]
                    if pet_a.name != pet_b.name:  # Phase 4 Step 4: only flag cross-pet conflicts
                        warnings.append(
                            f"Conflict: '{task_a.name}' ({pet_a.name}) and "
                            f"'{task_b.name}' ({pet_b.name}) overlap in the {slot.name.capitalize()} slot."
                        )

        return warnings

    def safe_detect_conflicts(self) -> List[str]:  # Phase 4 Step 4
        """Lightweight wrapper that runs all conflict checks and returns warnings without crashing.

        Wraps detect_conflicts() and detect_time_conflicts() each in a try/except so that
        any unexpected error produces a readable warning instead of stopping the program.
        Returns:
            A list of warning strings. If no issues are found, returns a clean confirmation message.
        """
        warnings = []

        try:  # Phase 4 Step 4: guard slot overload check
            warnings.extend(self.detect_conflicts())
        except Exception as e:
            warnings.append(f"Warning: slot conflict check could not complete — {e}")

        try:  # Phase 4 Step 4: guard time overlap check
            warnings.extend(self.detect_time_conflicts())
        except Exception as e:
            warnings.append(f"Warning: time conflict check could not complete — {e}")

        if not warnings:  # Phase 4 Step 4: confirm clean schedule if no issues found
            warnings.append("No conflicts detected — schedule looks good.")

        return warnings

    def detect_conflicts(self) -> List[str]:  # Phase 4 Step 1
        """Check for time slot overloads and return a list of conflict warning strings."""
        warnings = []
        budget = self.owner.get_available_time()
        slot_budget = budget // 3  # Phase 4 Step 1: divide day equally across 3 slots

        slot_order = {TimeSlot.MORNING: 1, TimeSlot.AFTERNOON: 2, TimeSlot.EVENING: 3, TimeSlot.ANY: 4}
        slot_totals: dict = {TimeSlot.MORNING: 0, TimeSlot.AFTERNOON: 0, TimeSlot.EVENING: 0}

        for pet in self.owner.pets:
            for task in pet.get_pending_tasks():
                if task.time_slot in slot_totals:
                    slot_totals[task.time_slot] += task.duration_minutes

        for slot, total in slot_totals.items():  # Phase 4 Step 1: flag overloaded slots
            if total > slot_budget:
                warnings.append(
                    f"Conflict: {slot.name.capitalize()} slot is overloaded "
                    f"({total} min of tasks vs {slot_budget} min available)."
                )

        return warnings

    def explain_reasoning(self) -> str:  # newcode 2
        """Return a human-readable summary of scheduled and excluded tasks with pet context."""
        plan_with_pets = self._get_plan_with_pets()  # new code 3: use helper to get pet context
        budget = self.owner.get_available_time()
        plan_tasks = [task for _, task in plan_with_pets]
        all_pending = [t for t in self.owner.get_all_tasks() if not t.is_completed]
        excluded = [t for t in all_pending if t not in plan_tasks]

        lines = [
            f"Daily plan for {self.owner.name} — {budget} min available",
            f"Scheduled {len(plan_with_pets)} task(s):",
        ]
        for pet, task in plan_with_pets:  # new code 3: show pet name and species per task
            lines.append(f"  - {task} → {pet.name} ({pet.species})")

        if excluded:
            lines.append(f"Excluded {len(excluded)} task(s) due to time or species mismatch:")
            for task in excluded:
                lines.append(f"  - {task}")

        all_warnings = self.safe_detect_conflicts()  # Phase 4 Step 4: use safe wrapper for all conflict checks
        lines.append("Warnings:")
        for warning in all_warnings:
            lines.append(f"  ! {warning}")

        return "\n".join(lines)
