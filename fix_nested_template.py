import sys

with open('script-enhanced.js', 'r') as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    # Look for the line with the nested template
    if '${activity.startDate ? `<p>Schedule: ${formatDate(activity.startDate)} - ${formatDate(activity.endDate)}</p>`' in line:
        # Replace with concatenated version
        new_line = line.replace(
            '${activity.startDate ? `<p>Schedule: ${formatDate(activity.startDate)} - ${formatDate(activity.endDate)}</p>` : \'\'}',
            '${activity.startDate ? \'<p>Schedule: \' + formatDate(activity.startDate) + \' - \' + formatDate(activity.endDate) + \'</p>\' : \'\'}'
        )
        new_lines.append(new_line)
        print(f"Fixed line {i+1}")
    else:
        new_lines.append(line)

with open('script-enhanced.js', 'w') as f:
    f.writelines(new_lines)

print("Done")
