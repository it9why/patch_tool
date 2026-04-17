with open('script-enhanced.js', 'r') as f:
    lines = f.readlines()

# Find the line where the loadTemplatesFromStorage function starts
start_idx = -1
for i, line in enumerate(lines):
    if line.strip() == 'function loadTemplatesFromStorage() {':
        start_idx = i
        break

if start_idx == -1:
    print("Could not find loadTemplatesFromStorage function")
    exit(1)

# Determine the base indentation (should be 4 spaces)
# The line itself has some indentation. We'll use that.
base_indent = len(lines[start_idx]) - len(lines[start_idx].lstrip())
print(f"Base indentation for inner functions: {base_indent} spaces")

# Now, we'll replace from start_idx to the end with our new block.
# The new block includes three functions and the closing of DOMContentLoaded.
# We'll construct each line with proper indentation.

new_block = []

# Function loadTemplatesFromStorage
new_block.append(' ' * base_indent + 'function loadTemplatesFromStorage() {\n')
new_block.append(' ' * (base_indent + 4) + 'try {\n')
new_block.append(' ' * (base_indent + 8) + 'const templatesJson = localStorage.getItem(\'activityTemplates\');\n')
new_block.append(' ' * (base_indent + 8) + 'return templatesJson ? JSON.parse(templatesJson) : [];\n')
new_block.append(' ' * (base_indent + 4) + '} catch (error) {\n')
new_block.append(' ' * (base_indent + 8) + 'console.error(\'Error loading templates from storage:\', error);\n')
new_block.append(' ' * (base_indent + 8) + 'return [];\n')
new_block.append(' ' * (base_indent + 4) + '}\n')
new_block.append(' ' * base_indent + '}\n')
new_block.append('\n')

# Function saveTemplatesToStorage
new_block.append(' ' * base_indent + 'function saveTemplatesToStorage(templates) {\n')
new_block.append(' ' * (base_indent + 4) + 'try {\n')
new_block.append(' ' * (base_indent + 8) + 'localStorage.setItem(\'activityTemplates\', JSON.stringify(templates));\n')
new_block.append(' ' * (base_indent + 4) + '} catch (error) {\n')
new_block.append(' ' * (base_indent + 8) + 'console.error(\'Error saving templates to storage:\', error);\n')
new_block.append(' ' * (base_indent + 4) + '}\n')
new_block.append(' ' * base_indent + '}\n')
new_block.append('\n')

# Helper function generateId
new_block.append(' ' * base_indent + '// Helper function to generate unique ID\n')
new_block.append(' ' * base_indent + 'function generateId() {\n')
new_block.append(' ' * (base_indent + 4) + 'return Date.now().toString(36) + Math.random().toString(36).substr(2);\n')
new_block.append(' ' * base_indent + '}\n')
# Closing of DOMContentLoaded function (no indentation)
new_block.append('});\n')

# Replace the lines from start_idx to the end
lines[start_idx:] = new_block

# Write back
with open('script-enhanced.js', 'w') as f:
    f.writelines(lines)

print('Replaced the end of the file with a corrected block.')
