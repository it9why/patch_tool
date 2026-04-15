import sys

with open('script-enhanced.js', 'r') as f:
    lines = f.readlines()

# Find the window.addActivity function
start = -1
end = -1
for i, line in enumerate(lines):
    if 'window.addActivity = function(event)' in line:
        start = i
        # find matching brace
        brace_count = 0
        for j in range(i, len(lines)):
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

# Extract function lines
function_lines = lines[start:end+1]

# Remove the function from its current location
lines = lines[:start] + lines[end+1:]

# Now find the line where we add event listener (the line with addActivityBtn.addEventListener)
event_listener_line = -1
for i, line in enumerate(lines):
    if 'addActivityBtn.addEventListener' in line and 'click' in line:
        event_listener_line = i
        break

if event_listener_line == -1:
    print("Could not find event listener line")
    sys.exit(1)

# Insert the function definition right before the event listener line
lines = lines[:event_listener_line] + function_lines + lines[event_listener_line:]

# Write back
with open('script-enhanced.js', 'w') as f:
    f.writelines(lines)

print("Moved addActivity function before event listener")
