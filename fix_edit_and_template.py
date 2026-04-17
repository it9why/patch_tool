import re

with open('script-enhanced.js', 'r') as f:
    content = f.read()

# 1. Fix renderActivitiesList to use string concatenation and add an Edit button.
# We'll replace the template literal with concatenation and add an Edit button.

# First, find the renderActivitiesList function.
# We'll use a regex to capture the function and then replace the inner HTML part.
renderActivitiesList_pattern = r'(function renderActivitiesList\(\) \{[\s\S]*?\n    \})'
def replace_renderActivitiesList(match):
    func = match.group(0)
    # Replace the innerHTML assignment with concatenated string.
    # We'll break the HTML into multiple lines for readability.
    new_func = '''function renderActivitiesList() {
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
    return new_func

content = re.sub(renderActivitiesList_pattern, replace_renderActivitiesList, content, flags=re.DOTALL)

# 2. Fix renderScheduleTimeline to use string concatenation.
renderScheduleTimeline_pattern = r'(function renderScheduleTimeline\(\) \{[\s\S]*?\n    \})'
def replace_renderScheduleTimeline(match):
    func = match.group(0)
    new_func = '''function renderScheduleTimeline() {
        if (state.schedule.length === 0) {
            scheduleTimelineElement.innerHTML = '<p class="empty-message">No schedule generated yet. Add activities and click "Generate Schedule".</p>';
            return;
        }

        scheduleTimelineElement.innerHTML = '';

        state.schedule.forEach(activity => {
            const timelineItem = document.createElement('div');
            timelineItem.className = 'timeline-item';
            
            const startDateStr = activity.startDate ? activity.startDate.toLocaleString() : 'Not scheduled';
            const endDateStr = activity.endDate ? activity.endDate.toLocaleString() : 'Not scheduled';
            
            let timelineHTML = '';
            timelineHTML += '<div>';
            timelineHTML += '<h4>' + escapeHtml(activity.name) + '</h4>';
            timelineHTML += '<p>Duration: ' + activity.duration + ' day' + (activity.duration > 1 ? 's' : '') + '</p>';
            if (activity.dependency) {
                timelineHTML += '<p>Depends on: ' + escapeHtml(getActivityName(activity.dependency)) + '</p>';
            }
            timelineHTML += '</div>';
            timelineHTML += '<div class="timeline-dates">';
            timelineHTML += escapeHtml(startDateStr) + ' - ' + escapeHtml(endDateStr);
            timelineHTML += '</div>';
            timelineItem.innerHTML = timelineHTML;
            
            scheduleTimelineElement.appendChild(timelineItem);
        });
    }'''
    return new_func

content = re.sub(renderScheduleTimeline_pattern, replace_renderScheduleTimeline, content, flags=re.DOTALL)

# 3. Add the missing editActivity function (if not present).
if 'window.editActivity = function' not in content:
    # We'll insert it after the editActivityDate function.
    # Find the editActivityDate function and then add editActivity after it.
    editActivityDate_pattern = r'(window\.editActivityDate = function\(id\) \{[\s\S]*?\n    \})'
    def add_editActivity_after(match):
        editActivityDate_func = match.group(0)
        editActivity_func = '''
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
    }'''
        return editActivityDate_func + editActivity_func
    content = re.sub(editActivityDate_pattern, add_editActivity_after, content, flags=re.DOTALL)

# 4. Add the escapeHtml helper function if not present.
if 'function escapeHtml' not in content:
    # Find a good place to insert it, perhaps after formatDate function.
    formatDate_pattern = r'(function formatDate\(dateObj\) \{[\s\S]*?\n    \})'
    escapeHtml_func = '''
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
    def insert_after_formatDate(match):
        return match.group(0) + escapeHtml_func
    content = re.sub(formatDate_pattern, insert_after_formatDate, content, flags=re.DOTALL)

# Write the fixed content back
with open('script-enhanced.js', 'w') as f:
    f.write(content)

print('Fixed renderActivitiesList, renderScheduleTimeline, added editActivity and escapeHtml.')
