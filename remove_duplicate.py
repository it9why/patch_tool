import sys

with open('script-enhanced.js', 'r') as f:
    lines = f.readlines()

# Find the start of the duplicate block: line containing "        // Create activity object" after the window.addActivity function.
# We'll look for the line that has that comment and is preceded by a blank line or start of file.
# Actually, we can search for the pattern: after the window.addActivity function, there is a duplicate block starting with that comment.

# First, find the line number of the end of the window.addActivity function (the closing brace).
# The function ends at line with "    }" (the one after alert). We have line numbers from previous output.

# Let's find the line number where the function ends (the first "    }" after the alert line).
# We'll search for "window.addActivity = function(event)" and then find the matching closing brace.

start_func = -1
for i, line in enumerate(lines):
    if 'window.addActivity = function(event)' in line:
        start_func = i
        break

if start_func == -1:
    print("Could not find addActivity function")
    sys.exit(1)

# Find the matching closing brace
brace_count = 0
end_func = -1
for i in range(start_func, len(lines)):
    if '{' in lines[i]:
        brace_count += 1
    if '}' in lines[i]:
        brace_count -= 1
        if brace_count == 0:
            end_func = i
            break

if end_func == -1:
    print("Could not find end of addActivity function")
    sys.exit(1)

print(f"addActivity function ends at line {end_func}")

# Now, find the duplicate block that starts after this function.
# The duplicate block starts with "        // Create activity object" and ends with "    }" (the one that is causing the syntax error).
# We'll look for that comment after end_func.

dup_start = -1
for i in range(end_func+1, len(lines)):
    if '// Create activity object' in lines[i] and 'id: generateId()' in lines[i+1]:
        dup_start = i
        break

if dup_start == -1:
    print("Could not find duplicate block start")
    sys.exit(1)

# Now find the end of this duplicate block (the next "    }" that is at the same indentation level as the start).
# The duplicate block is a full function body duplicate, so it ends with a line that is just "    }" (with 4 spaces? Actually, the code uses 4 spaces per indent, but the duplicate block lines have 8 spaces.)
# Let's find the next line that is exactly "    }" (with 4 spaces) after dup_start.

dup_end = -1
for i in range(dup_start, len(lines)):
    if lines[i].rstrip() == '    }':
        dup_end = i
        break

if dup_end == -1:
    print("Could not find duplicate block end")
    sys.exit(1)

print(f"Duplicate block from line {dup_start} to {dup_end}")

# Remove the duplicate block
lines = lines[:dup_start] + lines[dup_end+1:]

# Write back
with open('script-enhanced.js', 'w') as f:
    f.writelines(lines)

print("Duplicate block removed")
