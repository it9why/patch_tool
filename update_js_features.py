import sys

with open('script-enhanced.js', 'r') as f:
    content = f.read()

# We'll make several modifications. Let's do them step by step.

# 1. Add new DOM elements for filter and quick delete
# Find the DOM Elements section and add
dom_elements_marker = '// DOM Elements'
if dom_elements_marker in content:
    # Insert after the existing DOM elements
    insert_pos = content.find(dom_elements_marker) + len(dom_elements_marker)
    # Find the next line after the last DOM element (look for the line with 'scheduleTimelineElement')
    # Actually, we can insert after the line that defines scheduleTimelineElement.
    # Let's do a more robust approach: we'll insert after the line with 'scheduleTimelineElement'
    lines = content.splitlines()
    new_lines = []
    for line in lines:
        new_lines.append(line)
        if 'scheduleTimelineElement' in line:
            # Insert our new DOM elements
            new_lines.append('    const typeFilterSelect = document.getElementById(\'typeFilter\');')
            new_lines.append('    const quickDeleteTypeBtn = document.getElementById(\'quickDeleteType\');')
    content = '\n'.join(new_lines)

# 2. Add event listeners for the new elements
# Find the event listeners section and add after the existing listeners
event_listeners_marker = '// Event Listeners'
if event_listeners_marker in content:
    # We'll add after the importFileInput event listener
    lines = content.splitlines()
    new_lines = []
    i = 0
    while i < len(lines):
        new_lines.append(lines[i])
        if 'importFileInput.addEventListener' in lines[i]:
            # Insert our new event listeners
            new_lines.append('    typeFilterSelect.addEventListener(\'change\', filterActivitiesByType);')
            new_lines.append('    quickDeleteTypeBtn.addEventListener(\'click\', deleteActivitiesByType);')
        i += 1
    content = '\n'.join(new_lines)

# 3. Add function to update type filter options (and also update the datalist for suggestions)
# We'll add a new function updateTypeFilterAndSuggestions
new_function = '''
    // Function to update type filter dropdown and suggestions
    function updateTypeFilterAndSuggestions() {
        // Get all unique types from activities
        const types = [...new Set(state.activities.map(a => a.type || \'Default\'))];
        
        // Update filter dropdown
        typeFilterSelect.innerHTML = \'<option value="">All Types</option>\';
        types.forEach(type => {
            const option = document.createElement(\'option\');
            option.value = type;
            option.textContent = type;
            typeFilterSelect.appendChild(option);
        });
        
        // Update datalist for suggestions in the input field
        const datalist = document.getElementById(\'typeOptions\');
        if (datalist) {
            // Clear existing options except the static ones? We'll keep static ones and add dynamic ones.
            // Let's keep the static ones and add only new ones that are not already in static list.
            const staticOptions = [\'Development\', \'Design\', \'Meeting\', \'Testing\', \'Documentation\', \'Other\', \'Default\'];
            const existingOptions = Array.from(datalist.options).map(opt => opt.value);
            const allOptions = [...new Set([...staticOptions, ...types])];
            // Replace datalist content
            datalist.innerHTML = \'\';
            allOptions.forEach(type => {
                const option = document.createElement(\'option\');
                option.value = type;
                datalist.appendChild(option);
            });
        }
    }
'''

# Insert this function after the updateDependenciesSelect function
if 'function updateDependenciesSelect()' in content:
    # Find the end of that function (look for the closing brace)
    lines = content.splitlines()
    new_lines = []
    i = 0
    while i < len(lines):
        new_lines.append(lines[i])
        if 'function updateDependenciesSelect()' in lines[i]:
            # Find the closing brace of this function
            brace_count = 0
            for j in range(i, len(lines)):
                if '{' in lines[j]:
                    brace_count += 1
                if '}' in lines[j]:
                    brace_count -= 1
                    if brace_count == 0:
                        # Insert after this function
                        new_lines.append('\n' + new_function)
                        break
                new_lines.append(lines[j+1] if j+1 < len(lines) else '')
                i += 1
            continue
        i += 1
    content = '\n'.join(new_lines)

