import re

with open('script-enhanced.js', 'r') as f:
    lines = f.readlines()

# Find the line containing "});" at the end of the file.
for i, line in enumerate(lines):
    if line.strip() == '});':
        # Insert a '}' line before this line if the previous line is not a '}'
        if i > 0 and lines[i-1].strip() != '}':
            lines.insert(i, '    }\n')
            break

# Write back
with open('script-enhanced.js', 'w') as f:
    f.writelines(lines)

print('Added missing closing brace for generateId function.')
