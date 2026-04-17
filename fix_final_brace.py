import re

with open('script-enhanced.js', 'r') as f:
    lines = f.readlines()

# Find the line that is '});'
for i, line in enumerate(lines):
    if line.strip() == '});':
        # Replace this line with two lines: '}' and '});'
        indent = len(line) - len(line.lstrip())
        lines[i] = ' ' * indent + '}\n' + ' ' * indent + '});\n'
        break

# Write back
with open('script-enhanced.js', 'w') as f:
    f.writelines(lines)

print('Added missing closing brace for DOMContentLoaded function.')
