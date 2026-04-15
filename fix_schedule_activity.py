import sys

with open('script-enhanced.js', 'r') as f:
    content = f.read()

# Replace the scheduleActivity function to use adjusted start date
new_schedule_activity = '''        // Function to schedule an activity
        const scheduleActivity = (activity, startDate) => {
            let currentDate = startDate;
            let daysScheduled = 0;

            // Skip non-working days before starting the activity
            while (!isWorkingDay(currentDate)) {
                currentDate = currentDate.plus({ days: 1 });
            }
            const actualStartDate = currentDate;

            while (daysScheduled < activity.duration) {
                // Skip weekends and holidays (should already be skipped, but keep as safety)
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

            activity.startDate = actualStartDate;
            activity.endDate = currentDate;
            scheduledActivities.add(activity.id);
            state.schedule.push({ ...activity });

            // Return the next day after the end date
            return currentDate.plus({ days: 1 });
        };'''

# Find the scheduleActivity function and replace it.
import re
# Pattern to match the scheduleActivity function definition and its body up to the closing brace and semicolon.
# We'll use a more robust pattern that matches from 'const scheduleActivity = (activity, startDate) => {' 
# until we see a line that ends with '};' (the end of the function).
# Since the function is defined inside calculateSchedule, we can't easily use regex. Let's instead find the function's start and end within calculateSchedule.

# We'll find the calculateSchedule function and then replace within it.
# Let's do a simpler approach: replace the entire calculateSchedule function with a corrected version.
# First, let's read the current calculateSchedule function lines.

lines = content.splitlines()
in_calc = False
calc_start = -1
calc_end = -1
brace_count = 0
for i, line in enumerate(lines):
    if 'function calculateSchedule() {' in line:
        in_calc = True
        calc_start = i
        brace_count = 1
    elif in_calc:
        if '{' in line:
            brace_count += line.count('{')
        if '}' in line:
            brace_count -= line.count('}')
            if brace_count == 0:
                calc_end = i
                break

if calc_start == -1 or calc_end == -1:
    print("Could not find calculateSchedule function")
    sys.exit(1)

# Build the new calculateSchedule function with the corrected scheduleActivity.
# We'll take the original lines and replace the scheduleActivity part.
# Let's extract the function and modify it with string replacement.

# We'll create a new calculateSchedule function by replacing the scheduleActivity block.
calc_lines = lines[calc_start:calc_end+1]
calc_content = '\n'.join(calc_lines)

# Replace the old scheduleActivity function with the new one.
# The old scheduleActivity function is from the line containing 'const scheduleActivity = (activity, startDate) => {' 
# to the line containing '};' that ends the function.
# We'll use a regex to replace that block.
old_pattern = r'const scheduleActivity = \(activity, startDate\) => \{.*?\n\s*return currentDate\.plus\(\{ days: 1 \}\);\s*\n\s*\};'
new_calc_content = re.sub(old_pattern, new_schedule_activity, calc_content, flags=re.DOTALL)

# Also, there might be multiple occurrences of 'toMillis' but we already replaced one. Let's also change any other occurrences.
new_calc_content = new_calc_content.replace('toMillis()', 'valueOf()')

# Replace the old calculateSchedule function in the original content.
new_lines = lines[:calc_start] + new_calc_content.splitlines() + lines[calc_end+1:]
new_content = '\n'.join(new_lines)

with open('script-enhanced.js', 'w') as f:
    f.write(new_content)

print("Fixed scheduleActivity function and replaced toMillis with valueOf")
