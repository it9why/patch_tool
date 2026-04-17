import sys

with open('script-enhanced.js', 'r') as f:
    content = f.read()

# Find the renderActivitiesList function (the new one with filterType parameter)
# We'll replace the entire function with a corrected version.
# Let's locate the function definition.

# We'll use a regex to capture the function from 'function renderActivitiesList(filterType = '') { ... }'
# up to the next closing brace that matches the function's scope.
# However, due to nested braces, we need a more careful approach.

# Instead, we can fix just the problematic line by finding and replacing it.
# The line we need to fix contains:
#   ${activity.startDate ? `<p>Schedule: ${formatDate(activity.startDate)} - ${formatDate(activity.endDate)}</p>` : ''}
# We want to change it to:
#   ${activity.startDate ? '<p>Schedule: ' + formatDate(activity.startDate) + ' - ' + formatDate(activity.endDate) + '</p>' : ''}

import re

# Pattern to match the problematic line (note the backslashes in the file)
pattern = r'\\\$\\{activity\.startDate \? `<p>Schedule: \\\$\\{formatDate\(activity\.startDate\)} - \\\$\\{formatDate\(activity\.endDate\)}</p>` : \'\'\\\}'

# The line in the file has escaped backslashes, so we need to match exactly.
# Let's look for the line with a more generic pattern.

# We'll split the content into lines and find the line that contains the nested template.
lines = content.splitlines()
new_lines = []
for line in lines:
    if '${activity.startDate ? `<p>Schedule: ${formatDate(activity.startDate)} - ${formatDate(activity.endDate)}</p>`' in line:
        # Replace the nested template with concatenation
        new_line = line.replace(
            '${activity.startDate ? `<p>Schedule: ${formatDate(activity.startDate)} - ${formatDate(activity.endDate)}</p>` : \'\'}',
            '${activity.startDate ? \'<p>Schedule: \' + formatDate(activity.startDate) + \' - \' + formatDate(activity.endDate) + \'</p>\' : \'\'}'
        )
        new_lines.append(new_line)
    else:
        new_lines.append(line)

# Write back
with open('script-enhanced.js', 'w') as f:
    f.write('\n'.join(new_lines))

print("Fixed the nested template literal in renderActivitiesList")
