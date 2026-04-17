import re

with open('script-enhanced.js', 'r') as f:
    content = f.read()

# Replace all occurrences of 'dependencySelect' with 'dependenciesSelect'
content = re.sub(r'\bdependencySelect\b', 'dependenciesSelect', content)

with open('script-enhanced.js', 'w') as f:
    f.write(content)

print('Fixed variable name: dependencySelect -> dependenciesSelect')
