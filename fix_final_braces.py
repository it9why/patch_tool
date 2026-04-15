import sys

with open('script-enhanced.js', 'r') as f:
    lines = f.readlines()

# Find the last three lines
# We expect the last line to be '});' and the one before that to be '}'
# But we have two '}' before '});'? Let's examine.

# Remove empty lines at the end
while lines and lines[-1].strip() == '':
    lines.pop()

# Now the last line should be '});'
if lines[-1].strip() == '});':
    # The line before should be '}'
    if lines[-2].strip() == '}':
        # Remove the extra '}'
        lines.pop(-2)
        print("Removed extra '}' before '});'")
    else:
        print("Unexpected structure at end of file")
else:
    print("Last line is not '});'")

# Write back
with open('script-enhanced.js', 'w') as f:
    f.writelines(lines)

print("Fixed final braces")
