import sys

with open('script-enhanced.js', 'r') as f:
    content = f.read()

# We'll replace the entire renderActivitiesList function with a corrected version.
# First, find the function definition and the end of the function.
# The function is defined as: function renderActivitiesList(filterType = '') {
# We'll use a regex that captures until the closing brace that matches the function's opening.

import re

# Pattern to match the function (non-greedy until the closing brace of the function)
# We need to account for nested braces (like the forEach callback). We'll use a simple stack counter.
# We'll find the function start and then count braces until we reach the matching closing brace.

lines = content.splitlines()
new_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    # Check if this line starts the function (note: there might be spaces)
    if line.strip().startswith('function renderActivitiesList'):
        # We'll replace from this line until the matching closing brace.
        # Let's collect the lines and count braces.
        func_lines = []
        brace_count = 0
        j = i
        while j < len(lines):
            func_lines.append(lines[j])
            # Count opening and closing braces in this line
            brace_count += lines[j].count('{')
            brace_count -= lines[j].count('}')
            if brace_count == 0:
                # We've reached the end of the function
                break
            j += 1
        # Now we have the function lines in func_lines (from i to j inclusive).
        # We'll replace this block with a corrected version.
        # Build the corrected function.
        corrected_func = '''    // Modified renderActivitiesList to accept filter type
    function renderActivitiesList(filterType = '') {
        if (state.activities.length === 0) {
            activitiesContainer.innerHTML = '<p class="empty-message">No activities added yet. Add your first activity above.</p>';
            return;
        }

        // Filter activities if a type is selected
        const activitiesToShow = filterType ? 
            state.activities.filter(activity => (activity.type || 'Default') === filterType) : 
            state.activities;

        if (activitiesToShow.length === 0) {
            activitiesContainer.innerHTML = `<p class="empty-message">No activities of type "\${filterType}" found.</p>`;
            return;
        }

        activitiesContainer.innerHTML = '';

        activitiesToShow.forEach(activity => {
            const activityElement = document.createElement('div');
            activityElement.className = 'activity-item';
            activityElement.innerHTML = `
                <div class="activity-info">
                    <h4>\${activity.name}</h4>
                    <p>Duration: \${activity.duration} day\${activity.duration > 1 ? 's' : ''}</p>
                    <p>Type: \${activity.type}</p>
                    <p>Dependencies: \${activity.dependencies && activity.dependencies.length > 0 ? activity.dependencies.map(depId => getActivityName(depId)).join(', ') : 'None'}</p>
                    \${activity.startDate ? '<p>Schedule: ' + formatDate(activity.startDate) + ' - ' + formatDate(activity.endDate) + '</p>' : ''}
                </div>
                <div class="activity-actions">
                    <button class="btn-secondary edit-activity-btn" onclick="editActivity('\${activity.id}')">
                        <i class="fas fa-edit"></i> Edit
                    </button>
                    <button class="btn-secondary edit-date-btn" onclick="editActivityDate('\${activity.id}')">
                        <i class="fas fa-calendar-edit"></i> Edit Date
                    </button>
                    <button class="btn-danger" onclick="removeActivity('\${activity.id}')">
                        <i class="fas fa-trash"></i> Remove
                    </button>
                </div>
            `;
            activitiesContainer.appendChild(activityElement);
        });
    }'''
        # Append the corrected function
        new_lines.append(corrected_func)
        # Skip the original function lines
        i = j + 1
        continue
    else:
        new_lines.append(line)
        i += 1

# Write back
with open('script-enhanced.js', 'w') as f:
    f.write('\n'.join(new_lines))

print("Replaced renderActivitiesList function with corrected version")
