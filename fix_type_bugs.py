import re

with open('script-enhanced.js', 'r') as f:
    content = f.read()

# 1. Add DOM element references for type input, filter, and datalist.
# Find the line where other DOM elements are defined (around line 19).
# We'll insert after the dependenciesSelect line.
dom_elements_insertion = """
    // DOM Elements
    const activityNameInput = document.getElementById('activityName');
    const durationInput = document.getElementById('duration');
    const dependenciesSelect = document.getElementById('dependencies');
    const addActivityBtn = document.getElementById('addActivity');
    const activitiesContainer = document.getElementById('activitiesContainer');
    const startDateInput = document.getElementById('startDate');
    const generateScheduleBtn = document.getElementById('generateSchedule');
    const clearAllBtn = document.getElementById('clearAll');
    const currentMonthElement = document.getElementById('currentMonth');
    const prevMonthBtn = document.getElementById('prevMonth');
    const nextMonthBtn = document.getElementById('nextMonth');
    const calendarElement = document.getElementById('calendar');
    const scheduleTimelineElement = document.getElementById('scheduleTimeline');"""

new_dom_elements = """
    // DOM Elements
    const activityNameInput = document.getElementById('activityName');
    const durationInput = document.getElementById('duration');
    const dependenciesSelect = document.getElementById('dependencies');
    const addActivityBtn = document.getElementById('addActivity');
    const activitiesContainer = document.getElementById('activitiesContainer');
    const startDateInput = document.getElementById('startDate');
    const generateScheduleBtn = document.getElementById('generateSchedule');
    const clearAllBtn = document.getElementById('clearAll');
    const currentMonthElement = document.getElementById('currentMonth');
    const prevMonthBtn = document.getElementById('prevMonth');
    const nextMonthBtn = document.getElementById('nextMonth');
    const calendarElement = document.getElementById('calendar');
    const scheduleTimelineElement = document.getElementById('scheduleTimeline');
    // Type-related elements
    const typeInput = document.getElementById('activityType');
    const typeFilterSelect = document.getElementById('typeFilter');
    const typeOptionsDatalist = document.getElementById('typeOptions');"""

# Replace the DOM elements block
content = content.replace(dom_elements_insertion, new_dom_elements)

# 2. In the addActivity function, read the type input and add to activity object.
# Find the addActivity function and update it.
addActivity_pattern = r'(function addActivity\(\) \{[\s\S]*?const name = activityNameInput\.value\.trim\(\);[\s\S]*?const duration = parseInt\(durationInput\.value\);[\s\S]*?const dependencies = Array\.from\(dependenciesSelect\.selectedOptions\).map\(option => option\.value\);[\s\S]*?\})'
def update_addActivity(match):
    func = match.group(0)
    # Insert reading of type after reading dependencies.
    func = re.sub(r'(const dependencies = Array\.from\(dependenciesSelect\.selectedOptions\).map\(option => option\.value\);)\s*',
                  r'\1\n        const type = typeInput.value.trim() || \'Default\';', func)
    # Then update the activity object to include type.
    func = re.sub(r'(const activity = \{[\s\S]*?id: generateId\(\),[\s\S]*?name,[\s\S]*?duration,[\s\S]*?dependencies: dependencies,[\s\S]*?startDate: null,[\s\S]*?endDate: null[\s\S]*?\})',
                  r'const activity = {\n            id: generateId(),\n            name,\n            duration,\n            type,\n            dependencies: dependencies,\n            startDate: null,\n            endDate: null\n        };', func)
    # Also clear the type input after adding activity.
    func = re.sub(r'(activityNameInput\.value = \'\';[\s\S]*?durationInput\.value = \'1\';)',
                  r'\1\n        typeInput.value = \'\';', func)
    return func

content = re.sub(addActivity_pattern, update_addActivity, content, flags=re.DOTALL)

# 3. Update renderActivitiesList to show the type.
# We need to find the function and add a line for type.
renderActivitiesList_pattern = r'(function renderActivitiesList\(\) \{[\s\S]*?let html = \'\';\s*html \+= \'<div class="activity-info">\'\s*;\s*html \+= \'<h4>\' \+ escapeHtml\(activity\.name\) \+ \'</h4>\'\s*;\s*html \+= \'<p>Duration: \' \+ activity\.duration \+ \' day\' \+ \(activity\.duration > 1 \? \'s\' : \'\'\) \+ \'</p>\'\s*;)'
def update_renderActivitiesList(match):
    # We'll add a line for type after the duration line.
    return match.group(0) + '\n            html += \'<p>Type: \' + escapeHtml(activity.type || \'Default\') + \'</p>\';'

content = re.sub(renderActivitiesList_pattern, update_renderActivitiesList, content, flags=re.DOTALL)

