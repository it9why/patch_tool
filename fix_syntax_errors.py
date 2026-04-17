import re

with open('script-enhanced.js', 'r') as f:
    lines = f.readlines()

# Fix editActivityDate function: move console.log out of prompt arguments
in_editActivityDate = False
for i, line in enumerate(lines):
    if 'window.editActivityDate = function(id)' in line:
        in_editActivityDate = True
    if in_editActivityDate and 'const newStartDate = prompt' in line:
        # The next line is console.log, we need to swap them
        # Actually, we need to move the console.log before the prompt
        # The current structure:
        # line i: const newStartDate = prompt(`Edit start date for "${activity.name}" (YYYY-MM-DD):`, 
        # line i+1: console.log("editActivityDate called with id:", id);
        # line i+2: activity.startDate ? activity.startDate.toISODate() : '');
        # We want:
        # line i: console.log("editActivityDate called with id:", id);
        # line i+1: const newStartDate = prompt(`Edit start date for "${activity.name}" (YYYY-MM-DD):`, 
        # line i+2: activity.startDate ? activity.startDate.toISODate() : '');
        if i+2 < len(lines):
            # Check if line i+1 is the console.log we inserted
            if 'console.log("editActivityDate called with id:"' in lines[i+1]:
                # Swap lines[i] and lines[i+1]
                lines[i], lines[i+1] = lines[i+1], lines[i]
        break

# Fix editActivity function: move console.log out of the condition block
for i, line in enumerate(lines):
    if 'window.editActivity = function(id)' in line:
        # Find the console.log line that is inside the function
        # It's currently after the prompt for newName and before the condition for duration
        # We'll look for the line with the console.log and move it to the beginning of the function
        pass  # We'll handle this by rewriting the function more carefully.

# Instead of complex line manipulations, let's rewrite the function with correct syntax.
# We'll read the entire file as a string and use regex to replace the editActivity function.

with open('script-enhanced.js', 'r') as f:
    content = f.read()

# Replace editActivity function with corrected version
editActivity_pattern = r'window\.editActivity = function\(id\) \{[\s\S]*?\n    \}'
# We'll use a placeholder for the function, but it's better to fix by editing the specific lines.

# Let's do a simpler fix: find the line with the misplaced console.log in editActivity and move it.
# In the file, the function looks like:
#        const newName = prompt('Edit activity name:', activity.name);
#        if (newName === null) return; // User cancelled
#
#        const newDuration = prompt('Edit duration (days):', activity.duration);
#        if (newDuration === null) return;
#
#        const duration = parseInt(newDuration);
#        if (isNaN(duration) || duration < 1) {
#        console.log("editActivity called with id:", id);
#            alert('Duration must be a positive number');
#            return;
#        }
# We need to move the console.log outside the if block.

# We'll do a regex replace for that block.
# First, let's fix the editActivityDate function more robustly.
# We'll replace from the start of editActivityDate to the end of the function? Too complex.

# Instead, let's write a corrected version of the entire function and replace it.
# We'll extract the function and fix it manually.

# However, due to time, let's do a targeted fix for the two functions.

# Fix editActivityDate:
# We'll replace the three lines (prompt, console.log, and the third line) with two lines: console.log first, then prompt.
content = re.sub(
    r'(window\.editActivityDate = function\(id\) \{[\s\S]*?)const newStartDate = prompt\(`Edit start date for "\$\{activity\.name\}" \(YYYY-MM-DD\):`,[\s\S]*?console\.log\("editActivityDate called with id:", id\);[\s\S]*?activity\.startDate \? activity\.startDate\.toISODate\(\) : \'\'\);',
    r'\1        console.log("editActivityDate called with id:", id);\n        const newStartDate = prompt(`Edit start date for "${activity.name}" (YYYY-MM-DD):`, \n            activity.startDate ? activity.startDate.toISODate() : \'\');',
    content,
    flags=re.DOTALL
)

# Fix editActivity:
# We'll move the console.log to the beginning of the function.
content = re.sub(
    r'(window\.editActivity = function\(id\) \{[\s\S]*?)(const activity = state\.activities\.find\(a => a\.id === id\);)',
    r'\1        console.log("editActivity called with id:", id);\n        \2',
    content,
    flags=re.DOTALL
)

# Also, in editActivity, there's a misplaced console.log inside the if block. We'll remove it from there.
content = re.sub(
    r'if \(isNaN\(duration\) \|\| duration < 1\) \{[\s\S]*?console\.log\("editActivity called with id:", id\);[\s\S]*?alert\([\s\S]*?return;[\s\S]*?\}',
    r'if (isNaN(duration) || duration < 1) {\n            alert(\'Duration must be a positive number\');\n            return;\n        }',
    content,
    flags=re.DOTALL
)

