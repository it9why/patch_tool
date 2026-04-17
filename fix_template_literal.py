import re

with open('script-enhanced.js', 'r') as f:
    content = f.read()

# Find the renderActivitiesList function
# We'll use a regex that captures from the function start to the closing brace that matches the same indentation level.
# But easier: we can do a string replacement on the whole file for the specific pattern within the function.
# However, we must be careful not to replace other occurrences.

# Let's replace all occurrences of r'\${' with '${' in the entire file.
# This should be safe because the only place where we have such pattern is in the renderActivitiesList function.
# But note: there might be other places where we have escaped template literals in strings? Not likely.
# We'll do it globally.
new_content = content.replace(r'\${', '${')

with open('script-enhanced.js', 'w') as f:
    f.write(new_content)

print('Replaced \\${ with ${ in the entire file.')

# Now also need to fix the template literal for the filterType message.
# That line also uses \${filterType} but it's within backticks? Actually, that line is:
# activitiesContainer.innerHTML = `<p class="empty-message">No activities of type "\${filterType}" found.</p>`;
# This should also be fixed by the above replacement.

