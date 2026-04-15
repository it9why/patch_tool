import sys

with open('script-enhanced.js', 'r') as f:
    lines = f.readlines()

# Find the addActivity function and add code to clear the dependencies select.
# We'll also ensure that the updateDependenciesSelect is called (it already is).

output_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    # Look for the part where we clear inputs in addActivity
    if '// Clear inputs' in line:
        # We'll add after clearing durationInput.value
        # We need to find the line where durationInput.value is set.
        # Let's insert after that line.
        # We'll do a simple insertion: after the line that sets durationInput.value to '1'
        pass

    # Alternatively, we can insert after the line that sets durationInput.value = '1'
    if 'durationInput.value = \'1\';' in line:
        # Insert a line to clear the dependencies select
        output_lines.append(line)
        output_lines.append('\n        // Clear dependencies selection\n')
        output_lines.append('        dependenciesSelect.selectedIndex = -1;\n')
        i += 1
        continue

    output_lines.append(line)
    i += 1

# Write the updated file
with open('script-enhanced.js', 'w') as f:
    f.writelines(output_lines)

print("Added clearing of dependencies select in addActivity function")
