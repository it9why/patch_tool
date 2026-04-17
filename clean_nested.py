import re

with open('script-enhanced.js', 'r') as f:
    lines = f.readlines()

# We'll remove the nested function definition in addActivity.
# The nested function starts with "// Function to update the type filter dropdown and suggestions"
# and ends with the closing brace at the same indentation level.
# We are inside the addActivity function, which is defined as window.addActivity = function(event) { ... }
# We'll find the start of the nested function and then remove until the closing brace.

in_addActivity = False
in_nested_function = False
nested_indent = 0
output_lines = []

i = 0
while i < len(lines):
    line = lines[i]
    
    # Detect if we are inside the addActivity function
    if 'window.addActivity = function(event)' in line:
        in_addActivity = True
        output_lines.append(line)
        i += 1
        continue
    
    if in_addActivity and not in_nested_function:
        # Check if this line starts the nested function definition
        if '// Function to update the type filter dropdown and suggestions' in line:
            # We are entering the nested function. We will skip until the closing brace.
            in_nested_function = True
            nested_indent = len(line) - len(line.lstrip())
            # Skip this line
            i += 1
            continue
    
    if in_nested_function:
        # Skip until we find a line that is just a closing brace at the same indent level
        if line.strip() == '}' and (len(line) - len(line.lstrip())) == nested_indent:
            in_nested_function = False
            # Skip this closing brace line
            i += 1
            continue
        # Skip all other lines in the nested function
        i += 1
        continue
    
    # If we are in addActivity and we encounter the closing brace of addActivity, we exit addActivity
    if in_addActivity and line.strip() == '}' and not in_nested_function:
        in_addActivity = False
        output_lines.append(line)
        i += 1
        continue
    
    output_lines.append(line)
    i += 1

with open('script-enhanced.js', 'w') as f:
    f.writelines(output_lines)

print('Removed nested function definition in addActivity.')
