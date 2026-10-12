# PawPal+ Project Reflection

## 1. System Design

**Three core actions users should be able to perform:**

1. Add a pet by entering its name, species, and other basic details.
2. Create care tasks such as feeding, walking, and administering medication.
3. Generate a daily schedule that organizes tasks based on priority, duration, and available time.

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My initial UML design consists of four classes: Owner, Pet, Task, and Scheduler. The Owner class stores information about the pet owner and manages their pets. The Pet class stores details about each pet and its care tasks. The Task class represents activities such as feeding, walking, and medication, including their duration, priority, and recurrence. Finally, the Scheduler class organizes these tasks into a daily plan based on available time and priority. I separated these responsibilities to keep the system organized and easier to maintain.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.



---

## 2. Scheduling Logic and Tradeoffs

### a. Constraints and priorities

My scheduler considers task priority, duration, preferred time, completion status, and the owner's available time. I decided that priority and available time should matter most because important activities need to be completed even when an owner has a busy schedule. Tasks are sorted by priority, and activities that exceed the remaining available time are skipped.

### b. Tradeoffs

One tradeoff my scheduler makes is prioritizing important tasks over strictly following their preferred times. For example, a high-priority medication task may be scheduled before a lower-priority grooming task, even if grooming has an earlier preferred time. I chose this approach because some pet care activities are more important than others. However, the generated schedule may not always match the exact times requested.
---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
