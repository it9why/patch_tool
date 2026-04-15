import sys
import re

with open('script-enhanced.js', 'r') as f:
    js = f.read()

# Add a check for addActivityBtn being null
# Find the line where addActivityBtn is defined and add a console.log after it
js = re.sub(r'(const addActivityBtn = document\.getElementById\(\'addActivity\'\);)\n',
            r'\1\n    console.log("addActivityBtn found:", addActivityBtn);\n', js)

# Also add a log before adding event listener
js = re.sub(r'(addActivityBtn\.addEventListener\(\'click\', addActivity\);)',
            r'console.log("Adding event listener to addActivityBtn");\n    \1', js)

with open('script-enhanced.js', 'w') as f:
    f.write(js)

print("Added debug logs for addActivity button")
