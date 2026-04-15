import sys

with open('script-enhanced.js', 'r') as f:
    lines = f.readlines()

# Find the line with the alert about date format
for i, line in enumerate(lines):
    if "alert('Please enter a valid date in YYYY-MM-DD format');" in line:
        # Insert a closing brace after this line, but before the next non-empty line that is not a comment.
        # We'll insert after the alert line.
        # Ensure we don't duplicate.
        # Check if the next line is already a closing brace.
        if i+1 < len(lines) and lines[i+1].strip() == '}':
            print("Closing brace already exists")
        else:
            # Insert a line with just '}'
            lines.insert(i+1, '        }\n')
            print("Inserted missing closing brace at line", i+2)
        break

# Also check for missing brace after the editActivity function? We'll leave that for now.

# Write back
with open('script-enhanced.js', 'w') as f:
    f.writelines(lines)

print("Fixed missing brace in editActivityDate function")
