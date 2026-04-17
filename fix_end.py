with open('script-enhanced.js', 'r') as f:
    lines = f.readlines()

# Remove any trailing empty lines
while lines and lines[-1].strip() == '':
    lines.pop()

# Now the last line should be '});' and the line before should be '}' (closing generateId).
# Let's check.
if len(lines) >= 2:
    print("Second last line:", repr(lines[-2]))
    print("Last line:", repr(lines[-1]))

# We want to ensure the last two lines are:
#     }
# });
# with correct indentation.

# The generateId function starts with an indentation of 4 spaces (one level). Let's find it.
indent = None
for i, line in enumerate(lines):
    if line.strip() == 'function generateId() {':
        indent = len(line) - len(line.lstrip())
        break

if indent is None:
    indent = 4  # fallback

# Now replace the last two lines.
new_last_two = [' ' * indent + '}\n', '});\n']
lines[-2:] = new_last_two

# Write back
with open('script-enhanced.js', 'w') as f:
    f.writelines(lines)

print('Replaced last two lines with correct indentation.')
