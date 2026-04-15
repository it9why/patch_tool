import sys

with open('script-enhanced.js', 'r') as f:
    content = f.read()

# Replace all occurrences of 'dependencySelect' (variable) with 'dependenciesSelect'
# But careful not to change the function name if it appears in a string? It doesn't.
content = content.replace('dependencySelect', 'dependenciesSelect')

# Also, note that the function updateDependenciesSelect is defined, but we have changed the variable inside.
# Now, we should also adjust the initial value of the select? The function sets innerHTML to '<option value="">None</option>'
# That is okay for multiple select? We might want to change it to have no default option? Let's keep it for now.

with open('script-enhanced.js', 'w') as f:
    f.write(content)

print("Fixed dependencySelect variable name to dependenciesSelect")
