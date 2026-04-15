import sys

with open('script-enhanced.js', 'r') as f:
    lines = f.readlines()

# Count braces to see if they are balanced.
balance = 0
for line in lines:
    balance += line.count('{')
    balance -= line.count('}')

print(f"Brace balance: {balance}")

# If balance is not zero, we need to fix.
# The error is at the end, so we can try to remove the last line and see the balance.
# But note: the last line is '});' which contains both '}' and ')'.

# Let's see the last few lines.
print("\nLast 10 lines:")
for i, line in enumerate(lines[-10:], start=len(lines)-9):
    print(f"{i}: {line.rstrip()}")

# We see that there is an extra '}' at line 943 (the line before the last line).
# Actually, line 943 is a single '}' and line 944 is '});'. That means we have two '}' in a row.
# The generateId function ends at line 942? Let's check.

# We'll look at lines 930-950.
print("\nLines 930-950:")
for i in range(929, min(950, len(lines))):
    print(f"{i+1}: {lines[i].rstrip()}")

# It seems that the generateId function is closed, then there is an extra '}' that closes the DOMContentLoaded function,
# and then the last line is '});' which is an extra closing.

# Actually, the DOMContentLoaded function should be closed by the last line. So we have:
#   } // closes generateId
#   } // closes DOMContentLoaded? Wait, the DOMContentLoaded function was opened at line 1.

# Let's find the opening of DOMContentLoaded.
for i, line in enumerate(lines):
    if 'DOMContentLoaded' in line and '{' in line:
        print(f"DOMContentLoaded opened at line {i+1}")

# We'll try to remove the extra '}' at line 943 (which is the second to last line).
# But note: the last line is '});' and it must stay to close the function and the event listener.

# Actually, the structure should be:
#   ... code ...
#   function generateId() { ... }
#   }); // closes DOMContentLoaded

# So we have an extra '}' before the last line. Let's remove it.

# We'll remove the line that is just '}' and then adjust the last line to be '});' if it isn't already.

# Find the line that is exactly '}' (with possible whitespace) and is the second to last line.
for i in range(len(lines)-2, -1, -1):
    if lines[i].strip() == '}':
        print(f"Found extra '}' at line {i+1}. Removing it.")
        del lines[i]
        break

# Now, the last line should be '});'. If it isn't, we can set it.
if lines[-1].strip() != '});':
    lines[-1] = '});\n'

# Write back
with open('script-enhanced.js', 'w') as f:
    f.writelines(lines)

print("Fixed extra brace.")