# Fix removeActivity: the console.log is already at the beginning, but note that the function has a syntax error:
# We see:
#        console.log("removeActivity called with id:", id);
#        const dependentActivities = state.activities.filter(a => a.dependencies && a.dependencies.includes(id));
#        
#        if (dependentActivities.length > 0) {
#        console.log("removeActivity called with id:", id);
#            const dependentNames = dependentActivities.map(a => a.name).join(', ');
#            if (!confirm(`The following activities depend on this one: ${dependentNames}. Do you still want to remove it?`)) {
#                return;
#            }
#        }
# There's a duplicate console.log. Remove the one inside the if block.
content = re.sub(
    r'if \(dependentActivities\.length > 0\) \{[\s\S]*?console\.log\("removeActivity called with id:", id\);[\s\S]*?const dependentNames',
    r'if (dependentActivities.length > 0) {\n            const dependentNames',
    content,
    flags=re.DOTALL
)

# Now, let's implement the updateTypeFilterAndSuggestions function.
# We need to add a datalist for activity type suggestions. First, check if there's a datalist in the HTML.
# We'll modify the script to update the datalist with unique types from activities.

# We'll add the function definition after the updateDependenciesSelect function.
# We can insert it after the line that updates the dependencies select.

# Find the line with "updateDependenciesSelect();" and then the next function definition.
# We'll insert our function there.

# First, let's create the function.
type_suggestion_function = '''
    // Function to update the type filter dropdown and suggestions
    function updateTypeFilterAndSuggestions() {
        // Get unique types from activities
        const types = [...new Set(state.activities.map(a => a.type || 'Default'))];
        
        // Update the type filter dropdown
        typeFilterSelect.innerHTML = '<option value="">All Types</option>';
        types.forEach(type => {
            const option = document.createElement('option');
            option.value = type;
            option.textContent = type;
            typeFilterSelect.appendChild(option);
        });
        
        // Update the datalist for suggestions (if it exists)
        const datalist = document.getElementById('typeSuggestions');
        if (datalist) {
            datalist.innerHTML = '';
            types.forEach(type => {
                const option = document.createElement('option');
                option.value = type;
                datalist.appendChild(option);
            });
        }
    }
'''

# Find the line with "updateDependenciesSelect();" and then the next function.
# We'll insert after the closing brace of updateDependenciesSelect.
# But note that the function updateDependenciesSelect is defined elsewhere. Let's search for the pattern.
# Actually, we can insert after the call to updateDependenciesSelect in the initialization.
# But we want the function to be defined inside the same scope.

# Let's find the line with "updateDependenciesSelect();" and then the line with "updateTypeFilterAndSuggestions();" (which is already there).
# We'll replace the entire block that has the two calls with the function definition in between.

# We'll look for the pattern:
#        updateDependenciesSelect();
#        updateTypeFilterAndSuggestions();
# and replace with:
#        updateDependenciesSelect();
#        // Function to update the type filter dropdown and suggestions
#        function updateTypeFilterAndSuggestions() { ... }
#        updateTypeFilterAndSuggestions();

# But note that the function is called twice: once in initialization and then in the event listeners.
# We can define the function first and then call it.

# Let's do a more robust replacement: find the line with "updateDependenciesSelect();" and the next line that is "updateTypeFilterAndSuggestions();"
# and then insert the function definition between them.

# Actually, the function is not defined yet, so we can insert the function definition before the call.

# We'll use regex to find the two lines and replace with the function definition and then the call.

pattern = r'(\s*)updateDependenciesSelect\(\);\n\s*updateTypeFilterAndSuggestions\(\);'
replacement = r'''\1updateDependenciesSelect();
\1// Function to update the type filter dropdown and suggestions
\1function updateTypeFilterAndSuggestions() {
\1    // Get unique types from activities
\1    const types = [...new Set(state.activities.map(a => a.type || 'Default'))];
\1    
\1    // Update the type filter dropdown
\1    typeFilterSelect.innerHTML = '<option value="">All Types</option>';
\1    types.forEach(type => {
\1        const option = document.createElement('option');
\1        option.value = type;
\1        option.textContent = type;
\1        typeFilterSelect.appendChild(option);
\1    });
\1    
\1    // Update the datalist for suggestions (if it exists)
\1    const datalist = document.getElementById('typeSuggestions');
\1    if (datalist) {
\1        datalist.innerHTML = '';
\1        types.forEach(type => {
\1            const option = document.createElement('option');
\1            option.value = type;
\1            datalist.appendChild(option);
\1        });
\1    }
\1}
\1updateTypeFilterAndSuggestions();'''

content = re.sub(pattern, replacement, content, flags=re.MULTILINE)

# Write the fixed content back
with open('script-enhanced.js', 'w') as f:
    f.write(content)

print('Fixed syntax errors and added updateTypeFilterAndSuggestions function')
