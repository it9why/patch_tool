import sys

with open('script-enhanced.js', 'r') as f:
    lines = f.readlines()

# Find the function addActivity
in_function = False
for i, line in enumerate(lines):
    if 'function addActivity(event)' in line:
        in_function = True
        start = i
    if in_function and line.strip() == '}':
        end = i
        break

# Reconstruct the function with proper formatting
if in_function:
    # We'll replace from start to end with a properly formatted version
    new_function = '''    function addActivity(event) {
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
    }'''

    lines = lines[:start] + [new_function] + lines[end+1:]

    with open('script-enhanced.js', 'w') as f:
        f.writelines(lines)
    print("Reformatted addActivity function")
else:
    print("Could not find addActivity function")
