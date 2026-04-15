import sys
import re

with open('script-enhanced.js', 'r') as f:
    content = f.read()

# Change function definition to attach to window
# We'll replace the function addActivity(event) { ... } with window.addActivity = function(event) { ... }
# We need to find the function and replace accordingly.

# We'll use a regex to capture the entire function
pattern = r'(function addActivity\(event\)\s*\{[^}]*(?:\}[^}]*)*\})'
match = re.search(pattern, content, re.DOTALL)
if match:
    func_body = match.group(1)
    # Remove the function keyword and name, and attach to window
    new_func = 'window.addActivity = function(event) ' + func_body[func_body.find('{'):]
    content = content.replace(func_body, new_func)
    print("Changed addActivity to be global (window.addActivity)")
else:
    print("Could not find addActivity function to make global")

# Also, update the event listener to use window.addActivity (but it's the same reference)
# We'll keep as is.

with open('script-enhanced.js', 'w') as f:
    f.write(content)

# Now update the HTML button to add onclick attribute
with open('index.html', 'r') as f:
    html = f.read()

# Find the button with id="addActivity" and add onclick attribute
html = re.sub(r'<button id="addActivity"([^>]*)>', r'<button id="addActivity" onclick="addActivity(event)"\1>', html)

with open('index.html', 'w') as f:
    f.write(html)

print("Added onclick attribute to addActivity button")
