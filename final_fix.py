import re

with open('script-enhanced.js', 'r') as f:
    content = f.read()

# 1. Fix the editActivityDate function: remove the escaped backslashes in the prompt argument.
# Find the line with: activity.startDate ? activity.startDate.toISODate() : \'\');
# Replace with: activity.startDate ? activity.startDate.toISODate() : '';
content = content.replace(
    "activity.startDate ? activity.startDate.toISODate() : \\'\\');",
    "activity.startDate ? activity.startDate.toISODate() : '');"
)

# 2. Remove duplicate nested definitions of updateTypeFilterAndSuggestions.
# We'll keep the top-level definition (the one after the initialization block) and remove the ones nested inside addActivity, editActivity, removeActivity, clearAll, handleFileImport, deleteActivitiesByType.
# We'll do this by replacing each nested function definition with just a call to the function.
# We'll look for patterns where the function is defined inside another function.

# First, let's define a helper to remove the nested function and replace with a call.
# We'll use regex to find the nested function and replace with the call.

# Pattern for nested function: it starts with a newline and then spaces and then "function updateTypeFilterAndSuggestions() {"
# and ends with a closing brace at the same indentation level.
# We'll replace the entire nested function with a single line: updateTypeFilterAndSuggestions();
# But we must be careful not to remove the top-level one.

# We'll do multiple passes for each context.

# We'll do a simpler approach: since the nested functions are identical, we can just delete them and keep the call that already exists after the function definition.
# In the code, we see that after each nested function definition, there is a call to updateTypeFilterAndSuggestions(); (sometimes on the same line, sometimes next line).
# We'll remove the function definition and leave the call.

# Let's write a regex that matches from the line with "function updateTypeFilterAndSuggestions() {" up to the next "}" that is at the same indentation level.
# We'll use re.DOTALL to match across lines.

nested_pattern = r'(\s*)// Function to update the type filter dropdown and suggestions\s*\n\s*function updateTypeFilterAndSuggestions\(\) \{[^}]+\}'
# This pattern is too greedy? We'll try to match the smallest block.

# Instead, we'll do line-by-line processing.
lines = content.split('\n')
output_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    # Check if this line starts a nested function definition (look for "function updateTypeFilterAndSuggestions() {")
    # and we are not in the top-level (we can check by looking at the preceding lines for being inside another function).
    # But a simpler heuristic: if the line contains "function updateTypeFilterAndSuggestions() {" and the previous line does not contain "updateTypeFilterAndSuggestions();" (which is the call), then it's a definition.
    # We'll just remove all nested definitions and keep the top one.
    # We'll keep the top-level definition which appears after the line "updateDependenciesSelect();" and before the next function.
    # Actually, we can keep the first occurrence and remove the rest.
    # Let's do that.

    if 'function updateTypeFilterAndSuggestions() {' in line:
        # Check if this is the first occurrence (top-level) by seeing if we have already added a definition.
        # We'll keep the first one and skip the rest.
        if 'updateTypeFilterAndSuggestions' not in '\n'.join(output_lines):
            # Keep this definition and the following lines until the closing brace.
            # We'll add the entire function block.
            # Find the closing brace at the same indentation level.
            indent = len(line) - len(line.lstrip())
            output_lines.append(line)
            i += 1
            while i < len(lines):
                current_line = lines[i]
                if current_line.strip() == '}' and len(current_line) - len(current_line.lstrip()) == indent:
                    output_lines.append(current_line)
                    i += 1
                    break
                output_lines.append(current_line)
                i += 1
            continue
        else:
            # Skip this nested definition entirely, but we must also skip the closing brace and the call that follows? The call is on a separate line.
            # We'll just skip until the matching '}'.
            indent = len(line) - len(line.lstrip())
            i += 1
            while i < len(lines):
                if lines[i].strip() == '}' and len(lines[i]) - len(lines[i].lstrip()) == indent:
                    i += 1
                    break
                i += 1
            # Now we are after the function definition. The next line might be a call to updateTypeFilterAndSuggestions(); we want to keep that call.
            # So we don't skip the call.
            continue
    output_lines.append(line)
    i += 1

content = '\n'.join(output_lines)

# 3. Fix the editActivity function: there is a stray backslash in the alert line.
# Find: alert(\'Duration must be a positive number\');
# Replace with: alert('Duration must be a positive number');
content = content.replace(
    "alert(\\'Duration must be a positive number\\');",
    "alert('Duration must be a positive number');"
)

# 4. Also, there is a stray backslash in the editActivity function for the depsPrompt string? Actually, the depsPrompt uses escaped newline characters, which are fine.
# But we need to check for any other escaped single quotes.

# 5. Write the fixed content back.
with open('script-enhanced.js', 'w') as f:
    f.write(content)

print('Fixed syntax errors and removed duplicate nested function definitions.')
