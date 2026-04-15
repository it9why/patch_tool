import sys

with open('script-enhanced.js', 'r') as f:
    content = f.read()

# Replace the entire exportActivities function with a clean version
import re

# Pattern for exportActivities function
pattern = r'(function exportActivities\(\) \{[\s\S]*?\n    \})'

def replace_export(match):
    # Return a clean implementation
    return '''    function exportActivities() {
        if (state.activities.length === 0) {
            alert('No activities to export');
            return;
        }
        
        // Prepare data for export
        const exportData = {
            activities: state.activities.map(activity => ({
                name: activity.name,
                duration: activity.duration,
                dependency: activity.dependency,
                type: activity.type || 'Default'
            })),
            exportedAt: new Date().toISOString(),
            version: '1.0'
        };
        
        // Create and download JSON file
        const dataStr = JSON.stringify(exportData, null, 2);
        const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
        const exportFileDefaultName = `activities-\${new Date().toISOString().slice(0,10)}.json`;
        
        const linkElement = document.createElement('a');
        linkElement.setAttribute('href', dataUri);
        linkElement.setAttribute('download', exportFileDefaultName);
        linkElement.click();
    }'''

# Perform replacement
new_content = re.sub(pattern, replace_export, content, flags=re.MULTILINE)

# Now fix exportSchedule similarly
pattern2 = r'(function exportSchedule\(\) \{[\s\S]*?\n    \})'

def replace_export_schedule(match):
    return '''    function exportSchedule() {
        if (state.schedule.length === 0) {
            alert('No schedule to export');
            return;
        }
        
        // Prepare schedule data for export
        const exportData = {
            schedule: state.schedule.map(activity => ({
                name: activity.name,
                duration: activity.duration,
                startDate: activity.startDate ? activity.startDate.toISODate() : null,
                endDate: activity.endDate ? activity.endDate.toISODate() : null,
                dependency: activity.dependency,
                type: activity.type || 'Default'
            })),
            exportedAt: new Date().toISOString(),
            version: '1.0'
        };
        
        // Create and download JSON file
        const dataStr = JSON.stringify(exportData, null, 2);
        const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
        const exportFileDefaultName = `schedule-\${new Date().toISOString().slice(0,10)}.json`;
        
        const linkElement = document.createElement('a');
        linkElement.setAttribute('href', dataUri);
        linkElement.setAttribute('download', exportFileDefaultName);
        linkElement.click();
    }'''

new_content = re.sub(pattern2, replace_export_schedule, new_content, flags=re.MULTILINE)

with open('script-enhanced.js', 'w') as f:
    f.write(new_content)

print("Fixed export functions with clean implementations")
