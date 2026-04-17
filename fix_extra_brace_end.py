import sys

with open('script-enhanced.js', 'r') as f:
    lines = f.readlines()

# Find the last two lines that are just '}'
# We'll look for the pattern where two consecutive lines are '}' and then '});'
# Actually, we want to remove the extra '}' before the closing '});'

# We'll scan from the end
for i in range(len(lines)-2, -1, -1):
    if lines[i].strip() == '}' and lines[i+1].strip() == '}' and lines[i+2].strip() == '});':
        # Remove the second '}' (line i+1)
        lines.pop(i+1)
        print("Removed extra '}' at line", i+2)
        break

# Write back
with open('script-enhanced.js', 'w') as f:
    f.writelines(lines)

print("Fixed extra brace at end")
