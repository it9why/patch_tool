import re

with open('script-enhanced.js', 'r') as f:
    lines = f.readlines()

# We'll fix the addActivity function by manually editing the lines.
new_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    # Look for the addActivity function
    if line.strip() == 'function addActivity() {':
        # Keep this line
        new_lines.append(line)
        i += 1
        # Read until the closing brace of the function, but we'll just fix the specific lines.
        # We'll collect the function lines and rewrite them.
        # For simplicity, we'll replace the entire function with a corrected version.
        # Let's find the end of the function by counting braces.
        brace_count = 1
        func_lines = [line]
        i_start = i
        while i < len(lines) and brace_count > 0:
            l = lines[i]
            func_lines.append(l)
            if '{' in l:
                brace_count += 1
            if '}' in l:
                brace_count -= 1
            i += 1
        # Now we have the function lines in func_lines.
        # We'll rewrite the function with corrections.
        # First, join them to a string for easier replacement.
        func_str = ''.join(func_lines)
        # Fix the missing newline after the type declaration.
        func_str = re.sub(r'(const type = typeInput\.value\.trim\(\) \|\| \'Default\'\);)\s*if \(!name\)', r'\1\n        if (!name)', func_str)
        # Fix the activity object to include type.
        # We'll replace the activity object with one that includes type.
        # Pattern: const activity = { ... };
        # We'll capture the object and modify it.
        # We'll do a simple replacement: after 'duration,' insert 'type,'.
        func_str = re.sub(r'(duration,\s*)', r'\1            type,\n            ', func_str)
        # Also ensure the dependencies property is correct (should be dependencies: dependencies).
        # It already is.
        # Now we need to also clear the type input after adding activity.
        # Look for the clearing of inputs and add typeInput.value = '';
        func_str = re.sub(r'(activityNameInput\.value = \'\';[\s\S]*?durationInput\.value = \'1\';)', r'\1\n        typeInput.value = \'\';', func_str)
        # Add the function back to new_lines.
        new_lines.append(func_str)
        # We've already advanced i, so continue without incrementing again.
        continue
    else:
        new_lines.append(line)
        i += 1

# Now we also need to ensure the updateTypeFilterAndSuggestions function exists and is called.
# But we already added it in the previous script. Let's just check for syntax errors in the rest of the file.
# Write the fixed lines back.
with open('script-enhanced.js', 'w') as f:
    f.writelines(new_lines)

print('Fixed addActivity function (type property, newline, and clearing).')
