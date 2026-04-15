import sys

with open('script-enhanced.js', 'r') as f:
    lines = f.readlines()

# We need to change the variable name in the updateDependenciesSelect function from dependencySelect to dependenciesSelect.
# Also, we'll add a function to edit activities.

output_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    
    # Change variable name in updateDependenciesSelect
    if 'dependencySelect.innerHTML' in line:
        line = line.replace('dependencySelect', 'dependenciesSelect')
    if 'dependencySelect.appendChild' in line:
        line = line.replace('dependencySelect', 'dependenciesSelect')
    
    # We also need to update the call to updateDependenciesSelect in removeActivity (line 218)
    # Actually, the line is already updated by our previous script? Let's check later.
    
    # Now, we'll add an edit button and edit function.
    # We'll change the renderActivitiesList to include an edit button.
    # Look for the activity-actions section.
    if '<button class="btn-secondary edit-date-btn" onclick="editActivityDate' in line:
        # We'll change the existing edit-date button to just edit the date, and add a new button for editing the activity details.
        # Actually, we want to allow editing the activity (name, duration, dependencies). We'll add a new button.
        # We'll replace the entire activity-actions div.
        # Let's find the closing of that div.
        # Instead of doing complex string replacement, we'll write a new function for rendering the activity item.
        # But given the time, let's do a simpler approach: we'll add a new button for editing the activity.
        # We'll change the line to include a new button.
        # The current line is:
        # <button class="btn-secondary edit-date-btn" onclick="editActivityDate('${activity.id}')">
        # We'll change the class and onclick to a new function editActivity.
        # Actually, we can keep the date edit button and add another button for editing activity.
        # Let's change the activity-actions div.
        # We'll replace from the line that contains "activity-actions" until the closing div.
        # But note: the activity-actions div is defined in the template string.
        # Instead, we'll change the template string in the renderActivitiesList function.
        # We'll do a targeted replacement of the entire renderActivitiesList function.
        pass
    
    output_lines.append(line)
    i += 1

# Now, let's find the renderActivitiesList function and replace it.
# We'll write a new version of renderActivitiesList that includes an edit button for activity details.

new_render_function = '''    function renderActivitiesList() {
        if (state.activities.length === 0) {
            activitiesContainer.innerHTML = '<p class="empty-message">No activities added yet. Add your first activity above.</p>';
            return;
        }

        activitiesContainer.innerHTML = '';

        state.activities.forEach(activity => {
            const activityElement = document.createElement('div');
            activityElement.className = 'activity-item';
            activityElement.innerHTML = \`
                <div class="activity-info">
                    <h4>\${activity.name}</h4>
                    <p>Duration: \${activity.duration} day\${activity.duration > 1 ? 's' : ''}</p>
                    <p>Dependencies: \${activity.dependencies && activity.dependencies.length > 0 ? activity.dependencies.map(depId => getActivityName(depId)).join(', ') : 'None'}</p>
                    \${activity.startDate ? \`<p>Schedule: \${formatDate(activity.startDate)} - \${formatDate(activity.endDate)}</p>\` : ''}
                </div>
                <div class="activity-actions">
                    <button class="btn-secondary edit-activity-btn" onclick="editActivity('\\\${activity.id}')">
                        <i class="fas fa-edit"></i> Edit
                    </button>
                    <button class="btn-secondary edit-date-btn" onclick="editActivityDate('\\\${activity.id}')">
                        <i class="fas fa-calendar-edit"></i> Edit Date
                    </button>
                    <button class="btn-danger" onclick="removeActivity('\\\${activity.id}')">
                        <i class="fas fa-trash"></i> Remove
                    </button>
                </div>
            \`;
            activitiesContainer.appendChild(activityElement);
        });
    }'''

# Find the start and end of the renderActivitiesList function.
start_line = -1
end_line = -1
brace_count = 0
for i, line in enumerate(lines):
    if 'function renderActivitiesList() {' in line:
        start_line = i
        brace_count = 1
        j = i + 1
        while j < len(lines):
            if '{' in lines[j]:
                brace_count += lines[j].count('{')
            if '}' in lines[j]:
                brace_count -= lines[j].count('}')
            if brace_count == 0:
                end_line = j
                break
            j += 1
        break

if start_line != -1 and end_line != -1:
    # Replace the function
    output_lines = lines[:start_line] + [new_render_function] + lines[end_line+1:]
else:
    print("Could not find renderActivitiesList function")
    sys.exit(1)

# Now, we need to add the editActivity function.
# We'll add it after the editActivityDate function.

# Find the editActivityDate function and insert after it.
for i, line in enumerate(output_lines):
    if 'window.editActivityDate = function(id) {' in line:
        insert_line = i
        # Find the closing brace of the function.
        brace_count = 0
        for j in range(i, len(output_lines)):
            if '{' in output_lines[j]:
                brace_count += 1
            if '}' in output_lines[j]:
                brace_count -= 1
                if brace_count == 0:
                    insert_line = j + 1
                    break
        # Insert the new function after the editActivityDate function.
        new_edit_function = '''
    // Function to edit activity (name, duration, dependencies) (exposed to window)
    window.editActivity = function(id) {
        const activity = state.activities.find(a => a.id === id);
        if (!activity) return;

        // Create a form for editing
        const newName = prompt('Edit activity name:', activity.name);
        if (newName === null) return; // User cancelled

        const newDuration = prompt('Edit duration (days):', activity.duration);
        if (newDuration === null) return;

        const duration = parseInt(newDuration);
        if (isNaN(duration) || duration < 1) {
            alert('Duration must be a positive number');
            return;
        }

        // Show current dependencies and let user edit
        let currentDeps = '';
        if (activity.dependencies && activity.dependencies.length > 0) {
            currentDeps = activity.dependencies.map(depId => getActivityName(depId)).join(', ');
        }
        const depsPrompt = prompt('Edit dependencies (enter activity IDs separated by comma, leave empty for none).\\nCurrent dependencies: ' + currentDeps + '\\nAvailable activities:\\n' + 
            state.activities.filter(a => a.id !== id).map(a => a.id + ': ' + a.name).join('\\n'), 
            activity.dependencies ? activity.dependencies.join(',') : '');
        
        let newDependencies = [];
        if (depsPrompt !== null && depsPrompt.trim() !== '') {
            const depIds = depsPrompt.split(',').map(id => id.trim()).filter(id => id !== '');
            // Validate each ID exists
            for (const depId of depIds) {
                if (!state.activities.find(a => a.id === depId)) {
                    alert('Invalid activity ID: ' + depId);
                    return;
                }
            }
            newDependencies = depIds;
        }

        // Update activity
        activity.name = newName.trim();
        activity.duration = duration;
        activity.dependencies = newDependencies;

        // If the activity is scheduled, we need to reschedule
        // For now, we'll remove the schedule and let the user regenerate
        // Remove from schedule
        state.schedule = state.schedule.filter(a => a.id !== id);
        activity.startDate = null;
        activity.endDate = null;

        // Update UI
        renderActivitiesList();
        updateDependenciesSelect();
        renderScheduleTimeline();
        renderCalendar();
    };
'''
        output_lines = output_lines[:insert_line] + [new_edit_function] + output_lines[insert_line:]
        break

# Write the updated file
with open('script-enhanced.js', 'w') as f:
    f.writelines(output_lines)

print("Updated renderActivitiesList and added editActivity function")
