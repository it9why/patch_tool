import re

with open('script-enhanced.js', 'r') as f:
    lines = f.readlines()

# Find the line containing the typeFilterSelect.addEventListener
for i, line in enumerate(lines):
    if 'typeFilterSelect.addEventListener' in line:
        # Check the next few lines.
        # We expect:
        #     typeFilterSelect.addEventListener('change', function() {
        #         renderActivitiesList();
        #     }
        #     });
        # We want to change to:
        #     typeFilterSelect.addEventListener('change', function() {
        #         renderActivitiesList();
        #     });
        # So we need to delete the line that is just '}' (line i+2) and change the line after that to '});' (but it already is '});'?).
        # Let's see indices.
        # line i: typeFilterSelect.addEventListener('change', function() {
        # line i+1: renderActivitiesList();
        # line i+2: }
        # line i+3: });
        # We'll replace lines i+2 and i+3 with a single line '});'
        if lines[i+2].strip() == '}' and lines[i+3].strip() == '});':
            # Determine indentation of line i
            indent = len(lines[i]) - len(lines[i].lstrip())
            # Create new line for the closing brace with same indentation as line i
            new_line = ' ' * indent + '});\n'
            # Delete lines i+2 and i+3, and insert new_line at i+2
            del lines[i+2]
            del lines[i+2]  # after first deletion, the '});' line is now at i+2
            lines.insert(i+2, new_line)
            break

# Write back
with open('script-enhanced.js', 'w') as f:
    f.writelines(lines)

print('Fixed typeFilterSelect event listener.')
