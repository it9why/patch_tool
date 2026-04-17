import re

with open('script-enhanced.js', 'r') as f:
    lines = f.readlines()

# 1. Remove the nested function definition in addActivity.
# We'll find the addActivity function and remove the nested function.
in_addActivity = False
in_nested = False
nested_indent = 0
output_lines = []

i = 0
while i < len(lines):
    line = lines[i]
    
    # Detect entering addActivity
    if 'window.addActivity = function(event)' in line:
        in_addActivity = True
        output_lines.append(line)
        i += 1
        continue
    
    if in_addActivity and not in_nested:
        # Look for the start of the nested function
        if '// Function to update the type filter dropdown and suggestions' in line:
            in_nested = True
            nested_indent = len(line) - len(line.lstrip())
            # Skip this line and the entire nested function
            i += 1
            # Skip until we find a line with just a closing brace at the same indent level
            while i < len(lines):
                cur_line = lines[i]
                if cur_line.strip() == '}' and (len(cur_line) - len(cur_line.lstrip())) == nested_indent:
                    i += 1
                    break
                i += 1
            # After the nested function, there is a call to updateTypeFilterAndSuggestions();
            # We want to keep that call. So we continue without adding the nested function lines.
            continue
    
    if in_addActivity and in_nested:
        # We are inside the nested function, skip lines until we find the closing brace
        # (this should have been handled above, but just in case)
        if line.strip() == '}' and (len(line) - len(line.lstrip())) == nested_indent:
            in_nested = False
            i += 1
            continue
        i += 1
        continue
    
    # Detect leaving addActivity
    if in_addActivity and line.strip() == '}' and not in_nested:
        in_addActivity = False
        output_lines.append(line)
        i += 1
        continue
    
    output_lines.append(line)
    i += 1

# 2. Now we need to add a top-level definition of updateTypeFilterAndSuggestions.
# Find a good place to insert it. We'll insert after the filterActivitiesByType function.
# Let's find the line with "function filterActivitiesByType() {"
new_lines = []
inserted = False
for line in output_lines:
    new_lines.append(line)
    if 'function filterActivitiesByType() {' in line and not inserted:
        # Insert the function definition after the closing brace of filterActivitiesByType.
        # But we need to find the closing brace.
        # We'll do a simple approach: insert after the entire function.
        # We'll keep track of braces.
        pass

# Instead, let's do a simpler approach: insert the function definition right after the line
# where we call updateTypeFilterAndSuggestions in the initialization? Actually, we can insert
# after the definition of filterActivitiesByType.

# Let's parse the file again with a better method.
# We'll use a state machine to find the end of filterActivitiesByType.

with open('script-enhanced.js', 'r') as f:
    content = f.read()

# Remove the nested function in addActivity using regex.
# Pattern: from "// Function to update the type filter dropdown and suggestions" until the next "}" at the same indent level.
# We'll use re.DOTALL to match across lines.
# We'll replace with empty string, but keep the call to updateTypeFilterAndSuggestions(); that follows.
# Actually, the nested function is defined and then called. We want to remove the definition but keep the call.
# So we need to remove the function definition only.

# Let's write a regex that matches the function definition (including the comment) and the following call? No, we'll remove the function definition and leave the call.
# The pattern should match from the comment line to the closing brace of the function, but not the call.

# Since the nested function is inside addActivity, we can target it by looking for the pattern within addActivity.

# Alternatively, we can just delete the nested function and then add a top-level function.

# Let's do a two-step process:
# Step 1: Remove the nested function definition (but not the call) in addActivity.
# Step 2: Add a top-level function definition.

# Step 1:
# We'll find the addActivity function and replace the nested function definition with nothing.
# We'll use a regex that matches the nested function definition.

pattern = r'(\s*// Function to update the type filter dropdown and suggestions\s*\n\s*function updateTypeFilterAndSuggestions\(\) \{[\s\S]*?\n\s*\})'
# Replace with empty string, but we must be careful to only match the nested one.

# We'll do a replacement that removes the nested function definition and leaves the call.
# Actually, the call is on the next line after the function definition? In the code, the call is right after the function definition.
# We want to keep the call, so we remove the function definition and the comment, but leave the call.

# Let's write a more specific pattern that matches the comment, the function, and then the call? No, we'll remove only the function definition.

# We'll do a simpler approach: we'll remove the nested function by deleting the lines in the range we identified earlier.

# We already did that with the line-by-line processing, but we didn't write the result.

# Let's write the output_lines to a string and then insert the top-level function.

temp_content = '\n'.join(output_lines)

# Now, insert the top-level function definition after the filterActivitiesByType function.
# Find the index of the end of filterActivitiesByType.
lines = temp_content.split('\n')
new_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    new_lines.append(line)
    if 'function filterActivitiesByType() {' in line:
        # Find the closing brace of this function.
        brace_count = 1
        j = i + 1
        while j < len(lines):
            if '{' in lines[j]:
                brace_count += 1
            if '}' in lines[j]:
                brace_count -= 1
            if brace_count == 0:
                # We are at the closing brace of filterActivitiesByType.
                # Insert our function definition after this line.
                new_lines.append(lines[j])
                # Insert the top-level function definition after this line.
                new_lines.append('')
                new_lines.append('    // Function to update the type filter dropdown and suggestions')
                new_lines.append('    function updateTypeFilterAndSuggestions() {')
                new_lines.append('        // Get unique types from activities')
                new_lines.append('        const types = [...new Set(state.activities.map(a => a.type || \'Default\'))];')
                new_lines.append('')
                new_lines.append('        // Update the type filter dropdown')
                new_lines.append('        typeFilterSelect.innerHTML = \'<option value="">All Types</option>\';')
                new_lines.append('        types.forEach(type => {')
                new_lines.append('            const option = document.createElement(\'option\');')
                new_lines.append('            option.value = type;')
                new_lines.append('            option.textContent = type;')
                new_lines.append('            typeFilterSelect.appendChild(option);')
                new_lines.append('        });')
                new_lines.append('')
                new_lines.append('        // Update the datalist for suggestions (if it exists)')
                new_lines.append('        const datalist = document.getElementById(\'typeOptions\');')
                new_lines.append('        if (datalist) {')
                new_lines.append('            datalist.innerHTML = \'\';')
                new_lines.append('            types.forEach(type => {')
                new_lines.append('                const option = document.createElement(\'option\');')
                new_lines.append('                option.value = type;')
                new_lines.append('                datalist.appendChild(option);')
                new_lines.append('            });')
                new_lines.append('        }')
                new_lines.append('    }')
                i = j  # We will have already added the closing brace, so skip it in the next iteration.
                break
            j += 1
        i = j + 1
        continue
    i += 1

# Write the result back
with open('script-enhanced.js', 'w') as f:
    f.write('\n'.join(new_lines))

print('Fixed: removed nested function and added top-level updateTypeFilterAndSuggestions.')
