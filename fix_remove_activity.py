import sys

with open('script-enhanced.js', 'r') as f:
    lines = f.readlines()

# Find the removeActivity function
in_remove = False
brace_count = 0
start = -1
for i, line in enumerate(lines):
    if 'window.removeActivity = function(id)' in line:
        start = i
        break

if start == -1:
    print("removeActivity function not found")
    sys.exit(1)

# We'll look for the pattern and fix the missing brace.
# We'll look for the line with the inner if and then the return.
# The structure is:
#        if (dependentActivities.length > 0) {
#            const dependentNames = ...;
#            if (!confirm(...)) {
#                return;
#            }
#        // Missing '}' here
#        // Remove the activity
# We need to insert a '}' after the inner if's block.

# Let's find the line with "if (dependentActivities.length > 0) {"
for i in range(start, len(lines)):
    if 'if (dependentActivities.length > 0)' in lines[i] and '{' in lines[i]:
        # Now we need to find the inner if and then the return.
        # We'll look for the next line that has a return and then a closing brace? Actually, the inner if is one line.
        # Let's find the line that has the inner if and then the return block.
        # We'll count braces until we find the matching closing brace for the outer if.
        # But we know we are missing one, so we can insert a '}' after the inner if's block.

        # We'll look for the line that contains the inner if's closing brace? Actually, the inner if does not have a closing brace because it's a one-liner with return.
        # The inner if is: if (!confirm(...)) { return; }
        # This is a block with one statement. We need to close the outer if after this block.

        # Let's find the line that has the inner if's closing brace (it's the same line as the return? Actually, the inner if's block is:
        #            if (!confirm(`The following activities depend on this one: ${dependentNames}. Do you still want to remove it?`)) {
        #                return;
        #            }
        # So there are two lines: the if line and the return line, and then the closing brace for the inner if is missing? No, the inner if is a block with one statement and then a closing brace.

        # Wait, the code we have does not have a closing brace for the inner if. Let's look at the actual lines:

        # 298:        if (dependentActivities.length > 0) {
        # 299:            const dependentNames = dependentActivities.map(a => a.name).join(', ');
        # 300:            if (!confirm(`The following activities depend on this one: ${dependentNames}. Do you still want to remove it?`)) {
        # 301:                return;
        # 302:            }
        # 303:
        # 304:        // Remove the activity

        # So the inner if does not have a closing brace. Actually, the inner if is a block with a return statement, and the closing brace is missing.

        # We need to fix two issues:
        # 1. The inner if is missing a closing brace.
        # 2. The outer if is missing a closing brace.

        # Let's fix by inserting two closing braces: one for the inner if and one for the outer if.

        # We'll insert a '}' at line 303 (after the return line) and then another '}' at line 304? Actually, we need to close the inner if and then the outer if.

        # The structure should be:
        #        if (dependentActivities.length > 0) {
        #            const dependentNames = ...;
        #            if (!confirm(...)) {
        #                return;
        #            }
        #        }   // This closes the outer if
        #        // Remove the activity

        # But note: the inner if is also a block and should have a closing brace.

        # So we should change lines 300-302 to:
        #            if (!confirm(`The following activities depend on this one: ${dependentNames}. Do you still want to remove it?`)) {
        #                return;
        #            }

        # Actually, the inner if block is already closed by the return? No, in JavaScript, if you have a block, you need a closing brace.

        # Let's look at the original code again. The inner if is written as:
        #            if (!confirm(...)) {
        #                return;
        #            }
        # This is actually correct: the inner if has a block with a return statement and then the closing brace is on line 302? Wait, line 302 is just a line with a closing brace? Actually, in the sed output we don't see a closing brace.

        # Let's examine the exact lines from the file. We'll read the lines from start to start+30.

        for j in range(i, min(i+30, len(lines))):
            print(f"{j}: {lines[j]}", end='')

        # We'll do a more robust fix by counting braces.

        break

print("Need to manually inspect. Let's do a simpler fix: we'll insert a '}' after the inner if block and then another '}' after that to close the outer if.")
print("But we must be careful. Let's write a script that counts braces and inserts the missing ones.")

