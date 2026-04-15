import sys

with open('script-enhanced.js', 'r') as f:
    lines = f.readlines()

# Find the DOM elements section and add activityTypeInput
for i, line in enumerate(lines):
    if 'const dependenciesSelect = document.getElementById' in line:
        # Insert after this line
        lines.insert(i+1, '    const activityTypeInput = document.getElementById(\'activityType\');\n')
        break

# Find the addActivity function and add type handling
for i, line in enumerate(lines):
    if 'window.addActivity = function(event)' in line:
        # Find the function body and add type reading
        # We'll look for the line with const dependencies
        for j in range(i, len(lines)):
            if 'const dependencies = Array.from' in lines[j]:
                # Insert before this line
                lines.insert(j, '        const type = activityTypeInput.value.trim() || \'Default\';\n')
                break
        break

# Now update the activity object creation
for i, line in enumerate(lines):
    if '// Create activity object' in line:
        # Find the next lines until the closing brace of the object
        for j in range(i, len(lines)):
            if 'startDate: null,' in lines[j]:
                # Insert after this line
                lines.insert(j+1, '            type: type,')
                break
        break

# Update renderActivitiesList to show type
for i, line in enumerate(lines):
    if '<p>Duration: ${activity.duration}' in lines[i]:
        # Insert after this line
        lines.insert(i+1, '                    <p>Type: ${activity.type}</p>')
        break

# Update editActivity to handle type editing
# Find the editActivity function
for i, line in enumerate(lines):
    if 'window.editActivity = function(id)' in line:
        # We'll add a prompt for type after the dependencies prompt
        # Find the line with newDependencies
        for j in range(i, len(lines)):
            if 'newDependencies = depIds;' in lines[j]:
                # Insert after this block, before the "// Update activity" comment
                # Look for the comment
                for k in range(j, len(lines)):
                    if '// Update activity' in lines[k]:
                        # Insert before this line
                        lines.insert(k, '        // Ask for type\n        const newType = prompt(\'Edit type:\', activity.type || \'Default\');\n        if (newType === null) return;\n')
                        break
                break
        break

# Now update the activity update section to include type
for i, line in enumerate(lines):
    if 'activity.dependencies = newDependencies;' in line:
        # Insert after this line
        lines.insert(i+1, '        activity.type = newType.trim();')
        break

# Update exportActivities to include type
for i, line in enumerate(lines):
    if 'exportActivities()' in line:
        # Find the activities mapping
        for j in range(i, len(lines)):
            if 'activities: state.activities.map' in lines[j]:
                # Update the mapping to include type
                # We'll replace the whole line
                lines[j] = '            activities: state.activities.map(activity => ({\n                name: activity.name,\n                duration: activity.duration,\n                dependency: activity.dependency,\n                type: activity.type || \'Default\'\n            })),'
                break
        break

# Update exportSchedule to include type
for i, line in enumerate(lines):
    if 'exportSchedule()' in line:
        for j in range(i, len(lines)):
            if 'schedule: state.schedule.map' in lines[j]:
                lines[j] = '            schedule: state.schedule.map(activity => ({\n                name: activity.name,\n                duration: activity.duration,\n                startDate: activity.startDate ? activity.startDate.toISODate() : null,\n                endDate: activity.endDate ? activity.endDate.toISODate() : null,\n                dependency: activity.dependency,\n                type: activity.type || \'Default\'\n            })),'
                break
        break

# Update import functions to handle type
# Find handleFileImport function
for i, line in enumerate(lines):
    if 'function handleFileImport(event)' in line:
        # Find where activities are created from importData
        for j in range(i, len(lines)):
            if 'const activity = {' in lines[j] and 'id: generateId()' in lines[j+1]:
                # Insert type after dependency
                # Find the line with dependency
                for k in range(j, len(lines)):
                    if 'dependency: activityData.dependency || null,' in lines[k]:
                        lines.insert(k+1, '                            type: activityData.type || \'Default\',')
                        break
                break
        break

# Update the schedule import similarly
for i, line in enumerate(lines):
    if 'const activity = {' in line and 'id: generateId()' in lines[i+1] and 'scheduleData.startDate' in lines[i+4]:
        # This is the schedule import block
        for k in range(i, len(lines)):
            if 'dependency: scheduleData.dependency || null,' in lines[k]:
                lines.insert(k+1, '                            type: scheduleData.type || \'Default\',')
                break
        break

# Write back
with open('script-enhanced.js', 'w') as f:
    f.writelines(lines)

print("Updated JavaScript for Type property")
