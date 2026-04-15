import sys

with open('script-enhanced.js', 'r') as f:
    lines = f.readlines()

# We'll look for the pattern where there are two consecutive lines with just '};'
# and remove one of them, but only in the area after editActivity function.

# First, find the start of editActivity function
edit_start = -1
for i, line in enumerate(lines):
    if 'window.editActivity = function(id) {' in line:
        edit_start = i
        break

if edit_start == -1:
    print("Could not find editActivity function")
    sys.exit(1)

# Now, find the end of the function (the first '};' after the start)
# We'll track braces
brace_count = 0
in_function = False
edit_end = -1
for i in range(edit_start, len(lines)):
    if '{' in lines[i]:
        brace_count += 1
        in_function = True
    if '}' in lines[i]:
        brace_count -= 1
        if brace_count == 0 and in_function:
            edit_end = i
            break

if edit_end == -1:
    print("Could not find end of editActivity function")
    sys.exit(1)

# Now, check if there is an extra '};' right after the function end.
# We'll look at the next line that is not empty.
next_line_index = edit_end + 1
while next_line_index < len(lines) and lines[next_line_index].strip() == '':
    next_line_index += 1

# If the next non-empty line is '};', then it's an extra closing brace.
if next_line_index < len(lines) and lines[next_line_index].strip() == '};':
    # Remove that extra line
    lines.pop(next_line_index)
    print("Removed extra closing brace after editActivity function")
else:
    print("No extra closing brace found after editActivity function")

# Write the file back
with open('script-enhanced.js', 'w') as f:
    f.writelines(lines)

print("Fixed editActivity function")
