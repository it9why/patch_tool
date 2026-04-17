import re

with open('script-enhanced.js', 'r') as f:
    content = f.read()

# 1. Fix the escaped single quote in the addActivity function.
# Replace `\'Default\'` with `'Default'`.
content = re.sub(r"\\'Default\\'", "'Default'", content)

# 2. Ensure there is a newline after the type declaration before the next statement.
# Look for the pattern: `const type = ...;if (` and replace with `const type = ...;\n        if (`
content = re.sub(r'(const type = typeInput\.value\.trim\(\) \|\| \'Default\'\);if \(!)', r'\1\n        if (!', content)

# 3. Also check for any other occurrences of escaped single quotes in the file that might have been introduced.
content = re.sub(r"\\'", "'", content)

# 4. There might be an issue with the activity object creation: we changed the activity object structure but the regex might have left some extra characters.
# Let's find the activity object creation and make sure it's correct.
# We'll look for the pattern: `const activity = { ... }` in the addActivity function and replace with a clean version.
add_activity_pattern = r'(function addActivity\(\) \{[\s\S]*?)(const activity = \{[\s\S]*?\};)'
def replace_activity_object(match):
    func_start = match.group(1)
    # We'll replace the activity object with a clean one that matches the new structure.
    # The new structure should be:
    # const activity = {
    #     id: generateId(),
    #     name,
    #     duration,
    #     type,
    #     dependencies: dependencies,
    #     startDate: null,
    #     endDate: null
    # };
    # But note that the original object might have been changed. We'll just fix the type property.
    # We'll replace the entire activity object with a clean version.
    # However, we don't want to break other parts. Instead, let's fix the type property if it's missing.
    # We'll look for the existing object and ensure it has a type property.
    # We'll do a simpler fix: replace the line that defines the activity object with a corrected one.
    # We'll assume the object is on multiple lines. Let's capture the whole object and then replace.
    # We'll use a more specific pattern for the object.
    activity_object = match.group(2)
    # If the object does not have a 'type' property, we add it.
    if 'type' not in activity_object:
        # We'll insert after the duration property.
        activity_object = re.sub(r'(duration:\s*duration,)', r'\1\n            type,', activity_object)
    # Also make sure the dependencies property uses the variable 'dependencies' (not 'dependency').
    activity_object = re.sub(r'dependencies:\s*dependency', 'dependencies: dependencies', activity_object)
    return func_start + activity_object

content = re.sub(add_activity_pattern, replace_activity_object, content, flags=re.DOTALL)

# 5. Check for any other syntax errors that might have been introduced by the previous regex replacements.
# For example, double semicolons or missing commas.

# Write the fixed content back
with open('script-enhanced.js', 'w') as f:
    f.write(content)

print('Fixed syntax errors in addActivity function.')
