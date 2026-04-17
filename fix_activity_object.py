import sys

with open('script-enhanced.js', 'r') as f:
    lines = f.readlines()

# Fix the activity object in addActivity function
for i, line in enumerate(lines):
    if 'type: type,            endDate: null' in line:
        lines[i] = '            type: type,\n'
        # Insert a new line after this line
        lines.insert(i+1, '            endDate: null\n')
        break

# Also fix the similar pattern in the import function? Let's check for other occurrences.
# We'll search for 'type: type,' followed by spaces and 'endDate: null'
for i, line in enumerate(lines):
    if 'type: type,' in line and 'endDate: null' in line and line.count(',') > 1:
        # Replace with two lines
        lines[i] = '            type: type,\n'
        lines.insert(i+1, '            endDate: null\n')
        break

# Write back
with open('script-enhanced.js', 'w') as f:
    f.writelines(lines)

print("Fixed activity object syntax")
