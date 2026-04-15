import sys

with open('script-enhanced.js', 'r') as f:
    lines = f.readlines()

# Find the addActivity function (window.addActivity = function(event))
start = -1
end = -1
brace_count = 0
for i, line in enumerate(lines):
    if 'window.addActivity = function(event)' in line:
        start = i
        brace_count = 1
        for j in range(i+1, len(lines)):
            if '{' in lines[j]:
                brace_count += 1
            if '}' in lines[j]:
                brace_count -= 1
                if brace_count == 0:
                    end = j
                    break
        break

if start == -1 or end == -1:
    print("Could not find addActivity function")
    sys.exit(1)

# Now, we need to insert the alert line before the closing brace.
# But note: there are two alert lines (one inside the function, one outside). We'll remove the one outside.
# Let's first find the line with the alert that is inside the function (should be after console.log).
# We'll reconstruct the function from start to end.

# We'll look for the line with console.log('Activity added:', activity);
# and then we'll insert the alert after that line, but before the function's closing brace.

# Also, note there is an extra alert line after the function (line 149). We'll remove it.

# Let's first remove the extra alert line (the one after the function).
# We'll look for the line that is exactly "        alert('Activity added successfully!');" and is not between start and end.
for i in range(len(lines)):
    if i < start or i > end:
        if "alert('Activity added successfully!');" in lines[i]:
            # Remove this line
            lines[i] = ''

# Now, inside the function, we want to add the alert after the console.log line.
# We'll do this by building a new set of lines for the function.
function_lines = lines[start:end+1]
# Find the index of the console.log line within function_lines.
for i, line in enumerate(function_lines):
    if "console.log('Activity added:', activity);" in line:
        # Insert the alert after this line, but before the next line (which should be the closing brace?).
        # Actually, we see that after the console.log, there is a line with "    }" (the closing brace).
        # So we need to insert before the closing brace.
        # Let's check the next few lines.
        # We'll insert the alert line after the console.log line.
        function_lines.insert(i+1, '        alert("Activity added successfully!");\n')
        break

# Replace the original function lines
lines = lines[:start] + function_lines + lines[end+1:]

# Write back
with open('script-enhanced.js', 'w') as f:
    f.writelines(lines)

print("Fixed addActivity function: moved alert inside and removed duplicate.")
