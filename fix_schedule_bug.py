import sys

with open('script-enhanced.js', 'r') as f:
    lines = f.readlines()

# Replace toMillis with valueOf
for i, line in enumerate(lines):
    if 'toMillis()' in line:
        lines[i] = line.replace('toMillis()', 'valueOf()')

with open('script-enhanced.js', 'w') as f:
    f.writelines(lines)

print("Fixed toMillis() -> valueOf() in calculateSchedule")
