import re

with open('script-enhanced.js', 'r') as f:
    lines = f.readlines()

# Find the line with "function generateId() {"
for i, line in enumerate(lines):
    if line.strip() == 'function generateId() {':
        # Find the next line that contains 'return' and then the line after that.
        # We'll insert a '}' after the return line.
        # But note: there might be a line after the return line that is empty or something.
        # We'll look for the line that contains the return statement and then insert a '}' after it.
        # Actually, the function body is only one line: the return statement.
        # So we can insert a '}' after the return line, but before any other line that is not part of the function.
        # Let's assume the function body is exactly one line.
        # We'll find the line with the return statement (i+1) and then insert a '}' after it.
        # But we must be careful not to break the existing structure.
        # Let's look at lines i to i+5.
        for j in range(i, min(i+5, len(lines))):
            if lines[j].strip().startswith('return'):
                # Insert a '}' line after line j, with the same indentation as the function.
                indent = len(lines[i]) - len(lines[i].lstrip())
                lines.insert(j+1, ' ' * indent + '}\n')
                break
        break

# Now we need to ensure that the DOMContentLoaded function is closed with '});' and that there is exactly one '});' at the end.
# Let's find the last line that is '});' and make sure there is a '}' before it for the generateId function.
# We already added the '}' for generateId, so now the last line should be '});' (closing the DOMContentLoaded).
# But we might have an extra '}'? We'll just trust the structure.

# Write back
with open('script-enhanced.js', 'w') as f:
    f.writelines(lines)

print('Added missing closing brace for generateId function.')
