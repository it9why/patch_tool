import re

with open('script-enhanced.js', 'r') as f:
    content = f.read()

# The issue is that the single quotes in the onclick strings are not properly escaped.
# We need to replace:
#   onclick="editActivity('' + activity.id + '')" 
# with:
#   onclick="editActivity(\'' + activity.id + '\')"
# But note that the string is built with concatenation: 
#   'onclick="editActivity(\'' + activity.id + '\')"'
# In the file, the backslashes are escaped, so we look for: 
#   onclick="editActivity('' + activity.id + '')"
# which is missing the backslashes.

# We'll fix the three buttons in the renderActivitiesList function.

# First, let's locate the renderActivitiesList function.
# We'll replace the entire function with a corrected version.
# We'll write a corrected version of the function.

corrected_render = '''    function renderActivitiesList() {
        // Get the selected type filter
        const selectedType = typeFilterSelect.value;
        
        // Filter activities by type if a type is selected
        let activitiesToShow = state.activities;
        if (selectedType) {
            activitiesToShow = state.activities.filter(a => (a.type || 'Default') === selectedType);
        }

        if (activitiesToShow.length === 0) {
            activitiesContainer.innerHTML = '<p class="empty-message">No activities ' + (selectedType ? 'of type "' + selectedType + '" ' : '') + 'added yet. Add your first activity above.</p>';
            return;
        }

        activitiesContainer.innerHTML = '';

        activitiesToShow.forEach(activity => {
            const activityElement = document.createElement('div');
            activityElement.className = 'activity-item';
            
            // Build HTML string using concatenation
            let html = '';
            html += '<div class="activity-info">';
            html += '<h4>' + escapeHtml(activity.name) + '</h4>';
            html += '<p>Duration: ' + activity.duration + ' day' + (activity.duration > 1 ? 's' : '') + '</p>';
            html += '<p>Type: ' + escapeHtml(activity.type || 'Default') + '</p>';
            let depsText = 'None';
            if (activity.dependencies && activity.dependencies.length > 0) {
                depsText = activity.dependencies.map(depId => escapeHtml(getActivityName(depId))).join(', ');
            }
            html += '<p>Dependencies: ' + depsText + '</p>';
            if (activity.startDate) {
                html += '<p>Schedule: ' + formatDate(activity.startDate) + ' - ' + formatDate(activity.endDate) + '</p>';
            }
            html += '</div>';
            html += '<div class="activity-actions">';
            html += '<button class="btn-secondary edit-activity-btn" onclick="editActivity(\\'' + activity.id + '\\')">';
            html += '<i class="fas fa-edit"></i> Edit';
            html += '</button>';
            html += '<button class="btn-secondary edit-date-btn" onclick="editActivityDate(\\'' + activity.id + '\\')">';
            html += '<i class="fas fa-calendar-edit"></i> Edit Date';
            html += '</button>';
            html += '<button class="btn-danger" onclick="removeActivity(\\'' + activity.id + '\\')">';
            html += '<i class="fas fa-trash"></i> Remove';
            html += '</button>';
            html += '</div>';
            
            activityElement.innerHTML = html;
            activitiesContainer.appendChild(activityElement);
        });
    }'''

# Now replace the existing function with the corrected one.
# We'll use a regex to find the function definition and replace it.
pattern = r'function renderActivitiesList\(\) \{[\s\S]*?\n    \}'
content = re.sub(pattern, corrected_render, content, flags=re.DOTALL)

# Write the fixed content back
with open('script-enhanced.js', 'w') as f:
    f.write(content)

print('Fixed onclick strings in renderActivitiesList function.')
