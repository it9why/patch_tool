import sys
import re

# 1. Remove the debugging alert at the beginning of addActivity and add a success alert at the end.
with open('script-enhanced.js', 'r') as f:
    js = f.read()

# Remove the alert we added for debugging at the beginning.
js = re.sub(r'\n\s*alert\("Adding activity\.\.\."\);\s*\n', '\n', js)

# Add a success alert at the end of the function, just before the closing brace.
# We need to find the addActivity function and insert before the last line (which is '}').
# We'll look for the pattern: console.log('Activity added:', activity);\n    }
# and replace with: console.log('Activity added:', activity);\n        alert('Activity added successfully!');\n    }
js = re.sub(r'(console\.log\(\'Activity added:\', activity\);\s*\n\s*\})',
            r'\1\n        alert(\'Activity added successfully!\');', js)

with open('script-enhanced.js', 'w') as f:
    f.write(js)

print("Replaced debugging alert with success alert at the end of addActivity")

# 2. Check if the button is inside a form by looking at the HTML structure.
with open('index.html', 'r') as f:
    html = f.read()

# Find the button and see if there is a form tag before it.
# We'll just check if there is any <form> tag in the file.
if '<form' in html.lower():
    print("WARNING: Found a form tag in index.html. This might cause page reload.")
    # We can try to add an onsubmit handler to prevent default, but let's first see the structure.
    # We'll also ensure the button has type="button". We already added that.
else:
    print("No form tag found in index.html.")

# 3. Ensure the button has type="button" (we already did, but double-check)
if 'type="button"' in html or "type='button'" in html:
    print("Button has type='button' attribute.")
else:
    print("Button does NOT have type='button' attribute. Adding it.")
    html = re.sub(r'<button id="addActivity"', '<button id="addActivity" type="button"', html)
    with open('index.html', 'w') as f:
        f.write(html)

# 4. Also, check if there is any other event listener that might interfere with the button.
# We'll look for any other addEventListener for the addActivityBtn.
# But we can't do much about that.

# 5. Let's also ensure that the addActivity function is attached to window (we already did) and that the event listener is using the same function.
# The event listener uses addActivity, which is now window.addActivity, so it's the same.

# 6. Let's add a fallback: if the event listener fails, we can also attach the function via onclick in the HTML.
# But we already tried that and removed it. Let's not do it again.

print("Final fixes applied. Please test the application.")
