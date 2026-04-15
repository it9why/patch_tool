import sys

with open('script-enhanced.js', 'r') as f:
    lines = f.readlines()

# Find the line with the alert about date format in editActivityDate function
for i, line in enumerate(lines):
    if "alert('Please enter a valid date in YYYY-MM-DD format');" in line:
        # We need to insert a closing brace after this line, but only if the next line is not already a closing brace.
        # Let's check the next non-empty line.
        j = i + 1
        while j < len(lines) and lines[j].strip() == '':
            j += 1
        if j < len(lines) and lines[j].strip() == '}':
            print("Closing brace already exists")
        else:
            # Insert a line with just '}'
            lines.insert(i+1, '    }\n')
            print("Inserted missing closing brace at line", i+2)
        break

# Also, we need to ensure that the editActivity function is properly closed. But let's first fix the missing brace.

# Write back
with open('script-enhanced.js', 'w') as f:
    f.writelines(lines)

print("Fixed missing brace in editActivityDate function")
