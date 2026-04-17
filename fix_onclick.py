import re

with open('script-enhanced.js', 'r') as f:
    lines = f.readlines()

# We'll find the renderActivitiesList function and fix the onclick strings.
in_render = False
in_function = False
brace_count = 0
output_lines = []

for i, line in enumerate(lines):
    if 'function renderActivitiesList()' in line:
        in_render = True
        output_lines.append(line)
        continue

    if in_render:
        # We'll look for the lines that contain the onclick strings and replace them.
        # We'll do a simple string replacement for the three buttons.
        if 'onclick="editActivity' in line:
            # Fix the editActivity onclick
            line = re.sub(r'onclick="editActivity\\(\\\\\'\\\' + activity\.id + \\\\\'\\\'\\)"', 'onclick="editActivity(\\'' + activity.id + '\\')"', line)
            # Actually, the pattern is messy. Let's just rewrite the whole line.
            # We'll replace the entire button HTML with correct concatenation.
            # But we need to be careful because the line is part of a larger string building.
            # Instead, let's replace the whole function with a corrected version.
            pass
        output_lines.append(line)
        if line.strip() == '}':
            in_render = False
    else:
        output_lines.append(line)

# Instead of trying to patch, let's rewrite the renderActivitiesList function completely.
# We'll read the file as a string and replace the entire function.
with open('script-enhanced.js', 'r') as f:
    content = f.read()

# Define the corrected function
corrected_render = '''function renderActivitiesList() {
        if (state.activities.length === 0) {
            activitiesContainer.innerHTML = '<p class="empty-message">No activities added yet. Add your first activity above.</p>';
            return;
        }

        activitiesContainer.innerHTML = '';

        state.activities.forEach(activity => {
            const activityElement = document.createElement('div');
            activityElement.className = 'activity-item';
            
            // Build HTML string using concatenation
            let html = '';
            html += '<div class="activity-info">';
            html += '<h4>' + escapeHtml(activity.name) + '</h4>';
            html += '<p>Duration: ' + activity.duration + ' day' + (activity.duration > 1 ? 's' : '') + '</p>';
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

# But wait, the onclick strings are still using double backslashes. Let's write them correctly:
# We want to generate: onclick="editActivity('123')"
# In a JavaScript string, we need to escape the backslashes and quotes appropriately.
# Let's write the function with proper escaping.

# Actually, we are writing the function as a string in Python. We need to escape for Python.
# Let's do it step by step: the HTML we want is:
#   <button onclick="editActivity('123')">
# In JavaScript string, we write: '<button onclick="editActivity(\\'123\\')">'
# Because we need to escape the single quotes inside the double-quoted string.

# So in the JavaScript function, we need to concatenate:
#   'onclick="editActivity(\\'' + activity.id + '\\')"'

# Let's write the corrected function with proper escaping for Python string.

corrected_render = '''function renderActivitiesList() {
        if (state.activities.length === 0) {
            activitiesContainer.innerHTML = '<p class="empty-message">No activities added yet. Add your first activity above.</p>';
            return;
        }

        activitiesContainer.innerHTML = '';

        state.activities.forEach(activity => {
            const activityElement = document.createElement('div');
            activityElement.className = 'activity-item';
            
            // Build HTML string using concatenation
            let html = '';
            html += '<div class="activity-info">';
            html += '<h4>' + escapeHtml(activity.name) + '</h4>';
            html += '<p>Duration: ' + activity.duration + ' day' + (activity.duration > 1 ? 's' : '') + '</p>';
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

# But note: the above string is in Python, and we are writing it to a file. The backslashes are escaped for Python.
# When written to the file, it will be as we want.

# Now replace the function in the content.
import re
pattern = r'function renderActivitiesList\(\) \{[\s\S]*?\n    \}'
content = re.sub(pattern, corrected_render, content, flags=re.DOTALL)

# Write back
with open('script-enhanced.js', 'w') as f:
    f.write(content)

print('Fixed renderActivitiesList function with correct onclick strings.')
