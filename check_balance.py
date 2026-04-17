import sys

with open('script-enhanced.js', 'r') as f:
    content = f.read()

stack = []
line_number = 1
for i, ch in enumerate(content):
    if ch == '\n':
        line_number += 1
    if ch in '({[':
        stack.append((ch, line_number))
    elif ch in ')}]':
        if not stack:
            print(f'Extra closing {ch} at position {i}, line {line_number}')
            sys.exit(1)
        opening, open_line = stack.pop()
        if (opening == '(' and ch != ')') or (opening == '{' and ch != '}') or (opening == '[' and ch != ']'):
            print(f'Mismatch: {opening} at line {open_line} closed by {ch} at line {line_number}')
            sys.exit(1)

if stack:
    for opening, open_line in stack:
        print(f'Unclosed {opening} at line {open_line}')
else:
    print('All braces and parentheses are balanced.')
