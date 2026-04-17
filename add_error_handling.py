import re

with open('script-enhanced.js', 'r') as f:
    content = f.read()

# 1. Wrap editActivityDate function body in try-catch
pattern1 = r'(window\.editActivityDate = function\(id\) \{[\s\S]*?\n    \})'
def replace_editActivityDate(match):
    func = match.group(0)
    # Insert try-catch after the opening brace and the console.log line.
    # We'll replace the function body from after the opening brace to before the closing brace.
    # Let's do a simple approach: split by lines and insert.
    lines = func.split('\n')
    new_lines = []
    for line in lines:
        new_lines.append(line)
        if line.strip() == 'window.editActivityDate = function(id) {':
            new_lines.append('        try {')
        elif line.strip() == '    }':
            new_lines.append('        } catch (error) {')
            new_lines.append('            console.error("Error in editActivityDate:", error);')
            new_lines.append('        }')
    return '\n'.join(new_lines)

content = re.sub(pattern1, replace_editActivityDate, content, flags=re.DOTALL)

# 2. Wrap editActivity function body in try-catch
pattern2 = r'(window\.editActivity = function\(id\) \{[\s\S]*?\n    \})'
def replace_editActivity(match):
    func = match.group(0)
    lines = func.split('\n')
    new_lines = []
    for line in lines:
        new_lines.append(line)
        if line.strip() == 'window.editActivity = function(id) {':
            new_lines.append('        try {')
        elif line.strip() == '    }':
            new_lines.append('        } catch (error) {')
            new_lines.append('            console.error("Error in editActivity:", error);')
            new_lines.append('        }')
    return '\n'.join(new_lines)

content = re.sub(pattern2, replace_editActivity, content, flags=re.DOTALL)

# 3. Wrap removeActivity function body in try-catch
pattern3 = r'(window\.removeActivity = function\(id\) \{[\s\S]*?\n    \})'
def replace_removeActivity(match):
    func = match.group(0)
    lines = func.split('\n')
    new_lines = []
    for line in lines:
        new_lines.append(line)
        if line.strip() == 'window.removeActivity = function(id) {':
            new_lines.append('        try {')
        elif line.strip() == '    }':
            new_lines.append('        } catch (error) {')
            new_lines.append('            console.error("Error in removeActivity:", error);')
            new_lines.append('        }')
    return '\n'.join(new_lines)

content = re.sub(pattern3, replace_removeActivity, content, flags=re.DOTALL)

with open('script-enhanced.js', 'w') as f:
    f.write(content)

print('Added try-catch error handling to the three functions.')
