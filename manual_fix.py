import re

with open('script-enhanced.js', 'r') as f:
    lines = f.readlines()

# 1. Update the datalist id in updateTypeFilterAndSuggestions function.
for i, line in enumerate(lines):
    if "document.getElementById('typeSuggestions')" in line:
        lines[i] = line.replace("document.getElementById('typeSuggestions')", "document.getElementById('typeOptions')")

# 2. Fix editActivityDate function: move console.log before prompt.
# We'll find the function and then locate the lines we need.
in_editActivityDate = False
for i, line in enumerate(lines):
    if 'window.editActivityDate = function(id)' in line:
        in_editActivityDate = True
    if in_editActivityDate and 'const newStartDate = prompt' in line:
        # The next line is console.log, we need to swap them.
        # Actually, we need to move the console.log before the prompt.
        # We'll check the next line for the console.log.
        if i+1 < len(lines) and 'console.log("editActivityDate called with id:"' in lines[i+1]:
            # Swap lines[i] and lines[i+1]
            lines[i], lines[i+1] = lines[i+1], lines[i]
        break

# 3. Fix editActivity function: remove duplicate console.log inside the if block.
# We'll find the line with the console.log inside the if block and remove it.
for i, line in enumerate(lines):
    if 'if (isNaN(duration) || duration < 1) {' in line:
        # Look ahead for the console.log line and remove it.
        j = i + 1
        while j < len(lines) and '}' not in lines[j]:
            if 'console.log("editActivity called with id:"' in lines[j]:
                # Remove this line
                lines.pop(j)
                break
            j += 1

# 4. Fix removeActivity function: remove duplicate console.log inside the if block.
for i, line in enumerate(lines):
    if 'if (dependentActivities.length > 0) {' in line:
        j = i + 1
        while j < len(lines) and 'const dependentNames' not in lines[j]:
            if 'console.log("removeActivity called with id:"' in lines[j]:
                lines.pop(j)
                break
            j += 1

# 5. Add calculateEndDate function if missing.
# Check if calculateEndDate is defined.
calculate_end_date_exists = any('function calculateEndDate' in line for line in lines)
if not calculate_end_date_exists:
    # Find the formatDate function and insert after it.
    for i, line in enumerate(lines):
        if 'function formatDate(dateObj)' in line:
            # Insert after the closing brace of the formatDate function.
            # Find the closing brace at the same indentation level.
            j = i
            while j < len(lines) and '}' not in lines[j]:
                j += 1
            # Now lines[j] contains the '}'
            # Insert after that line.
            indent = '    '  # assume 4 spaces
            lines.insert(j+1, '\n')
            lines.insert(j+2, indent + '// Function to calculate end date given start date and duration (excluding weekends/holidays)\n')
            lines.insert(j+3, indent + 'function calculateEndDate(startDate, duration) {\n')
            lines.insert(j+4, indent + '    let currentDate = startDate;\n')
            lines.insert(j+5, indent + '    let daysCounted = 0;\n')
            lines.insert(j+6, indent + '    while (daysCounted < duration) {\n')
            lines.insert(j+7, indent + '        // Move to next day\n')
            lines.insert(j+8, indent + '        currentDate = currentDate.plus({ days: 1 });\n')
            lines.insert(j+9, indent + '        // Check if it\'s a working day\n')
            lines.insert(j+10, indent + '        if (isWorkingDay(currentDate)) {\n')
            lines.insert(j+11, indent + '            daysCounted++;\n')
            lines.insert(j+12, indent + '        }\n')
            lines.insert(j+13, indent + '    }\n')
            lines.insert(j+14, indent + '    return currentDate;\n')
            lines.insert(j+15, indent + '}\n')
            break

# Write back
with open('script-enhanced.js', 'w') as f:
    f.writelines(lines)

print('Applied manual fixes: datalist id, editActivityDate, editActivity, removeActivity, added calculateEndDate.')
