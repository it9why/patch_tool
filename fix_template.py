import sys

with open('script-enhanced.js', 'r') as f:
    content = f.read()

# We'll replace the entire renderActivitiesList function with a version that uses correct template literals.
# Use triple quotes for the multi-line string and escape backticks and dollar signs appropriately.

new_render = '''    // Enhanced function to render activities list with edit buttons
    function renderActivitiesList() {
        if (state.activities.length === 0) {
            activitiesContainer.innerHTML = '<p class="empty-message">No activities added yet. Add your first activity above.</p>';
            return;
        }

        activitiesContainer.innerHTML = '';

        state.activities.forEach(activity => {
            const activityElement = document.createElement('div');
            activityElement.className = 'activity-item';
            activityElement.innerHTML = `
                <div class="activity-info">
                    <h4>${activity.name}</h4>
                    <p>Duration: ${activity.duration} day${activity.duration > 1 ? 's' : ''}</p>
                    <p>Dependencies: ${activity.dependencies && activity.dependencies.length > 0 ? activity.dependencies.map(depId => getActivityName(depId)).join(', ') : 'None'}</p>
                    ${activity.startDate ? `<p>Schedule: ${formatDate(activity.startDate)} - ${formatDate(activity.endDate)}</p>` : ''}
                </div>
                <div class="activity-actions">
                    <button class="btn-secondary edit-activity-btn" onclick="editActivity('${activity.id}')">
                        <i class="fas fa-edit"></i> Edit
                    </button>
                    <button class="btn-secondary edit-date-btn" onclick="editActivityDate('${activity.id}')">
                        <i class="fas fa-calendar-edit"></i> Edit Date
                    </button>
                    <button class="btn-danger" onclick="removeActivity('${activity.id}')">
                        <i class="fas fa-trash"></i> Remove
                    </button>
                </div>
            `;
            activitiesContainer.appendChild(activityElement);
        });
    }'''

# Now we need to find and replace the function.
# We'll use a simple regex to find the function and replace it.
import re
pattern = r'function renderActivitiesList\(\) \{.*?\n    \}'
# Use DOTALL to match across lines.
pattern = re.compile(r'function renderActivitiesList\(\) \{.*?\n    \}', re.DOTALL)

# Replace the function
new_content = re.sub(pattern, new_render, content)

with open('script-enhanced.js', 'w') as f:
    f.write(new_content)

print("Fixed template literals in renderActivitiesList")
