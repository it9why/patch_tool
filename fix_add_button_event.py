import sys
import re

with open('script-enhanced.js', 'r') as f:
    content = f.read()

# 1. Modify addActivity function to accept event parameter and prevent default
# Find the function definition and add event parameter
content = re.sub(r'function addActivity\(\)\s*\{',
                 'function addActivity(event) {\n        if (event) event.preventDefault();', content)

# 2. Also, we should ensure the event listener passes the event.
# It already does because we used addEventListener('click', addActivity).
# That will pass the event object.

# 3. Remove the alert we added earlier (optional) but keep console.log.
# We'll keep the alert for now.

with open('script-enhanced.js', 'w') as f:
    f.write(content)

print("Modified addActivity to prevent default")