# 4. Add function to filter activities by type
filter_function = '''
    // Function to filter activities by selected type
    function filterActivitiesByType() {
        const selectedType = typeFilterSelect.value;
        renderActivitiesList(selectedType);
    }
    
    // Modified renderActivitiesList to accept filter type
    function renderActivitiesList(filterType = \'\') {
        if (state.activities.length === 0) {
            activitiesContainer.innerHTML = \'<p class="empty-message">No activities added yet. Add your first activity above.</p>\';
            return;
        }

        // Filter activities if a type is selected
        const activitiesToShow = filterType ? 
            state.activities.filter(activity => (activity.type || \'Default\') === filterType) : 
            state.activities;

        if (activitiesToShow.length === 0) {
            activitiesContainer.innerHTML = `<p class="empty-message">No activities of type "\${filterType}" found.</p>`;
            return;
        }

        activitiesContainer.innerHTML = \'\';

        activitiesToShow.forEach(activity => {
            const activityElement = document.createElement(\'div\');
            activityElement.className = \'activity-item\';
            activityElement.innerHTML = `
                <div class="activity-info">
                    <h4>\${activity.name}</h4>
                    <p>Duration: \${activity.duration} day\${activity.duration > 1 ? \'s\' : \'\'}</p>
                    <p>Type: \${activity.type}</p>
                    <p>Dependencies: \${activity.dependencies && activity.dependencies.length > 0 ? activity.dependencies.map(depId => getActivityName(depId)).join(\', \') : \'None\'}</p>
                    \${activity.startDate ? `<p>Schedule: \${formatDate(activity.startDate)} - \${formatDate(activity.endDate)}</p>` : \'\'}
                </div>
                <div class="activity-actions">
                    <button class="btn-secondary edit-activity-btn" onclick="editActivity(\'\${activity.id}\')">
                        <i class="fas fa-edit"></i> Edit
                    </button>
                    <button class="btn-secondary edit-date-btn" onclick="editActivityDate(\'\${activity.id}\')">
                        <i class="fas fa-calendar-edit"></i> Edit Date
                    </button>
                    <button class="btn-danger" onclick="removeActivity(\'\${activity.id}\')">
                        <i class="fas fa-trash"></i> Remove
                    </button>
                </div>
            \`;
            activitiesContainer.appendChild(activityElement);
        });
    }
'''

# We need to replace the existing renderActivitiesList function with the new one.
# Let's find the function and replace it.
import re
# Pattern for the original renderActivitiesList function
pattern = r'function renderActivitiesList\(\) \{[\s\S]*?\n    \}'
# Replace with our new function
content = re.sub(pattern, filter_function, content)

# 5. Add function to delete all activities of the selected type
delete_function = '''
    // Function to delete all activities of the selected type
    function deleteActivitiesByType() {
        const selectedType = typeFilterSelect.value;
        if (!selectedType) {
            alert(\'Please select a type to delete.\');
            return;
        }
        
        const activitiesOfType = state.activities.filter(activity => (activity.type || \'Default\') === selectedType);
        if (activitiesOfType.length === 0) {
            alert(`No activities of type "\${selectedType}" found.`);
            return;
        }
        
        if (!confirm(`Are you sure you want to delete all \${activitiesOfType.length} activities of type "\${selectedType}"?`)) {
            return;
        }
        
        // Remove activities of this type
        state.activities = state.activities.filter(activity => (activity.type || \'Default\') !== selectedType);
        
        // Also remove from schedule
        state.schedule = state.schedule.filter(activity => (activity.type || \'Default\') !== selectedType);
        
        // Update dependencies: remove any dependency that points to a deleted activity
        const deletedIds = activitiesOfType.map(a => a.id);
        state.activities.forEach(activity => {
            if (activity.dependencies) {
                activity.dependencies = activity.dependencies.filter(depId => !deletedIds.includes(depId));
            }
        });
        
        // Update UI
        renderActivitiesList();
        updateDependenciesSelect();
        updateTypeFilterAndSuggestions();
        renderScheduleTimeline();
        renderCalendar();
        
        alert(`Deleted \${activitiesOfType.length} activities of type "\${selectedType}".`);
    }
'''

# Insert this function after the filterActivitiesByType function (which is part of renderActivitiesList now)
# We'll just append it at the end of the file before the closing braces? Actually, we need to insert it in the right scope.
# Let's find the closing brace of the DOMContentLoaded function and insert before it.
# We'll look for the last '});' that closes the DOMContentLoaded function.
# But note: there are multiple functions inside. Let's insert before the final '});' that closes the DOMContentLoaded.
# We can do: split the content by lines and find the last line that is '});'
lines = content.splitlines()
insert_index = -1
for i in range(len(lines)-1, -1, -1):
    if lines[i].strip() == '});':
        insert_index = i
        break

if insert_index != -1:
    # Insert the delete function before the closing '});'
    lines.insert(insert_index, delete_function)
    content = '\n'.join(lines)

# 6. Modify the import function to accumulate activities (not replace)
# Find the handleFileImport function and change the part that clears current state.
# We want to change:
#   // Clear current state
#   state.activities = [];
#   state.schedule = [];
#   state.startDate = null;
# To not clear, but we should still clear schedule and startDate? Actually, the import is for activities, so we can keep existing activities and add new ones.
# But the schedule might be invalid after adding new activities. We'll clear schedule and startDate.
# Let's change the confirmation message and the clearing logic.

