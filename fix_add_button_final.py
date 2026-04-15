import sys
import re

with open('script-enhanced.js', 'r') as f:
    content = f.read()

# 1. Remove duplicate comments for renderActivitiesList
# The pattern: look for the line "// Enhanced function to render activities list with edit buttons" repeated.
# We'll replace multiple occurrences with a single one.
lines = content.splitlines()
new_lines = []
skip_next = False
for i, line in enumerate(lines):
    if line.strip() == "// Enhanced function to render activities list with edit buttons":
        if i>0 and lines[i-1].strip() == "// Enhanced function to render activities list with edit buttons":
            # Skip this duplicate line
            continue
    new_lines.append(line)

content = '\n'.join(new_lines)

# 2. Add an alert at the beginning of addActivity function for debugging
content = re.sub(r'(function addActivity\(\)\s*\{[^}]*?console\.log\("[^"]*"\);)',
                 r'\1\n        alert("Add activity function called!");', content, count=1)

# 3. Also, make sure the button is not disabled by checking if the element is null and adding a check.
# We already added console.log for addActivityBtn.

with open('script-enhanced.js', 'w') as f:
    f.write(content)

print("Cleaned duplicate comments and added alert to addActivity function")
