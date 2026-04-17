import re

with open('script-enhanced.js', 'r') as f:
    lines = f.readlines()

# Count total lines
total_lines = len(lines)

# Find the line number of the start of the DOMContentLoaded function (line containing "document.addEventListener('DOMContentLoaded', function() {")
start_line = -1
for i, line in enumerate(lines):
    if "document.addEventListener('DOMContentLoaded', function()" in line:
        start_line = i
        break

if start_line == -1:
    print("Could not find DOMContentLoaded start.")
    exit(1)

# Now we need to find the matching closing brace for the entire function.
# We'll count braces from start_line.
brace_count = 0
for i in range(start_line, total_lines):
    line = lines[i]
    for ch in line:
        if ch == '{':
            brace_count += 1
        elif ch == '}':
            brace_count -= 1
        # When brace_count becomes 0, we have closed the DOMContentLoaded function.
        # However, note that there might be nested functions. We'll just rely on the fact that the entire file ends with '});' and we want to replace the last '});' with the correct one.
        # Actually, we can just fix the last two lines of the file.

# Let's look at the last 5 lines.
last_lines = lines[-5:]
print("Last 5 lines before fix:")
for i, line in enumerate(last_lines):
    print(f"{total_lines-5+i}: {line.rstrip()}")

# The issue is that there is an extra '});' at the end. Let's check the last two lines:
# We expect:
#     }
# });
# But we have:
#     }
# 
# });
# Actually, looking at the tail output, we have:
#     }
# 
# });
# There is an empty line? Let's see the exact characters.

# Let's remove any empty lines at the end and ensure there is exactly one '});' after the '}' of the generateId function.
# We'll remove the last line and then add the correct closing.

# Find the index of the last non-empty line.
last_nonempty = total_lines - 1
while last_nonempty >= 0 and lines[last_nonempty].strip() == '':
    last_nonempty -= 1

# Now the last non-empty line should be '});' (line 1092).
# The line before that should be '}' (closing the generateId function) but we see an empty line? Actually, the tail output shows:
#    }
# 
# });
# So there is an empty line between '}' and '});'. We need to remove that empty line and ensure the '});' is directly after the '}' with the correct indentation.

# Let's rebuild the last few lines from the start of the generateId function.
# We'll find the line with "function generateId() {"
generate_id_start = -1
for i in range(total_lines):
    if lines[i].strip() == 'function generateId() {':
        generate_id_start = i
        break

if generate_id_start == -1:
    print("Could not find generateId function.")
    exit(1)

# Now we'll keep everything up to the return line, then a '}', then the '});' (closing the DOMContentLoaded).
# Let's create a new list of lines up to the return line, then add the '}', then the '});'.
# But note that there might be other functions after generateId? There aren't.

# We'll slice the lines up to the line with the return statement, then add the '}', then the '});'.
# Let's find the return line and the line after that (which should be the '}' we added and then the '});').
for i in range(generate_id_start, total_lines):
    if lines[i].strip().startswith('return'):
        return_line = i
        break

# Now, we want to keep lines from 0 to return_line (inclusive), then add a '}', then the '});'.
# We'll also need to remove everything after that until the end of the file.
# Let's do:

new_lines = lines[:return_line+1]  # up to and including the return line
# Add the closing brace of generateId with the same indentation as the function.
indent = len(lines[generate_id_start]) - len(lines[generate_id_start].lstrip())
new_lines.append(' ' * indent + '}\n')
# Add the closing of the DOMContentLoaded function.
new_lines.append('});\n')

# Write the new lines back to the file.
with open('script-enhanced.js', 'w') as f:
    f.writelines(new_lines)

print('Fixed the ending of the file.')
