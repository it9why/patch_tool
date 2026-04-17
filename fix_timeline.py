import re

with open('script-enhanced.js', 'r') as f:
    content = f.read()

# Find the function renderScheduleTimeline
# We'll replace the timelineItem.innerHTML block.

# First, let's locate the function.
# We can use a regex to find the function and then within it, the timelineItem.innerHTML assignment.
# But it's easier to replace the specific assignment.

# We'll replace from "timelineItem.innerHTML = `" to the matching backtick (which is 11 lines later?).
# Let's capture the exact block and replace with concatenated string.

# We'll use a regex that matches the assignment and the following backtick string.
# Since the string contains backticks and nested template literals, we need to be careful.

# Alternatively, we can replace the entire function, but that's more complex.

# Let's write the new assignment using concatenation.

new_assignment = '''            let timelineHTML = '';
            timelineHTML += '<div>';
            timelineHTML += '<h4>' + escapeHtml(activity.name) + '</h4>';
            timelineHTML += '<p>Duration: ' + activity.duration + ' day' + (activity.duration > 1 ? 's' : '') + '</p>';
            if (activity.dependency) {
                timelineHTML += '<p>Depends on: ' + escapeHtml(getActivityName(activity.dependency)) + '</p>';
            }
            timelineHTML += '</div>';
            timelineHTML += '<div class="timeline-dates">';
            timelineHTML += escapeHtml(startDateStr) + ' - ' + escapeHtml(endDateStr);
            timelineHTML += '</div>';
            timelineItem.innerHTML = timelineHTML;'''

# Now we need to replace the old assignment and the backtick string.
# We'll look for the pattern:
# timelineItem.innerHTML = `
#                 <div>
#                     <h4>${activity.name}</h4>
#                     <p>Duration: ${activity.duration} day${activity.duration > 1 ? 's' : ''}</p>
#                     ${activity.dependency ? `<p>Depends on: ${getActivityName(activity.dependency)}</p>` : ''}
#                 </div>
#                 <div class="timeline-dates">
#                     ${startDateStr} - ${endDateStr}
#                 </div>
#             `;

# We'll use a regex that matches from "timelineItem.innerHTML = `" to the next "`;" that is at the end of the block.
# We'll use re.DOTALL to match across lines.

pattern = r'(\s*)timelineItem\.innerHTML = `([\s\S]*?)`;'

def replace_func(match):
    indent = match.group(1)
    # We'll return the new assignment, but we need to adjust indentation.
    # We'll split the new assignment by lines and add the same indentation.
    lines = new_assignment.split('\n')
    # First line already has indentation from the pattern, but we want to keep the same indentation level as the original.
    # The original had 12 spaces (maybe). We'll use the same indent as the line before.
    # We'll prepend the indent to each line.
    new_lines = [indent + line for line in lines]
    return '\n'.join(new_lines)

content = re.sub(pattern, replace_func, content)

with open('script-enhanced.js', 'w') as f:
    f.write(content)

print('Fixed timelineItem.innerHTML')
