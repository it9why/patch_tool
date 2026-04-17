import re

with open('script-enhanced.js', 'r') as f:
    lines = f.readlines()

# Function to find the matching closing brace for a function starting at line start_index.
def find_function_end(lines, start_index):
    brace_count = 0
    i = start_index
    while i < len(lines):
        line = lines[i]
        for ch in line:
            if ch == '{':
                brace_count += 1
            elif ch == '}':
                brace_count -= 1
                if brace_count == 0:
                    return i  # line index of the closing brace
        i += 1
    return -1  # not found

# List of function names to wrap
functions = [
    'window.editActivityDate = function(id)',
    'window.editActivity = function(id)',
    'window.removeActivity = function(id)'
]

# We'll process from the bottom to avoid messing up indices
lines = lines  # make a copy? Actually, we'll modify in place but we'll use a new list.
new_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    # Check if this line starts any of the functions we want to wrap
    wrapped = False
    for func in functions:
        if func in line:
            # Find the function end
            end_line = find_function_end(lines, i)
            if end_line == -1:
                # Not found, just copy and break
                break
            # We have from i to end_line inclusive.
            # We want to wrap the function body (excluding the opening and closing braces) in try-catch.
            # We'll extract the function lines and rebuild.
            function_lines = lines[i:end_line+1]
            # Find the opening brace line (should be the same line or next line)
            # We'll assume it's the same line.
            # We'll split the function into three parts: before opening brace, body, and closing brace.
            # But we want to keep the function signature and opening brace, then insert 'try {', then the body, then '} catch (error) { console.error(error); return; }', then the closing brace.
            # Actually, we want:
            #   window.editActivityDate = function(id) {
            #       try {
            #           ... body ...
            #       } catch (error) {
            #           console.error(error);
            #           return;
            #       }
            #   }
            # So we need to:
            #   - Keep the signature line (which includes the opening brace)
            #   - Insert a line with 'try {'
            #   - Then the body (which is everything except the last line (the closing brace))
            #   - Then a line with '} catch (error) {'
            #   - Then a line with 'console.error(error);'
            #   - Then a line with 'return;'
            #   - Then a line with '}'
            #   - Then the original closing brace (but we are already going to have one from the function, so we need to adjust.
            # Actually, the function's original closing brace is the last line of the function_lines.
            # We'll remove the last line (the closing brace) and then add our own closing brace for the try-catch and then the function closing brace.
            # But note: the function's closing brace is the one we found. We want to replace the function's closing brace with:
            #   } catch (error) {
            #       console.error(error);
            #       return;
            #   }
            #   }
            # That's two closing braces: one for the try block and one for the function.
            # So we need to adjust the brace count.
            # Alternatively, we can keep the function's closing brace and just insert the catch block before it.
            # Let's do:
            #   function signature {
            #       try {
            #           ... body ...
            #       } catch (error) {
            #           console.error(error);
            #           return;
            #       }
            #   }
            # So the function's closing brace is the same as the one we have.
            # We'll keep the function's closing brace and put the catch block inside the function, before the function's closing brace.
            # That means we need to remove the function's closing brace, then add the catch block, then add the function's closing brace.
            # But note: the function's body already has a closing brace at the end. We want to replace that closing brace with:
            #   } catch (error) {
            #       console.error(error);
            #       return;
            #   }
            #   }
            # So we need to add an extra closing brace for the try block and then the function's closing brace.
            # Let's break it down:
            #   Original function lines:
            #       line i: window.editActivityDate = function(id) {
            #       ... body lines ...
            #       last line: }
            #   We want:
            #       window.editActivityDate = function(id) {
            #           try {
            #               ... body lines ...
            #           } catch (error) {
            #               console.error(error);
            #               return;
            #           }
            #       }
            #   So we need to:
            #       - Keep the first line (with the opening brace)
            #       - Insert a line with the try block opening brace (with same indentation as the function body)
            #       - Then the body lines (with their original indentation)
            #       - Then a line with the catch block opening (with same indentation as the try block)
            #       - Then two lines for the catch block body (with one more level of indentation)
            #       - Then a line for the catch block closing brace (with same indentation as the try block)
            #       - Then the function closing brace (with original indentation)

            # Determine indentation of the function body (first line after the opening brace)
            # We'll assume the function body is indented by 4 spaces relative to the function signature.
            # We'll get the indentation of the first line of the function body (line i+1).
            if i+1 < len(lines):
                body_line = lines[i+1]
                indent = len(body_line) - len(body_line.lstrip())
            else:
                indent = 4  # fallback

            # Build the new function lines
            new_function_lines = []
            # First line: function signature and opening brace
            new_function_lines.append(line)
            # Line for try block opening
            new_function_lines.append(' ' * indent + 'try {\n')
            # Add the body lines (excluding the first line and the last line (the closing brace))
            # Actually, the body lines are from i+1 to end_line-1 (because the last line is the closing brace of the function)
            for j in range(i+1, end_line):
                new_function_lines.append(lines[j])
            # Now add the catch block
            new_function_lines.append(' ' * indent + '} catch (error) {\n')
            new_function_lines.append(' ' * (indent + 4) + 'console.error(error);\n')
            new_function_lines.append(' ' * (indent + 4) + 'return;\n')
            new_function_lines.append(' ' * indent + '}\n')
            # Finally, the function closing brace (which is the last line of the function)
            new_function_lines.append(lines[end_line])

            # Now we need to replace the original function lines with the new ones in the output.
            # We'll add the new_function_lines to new_lines and skip the original lines.
            new_lines.extend(new_function_lines)
            i = end_line + 1
            wrapped = True
            break

    if not wrapped:
        new_lines.append(line)
        i += 1

# Write the modified content back
with open('script-enhanced.js', 'w') as f:
    f.writelines(new_lines)

print('Wrapped editActivityDate, editActivity, and removeActivity in try-catch blocks.')
