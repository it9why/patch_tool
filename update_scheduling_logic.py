import sys

with open('script-enhanced.js', 'r') as f:
    lines = f.readlines()

# Find the calculateSchedule function
start = -1
end = -1
brace_count = 0
for i, line in enumerate(lines):
    if 'function calculateSchedule()' in line:
        start = i
        brace_count = 1
        for j in range(i+1, len(lines)):
            if '{' in lines[j]:
                brace_count += 1
            if '}' in lines[j]:
                brace_count -= 1
                if brace_count == 0:
                    end = j
                    break
        break

if start == -1 or end == -1:
    print("Could not find calculateSchedule function")
    sys.exit(1)

# Build the new function content
new_calculate = '''    // Function to calculate schedule considering dependencies, holidays, and types
    function calculateSchedule() {
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

        // Track the next available date for each type
        const typeNextAvailable = {};

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

            // Update next available date for this activity's type
            const type = activity.type || 'Default';
            typeNextAvailable[type] = currentDate.plus({ days: 1 });

            return currentDate.plus({ days: 1 });
        };

        // Separate activities with manually set dates
        const manuallyScheduled = activitiesToSchedule.filter(a => a.startDate !== null);
        const toAutoSchedule = activitiesToSchedule.filter(a => a.startDate === null);

        // Add manually scheduled activities to schedule
        manuallyScheduled.forEach(activity => {
            scheduledActivities.add(activity.id);
            state.schedule.push({ ...activity });
            // Update type next available date for manually scheduled activities
            const type = activity.type || 'Default';
            if (activity.endDate) {
                const nextAvail = activity.endDate.plus({ days: 1 });
                if (!typeNextAvailable[type] || DateTime.isAfter(nextAvail, typeNextAvailable[type])) {
                    typeNextAvailable[type] = nextAvail;
                }
            }
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
                    // Determine start date based on type and dependencies
                    let startDate = state.startDate;
                    const type = activity.type || 'Default';
                    
                    // Consider type's next available date
                    if (typeNextAvailable[type]) {
                        startDate = DateTime.isAfter(typeNextAvailable[type], startDate) 
                            ? typeNextAvailable[type] 
                            : startDate;
                    }
                    
                    // Consider dependencies' end dates
                    if (activity.dependencies && activity.dependencies.length > 0) {
                        activity.dependencies.forEach(depId => {
                            const dep = state.activities.find(a => a.id === depId);
                            if (dep && dep.endDate) {
                                if (DateTime.isAfter(dep.endDate, startDate)) {
                                    startDate = dep.endDate;
                                }
                            }
                        });
                    }
                    
                    // Schedule the activity
                    scheduleActivity(activity, startDate);
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
        state.schedule.sort((a, b) => a.startDate.valueOf() - b.startDate.valueOf());

        // Update UI
        renderScheduleTimeline();
        renderCalendar();
    }'''

# Replace the old function with the new one
lines = lines[:start] + [new_calculate] + lines[end+1:]

# Write back
with open('script-enhanced.js', 'w') as f:
    f.writelines(lines)

print("Updated scheduling logic to support concurrency by type")
