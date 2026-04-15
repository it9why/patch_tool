import sys
import re

# 1. Fix the button in index.html
with open('index.html', 'r') as f:
    html = f.read()

# Add type="button" to the addActivity button
html = re.sub(r'<button id="addActivity" class="btn-primary"(?![^>]*type=)',
              '<button id="addActivity" class="btn-primary" type="button"', html)

with open('index.html', 'w') as f:
    f.write(html)

print("Added type='button' to addActivity button")

# 2. Add a console.log in the addActivity function for debugging
with open('script-enhanced.js', 'r') as f:
    js = f.read()

# Find the addActivity function and insert a console.log at the beginning
# We'll look for the function definition and then the opening brace
# We'll insert after the opening brace of the function body.

# Use a regex to find the function addActivity() { ... }
# We'll capture the function up to the opening brace and then insert.
# We'll do a simple replacement: after 'function addActivity() {' we add a new line with console.log.

js = re.sub(r'(function addActivity\(\)\s*\{)',
            r'\1\n        console.log("addActivity function called");', js)

with open('script-enhanced.js', 'w') as f:
    f.write(js)

print("Added console.log to addActivity function")

