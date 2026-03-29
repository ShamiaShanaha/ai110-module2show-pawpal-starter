# PawPal+ Project Reflection

## 1. System Design

**Three core actions**
1. Set up their pet profile
2. Manage care tasks 
3. Generate and view the daily plan

**a. Initial design**

- Briefly describe your initial UML design.
The diagram shows a pet care scheduling system with four classes connected in a simple chain: an Owner manages a Pet and a list of Task objects, and a Scheduler uses the Owner to create a prioritized daily plan.

- What classes did you include, and what responsibilities did you assign to each?
1. Pet that holds the animal name,speciies, age, and special needs. Its only responsibility is returning a readable summary of that info through get_profile()

2. Task, which is a single care activity with a name, category, duration, priority, and completion status. It can mark itself complete and allow edits to its own fields.

3. The Owner holds the available daily time and preferences, and owns a list of multiple pets. It is responsible for exposing available time, updating preferences, and returning a flat list of all tasks across every pet through get_all_tasks()

4. Scheduler takes an Owner as input, reads their pets' tasks and available time, and decides which tasks to include, what order to run them in, and why. It also handles sorting by time slot, filtering by pet or status, conflict detection, and recurring task rescheduling. No other class touches scheduling logic.

**b. Design changes**

- Did your design change during implementation?
Yes I did.
- If yes, describe at least one change and why you made it.
The UML had no link between Task and Pet. During implementation, it became obvious that without one, the scheduler had no way to know that a "morning walk" only applies to dogs. Adding species_filter: Optional[str] to the task, where None means the task applies to any pet, was the minimal fix that kept the task as a simple dataclass while still giving scheduler.generate_plan() enough information to filter correctly.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
1. Time budget - Tasks that don't fit are excluded.
2. Priority - HIGH, MEDIUM, LOW determines which tasks are scheduled first 
3. Species filter - tasks tagged with a species_filter, like dog, are only scheduled for pets of that species.
4. Time slot - MORNING, AFTERNOON, EVENING groups tasks into preferred parts of the day.
5. Frequency - DAILY tasks are always pulled to the top of the plan before optional ones.

- How did you decide which constraints mattered most?
Time budget and priority were the ones that mattered the most because they directly address the issue of a busy owner can't do everything, so the scheduler needs to decide what gets done and in what order. The species filter came next because scheduling the wrong task for the wrong pet can make an invalid plan. Time slot and frequency were added later to make the plan more realistic and useful.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
The scheduler sorts by priority first, then fits tasks within the time budget by picking the highest priority tasks first and then stops when time runs out. It does not run every possible combination to find the most efficient use of available time.

- Why is that tradeoff reasonable for this scenario?
A pet care app does not need a perfect schedule, but it needs a fast and predictable one. A busy owner glancing at their phone wants an instant answer, not an optimized solution that took 10 seconds to compute.
---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
I used it to brainstorm the design of the UML. I used it to debug some of my code and also make comments on my code.
- What kinds of prompts or questions were most helpful?
The questions were most helpful when I asked what some of the codes did so that I could understand them more.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
One moment, I did not accept an AI suggestion to change the algorithm to make it simpler. I thought it was fine the way it was. 
- How did you evaluate or verify what the AI suggested?
I told the AI not to make any changes so I could read what it wrote.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
1. Verified that calling mark_complete() on a task correctly updates its status from incomplete to complete.
2. Verified that calling add_task() on a pet successfully adds the task and increases the pet's total task count.
3. Verified that sort_by_time() correctly reorders tasks chronologically from morning to evening, even when they were added in a different order.
4. Verified that recurring tasks behave correctly. A daily task reschedules for the next day, a weekly task reschedules for seven days later, and an as-needed task does not reschedule at all.
5. Verified that complete_and_reschedule() not only marks the task as done but also adds the next occurrence directly to the pet's task list automatically.
6. Verified that the conflict detector correctly raises a warning when two different pets have tasks assigned to the same time slot.
7. Verified that safe_detect_conflicts() returns a clean confirmation message when the schedule has no issues, rather than returning an empty result.

- Why were these tests important?
These behaviors are important because if mark_complete() does not work, no task ever gets finished. If sorting is wrong, the owner sees the tasks in the wrong order. If recurrence fails, the daily care tasks disappear after one completion. Testing these gave confidence that the scheduler outputs are working before connecting them to the Streamlit UI.

**b. Confidence**

- How confident are you that your scheduler works correctly?
I am 4/5 because 11/11 tests have passed. The one less point comes from the untested edge cases. If an owner has no pet, a zero-minute budget, and the same task has not been verified.
- What edge cases would you test next if you had more time?
1. Owner with no pets
2. Zero available minutes 
3. Completing the sam task twice

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
I am satisfied with my test cases passing.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
1. Add save/load data. If the program closes, then all the data is lost, so have a database.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
That UML is a starting point. The design changes as you continue to develop the code. 
