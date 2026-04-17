import re

with open('script-enhanced.js', 'r') as f:
    lines = f.readlines()

# Find the line with "function generateId() {" and then the two '}' lines after the return.
for i, line in enumerate(lines):
    if line.strip() == 'function generateId() {':
        # Find the return line
        for j in range(i, len(lines)):
            if lines[j].strip().startswith('return'):
                # Now we have two '}' lines after the return line? Let's look at lines j+1 and j+2.
                if lines[j+1].strip() == '}' and lines[j+2].strip() == '}':
                    # Remove the extra '}' line (the first one)
                    del lines[j+1]
                    break
        break

# Write back
with open('script-enhanced.js', 'w') as f:
    f.writelines(lines)

print('Removed extra closing brace after generateId function.')
