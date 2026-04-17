import re

with open('script-enhanced.js', 'r') as f:
    lines = f.readlines()

# 1. Remove duplicate updateTypeFilterAndSuggestions function
# Find the second occurrence (the one that appears after the first one)
# We'll look for the pattern "function updateTypeFilterAndSuggestions() {" 
# and remove the entire function block (including the opening and closing braces)
# but we must keep the first one.

found_first = False
output_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    if 'function updateTypeFilterAndSuggestions() {' in line:
        if not found_first:
            # First occurrence - keep it
            found_first = True
            output_lines.append(line)
            i += 1
            # Keep the entire function block
            # Count braces to find the end
            brace_count = 1
            while i < len(lines) and brace_count > 0:
                if '{' in lines[i]:
                    brace_count += 1
                if '}' in lines[i]:
                    brace_count -= 1
                output_lines.append(lines[i])
                i += 1
            continue
        else:
            # Second occurrence - skip it
            i += 1
            # Skip the entire function block
            brace_count = 1
            while i < len(lines) and brace_count > 0:
                if '{' in lines[i]:
                    brace_count += 1
                if '}' in lines[i]:
                    brace_count -= 1
                i += 1
            continue
    output_lines.append(line)
    i += 1

# 2. Add debug logs for the three functions at the end of the script (right before the closing brace of DOMContentLoaded)
# Find the line with "});" that closes the DOMContentLoaded event listener
new_output_lines = []
for line in output_lines:
    new_output_lines.append(line)
    if line.strip() == '});':
        # Insert debug logs before this line
        new_output_lines.pop()  # remove the line temporarily
        new_output_lines.append('    // Debug: check if functions are defined\n')
        new_output_lines.append('    console.log("editActivityDate defined?", typeof window.editActivityDate);\n')
        new_output_lines.append('    console.log("editActivity defined?", typeof window.editActivity);\n')
        new_output_lines.append('    console.log("removeActivity defined?", typeof window.removeActivity);\n')
        new_output_lines.append('});\n')
        break

# Write back
with open('script-enhanced.js', 'w') as f:
    f.writelines(new_output_lines)

print('Removed duplicate updateTypeFilterAndSuggestions and added debug logs.')
