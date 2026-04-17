const fs = require('fs');
const content = fs.readFileSync('script-enhanced.js', 'utf8');

// We need to fix the forEach block. Let's find the problematic pattern.
// The pattern is:
// activity.dependencies.forEach(depId => {
//     const dep = state.activities.find(a => a.id === depId);
//     if (dep && dep.endDate) {
//         if (DateTime.isAfter(dep.endDate, startDate)) {
//             startDate = dep.endDate;
//         }
// });
// We are missing a closing brace for the if (dep && dep.endDate) block and for the forEach function.

// Let's do a replacement using a more robust method: find the line with `});` that is currently on line 457 (after the inner if) and change it to `}});`
// Actually, we need two closing braces: one for the inner if and one for the outer if? Wait, let's examine:

// The code should be:
// activity.dependencies.forEach(depId => {
//     const dep = state.activities.find(a => a.id === depId);
//     if (dep && dep.endDate) {
//         if (DateTime.isAfter(dep.endDate, startDate)) {
//             startDate = dep.endDate;
//         }
//     }
// });

// So we are missing the closing brace for the `if (dep && dep.endDate)` block.

// Let's look for the exact lines and replace.

const lines = content.split('\n');
let changed = false;
for (let i = 0; i < lines.length; i++) {
    if (lines[i].includes('activity.dependencies.forEach(depId => {') && i+5 < lines.length) {
        // We found the start. Look for the line that currently ends with '});' but is missing a brace.
        for (let j = i; j < lines.length; j++) {
            if (lines[j].trim() === '});') {
                // This is the line that closes the forEach. We need to adjust the previous line.
                // The previous line should be the closing of the inner if? Actually, the inner if is two levels.
                // Let's check the structure by counting braces from i to j.
                // Instead, we can replace the entire block from i to j with a corrected version.
                // But to be safe, we can just add a '}' before the '});' in the same line or adjust the previous line.
                // Let's look at the line before j (j-1). It should be the line with the inner if's closing brace.
                // Currently, j-1 is: "                                }" (maybe missing)
                // Actually, the line before j is: "                                }" (the closing of the inner if)
                // But we are missing the closing for the outer if.
                // So we need to change the line at j-1 to have two braces? Or add a line.
                // Let's change the line at j-1 to have two closing braces and then the line j becomes just '});'? 
                // Actually, the current j-1 is: "                                }" (closing the inner if)
                // We need to add another '}' for the outer if. So we can change j-1 to "                                }" and then add a line with "                            }" before j?
                // This is getting messy.

                // Alternative: replace the entire block with a corrected string.
                // We'll do a simple string replacement for the entire function.

                // Let's replace from line i to line j (inclusive) with:
                //                     activity.dependencies.forEach(depId => {
                //                         const dep = state.activities.find(a => a.id === depId);
                //                         if (dep && dep.endDate) {
                //                             if (DateTime.isAfter(dep.endDate, startDate)) {
                //                                 startDate = dep.endDate;
                //                             }
                //                         }
                //                     });
                const correctedBlock = `                        activity.dependencies.forEach(depId => {
                            const dep = state.activities.find(a => a.id === depId);
                            if (dep && dep.endDate) {
                                if (DateTime.isAfter(dep.endDate, startDate)) {
                                    startDate = dep.endDate;
                                }
                            }
                        });`;
                // Replace lines i through j with the correctedBlock split into lines.
                const newLines = correctedBlock.split('\n');
                lines.splice(i, j - i + 1, ...newLines);
                changed = true;
                break;
            }
        }
        if (changed) break;
    }
}

if (!changed) {
    // Try another pattern: the forEach block might be written differently.
    // Let's do a global replace with regex.
    const regex = /(activity\.dependencies\.forEach\(depId => \{[\s\S]*?)if \(dep && dep\.endDate\) \{[\s\S]*?if \(DateTime\.isAfter\(dep\.endDate, startDate\)\) \{[\s\S]*?startDate = dep\.endDate;\s*\}([\s\S]*?)\}\);?/g;
    // This is complex. Instead, let's do a more targeted fix.

    // We'll just manually fix the lines we saw.
    // Find the line with the forEach and then the next few lines.
    for (let i = 0; i < lines.length; i++) {
        if (lines[i].includes('activity.dependencies.forEach(depId => {')) {
            // Find the line with '});' after it.
            let j = i;
            while (j < lines.length && !lines[j].includes('});')) {
                j++;
            }
            if (j < lines.length) {
                // Check the line before j: it should close the inner if, but we need to close the outer if too.
                // Let's insert a line with a closing brace before j.
                lines.splice(j, 0, '                        }');
                changed = true;
                break;
            }
        }
    }
}

if (changed) {
    fs.writeFileSync('script-enhanced.js', lines.join('\n'));
    console.log('Fixed missing brace in forEach block.');
} else {
    console.log('Could not find the problematic block. Manual fix required.');
}