# 4. Create the updateTypeFilterAndSuggestions function.
# We'll insert it after the updateDependenciesSelect function.
updateDependenciesSelect_pattern = r'(function updateDependenciesSelect\(\) \{[\s\S]*?\n    \})'
updateTypeFilterAndSuggestions_function = '''
    // Function to update the type filter dropdown and suggestions
    function updateTypeFilterAndSuggestions() {
        // Get unique types from activities
        const types = [...new Set(state.activities.map(a => a.type || 'Default'))];

        // Update the type filter dropdown
        typeFilterSelect.innerHTML = '<option value="">All Types</option>';
        types.forEach(type => {
            const option = document.createElement('option');
            option.value = type;
            option.textContent = type;
            typeFilterSelect.appendChild(option);
        });

        // Update the datalist for suggestions (if it exists)
        if (typeOptionsDatalist) {
            typeOptionsDatalist.innerHTML = '';
            types.forEach(type => {
                const option = document.createElement('option');
                option.value = type;
                typeOptionsDatalist.appendChild(option);
            });
        }
    }'''

content = re.sub(updateDependenciesSelect_pattern, r'\1\n' + updateTypeFilterAndSuggestions_function, content, flags=re.DOTALL)

# 5. Call updateTypeFilterAndSuggestions after activities are updated.
# We'll find all places where renderActivitiesList is called after state.activities changes.
# We'll add a call to updateTypeFilterAndSuggestions right after renderActivitiesList.

# In addActivity, after renderActivitiesList and updateDependenciesSelect.
# We already have a call to renderActivitiesList and updateDependenciesSelect. We'll add updateTypeFilterAndSuggestions after.
addActivity_call_pattern = r'(renderActivitiesList\(\);\s*updateDependenciesSelect\(\);)'
content = re.sub(addActivity_call_pattern, r'\1\n        updateTypeFilterAndSuggestions();', content)

# In editActivity, after renderActivitiesList and updateDependenciesSelect.
# There is a call to renderActivitiesList and updateDependenciesSelect in editActivity.
# We'll replace similarly.
editActivity_call_pattern = r'(renderActivitiesList\(\);\s*updateDependenciesSelect\(\);)'
# But note: there might be multiple occurrences. We'll do a more targeted replacement by looking at the editActivity function.
# We'll do a replacement that only affects the editActivity function.
editActivity_function_pattern = r'(window\.editActivity = function\(id\) \{[\s\S]*?renderActivitiesList\(\);\s*updateDependenciesSelect\(\);\s*renderScheduleTimeline\(\);\s*renderCalendar\(\);\s*\})'
def update_editActivity(match):
    func = match.group(0)
    func = re.sub(r'(renderActivitiesList\(\);\s*updateDependenciesSelect\(\);\s*renderScheduleTimeline\(\);\s*renderCalendar\(\);)',
                  r'renderActivitiesList();\n        updateDependenciesSelect();\n        updateTypeFilterAndSuggestions();\n        renderScheduleTimeline();\n        renderCalendar();', func)
    return func

content = re.sub(editActivity_function_pattern, update_editActivity, content, flags=re.DOTALL)

# In removeActivity, after renderActivitiesList and updateDependenciesSelect.
removeActivity_function_pattern = r'(window\.removeActivity = function\(id\) \{[\s\S]*?renderActivitiesList\(\);\s*updateDependenciesSelect\(\);\s*renderScheduleTimeline\(\);\s*renderCalendar\(\);\s*\})'
def update_removeActivity(match):
    func = match.group(0)
    func = re.sub(r'(renderActivitiesList\(\);\s*updateDependenciesSelect\(\);\s*renderScheduleTimeline\(\);\s*renderCalendar\(\);)',
                  r'renderActivitiesList();\n        updateDependenciesSelect();\n        updateTypeFilterAndSuggestions();\n        renderScheduleTimeline();\n        renderCalendar();', func)
    return func

content = re.sub(removeActivity_function_pattern, update_removeActivity, content, flags=re.DOTALL)

# In clearAll, after renderActivitiesList and updateDependenciesSelect.
clearAll_pattern = r'(renderActivitiesList\(\);\s*updateDependenciesSelect\(\);\s*renderScheduleTimeline\(\);\s*renderCalendar\(\);)'
content = re.sub(clearAll_pattern, r'renderActivitiesList();\n        updateDependenciesSelect();\n        updateTypeFilterAndSuggestions();\n        renderScheduleTimeline();\n        renderCalendar();', content)

