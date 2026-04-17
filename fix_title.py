import re

with open('script-enhanced.js', 'r') as f:
    content = f.read()

# Replace the dayElement.title assignment with string concatenation.
# Find line with: dayElement.title = `Scheduled activities: ${scheduledActivities.map(a => a.name).join(', ')}`;
# Replace with: dayElement.title = 'Scheduled activities: ' + scheduledActivities.map(a => a.name).join(', ');

pattern = r'dayElement\.title = `Scheduled activities: \$\{scheduledActivities\.map\(a => a\.name\)\.join\(\', \'\)\}`;'

new_line = "                dayElement.title = 'Scheduled activities: ' + scheduledActivities.map(a => a.name).join(', ');"

content = re.sub(pattern, new_line, content)

with open('script-enhanced.js', 'w') as f:
    f.write(content)

print('Fixed dayElement.title')
