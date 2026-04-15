import sys

with open('script-enhanced.js', 'r') as f:
    lines = f.readlines()

# Find the start and end of the renderActivitiesList function
start = -1
end = -1
brace_count = 0
for i, line in enumerate(lines):
    if 'function renderActivitiesList() {' in line:
        start = i
        brace_count = 1
        j = i + 1
        while j < len(lines) and brace_count > 0:
            if '{' in lines[j]:
                brace_count += 1
            if '}' in lines[j]:
                brace_count -= 1
                if brace_count == 0:
                    end = j
                    break
            j += 1
        break

if start == -1 or end == -1:
    print("Could not find renderActivitiesList function")
    sys.exit(1)

# Replace the function with a corrected version
new_function = '''    // Enhanced function to render activities list with edit buttons
    function renderActivitiesList() {
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
            \`;
            activitiesContainer.appendChild(activityElement);
        });
    }'''

# Replace the function
lines = lines[:start] + [new_function] + lines[end+1:]

# Write back
with open('script-enhanced.js', 'w') as f:
    f.writelines(lines)

print("Fixed renderActivitiesList function syntax")
