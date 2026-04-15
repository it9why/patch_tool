import sys

with open('script-enhanced.js', 'r') as f:
    lines = f.readlines()

# Find the start of the window.addActivity function
start_idx = -1
for i, line in enumerate(lines):
    if 'window.addActivity = function(event)' in line:
        start_idx = i
        break

if start_idx == -1:
    print("Could not find addActivity function")
    sys.exit(1)

# Find the end of the function by counting braces
brace_count = 0
end_idx = -1
for i in range(start_idx, len(lines)):
    if '{' in lines[i]:
        brace_count += 1
    if '}' in lines[i]:
        brace_count -= 1
        if brace_count == 0:
            end_idx = i
            break

if end_idx == -1:
    print("Could not find end of addActivity function")
    sys.exit(1)

print(f"Function spans lines {start_idx+1} to {end_idx+1}")

# Now, we see that after the function ends, there is duplicate code until another '}'.
# Let's find the next '}' after the function that is at the same indentation level as the function?
# Actually, the duplicate block starts at line end_idx+1 and continues until the next '}' that is at the same level as the function? 
# But note: the function is inside the DOMContentLoaded event handler, so the duplicate block is inside that handler too.

# We'll look for the next line after the function that starts with "        if (duration < 1) {" and then find its matching '}'.
# Let's find the start of the duplicate block.
dup_start = -1
for i in range(end_idx+1, len(lines)):
    if 'if (duration < 1) {' in lines[i]:
        dup_start = i
        break

if dup_start == -1:
    print("No duplicate block found")
else:
    # Find the end of the duplicate block by counting braces from dup_start
    dup_brace_count = 0
    dup_end = -1
    for i in range(dup_start, len(lines)):
        if '{' in lines[i]:
            dup_brace_count += 1
        if '}' in lines[i]:
            dup_brace_count -= 1
            if dup_brace_count == 0:
                dup_end = i
                break
    
    if dup_end == -1:
        print("Could not find end of duplicate block")
    else:
        print(f"Duplicate block spans lines {dup_start+1} to {dup_end+1}")
        # Remove the duplicate block
        lines = lines[:dup_start] + lines[dup_end+1:]

# Write back
with open('script-enhanced.js', 'w') as f:
    f.writelines(lines)

print("Removed duplicate block")
