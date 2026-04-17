import sys

with open('script-enhanced.js', 'r') as f:
    lines = f.readlines()

# Find the removeActivity function start
start = -1
for i, line in enumerate(lines):
    if 'window.removeActivity = function(id)' in line:
        start = i
        break

if start == -1:
    print("removeActivity function not found")
    sys.exit(1)

# Find the line with the outer if
outer_if = -1
for i in range(start, len(lines)):
    if 'if (dependentActivities.length > 0)' in lines[i] and '{' in lines[i]:
        outer_if = i
        break

if outer_if == -1:
    print("outer if not found")
    sys.exit(1)

# We need to insert a closing brace after the inner if block.
# The inner if block ends at line with '}' (line 297). Actually, the inner if block has a closing brace at line 297.
# We need to insert a '}' after that line, before the comment "// Remove the activity".
# Let's find the line after the inner if block that is not empty and not a comment? Actually, we can insert at line 298 (which is currently empty).

# We'll insert at line index outer_if + 5? Let's do a more robust method: find the line after the inner if's closing brace that is not empty.
# But we know the structure: lines[outer_if] is the outer if, lines[outer_if+1] is const dependentNames..., lines[outer_if+2] is inner if, lines[outer_if+3] is return, lines[outer_if+4] is } (closing inner if), lines[outer_if+5] is empty, lines[outer_if+6] is comment.

# So we can insert at outer_if+5 (the empty line) with a '}'.

insert_index = outer_if + 5  # This is line 298 (0-indexed)
# Check that this line is empty
if lines[insert_index].strip() != '':
    # If not empty, we need to insert before the comment line.
    # Let's find the next line that is not empty? Actually, we can insert at insert_index anyway.
    pass

# Insert a line with 8 spaces and '}'
lines.insert(insert_index, '        }\n')

# Also, there is a duplicate updateTypeFilterAndSuggestions call in this function? Let's look at lines 313-316.
# We'll remove duplicate calls later.

# Write back
with open('script-enhanced.js', 'w') as f:
    f.writelines(lines)

print("Inserted missing closing brace for outer if in removeActivity")
