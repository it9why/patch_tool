import sys

with open('script-enhanced.js', 'r') as f:
    lines = f.readlines()

# We'll remove the saveTemplate and loadTemplate function definitions and any direct calls.
# Also remove the event listeners (already done, but just in case).

output_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    # Skip the entire saveTemplate function
    if line.strip() == 'function saveTemplate() {':
        # Skip until the matching closing brace
        brace_count = 1
        i += 1
        while i < len(lines) and brace_count > 0:
            if '{' in lines[i]:
                brace_count += 1
            if '}' in lines[i]:
                brace_count -= 1
            i += 1
        continue

    # Skip the entire loadTemplate function
    if line.strip() == 'function loadTemplate() {':
        brace_count = 1
        i += 1
        while i < len(lines) and brace_count > 0:
            if '{' in lines[i]:
                brace_count += 1
            if '}' in lines[i]:
                brace_count -= 1
            i += 1
        continue

    # Remove any direct calls to saveTemplate or loadTemplate (except the event listeners we already removed)
    # We'll just skip lines that contain these function calls? Not necessary.

    # Also remove the event listeners for saveTemplateBtn and loadTemplateBtn (they were already removed in the previous step, but just in case we missed)
    # We'll keep the line if it's not an event listener for these.

    output_lines.append(line)
    i += 1

# Now, we need to also remove the DOM references for saveTemplateBtn and loadTemplateBtn (they were already removed in the previous step).
# Let's check: the lines with const saveTemplateBtn and const loadTemplateBtn were removed earlier.

# Write the updated file
with open('script-enhanced.js', 'w') as f:
    f.writelines(output_lines)

print("Removed saveTemplate and loadTemplate functions")
