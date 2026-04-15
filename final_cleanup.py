import sys
import re

with open('script-enhanced.js', 'r') as f:
    content = f.read()

# Remove the alert we added for debugging
content = re.sub(r'\n\s*alert\("Add activity function called!"\);\s*', '\n', content)

# Remove the duplicate console.log for addActivity function call (keep the one we added earlier)
# We'll keep the first console.log and remove any extra ones.
# Actually, we want to keep the console.log we added at the beginning of addActivity.
# We'll leave it as is.

# Also, remove the duplicate comments for renderActivitiesList (already done)

# Write back
with open('script-enhanced.js', 'w') as f:
    f.write(content)

print("Removed alert from addActivity function")
