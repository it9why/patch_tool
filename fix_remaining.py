import re

with open('script-enhanced.js', 'r') as f:
    content = f.read()

# 1. Change the datalist id from 'typeSuggestions' to 'typeOptions' in updateTypeFilterAndSuggestions function
content = content.replace("document.getElementById('typeSuggestions')", "document.getElementById('typeOptions')")

# 2. Fix editActivityDate function: ensure the console.log is at the beginning and the prompt is correctly formatted.
# We'll replace the entire editActivityDate function with a corrected version.
# First, find the function using a regex pattern.
pattern_editActivityDate = r'window\.editActivityDate = function\(id\) \{[\s\S]*?\n    \}'
# We'll replace with a corrected version.
corrected_editActivityDate = '''window.editActivityDate = function(id) {
        console.log("editActivityDate called with id:", id);
        const activity = state.activities.find(a => a.id === id);
        if (!activity) return;

        // Create a date picker dialog
        const newStartDate = prompt(`Edit start date for "${activity.name}" (YYYY-MM-DD):`, 
            activity.startDate ? activity.startDate.toISODate() : '');
        
        if (newStartDate && newStartDate.match(/^\\d{4}-\\d{2}-\\d{2}$/)) {
            const startDate = DateTime.fromISO(newStartDate);
            const endDate = calculateEndDate(startDate, activity.duration);
            
            // Update activity dates
            activity.startDate = startDate;
            activity.endDate = endDate;
            
            // Update schedule if this activity is scheduled
            const scheduleIndex = state.schedule.findIndex(a => a.id === id);
            if (scheduleIndex !== -1) {
                state.schedule[scheduleIndex].startDate = startDate;
                state.schedule[scheduleIndex].endDate = endDate;
            }
            
            // Update UI
            renderActivitiesList();
            renderScheduleTimeline();
            renderCalendar();
        } else if (newStartDate !== null) {
            alert('Please enter a valid date in YYYY-MM-DD format');
        }
    }'''

content = re.sub(pattern_editActivityDate, corrected_editActivityDate, content, flags=re.DOTALL)

# 3. Fix editActivity function: remove duplicate console.log and ensure the function is correct.
# We'll replace the entire editActivity function with a cleaned version.
pattern_editActivity = r'window\.editActivity = function\(id\) \{[\s\S]*?\n    \}'
corrected_editActivity = '''window.editActivity = function(id) {
        console.log("editActivity called with id:", id);
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

        // Ask for type
        const newType = prompt('Edit type:', activity.type || 'Default');
        if (newType === null) return;
        // Update activity
        activity.name = newName.trim();
        activity.duration = duration;
        activity.dependencies = newDependencies;
        activity.type = newType.trim();
        // If the activity is scheduled, we need to reschedule
        // For now, we'll remove the schedule and let the user regenerate
        // Remove from schedule
        state.schedule = state.schedule.filter(a => a.id !== id);
        activity.startDate = null;
        activity.endDate = null;

        // Update UI
        renderActivitiesList();
        updateDependenciesSelect();
        updateTypeFilterAndSuggestions();
        renderScheduleTimeline();
        renderCalendar();
    }'''

content = re.sub(pattern_editActivity, corrected_editActivity, content, flags=re.DOTALL)

# 4. Fix removeActivity function: remove duplicate console.log inside the if block.
pattern_removeActivity = r'window\.removeActivity = function\(id\) \{[\s\S]*?\n    \}'
corrected_removeActivity = '''window.removeActivity = function(id) {
        console.log("removeActivity called with id:", id);
        // Check if any activity depends on this one
        const dependentActivities = state.activities.filter(a => a.dependencies && a.dependencies.includes(id));
        
        if (dependentActivities.length > 0) {
            const dependentNames = dependentActivities.map(a => a.name).join(', ');
            if (!confirm(`The following activities depend on this one: ${dependentNames}. Do you still want to remove it?`)) {
                return;
            }
        }

        // Remove the activity
        state.activities = state.activities.filter(a => a.id !== id);
        
        // Remove any dependencies pointing to this activity
        state.activities.forEach(a => {
            if (a.dependencies && a.dependencies.includes(id)) {
                a.dependencies = a.dependencies.filter(depId => depId !== id);
            }
        });

        // Remove from schedule
        state.schedule = state.schedule.filter(a => a.id !== id);

        // Update UI
        renderActivitiesList();
        updateDependenciesSelect();
        updateTypeFilterAndSuggestions();
        renderScheduleTimeline();
        renderCalendar();
    }'''

content = re.sub(pattern_removeActivity, corrected_removeActivity, content, flags=re.DOTALL)

# 5. Also, we need to define the calculateEndDate function? It's not defined in the script.
# Let's search for calculateEndDate. It's used in editActivityDate and elsewhere. We need to add it if missing.
# We'll search for function calculateEndDate.
if 'function calculateEndDate' not in content:
    # Insert it after the formatDate function.
    formatDate_pattern = r'function formatDate\(dateObj\) \{[\s\S]*?\n    \}'
    calculateEndDate_func = '''
    // Function to calculate end date given start date and duration (excluding weekends/holidays)
    function calculateEndDate(startDate, duration) {
        let currentDate = startDate;
        let daysCounted = 0;
        while (daysCounted < duration) {
            // Move to next day
            currentDate = currentDate.plus({ days: 1 });
            // Check if it's a working day
            if (isWorkingDay(currentDate)) {
                daysCounted++;
            }
        }
        return currentDate;
    }'''
    content = re.sub(formatDate_pattern, formatDate_pattern + calculateEndDate_func, content, flags=re.DOTALL)

# Write the fixed content back
with open('script-enhanced.js', 'w') as f:
    f.write(content)

print('Fixed datalist id, editActivityDate, editActivity, removeActivity, and added calculateEndDate function')
