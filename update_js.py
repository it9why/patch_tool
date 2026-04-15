import sys

with open('script-enhanced.js', 'r') as f:
    lines = f.readlines()

# We'll make several changes:

# 1. Remove the lines that reference saveTemplate and loadTemplate in the DOM elements and event listeners.
# 2. Change the dependency select to multiple and update the variable name.
# 3. Update the addActivity function to handle multiple dependencies.
# 4. Update the activity object to store multiple dependencies (array).
# 5. Update the activity rendering to show multiple dependencies.
# 6. Update the updateDependencySelect function to handle multiple selections.

# We'll do it step by step.

output_lines = []
i = 0
while i < len(lines):
    line = lines[i]

    # Remove the saveTemplate and loadTemplate DOM element lines
    if 'const saveTemplateBtn = document.getElementById' in line or 'const loadTemplateBtn = document.getElementById' in line:
        i += 1
        continue

    # Change the dependency select variable and make it multiple
    if 'const dependencySelect = document.getElementById' in line and "'dependency'" in line:
        line = "    const dependenciesSelect = document.getElementById('dependencies');\n"

    # Remove the event listeners for saveTemplate and loadTemplate
    if 'saveTemplateBtn.addEventListener' in line or 'loadTemplateBtn.addEventListener' in line:
        i += 1
        continue

    # Update the addActivity function to get multiple dependencies
    if 'function addActivity() {' in line:
        # We'll replace the entire function. Let's find the end of the function.
        # We'll do a simple approach: replace the function block.
        # We'll write a new function and skip until the closing brace.
        # But note: the function might be long. Let's instead replace the part that gets the dependency.
        pass

    # We'll do a more targeted approach: change the line that gets the dependency value.
    if 'const dependency = dependencySelect.value;' in line:
        line = "        const dependencies = Array.from(dependenciesSelect.selectedOptions).map(option => option.value);\n"

    # Change the activity object creation to use dependencies array
    if 'dependency: dependency || null,' in line:
        line = "            dependencies: dependencies,\n"

    # Update the updateDependencySelect function to handle multiple
    # We'll change the function name and its usage to updateDependenciesSelect
    if 'function updateDependencySelect() {' in line:
        line = 'function updateDependenciesSelect() {\n'

    # Update the call to updateDependencySelect to updateDependenciesSelect
    if 'updateDependencySelect();' in line and not 'function' in lines[i-2]:
        line = '    updateDependenciesSelect();\n'

    # In the renderActivitiesList, we need to update how dependencies are displayed.
    # We'll change the line that shows dependency.
    if 'Dependency: ${activity.dependency ? getActivityName(activity.dependency) : \'None\'}' in line:
        line = '                    <p>Dependencies: ${activity.dependencies && activity.dependencies.length > 0 ? activity.dependencies.map(depId => getActivityName(depId)).join(\', \') : \'None\'}</p>\n'

    # In the removeActivity function, we need to update the check for dependencies.
    # We'll change the condition to check if any activity has this activity in its dependencies array.
    if 'const dependentActivities = state.activities.filter(a => a.dependency === id);' in line:
        line = '        const dependentActivities = state.activities.filter(a => a.dependencies && a.dependencies.includes(id));\n'

    # Also in removeActivity, we need to remove the dependency from the array.
    if 'if (a.dependency === id) {' in line:
        line = '            if (a.dependencies && a.dependencies.includes(id)) {\n'
    if 'a.dependency = null;' in line:
        line = '                a.dependencies = a.dependencies.filter(depId => depId !== id);\n'

    # In the calculateSchedule function, we need to update the logic for dependencies.
    # We'll change the condition for availableActivities to check all dependencies are scheduled.
    # This is more complex. We'll leave it for now and come back.

    # For now, let's write the changes we have.
    output_lines.append(line)
    i += 1

# Now, we need to update the calculateSchedule function to handle multiple dependencies.
# We'll do a second pass for the calculateSchedule function.

# Let's write the updated file and then we'll manually adjust the calculateSchedule function.
with open('script-enhanced-updated.js', 'w') as f:
    f.writelines(output_lines)

print("Updated script saved as script-enhanced-updated.js")