# In loadTemplate (inside the loadTemplate function) and handleFileImport, we also update activities.
# We'll find the loadTemplate function and add the call.
loadTemplate_pattern = r'(function loadTemplate\(\) \{[\s\S]*?renderActivitiesList\(\);\s*updateDependenciesSelect\(\);\s*renderScheduleTimeline\(\);\s*renderCalendar\(\);\s*\})'
def update_loadTemplate(match):
    func = match.group(0)
    func = re.sub(r'(renderActivitiesList\(\);\s*updateDependenciesSelect\(\);\s*renderScheduleTimeline\(\);\s*renderCalendar\(\);)',
                  r'renderActivitiesList();\n        updateDependenciesSelect();\n        updateTypeFilterAndSuggestions();\n        renderScheduleTimeline();\n        renderCalendar();', func)
    return func

content = re.sub(loadTemplate_pattern, update_loadTemplate, content, flags=re.DOTALL)

# In handleFileImport, there are two branches (activities and schedule). We'll update both.
handleFileImport_pattern = r'(function handleFileImport\(event\) \{[\s\S]*?renderActivitiesList\(\);\s*updateDependenciesSelect\(\);\s*renderScheduleTimeline\(\);\s*renderCalendar\(\);\s*\})'
def update_handleFileImport(match):
    func = match.group(0)
    func = re.sub(r'(renderActivitiesList\(\);\s*updateDependenciesSelect\(\);\s*renderScheduleTimeline\(\);\s*renderCalendar\(\);)',
                  r'renderActivitiesList();\n                updateDependenciesSelect();\n                updateTypeFilterAndSuggestions();\n                renderScheduleTimeline();\n                renderCalendar();', func)
    return func

content = re.sub(handleFileImport_pattern, update_handleFileImport, content, flags=re.DOTALL)

# 6. Add event listener for typeFilter to filter activities.
# We'll add it in the event listeners section.
# Find where other event listeners are added (around line 60).
event_listeners_insertion = """
    // Event Listeners
    addActivityBtn.addEventListener('click', addActivity);
    generateScheduleBtn.addEventListener('click', generateSchedule);
    clearAllBtn.addEventListener('click', clearAll);
    prevMonthBtn.addEventListener('click', previousMonth);
    nextMonthBtn.addEventListener('click', nextMonth);"""

new_event_listeners = """
    // Event Listeners
    addActivityBtn.addEventListener('click', addActivity);
    generateScheduleBtn.addEventListener('click', generateSchedule);
    clearAllBtn.addEventListener('click', clearAll);
    prevMonthBtn.addEventListener('click', previousMonth);
    nextMonthBtn.addEventListener('click', nextMonth);
    // Type filter event listener
    typeFilterSelect.addEventListener('change', function() {
        renderActivitiesList();
    });"""

content = content.replace(event_listeners_insertion, new_event_listeners)

# 7. Modify renderActivitiesList to filter by selected type.
# We'll change the beginning of renderActivitiesList to consider the type filter.
renderActivitiesList_definition_pattern = r'(function renderActivitiesList\(\) \{[\s\S]*?if \(state\.activities\.length === 0\) \{[\s\S]*?return;\s*\}\s*activitiesContainer\.innerHTML = \'\'\s*;)'
def update_renderActivitiesList_definition(match):
    # Insert filtering logic at the beginning of the function.
    new_function = '''function renderActivitiesList() {
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

        activitiesContainer.innerHTML = '';'''
    # We need to replace the original function start with the new one.
    # We'll capture the rest of the function after the opening lines.
    # Instead, we'll replace the entire function with a new one? That's complex.
    # Let's do a different approach: we'll replace the entire function with a new version.
    # We'll extract the existing function body and modify it.
    # But we already changed the function earlier (added type display). We'll rewrite the whole function.
    # We'll write a new function and replace the old one.
    # We'll find the entire function and replace it.
    return new_function

# We'll do a full function replacement.
# First, let's get the current function (after our previous changes) and rewrite it.
# We'll use a pattern that captures the entire function.
full_render_pattern = r'(function renderActivitiesList\(\) \{[\s\S]*?\n    \})'
new_render_function = '''    function renderActivitiesList() {
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

content = re.sub(full_render_pattern, new_render_function, content, flags=re.DOTALL)

# 8. Initialize the type filter and suggestions on page load.
# We'll call updateTypeFilterAndSuggestions after initializing the calendar and updateDependenciesSelect.
# Find the line after updateDependenciesSelect in the initialization.
init_call_pattern = r'(renderCalendar\(\);\s*updateDependenciesSelect\(\);)'
content = re.sub(init_call_pattern, r'renderCalendar();\n    updateDependenciesSelect();\n    updateTypeFilterAndSuggestions();', content)

# Write the modified content back
with open('script-enhanced.js', 'w') as f:
    f.write(content)

print('Updated script to handle activity type, type filter, and type suggestions.')
