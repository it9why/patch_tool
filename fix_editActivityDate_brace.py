import sys

with open('script-enhanced.js', 'r') as f:
    content = f.read()

# Find the alert line and the following line that starts a new function.
# We want to insert a closing brace after the alert block, before the next function.
# We'll use a regex to find the pattern.

import re

# Pattern: alert line, then optional whitespace, then a line that starts with "    // Function"
# We'll insert a closing brace after the closing brace of the else block.
# Actually, the else block is already closed with a brace? Let's look at the structure.

# We'll find the line with the alert and then the next non-empty line that is not a comment.
# We'll split into lines.

lines = content.splitlines()
for i, line in enumerate(lines):
    if "alert('Please enter a valid date in YYYY-MM-DD format');" in line:
        # Find the next non-empty line that doesn't start with whitespace? Actually, we are inside the function.
        # We'll look ahead for a line that starts with "    // Function to edit activity"
        for j in range(i+1, len(lines)):
            if lines[j].strip().startswith("// Function to edit activity"):
                # Insert a line with "    }" before this line.
                lines.insert(j, "    }")
                print("Inserted missing closing brace before line", j+1)
                break
        break

# Write back
with open('script-enhanced.js', 'w') as f:
    f.write('\n'.join(lines))

print("Fixed editActivityDate function")
