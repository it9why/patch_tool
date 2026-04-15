import sys

with open('script-enhanced.js', 'r') as f:
    lines = f.readlines()

# Find the line numbers for specific patterns
for i, line in enumerate(lines):
    if 'const importFileInput = document.getElementById' in line:
        import_file_line = i
    if 'loadTemplateBtn.addEventListener' in line:
        load_template_listener_line = i
    if 'function loadTemplate()' in line:
        load_template_function_start = i
    if 'function handleTemplateSelect()' in line:
        handle_template_select_line = i

# 1. Insert new DOM variables after importFileInput
new_dom_vars = [
    '    const exportTemplateBtn = document.getElementById(\'exportTemplate\');\n',
    '    const importTemplateBtn = document.getElementById(\'importTemplate\');\n',
    '    const importTemplateFileInput = document.getElementById(\'importTemplateFile\');\n'
]
lines = lines[:import_file_line+1] + new_dom_vars + lines[import_file_line+1:]

# 2. Insert new event listeners after loadTemplateBtn event listener
# Update the line index because we inserted lines
load_template_listener_line = lines.index('    loadTemplateBtn.addEventListener(\'click\', loadTemplate);\n')
new_event_listeners = [
    '    exportTemplateBtn.addEventListener(\'click\', exportTemplate);\n',
    '    importTemplateBtn.addEventListener(\'click\', () => importTemplateFileInput.click());\n',
    '    importTemplateFileInput.addEventListener(\'change\', handleTemplateImport);\n'
]
lines = lines[:load_template_listener_line+1] + new_event_listeners + lines[load_template_listener_line+1:]

# 3. Find the line after the loadTemplate function
# We'll insert after the closing brace of loadTemplate function
# Look for the line with 'function loadTemplate()' and then find the matching '}'
load_template_function_start = lines.index('    function loadTemplate() {\n')
brace_count = 0
insert_line = None
for i in range(load_template_function_start, len(lines)):
    if '{' in lines[i]:
        brace_count += 1
    if '}' in lines[i]:
        brace_count -= 1
        if brace_count == 0:
            insert_line = i + 1
            break

# Define the new functions
new_functions = '''
    function exportTemplate() {
        const selectedTemplateName = templateSelect.value;
        if (!selectedTemplateName) {
            alert('Please select a template to export');
            return;
        }

        const template = state.templates.find(t => t.name === selectedTemplateName);
        if (!template) {
            alert('Template not found');
            return;
        }

        // Prepare data for export
        const exportData = {
            ...template,
            exportedAt: new Date().toISOString(),
            version: '1.0'
        };

        // Create and download JSON file
        const dataStr = JSON.stringify(exportData, null, 2);
        const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
        const exportFileDefaultName = `template-${template.name}-${new Date().toISOString().slice(0,10)}.json`;

        const linkElement = document.createElement('a');
        linkElement.setAttribute('href', dataUri);
        linkElement.setAttribute('download', exportFileDefaultName);
        linkElement.click();
    }

    function handleTemplateImport(event) {
        const file = event.target.files[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = function(e) {
            try {
                const importedTemplate = JSON.parse(e.target.result);

                // Validate the template structure
                if (!importedTemplate.name || !importedTemplate.activities) {
                    throw new Error('Invalid template file format');
                }

                // Check if template with same name already exists
                const existingTemplate = state.templates.find(t => t.name === importedTemplate.name);
                if (existingTemplate) {
                    if (!confirm(`Template "${importedTemplate.name}" already exists. Overwrite?`)) {
                        return;
                    }
                    // Remove the existing template
                    state.templates = state.templates.filter(t => t.name !== importedTemplate.name);
                }

                // Add the new template
                state.templates.push(importedTemplate);
                saveTemplatesToStorage(state.templates);
                updateTemplatesDropdown();

                alert(`Template "${importedTemplate.name}" imported successfully!`);
            } catch (error) {
                alert('Error importing template: ' + error.message);
                console.error(error);
            }

            // Reset file input
            event.target.value = '';
        };

        reader.readAsText(file);
    }
'''

# Insert the new functions
if insert_line:
    # Split the new functions into lines and insert
    new_func_lines = new_functions.splitlines(keepends=True)
    lines = lines[:insert_line] + new_func_lines + lines[insert_line:]

# Write the modified file
with open('script-enhanced-new.js', 'w') as f:
    f.writelines(lines)

print('Modified script saved as script-enhanced-new.js')
