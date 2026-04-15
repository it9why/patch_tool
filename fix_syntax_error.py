import sys
import re

with open('script-enhanced.js', 'r') as f:
    content = f.read()

# The regex replacement we did earlier used escaped quotes incorrectly.
# Let's find the exact line and fix it.

# First, find the addActivity function and replace the problematic line.
# We'll replace the entire function with a corrected version.
# Let's locate the function start and end.

lines = content.splitlines()
in_function = False
start = -1
end = -1
brace_count = 0
for i, line in enumerate(lines):
    if 'window.addActivity = function(event)' in line:
        in_function = True
        start = i
        brace_count = 1
    elif in_function:
        if '{' in line:
            brace_count += line.count('{')
        if '}' in line:
            brace_count -= line.count('}')
            if brace_count == 0:
                end = i
                break

if start == -1 or end == -1:
    print("Could not find addActivity function")
    sys.exit(1)

# Build the corrected function
# We'll keep the original lines but fix the alert line.
# Let's reconstruct the function lines and fix the alert line.

function_lines = lines[start:end+1]
# Find the line with the alert and fix the quotes.
for i in range(len(function_lines)):
    if 'alert(\\'Activity added successfully!\\'):' in function_lines[i]:
        # Replace with proper quotes
        function_lines[i] = function_lines[i].replace('alert(\\'Activity added successfully!\\'):', 'alert("Activity added successfully!");')
    elif 'alert(\\'Activity added successfully!\\');' in function_lines[i]:
        function_lines[i] = function_lines[i].replace('alert(\\'Activity added successfully!\\');', 'alert("Activity added successfully!");')

# Also, there might be a stray backslash in the alert line. Let's just replace the whole line.
# We'll search for the pattern and replace with correct syntax.
new_function_lines = []
for line in function_lines:
    if 'alert(\\'Activity added successfully!' in line:
        new_function_lines.append('        alert("Activity added successfully!");')
    else:
        new_function_lines.append(line)

# Replace the function in the original content
lines = lines[:start] + new_function_lines + lines[end+1:]

# Write back
with open('script-enhanced.js', 'w') as f:
    f.write('\n'.join(lines))

print("Fixed syntax error in addActivity function")
