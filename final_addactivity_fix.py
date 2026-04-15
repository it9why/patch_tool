import sys
import re

# 1. Remove onclick attribute from index.html
with open('index.html', 'r') as f:
    html = f.read()

# Remove the onclick attribute we added
html = re.sub(r' onclick="addActivity\(event\)"', '', html)

with open('index.html', 'w') as f:
    f.write(html)

print("Removed onclick attribute from button")

# 2. Ensure the addActivity function is defined and accessible
# We'll keep it as window.addActivity for debugging, but also keep the event listener.

# 3. Add an alert at the beginning of addActivity for immediate feedback
with open('script-enhanced.js', 'r') as f:
    js = f.read()

# Add alert after the console.log
js = re.sub(r'(console\.log\("addActivity function called"\);)\n',
            r'\1\n        alert("Adding activity...");\n', js)

with open('script-enhanced.js', 'w') as f:
    f.write(js)

print("Added alert to addActivity function")

# 4. Also add a check to ensure the button exists and the event listener is added
# We'll add a log right after the event listener line.
js = re.sub(r'(addActivityBtn\.addEventListener\(\'click\', addActivity\);)',
            r'\1\n    console.log("Event listener added to addActivityBtn");', js)

with open('script-enhanced.js', 'w') as f:
    f.write(js)

print("Added log after event listener")
