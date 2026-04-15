import re

with open('index.html', 'r') as f:
    content = f.read()

# Find the form-grid div and insert after the dependencies form-group.
# We'll look for the line with the dependencies select and then insert after the next closing div (which is the form-group).
# Actually, we can insert before the form-group for the button.

# We'll use a regex to find the form-grid div and then replace the button form-group with our new form-group and then the button.
# Let's break the content into lines and do line-by-line.

lines = content.splitlines()
new_lines = []
in_form_grid = False
for i, line in enumerate(lines):
    new_lines.append(line)
    if 'form-grid' in line:
        in_form_grid = True
    if in_form_grid and '<div class="form-group">' in line and 'Dependencies' in lines[i+1]:
        # Insert after the closing div of this form-group (we'll find the closing div after the select)
        # We'll look ahead for the closing div of this form-group.
        for j in range(i+1, len(lines)):
            if '</div>' in lines[j] and lines[j-1].strip().endswith('</select>'):
                # Insert after this line
                new_lines.append('                    <div class="form-group">')
                new_lines.append('                        <label for="activityType">Type</label>')
                new_lines.append('                        <input type="text" id="activityType" list="typeOptions" placeholder="e.g., Development">')
                new_lines.append('                        <datalist id="typeOptions">')
                new_lines.append('                            <option value="Development">')
                new_lines.append('                            <option value="Design">')
                new_lines.append('                            <option value="Meeting">')
                new_lines.append('                            <option value="Testing">')
                new_lines.append('                            <option value="Documentation">')
                new_lines.append('                            <option value="Other">')
                new_lines.append('                        </datalist>')
                new_lines.append('                    </div>')
                break

with open('index.html', 'w') as f:
    f.write('\n'.join(new_lines))

print("Updated HTML with Type field")