if 'function handleFileImport(event)' in content:
    # We'll replace the confirmation and clearing part.
    # Use a more robust replacement by regex.
    pattern = r'if \(!confirm\(\'Importing data will replace your current activities\. Continue\?\'\)\) \{[\s\S]*?state\.activities = \[\];'
    replacement = '''if (!confirm('Importing data will add to your current activities. Continue?')) {
                    return;
                }
                
                // We don't clear current activities, we add to them.
                // But we clear schedule and start date because the schedule may be invalid with new activities.
                state.schedule = [];
                state.startDate = null;'''
    content = re.sub(pattern, replacement, content)

# 7. We need to call updateTypeFilterAndSuggestions whenever activities change.
# We'll update the following functions to call it:
# - addActivity (after adding)
# - removeActivity (after removing)
# - editActivity (after editing)
# - clearAll (after clearing)
# - handleFileImport (after importing)
# We'll do this by adding a call to updateTypeFilterAndSuggestions() in those functions.

# Let's find each function and add the call.
# We'll do a simple string replacement for each.

# For addActivity: after renderActivitiesList and updateDependenciesSelect
if '// Add to state' in content:
    # Find the addActivity function and insert after updateDependenciesSelect()
    lines = content.splitlines()
    new_lines = []
    i = 0
    while i < len(lines):
        new_lines.append(lines[i])
        if 'updateDependenciesSelect();' in lines[i]:
            # Insert our call
            new_lines.append('        updateTypeFilterAndSuggestions();')
        i += 1
    content = '\n'.join(new_lines)

# For removeActivity: after renderActivitiesList and updateDependenciesSelect
if '// Remove from schedule' in content:
    # Actually, removeActivity is a window function. Let's look for the removeActivity function.
    # We'll do a replacement for the entire removeActivity function to add the call.
    pattern = r'window\.removeActivity = function\(id\) \{[\s\S]*?\n    \}'
    def replace_remove(match):
        func = match.group(0)
        # Insert after updateDependenciesSelect();
        if 'updateDependenciesSelect();' in func:
            func = func.replace('updateDependenciesSelect();', 'updateDependenciesSelect();\n        updateTypeFilterAndSuggestions();')
        return func
    content = re.sub(pattern, replace_remove, content)

# For editActivity: after renderActivitiesList and updateDependenciesSelect
if '// Update UI' in content and 'renderActivitiesList();' in content:
    # We'll look for the editActivity function and add the call.
    pattern = r'window\.editActivity = function\(id\) \{[\s\S]*?\n    \}'
    def replace_edit(match):
        func = match.group(0)
        if 'updateDependenciesSelect();' in func:
            func = func.replace('updateDependenciesSelect();', 'updateDependenciesSelect();\n        updateTypeFilterAndSuggestions();')
        return func
    content = re.sub(pattern, replace_edit, content)

# For clearAll: after renderActivitiesList and updateDependenciesSelect
if '// Reset start date to today' in content:
    # Find the clearAll function and add the call.
    # We'll look for the function definition.
    pattern = r'function clearAll\(\) \{[\s\S]*?\n    \}'
    def replace_clear(match):
        func = match.group(0)
        if 'updateDependenciesSelect();' in func:
            func = func.replace('updateDependenciesSelect();', 'updateDependenciesSelect();\n        updateTypeFilterAndSuggestions();')
        return func
    content = re.sub(pattern, replace_clear, content)

# For handleFileImport: after renderActivitiesList and updateDependenciesSelect
if '// Update UI' in content and 'renderActivitiesList();' in content and 'handleFileImport' in content:
    # We'll do a replacement for the part after importing.
    # Actually, we already modified handleFileImport. We'll now add the call to updateTypeFilterAndSuggestions.
    # Let's find the line with updateDependenciesSelect and add after it.
    lines = content.splitlines()
    new_lines = []
    i = 0
    while i < len(lines):
        new_lines.append(lines[i])
        if 'updateDependenciesSelect();' in lines[i] and 'handleFileImport' in content[:content.find(lines[i])]:
            new_lines.append('                updateTypeFilterAndSuggestions();')
        i += 1
    content = '\n'.join(new_lines)

# 8. Finally, we need to initialize the type filter and suggestions after the initial render.
# We'll call updateTypeFilterAndSuggestions after the initial updateDependenciesSelect.
# Find the line after updateDependenciesSelect in the initialization.
if 'updateDependenciesSelect();' in content:
    lines = content.splitlines()
    new_lines = []
    i = 0
    while i < len(lines):
        new_lines.append(lines[i])
        if lines[i].strip() == 'updateDependenciesSelect();' and '// Initialize calendar' in lines[i+1]:
            # This is the initial call. Add after it.
            new_lines.append('    updateTypeFilterAndSuggestions();')
        i += 1
    content = '\n'.join(new_lines)

# Write the updated content back
with open('script-enhanced.js', 'w') as f:
    f.write(content)

print("Updated JavaScript with new features")
