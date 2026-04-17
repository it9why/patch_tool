import re

with open('script-enhanced.js', 'r') as f:
    content = f.read()

# Replace all escaped single quotes with normal single quotes.
content = content.replace("\\'", "'")

# Now fix the activity object in addActivity to include the type property.
# We'll look for the pattern: 
#   const activity = {
#       id: generateId(),
#       name,
#       duration,
#       dependencies: dependencies,
#       startDate: null,
#       endDate: null
#   };
# and change it to include type after duration.

# We'll use a regex to capture the activity object and insert the type property.
# Note: There may be multiple occurrences, but we only want the one in addActivity.
# We'll target the function addActivity and replace the object.

# First, find the addActivity function and then the activity object within it.
# We'll use a more robust method: replace the object that is defined after the comment "// Create activity object".

# Let's break the content into lines and process line by line for better control.
lines = content.split('\n')
new_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    # If we find the line with "const activity = {"
    if line.strip().startswith('const activity = {') and i > 0 and lines[i-1].strip() == '// Create activity object':
        new_lines.append(line)
        i += 1
        # Now we need to collect the object lines until we find the closing brace.
        # We'll keep track of braces.
        brace_count = 1
        obj_lines = []
        while i < len(lines) and brace_count > 0:
            l = lines[i]
            obj_lines.append(l)
            if '{' in l:
                brace_count += 1
            if '}' in l:
                brace_count -= 1
            i += 1
        # Now we have the object lines in obj_lines.
        # We want to insert the type property after the duration property.
        # Let's reconstruct the object with the type property.
        new_obj_lines = []
        for l in obj_lines:
            new_obj_lines.append(l)
            # If the line contains "duration," then we want to insert a line with "type," after it.
            if 'duration,' in l and 'type,' not in l:
                # Insert a line with "type," (same indentation)
                indent = len(l) - len(l.lstrip())
                new_obj_lines.append(' ' * indent + 'type,')
        # Replace the old object lines with the new ones.
        new_lines.extend(new_obj_lines)
        # We have already advanced i, so continue the outer loop without incrementing i again.
        continue
    else:
        new_lines.append(line)
        i += 1

content = '\n'.join(new_lines)

# Write the fixed content back
with open('script-enhanced.js', 'w') as f:
    f.write(content)

print('Fixed escaped single quotes and added type property to activity object.')
