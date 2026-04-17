import re

with open('script-enhanced.js', 'r') as f:
    lines = f.readlines()

# 1. Add console.log statements to editActivity, editActivityDate, and removeActivity functions
# Find editActivity function and add a log at the beginning
for i, line in enumerate(lines):
    if 'window.editActivity = function(id)' in line:
        # Insert after the opening brace
        j = i + 1
        while j < len(lines) and '{' not in lines[j]:
            j += 1
        if j < len(lines):
            lines.insert(j + 1, '        console.log("editActivity called with id:", id);\n')
        break

# Find editActivityDate function
for i, line in enumerate(lines):
    if 'window.editActivityDate = function(id)' in line:
        j = i + 1
        while j < len(lines) and '{' not in lines[j]:
            j += 1
        if j < len(lines):
            lines.insert(j + 1, '        console.log("editActivityDate called with id:", id);\n')
        break

# Find removeActivity function
for i, line in enumerate(lines):
    if 'window.removeActivity = function(id)' in line:
        j = i + 1
        while j < len(lines) and '{' not in lines[j]:
            j += 1
        if j < len(lines):
            lines.insert(j + 1, '        console.log("removeActivity called with id:", id);\n')
        break

# 2. Add event listener for focus on the type input to update suggestions
# We need to find where the event listeners are set up (around line 80-100)
# Look for the line where other event listeners are added (like addActivityBtn.addEventListener)
# We'll add after the line that adds event listener to quickDeleteTypeBtn
for i, line in enumerate(lines):
    if 'quickDeleteTypeBtn.addEventListener' in line:
        # Insert after this line
        lines.insert(i + 1, '    activityTypeInput.addEventListener(\'focus\', updateTypeFilterAndSuggestions);\n')
        break

# Write back
with open('script-enhanced.js', 'w') as f:
    f.writelines(lines)

print('Added debug logs and focus event for type suggestions')
