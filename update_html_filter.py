import sys

with open('index.html', 'r') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    new_lines.append(line)
    # We want to insert the filter controls right after the <h3>Activities Added</h3> line
    if '<h3>Activities Added</h3>' in line:
        # Insert after this line
        new_lines.append('                <div class="type-filter-controls" style="margin-bottom: 15px;">\n')
        new_lines.append('                    <label for="typeFilter" style="margin-right: 10px;">Filter by Type:</label>\n')
        new_lines.append('                    <select id="typeFilter" style="padding: 5px; margin-right: 15px;">\n')
        new_lines.append('                        <option value="">All Types</option>\n')
        new_lines.append('                    </select>\n')
        new_lines.append('                    <button id="quickDeleteType" class="btn-danger" style="padding: 5px 10px;"><i class="fas fa-trash"></i> Delete All of Selected Type</button>\n')
        new_lines.append('                </div>\n')

with open('index.html', 'w') as f:
    f.writelines(new_lines)

print("Added filter and quick delete by type controls")
