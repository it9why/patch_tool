with open('script-enhanced.js', 'r') as f:
    lines = f.readlines()

# Find the line number of "function generateId() {"
generate_id_start = -1
for i, line in enumerate(lines):
    if line.strip() == 'function generateId() {':
        generate_id_start = i
        break

if generate_id_start == -1:
    print("generateId not found")
    exit(1)

# The line before generateId is a comment: "// Helper function to generate unique ID"
# We'll keep everything up to that comment line (including it) and then replace the rest.

# Determine indentation: assume 4 spaces per level.
# The DOMContentLoaded function body is indented by 4 spaces.
# So generateId should be indented by 8 spaces? Let's check the indentation of other inner functions.
# Look at function addActivity, which is defined inside DOMContentLoaded.
add_activity_line = -1
for i, line in enumerate(lines):
    if line.strip() == 'function addActivity() {':
        add_activity_line = i
        break

if add_activity_line != -1:
    indent_len = len(lines[add_activity_line]) - len(lines[add_activity_line].lstrip())
    print(f"addActivity indentation: {indent_len} spaces")
else:
    indent_len = 4  # default

# The generateId function currently has indent_len spaces? Let's see.
current_indent = len(lines[generate_id_start]) - len(lines[generate_id_start].lstrip())
print(f"generateId current indentation: {current_indent} spaces")

# We'll keep the same indentation as other inner functions.
# We'll create new lines for generateId with that indentation.

# We'll keep lines up to the line before the comment? Actually, we want to keep lines up to line generate_id_start-2 (the line before the comment) and then replace from there.
# Let's find the line with the comment.
comment_line = generate_id_start - 1
if lines[comment_line].strip() == '// Helper function to generate unique ID':
    # Keep everything up to the comment line (including it) and then replace the rest.
    new_lines = lines[:comment_line+1]  # include comment
else:
    new_lines = lines[:generate_id_start]  # keep up to the line before generateId

# Now add the generateId function with proper indentation.
# We'll use the same indentation as addActivity.
indent = ' ' * indent_len
new_lines.append(indent + 'function generateId() {\n')
new_lines.append(indent + '    return Date.now().toString(36) + Math.random().toString(36).substr(2);\n')
new_lines.append(indent + '}\n')
# Then close the DOMContentLoaded function.
# The DOMContentLoaded function closing brace should be at indent_len - 4? Actually, the DOMContentLoaded function is at the top level of the file.
# The file starts with "document.addEventListener('DOMContentLoaded', function() {" which is at column 0? Actually, it's at column 0.
# The closing brace for DOMContentLoaded should be at column 0.
new_lines.append('});\n')

# Write the new lines back to the file.
with open('script-enhanced.js', 'w') as f:
    f.writelines(new_lines)

print('Replaced the end of the file.')
