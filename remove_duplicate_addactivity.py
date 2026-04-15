import sys

with open('script-enhanced.js', 'r') as f:
    lines = f.readlines()

# Find the start and end of the window.addActivity function.
start = None
end = None
brace_count = 0
for i, line in enumerate(lines):
    if 'window.addActivity = function(event)' in line:
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

if start is None or end is None:
    print("Could not find window.addActivity function")
    sys.exit(1)

# Now we see that after the function ends, there is duplicate code starting at line 148 (the second "if (duration < 1) {").
# Let's examine lines from start to end and see if there is duplicate inside.
# Actually, the function appears to have duplicate body. We'll replace the entire function with a clean version.

clean_function = '''    window.addActivity = function(event) {
        if (event) event.preventDefault();
        console.log("addActivity function called");
        const name = activityNameInput.value.trim();
        const duration = parseInt(durationInput.value);
        const dependencies = Array.from(dependenciesSelect.selectedOptions).map(option => option.value);

        if (!name) {
            alert('Please enter an activity name');
            return;
        }

        if (duration < 1) {
            alert('Duration must be at least 1 day');
            return;
        }

        // Create activity object
        const activity = {
            id: generateId(),
            name,
            duration,
            dependencies: dependencies,
            startDate: null,
            endDate: null
        };

        // Add to state
        state.activities.push(activity);

        // Clear inputs
        activityNameInput.value = '';
        durationInput.value = '1';

        // Clear dependencies selection
        dependenciesSelect.selectedIndex = -1;

        // Update UI
        renderActivitiesList();
        updateDependenciesSelect();

        console.log('Activity added:', activity);
        alert("Activity added successfully!");
    }'''

# Replace the function
lines = lines[:start] + [clean_function + '\n'] + lines[end+1:]

# Write back
with open('script-enhanced.js', 'w') as f:
    f.writelines(lines)

print("Replaced duplicate addActivity function with clean version")
