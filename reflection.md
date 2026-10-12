# PawPal+ Project Reflection

## 1. System Design

**Three core actions users should be able to perform:**

1. Add a pet by entering its name, species, and other basic details.
2. Create care tasks such as feeding, walking, and administering medication.
3. Generate a daily schedule that organizes tasks based on priority, duration, and available time.

### a. Initial Design

My initial UML design consisted of four classes: Owner, Pet, Task, and Scheduler. The Owner class stores information about the pet owner and manages their pets. The Pet class stores details about each pet and its assigned care tasks. The Task class represents activities such as feeding, walking, and medication, including their duration, priority, and recurrence. Finally, the Scheduler class organizes these tasks into a daily plan based on available time and priority.

I separated these responsibilities because I wanted each class to have a clear purpose. This also made it easier to understand how the different parts of the application would communicate before I started writing the actual code.

### b. Design Changes

My design changed as I started implementing the scheduling logic. Initially, I planned for the Scheduler to receive a list of tasks directly. However, I realized it made more sense for the Scheduler to receive an Owner object and retrieve tasks from all the pets registered under that owner.

This made the relationship between my classes clearer and prevented me from maintaining separate copies of the same tasks.

I also introduced a due date attribute to the Task class when implementing recurring tasks. Originally, I only had a preferred time, but that wasn't enough to distinguish between today's tasks and tasks scheduled for future dates.

These changes helped make the system more organized and better suited for the additional features I implemented.

---

## 2. Scheduling Logic and Tradeoffs

### a. Constraints and Priorities

My scheduler considers task priority, duration, preferred time, completion status, due date, and the owner's available time.

I decided that priority and available time should matter most because some pet care activities are more important than others. For example, medication or feeding might need more attention than grooming, especially when an owner has limited time.

The scheduler organizes tasks by priority, using preferred times to break ties between tasks with the same priority. It also skips tasks that exceed the remaining available time and excludes activities that have already been completed.

### b. Tradeoffs

One tradeoff my scheduler makes is prioritizing important tasks over strictly following their preferred times.

For example, a high-priority medication task may be scheduled before a lower-priority grooming task, even if grooming has an earlier preferred time.

I chose this approach because I wanted the system to focus on getting important activities completed first. However, this also means the generated schedule might not always match the exact preferred times.

Another tradeoff was choosing a straightforward scheduling algorithm instead of implementing a more complicated optimization system. While a more advanced algorithm could produce better schedules, I felt the simpler approach was easier to understand, test, and maintain within the project's timeframe.

---

## 3. AI Collaboration

### a. How I Used AI

I used ChatGPT throughout the development process as a coding assistant, particularly for brainstorming, system architecture, implementing Python classes, writing scheduling algorithms, debugging, and generating automated tests.

One of the most useful parts was using AI to translate my UML design into Python class structures. It helped me understand how the Owner, Pet, Task, and Scheduler classes could work together.

AI was also useful when implementing recurring tasks and conflict detection. For example, I used it to understand how Python's `timedelta` could calculate the next occurrence of a daily or weekly task.

The most helpful prompts were the ones where I provided my existing code and asked AI to improve a specific part of the application while preserving what was already working.

I also found it helpful to work through the project in separate phases. Keeping the conversations focused on design, implementation, algorithms, and testing made it easier to understand what I was working on instead of trying to solve everything at once.

### b. Judgment and Verification

One important decision I made was changing how the Scheduler accessed tasks. Rather than having it manage a separate list of tasks, I decided it should retrieve them through the Owner object. This helped keep the design cleaner and reduced unnecessary duplication.

I also had to consider how recurring tasks should work. Simply marking a task as completed wasn't enough because daily and weekly activities needed to appear again on future dates. I updated the implementation so that completing a recurring task through the Scheduler creates its next occurrence.

I didn't just assume the AI-generated code worked. I ran the application through the terminal, checked the scheduling output, and used pytest to verify specific behaviors.

For example, I tested whether completing the same recurring task twice would accidentally create duplicate future tasks. This helped me verify that the implementation behaved as expected.

---

## 4. Testing and Verification

### a. What I Tested

I used pytest to create 10 automated tests covering the system's main features and important edge cases.

The tests included task completion, adding tasks to pets, sorting tasks chronologically, filtering tasks by pet, daily and weekly recurrence, overlapping task detection, and scheduling constraints.

I also tested cases where a pet had no tasks, two tasks were scheduled at exactly the same time, and a task required more time than the owner had available.

These tests were important because I wanted to make sure the system worked beyond the examples in my demo. A scheduler might work with a few normal tasks but fail when given conflicting schedules or unusual inputs.

I also used `main.py` to verify the backend through the terminal before connecting everything to the Streamlit interface.

After integrating the UI, I manually tested adding pets, creating tasks, marking activities as completed, and generating daily schedules.

### b. Confidence

I would rate my confidence in the system at **4 out of 5 stars**.

All 10 automated tests passed, and the Streamlit application worked during my manual testing. This gives me confidence that the core classes and scheduling algorithms behave correctly for the scenarios I tested.

However, I know that passing tests doesn't necessarily mean an application is completely free of bugs.

If I had more time, I would test more complicated scenarios, such as handling many pets with overlapping tasks, invalid scheduling inputs, and tasks that extend past midnight.

I would also test what happens when a user closes and reopens the application, since the current system doesn't permanently store data.

---

## 5. Reflection

### a. What Went Well

The part I'm most satisfied with is seeing the entire application come together, from the initial UML diagram to a working Streamlit interface.

At the beginning, the project was mainly a set of requirements and class definitions. By the end, I had a system where users could register pets, create tasks, generate schedules, detect conflicts, and manage recurring activities.

I also liked the CLI-first approach because it allowed me to focus on getting the backend working before worrying about how the interface looked.

Seeing my tests pass and then watching the same functionality work in the browser was probably the most satisfying part of the project.

### b. What I Would Improve

If I had another iteration, the first thing I would improve is how the application stores data. Right now, everything is kept in Streamlit session state, meaning the information isn't permanently saved.

I would consider using SQLite or PostgreSQL to store owners, pets, and tasks so users could return to their schedules later.

I would also improve the scheduling algorithm to handle fixed appointments and automatically resolve conflicts instead of only displaying warnings.

Another improvement would be adding notifications for important activities like medication and feeding. I think reminders would make the application much more useful in a real-world situation.

Finally, I would add the ability to edit or delete existing tasks directly from the interface.

### c. Key Takeaway

My biggest takeaway from this project is that building an application isn't just about writing code. It's also about making good design decisions, understanding how different components interact, and verifying that the system behaves the way it's supposed to.

Working with AI showed me how useful it can be for speeding up development, especially when brainstorming ideas, implementing algorithms, and generating tests. However, I also learned that AI-generated solutions still need to be reviewed and tested.

As the developer, I had to decide how the system should work, which tradeoffs were reasonable, and whether the suggested implementations actually met the project's requirements.

This project helped me better understand object-oriented programming, modular system design, and the importance of testing. Most importantly, it showed me that **AI can help write the code, but I still have to understand the system I'm building and take responsibility for the final result.**