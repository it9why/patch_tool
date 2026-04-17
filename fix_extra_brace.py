import sys

with open('script-enhanced.js', 'r') as f:
    lines = f.readlines()

# Look for the extra closing brace. We'll examine lines 340-350.
# We see two consecutive lines with just '    }' and then '    }' again.
# We need to remove one of them. Let's find the line numbers.

# We'll find the line that is just '    }' and the next line is also '    }'.
for i in range(len(lines)-1):
    if lines[i].strip() == '}' and lines[i+1].strip() == '}':
        # Keep the first one, remove the second one? Actually we need to see which one is extra.
        # The first one closes the function updateTypeFilterAndSuggestions, the second one is extra.
        # Let's check the context: the function updateTypeFilterAndSuggestions starts earlier.
        # We'll remove the second one (line i+1).
        lines.pop(i+1)
        print(f"Removed extra closing brace at line {i+2}")
        break

# Write back
with open('script-enhanced.js', 'w') as f:
    f.writelines(lines)

print("Fixed extra brace issue")
