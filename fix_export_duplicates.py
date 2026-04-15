import sys

with open('script-enhanced.js', 'r') as f:
    lines = f.readlines()

# Fix exportActivities function
new_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    # Look for the start of exportActivities function
    if 'function exportActivities()' in line:
        new_lines.append(line)
        i += 1
        # Skip until we find the closing brace of the function
        while i < len(lines) and not lines[i].strip().startswith('}'):
            # Inside the function, look for the problematic duplicate lines
            if 'activities: state.activities.map' in lines[i]:
                # We'll replace the whole block until the next '})),' line
                # Actually, we need to remove the duplicate lines.
                # The pattern is:
                #            activities: state.activities.map(activity => ({
                #                name: activity.name,
                #                duration: activity.duration,
                #                dependency: activity.dependency,
                #                type: activity.type || 'Default'
                #            })),                name: activity.name,
                #                duration: activity.duration,
                #                dependency: activity.dependency
                #            })),
                # We want to keep only one mapping.
                # Let's find the line that ends with '})),'
                # We'll capture from the start of the mapping until the line that ends with '})),'
                # But we have two '})),' lines? Actually, the duplicate is within the same line? Let's examine.
                # The line 852: "            })),                name: activity.name,"
                # That's a malformed line. We'll need to restructure.

                # Instead of trying to fix piecemeal, we'll rewrite the whole exportData object.
                # We'll replace from line i to the line containing "exportedAt:" (but before that).
                # Let's find the line index of "exportedAt:"
                start_idx = i
                exported_at_idx = -1
                for j in range(i, len(lines)):
                    if 'exportedAt:' in lines[j]:
                        exported_at_idx = j
                        break
                if exported_at_idx != -1:
                    # Replace the block with corrected version
                    new_lines.append('            activities: state.activities.map(activity => ({\n')
                    new_lines.append('                name: activity.name,\n')
                    new_lines.append('                duration: activity.duration,\n')
                    new_lines.append('                dependency: activity.dependency,\n')
                    new_lines.append('                type: activity.type || \'Default\'\n')
                    new_lines.append('            })),\n')
                    # Skip the old lines until the line before exportedAt
                    i = exported_at_idx - 1  # we'll skip to the line before exportedAt, then continue
                else:
                    # fallback: keep the line and continue
                    new_lines.append(line)
                    i += 1
                continue
            else:
                new_lines.append(lines[i])
                i += 1
        # Now add the closing brace line (which is lines[i] after the while loop)
        if i < len(lines):
            new_lines.append(lines[i])
            i += 1
        continue

    # Fix exportSchedule function similarly
    if 'function exportSchedule()' in line:
        new_lines.append(line)
        i += 1
        while i < len(lines) and not lines[i].strip().startswith('}'):
            if 'schedule: state.schedule.map' in lines[i]:
                # Find the exportedAt line for this function
                start_idx = i
                exported_at_idx = -1
                for j in range(i, len(lines)):
                    if 'exportedAt:' in lines[j]:
                        exported_at_idx = j
                        break
                if exported_at_idx != -1:
                    new_lines.append('            schedule: state.schedule.map(activity => ({\n')
                    new_lines.append('                name: activity.name,\n')
                    new_lines.append('                duration: activity.duration,\n')
                    new_lines.append('                startDate: activity.startDate ? activity.startDate.toISODate() : null,\n')
                    new_lines.append('                endDate: activity.endDate ? activity.endDate.toISODate() : null,\n')
                    new_lines.append('                dependency: activity.dependency,\n')
                    new_lines.append('                type: activity.type || \'Default\'\n')
                    new_lines.append('            })),\n')
                    i = exported_at_idx - 1
                else:
                    new_lines.append(lines[i])
                    i += 1
                continue
            else:
                new_lines.append(lines[i])
                i += 1
        if i < len(lines):
            new_lines.append(lines[i])
            i += 1
        continue

    # Default: copy line
    new_lines.append(line)
    i += 1

# Write back
with open('script-enhanced.js', 'w') as f:
    f.writelines(new_lines)

print("Fixed export functions")
