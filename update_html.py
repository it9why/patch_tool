import sys

with open('index.html', 'r') as f:
    lines = f.readlines()

# We'll remove the duplicate line and update the template-controls section
# Also update the dependency input to a multiple select.

output_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    # Remove duplicate template-controls div opening tag (line 77 and 78 are both opening)
    if 'class="template-controls"' in line and i+1 < len(lines) and 'class="template-controls"' in lines[i+1]:
        # Skip the next line (the duplicate)
        i += 1
        continue

    # Update the dependency select to multiple and change id
    if 'id="dependency"' in line:
        # Change the line to a multiple select
        line = line.replace('id="dependency"', 'id="dependencies" multiple')
        # Also update the label if we can find it, but it's not in the same line.
        # We'll also change the label text to "Dependencies (Optional)".
        # We'll need to find the label line. Let's do it in a separate step.

    # Remove the saveTemplate and loadTemplate buttons (lines with these ids)
    if 'id="saveTemplate"' in line or 'id="loadTemplate"' in line:
        # Skip this line and the next line (the button line and the following newline)
        # Actually, the button line is a single line, we just skip it.
        i += 1
        continue

    # Also remove the select for templateSelect? The requirement doesn't say to remove the template selection.
    # We'll keep the select and the export/import buttons.

    # Update the label for dependency to Dependencies (Optional) and change the select to multiple
    # We'll do this by looking for the line with "Dependency (Optional)"
    if 'Dependency (Optional)' in line:
        line = line.replace('Dependency (Optional)', 'Dependencies (Optional)')

    output_lines.append(line)
    i += 1

# Now write the updated HTML
with open('index.html', 'w') as f:
    f.writelines(output_lines)

print("Updated index.html")
