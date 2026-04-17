import re

with open('script-enhanced.js', 'r') as f:
    lines = f.readlines()

# Function to add a console.log at the beginning of a function
def add_log_to_function(lines, start_line_index):
    # Find the opening brace after the function definition.
    # We'll search from start_line_index forward.
    i = start_line_index
    while i < len(lines):
        if '{' in lines[i]:
            # Insert a console.log line after this line
            indent = len(lines[i]) - len(lines[i].lstrip())
            log_line = ' ' * indent + 'console.log("Function called with id:", id);\n'
            lines.insert(i + 1, log_line)
            return i + 2  # Return the new line index after insertion
        i += 1
    return start_line_index

# Find each function and add log
for i, line in enumerate(lines):
    if 'window.editActivityDate = function(id)' in line:
        add_log_to_function(lines, i)
    elif 'window.editActivity = function(id)' in line:
        add_log_to_function(lines, i)
    elif 'window.removeActivity = function(id)' in line:
        add_log_to_function(lines, i)

with open('script-enhanced.js', 'w') as f:
    f.writelines(lines)

print('Added console.log statements to editActivityDate, editActivity, removeActivity.')
