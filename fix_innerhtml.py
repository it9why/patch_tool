import re

with open('script-enhanced.js', 'r') as f:
    content = f.read()

# Replace the template literal for the empty message (line 150)
# We'll change:
# activitiesContainer.innerHTML = `<p class="empty-message">No activities of type "${filterType}" found.</p>`;
# to:
# activitiesContainer.innerHTML = '<p class="empty-message">No activities of type "' + filterType + '" found.</p>';
content = re.sub(
    r'activitiesContainer\.innerHTML = `<p class="empty-message">No activities of type "\$\{filterType\}" found\.</p>`;',
    r'activitiesContainer.innerHTML = \'<p class="empty-message">No activities of type "\' + filterType + \'" found.</p>\';',
    content
)

# Now replace the big template literal for each activity.
# We'll find the function renderActivitiesList and replace the innerHTML assignment.
# We'll do a more targeted replacement: from "activityElement.innerHTML = `" to the matching backtick.
# We'll capture the whole function and replace that part.
# But easier: we can replace the whole function with a new one.
# Let's extract the function body from line 138 to the closing brace (line 180?).
# We'll write a new function using string concatenation.

new_function = '''    function renderActivitiesList(filterType = '') {
        if (state.activities.length === 0) {
            activitiesContainer.innerHTML = '<p class="empty-message">No activities added yet. Add your first activity above.</p>';
            return;
        }

        // Filter activities if a type is selected
        const activitiesToShow = filterType ?
            state.activities.filter(activity => (activity.type || 'Default') === filterType) :
            state.activities;

        if (activitiesToShow.length === 0) {
            activitiesContainer.innerHTML = '<p class="empty-message">No activities of type "' + filterType + '" found.</p>';
            return;
        }

        activitiesContainer.innerHTML = '';

        activitiesToShow.forEach(activity => {
            const activityElement = document.createElement('div');
            activityElement.className = 'activity-item';
            
            // Build the HTML string using concatenation to avoid template literal issues
            let html = '';
            html += '<div class="activity-info">';
            html += '<h4>' + escapeHtml(activity.name) + '</h4>';
            html += '<p>Duration: ' + activity.duration + ' day' + (activity.duration > 1 ? 's' : '') + '</p>';
            html += '<p>Type: ' + escapeHtml(activity.type) + '</p>';
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

# We need to define escapeHtml function if not present. Let's add it at the top of the script.
# But we can add it inside the same closure. Let's find where we can insert it.
# We'll add it after the other helper functions, e.g., after formatDate.
# For now, let's just use a simple escape function and hope it's not needed for other parts.
# We'll add a helper function at the beginning of the script (inside the DOMContentLoaded event listener).
# Let's find the position after the formatDate function.

# First, replace the function in the content.
# We'll use a regex to find the entire renderActivitiesList function and replace it.
pattern = r'function renderActivitiesList\(filterType = \'\'\) \{[\s\S]*?\n    \}'
match = re.search(pattern, content)
if match:
    content = content[:match.start()] + new_function + content[match.end():]
    print('Replaced renderActivitiesList function')
else:
    print('Could not find renderActivitiesList function')
    # Fallback: find the function by line numbers? Not reliable.

# Also need to add escapeHtml function.
# Find a good place to insert: after the formatDate function.
# Look for "function formatDate(" and then the next function definition.
# We'll insert after the closing brace of formatDate.
format_date_pattern = r'function formatDate\(dateObj\) \{[\s\S]*?\n    \}'
match2 = re.search(format_date_pattern, content)
if match2:
    escape_func = '''
    // Helper to escape HTML special characters
    function escapeHtml(text) {
        if (typeof text !== 'string') return text;
        return text
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }'''
    content = content[:match2.end()] + escape_func + content[match2.end():]
    print('Added escapeHtml function')
else:
    print('Could not find formatDate function')

with open('script-enhanced.js', 'w') as f:
    f.write(content)

