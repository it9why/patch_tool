import sys

with open('script-enhanced.js', 'r') as f:
    content = f.read()

# Replace the calculateSchedule function with one that handles multiple dependencies.
new_calculate_schedule = '''    function calculateSchedule() {
        // Clear existing schedule
        state.schedule = [];

        // Create a copy of activities to process
        const activitiesToSchedule = [...state.activities];
        const scheduledActivities = new Set();

        // Initialize all activities
        activitiesToSchedule.forEach(activity => {
            // Only reset dates if they weren't manually set
            if (!activity.startDate) {
                activity.startDate = null;
                activity.endDate = null;
            }
        });

        // Function to schedule an activity
        const scheduleActivity = (activity, startDate) => {
            let currentDate = startDate;
            let daysScheduled = 0;

            while (daysScheduled < activity.duration) {
                // Skip weekends and holidays
                if (!isWorkingDay(currentDate)) {
                    currentDate = currentDate.plus({ days: 1 });
                    continue;
                }

                daysScheduled++;
                if (daysScheduled === activity.duration) {
                    break;
                }
                currentDate = currentDate.plus({ days: 1 });
            }

            activity.startDate = startDate;
            activity.endDate = currentDate;
            scheduledActivities.add(activity.id);
            state.schedule.push({ ...activity });

            return currentDate.plus({ days: 1 }); // Next available date
        };

        // Separate activities with manually set dates
        const manuallyScheduled = activitiesToSchedule.filter(a => a.startDate !== null);
        const toAutoSchedule = activitiesToSchedule.filter(a => a.startDate === null);

        // Add manually scheduled activities to schedule
        manuallyScheduled.forEach(activity => {
            scheduledActivities.add(activity.id);
            state.schedule.push({ ...activity });
        });

        // Helper to check if all dependencies are scheduled
        const allDependenciesScheduled = (activity) => {
            // If no dependencies, return true
            if (!activity.dependencies || activity.dependencies.length === 0) {
                return true;
            }
            // Check that every dependency is in scheduledActivities
            return activity.dependencies.every(depId => scheduledActivities.has(depId));
        };

        // Find activities with no dependencies to start
        let availableActivities = toAutoSchedule.filter(a => allDependenciesScheduled(a));
        let currentDate = state.startDate;

        while (availableActivities.length > 0) {
            // Sort by duration (shortest first) for better scheduling
            availableActivities.sort((a, b) => a.duration - b.duration);

            // Schedule all available activities
            for (const activity of availableActivities) {
                if (!scheduledActivities.has(activity.id)) {
                    currentDate = scheduleActivity(activity, currentDate);
                }
            }

            // Update available activities: those not scheduled and whose dependencies are all scheduled
            availableActivities = toAutoSchedule.filter(a =>
                !scheduledActivities.has(a.id) && allDependenciesScheduled(a)
            );
        }

        // Check for circular dependencies (unscheduled activities remaining)
        const unscheduled = toAutoSchedule.filter(a => !scheduledActivities.has(a.id));
        if (unscheduled.length > 0) {
            console.warn('Unscheduled activities (possible circular dependency):', unscheduled);
        }

        // Sort schedule by start date
        state.schedule.sort((a, b) => a.startDate.toMillis() - b.startDate.toMillis());

        // Update UI
        renderScheduleTimeline();
        renderCalendar();
    }'''

# Find the start and end of the calculateSchedule function.
import re
pattern = r'function calculateSchedule\(\) \{.*?\n    \}'
# We'll use a more robust method: find the function and then match braces.
lines = content.splitlines()
in_function = False
brace_count = 0
start_line = -1
for i, line in enumerate(lines):
    if 'function calculateSchedule() {' in line:
        start_line = i
        in_function = True
        brace_count = 1
    elif in_function:
        if '{' in line:
            brace_count += line.count('{')
        if '}' in line:
            brace_count -= line.count('}')
        if brace_count == 0:
            end_line = i
            break

if start_line != -1 and end_line != -1:
    # Replace the function
    new_lines = lines[:start_line] + new_calculate_schedule.splitlines() + lines[end_line+1:]
    new_content = '\n'.join(new_lines)
else:
    print("Could not find calculateSchedule function")
    sys.exit(1)

with open('script-enhanced.js', 'w') as f:
    f.write(new_content)

print("Updated calculateSchedule function")
