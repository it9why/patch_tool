import sys

with open('script-enhanced.js', 'r') as f:
    lines = f.readlines()

# Remove the last line if it is '});'
if lines[-1].strip() == '});':
    last_line = lines.pop()
else:
    last_line = None

# Add a new line with '}'
lines.append('}\n')

# Then add back the last line if we removed it
if last_line:
    lines.append(last_line)

# Write back
with open('script-enhanced.js', 'w') as f:
    f.writelines(lines)

print("Added missing '}' before the last line")
