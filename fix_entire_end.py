with open('script-enhanced.js', 'r') as f:
    lines = f.readlines()

# Find the line with the comment "// Helper function to generate unique ID"
comment_idx = -1
for i, line in enumerate(lines):
    if line.strip() == '// Helper function to generate unique ID':
        comment_idx = i
        break

if comment_idx == -1:
    print("Comment not found")
    exit(1)

# We'll keep lines up to the comment line (including the comment) and then add the generateId function and the closing brace.
# But we must also close the DOMContentLoaded function. We need to know the indentation of the inner functions.
# Let's look at the indentation of the addActivity function (or any inner function) to determine the inner function indentation.
inner_indent = None
for line in lines:
    if line.strip().startswith('function ') and '()' in line:
        # This is a function definition. We'll use its indentation as the inner function indentation.
        inner_indent = len(line) - len(line.lstrip())
        break

if inner_indent is None:
    inner_indent = 4  # default

# Now, we'll build the new lines from the start up to the comment line (inclusive).
new_lines = lines[:comment_idx+1]  # include the comment

# Then add the generateId function with the inner_indent.
new_lines.append(' ' * inner_indent + 'function generateId() {\n')
new_lines.append(' ' * (inner_indent + 4) + 'return Date.now().toString(36) + Math.random().toString(36).substr(2);\n')
new_lines.append(' ' * inner_indent + '}\n')
# Now we need to close the DOMContentLoaded function. The DOMContentLoaded function is the outermost function in this file.
# Its indentation is 0 (column 0). So we add a line with '});' at column 0.
new_lines.append('});\n')

# Write the new lines back to the file.
with open('script-enhanced.js', 'w') as f:
    f.writelines(new_lines)

print('Replaced the end of the file with a fixed block.')
