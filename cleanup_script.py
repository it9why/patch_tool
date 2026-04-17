import re

with open('script-enhanced.js', 'r') as f:
    lines = f.readlines()

# 1. Remove the nested function definition in addActivity.
# We'll find the addActivity function and remove the nested function.
in_addActivity = False
in_nested = False
nested_indent = 0
output_lines = []

i = 0
while i < len(lines):
    line = lines[i]
    
    # Detect entering addActivity
    if 'window.addActivity = function(event)' in line:
        in_addActivity = True
        output_lines.append(line)
        i += 1
        continue
    
    if in_addActivity and not in_nested:
        # Look for the start of the nested function
        if '// Function to update the type filter dropdown and suggestions' in line:
            in_nested = True
            nested_indent = len(line) - len(line.lstrip())
            # Skip this line and the entire nested function
            i += 1
            # Skip until we find a line with just a closing brace at the same indent level
            while i < len(lines):
                cur_line = lines[i]
                if cur_line.strip() == '}' and (len(cur_line) - len(cur_line.lstrip())) == nested_indent:
                    i += 1
                    break
                i += 1
            # After the nested function, there is a call to updateTypeFilterAndSuggestions();
            # We want to keep that call. So we continue without adding the nested function lines.
            continue
    
    if in_addActivity and in_nested:
        # We are inside the nested function, skip lines until we find the closing brace
        # (this should have been handled above, but just in case)
        if line.strip() == '}' and (len(line) - len(line.lstrip())) == nested_indent:
            in_nested = False
            i += 1
            continue
        i += 1
        continue
    
    # Detect leaving addActivity
    if in_addActivity and line.strip() == '}' and not in_nested:
        in_addActivity = False
        output_lines.append(line)
        i += 1
        continue
    
    output_lines.append(line)
    i += 1

# 2. Fix the indentation of console.log in editActivity and editActivityDate
# We'll also add a console.log in removeActivity.
new_lines = []
for line in output_lines:
    # Fix editActivityDate console.log
    if 'console.log("editActivityDate called with id:", id);' in line and '        ' in line:
        # Ensure it's at the same indentation as the function body (8 spaces?)
        # We'll replace with proper indentation: 8 spaces (two levels)
        line = '        console.log("editActivityDate called with id:", id);\n'
    # Fix editActivity console.log
    if 'console.log("editActivity called with id:", id);' in line and '                ' in line:
        # The current line has 16 spaces? We want 8 spaces (two levels)
        line = '        console.log("editActivity called with id:", id);\n'
    new_lines.append(line)

# 3. Add a console.log in removeActivity at the beginning of the function.
# Find the removeActivity function and insert a console.log after the opening brace.
output_lines2 = []
i = 0
while i < len(new_lines):
    line = new_lines[i]
    output_lines2.append(line)
    if 'window.removeActivity = function(id)' in line:
        # Find the opening brace and then insert a console.log.
        # The next line should be '{' or there might be a newline.
        j = i + 1
        while j < len(new_lines):
            if new_lines[j].strip() == '{':
                # Insert after the opening brace
                output_lines2.append(new_lines[j])
                output_lines2.append('        console.log("removeActivity called with id:", id);\n')
                i = j
                break
            else:
                output_lines2.append(new_lines[j])
            j += 1
        i = j + 1
        continue
    i += 1

# Write the result back
with open('script-enhanced.js', 'w') as f:
    f.writelines(output_lines2)

print('Removed nested function in addActivity, fixed console.log indentation, added console.log in removeActivity.')
