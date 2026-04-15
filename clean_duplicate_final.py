import sys

with open('script-enhanced.js', 'r') as f:
    lines = f.readlines()

# Find the start and end of window.addActivity function
start = -1
end = -1
brace_count = 0
for i, line in enumerate(lines):
    if 'window.addActivity = function(event)' in line:
        start = i
        brace_count = 1
        for j in range(i+1, len(lines)):
            if '{' in lines[j]:
                brace_count += 1
            if '}' in lines[j]:
                brace_count -= 1
                if brace_count == 0:
                    end = j
                    break
        break

if start == -1 or end == -1:
    print("Could not find window.addActivity function")
    sys.exit(1)

print(f"Function from line {start+1} to {end+1}")

# Now, we need to find duplicate block after the function.
# The duplicate block starts with "        // Create activity object" and continues until a closing brace.
# Let's find the first occurrence of "        // Create activity object" after the function.
dup_start = -1
for i in range(end+1, len(lines)):
    if '// Create activity object' in lines[i] and 'id: generateId()' in lines[i+1]:
        dup_start = i
        break

if dup_start != -1:
    # Find the matching closing brace for this duplicate block.
    # The duplicate block is inside a function? Actually, it seems to be a stray block.
    # Let's find the next line that contains "    }" with the same indentation.
    # We'll assume it ends at the next line that is just a closing brace with the same indentation as the start.
    # The start line has 8 spaces? Let's check the indentation.
    # We'll look for the next line that starts with 8 spaces and is just '}'.
    for i in range(dup_start, len(lines)):
        if lines[i].strip() == '}':
            dup_end = i
            break
    else:
        dup_end = -1
    
    if dup_end != -1:
        print(f"Duplicate block from line {dup_start+1} to {dup_end+1}")
        # Remove the duplicate block
        lines = lines[:dup_start] + lines[dup_end+1:]
    else:
        print("Could not find end of duplicate block")
else:
    print("No duplicate block found")

# Also, there might be a stray line "        // Create activity object" that is not part of a block? Let's just remove the entire duplicate block.

# Write back
with open('script-enhanced.js', 'w') as f:
    f.writelines(lines)

print("Cleaned duplicate block")
