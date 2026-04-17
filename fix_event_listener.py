import re

with open('script-enhanced.js', 'r') as f:
    lines = f.readlines()

# Find the problematic lines (around line 62) and fix them.
for i, line in enumerate(lines):
    if 'typeFilterSelect.addEventListener' in line and i+2 < len(lines):
        # Check if the next two lines are the function and then an extra '}'
        if lines[i+1].strip() == 'renderActivitiesList();' and lines[i+2].strip() == '}' and lines[i+3].strip() == '});':
            # We need to adjust: the function should be closed with '});' after the '}'
            # The current structure is:
            #     typeFilterSelect.addEventListener('change', function() {
            #         renderActivitiesList();
            #     }
            #     });
            # We want:
            #     typeFilterSelect.addEventListener('change', function() {
            #         renderActivitiesList();
            #     });
            # So we remove the extra '}' line and adjust the '});' line.
            # Let's replace lines[i] to lines[i+3] with the corrected version.
            indent = len(lines[i]) - len(lines[i].lstrip())
            new_lines = [
                lines[i].rstrip() + '\n',
                ' ' * (indent + 4) + 'renderActivitiesList();\n',
                ' ' * indent + '});\n'
            ]
            # We'll replace the four lines with three lines.
            # We'll do this by deleting the four lines and inserting the three.
            del lines[i:i+4]
            for j, nl in enumerate(new_lines):
                lines.insert(i+j, nl)
            break

# Write back
with open('script-enhanced.js', 'w') as f:
    f.writelines(lines)

print('Fixed event listener syntax.')
