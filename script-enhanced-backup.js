// Enhanced Task Scheduler with Import/Export, Templates, and Date Editing
document.addEventListener('DOMContentLoaded', function() {
    // Use DateUtils for date manipulation
    const DateTime = window.DateUtils || DateUtils;
    
    // State management
    const state = {
        activities: [],
        schedule: [],
        currentDate: DateTime.now(),
        calendarMonth: DateTime.now(),
        startDate: null,
        templates: loadTemplatesFromStorage()
    };

    // DOM Elements
    const activityNameInput = document.getElementById('activityName');
    const durationInput = document.getElementById('duration');
    const dependencySelect = document.getElementById('dependency');
    const addActivityBtn = document.getElementById('addActivity');
    const activitiesContainer = document.getElementById('activitiesContainer');
    const startDateInput = document.getElementById('startDate');
    const generateScheduleBtn = document.getElementById('generateSchedule');
    const clearAllBtn = document.getElementById('clearAll');
    const currentMonthElement = document.getElementById('currentMonth');
    const prevMonthBtn = document.getElementById('prevMonth');
    const nextMonthBtn = document.getElementById('nextMonth');
    const calendarElement = document.getElementById('calendar');
    const scheduleTimelineElement = document.getElementById('scheduleTimeline');
    
    // New DOM Elements for enhanced features
    const saveTemplateBtn = document.getElementById('saveTemplate');
    const loadTemplateBtn = document.getElementById('loadTemplate');
    const templateSelect = document.getElementById('templateSelect');
    const exportActivitiesBtn = document.getElementById('exportActivities');
    const importActivitiesBtn = document.getElementById('importActivities');
    const exportScheduleBtn = document.getElementById('exportSchedule');
    const importFileInput = document.getElementById('importFile');

    // Initialize date picker with today's date
    const today = DateTime.now().toISODate();
    startDateInput.value = today;
    startDateInput.min = today;

    // Initialize templates dropdown
    updateTemplatesDropdown();

    // Event Listeners
    addActivityBtn.addEventListener('click', addActivity);
    generateScheduleBtn.addEventListener('click', generateSchedule);
    clearAllBtn.addEventListener('click', clearAll);
    prevMonthBtn.addEventListener('click', previousMonth);
    nextMonthBtn.addEventListener('click', nextMonth);
    
    // Enhanced feature event listeners
    saveTemplateBtn.addEventListener('click', saveTemplate);
    loadTemplateBtn.addEventListener('click', loadTemplate);
    templateSelect.addEventListener('change', handleTemplateSelect);
    exportActivitiesBtn.addEventListener('click', exportActivities);
    importActivitiesBtn.addEventListener('click', () => importFileInput.click());
    exportScheduleBtn.addEventListener('click', exportSchedule);
    importFileInput.addEventListener('change', handleFileImport);

    // Initialize calendar
    renderCalendar();
    updateDependencySelect();

    // Function to add a new activity
    function addActivity() {
        const name = activityNameInput.value.trim();
        const duration = parseInt(durationInput.value);
        const dependency = dependencySelect.value;

        if (!name) {
            alert('Please enter an activity name');
            return;
        }

        if (duration < 1) {
            alert('Duration must be at least 1 day');
            return;
        }

        // Create activity object
        const activity = {
            id: generateId(),
            name,
            duration,
            dependency: dependency || null,
            startDate: null,
            endDate: null
        };

        // Add to state
        state.activities.push(activity);

        // Clear inputs
        activityNameInput.value = '';
        durationInput.value = '1';

        // Update UI
        renderActivitiesList();
        updateDependencySelect();

        console.log('Activity added:', activity);
    }

    // Enhanced function to render activities list with edit buttons
    function renderActivitiesList() {
        if (state.activities.length === 0) {
            activitiesContainer.innerHTML = '<p class="empty-message">No activities added yet. Add your first activity above.</p>';
            return;
        }

        activitiesContainer.innerHTML = '';

        state.activities.forEach(activity => {
            const activityElement = document.createElement('div');
            activityElement.className = 'activity-item';
            activityElement.innerHTML = `
                <div class="activity-info">
                    <h4>${activity.name}</h4>
                    <p>Duration: ${activity.duration} day${activity.duration > 1 ? 's' : ''}</p>
                    <p>Dependency: ${activity.dependency ? getActivityName(activity.dependency) : 'None'}</p>
                    ${activity.startDate ? `<p>Schedule: ${formatDate(activity.startDate)} - ${formatDate(activity.endDate)}</p>` : ''}
                </div>
                <div class="activity-actions">
                    <button class="btn-secondary edit-date-btn" onclick="editActivityDate('${activity.id}')">
                        <i class="fas fa-calendar-edit"></i> Edit Date
                    </button>
                    <button class="btn-danger" onclick="removeActivity('${activity.id}')">
                        <i class="fas fa-trash"></i> Remove
                    </button>
                </div>
            `;
            activitiesContainer.appendChild(activityElement);
        });
    }

    // Function to format date for display
    function formatDate(dateObj) {
        if (!dateObj) return 'Not scheduled';
        return dateObj.toLocaleString();
    }

    // Function to edit activity date (exposed to window)
    window.editActivityDate = function(id) {
        const activity = state.activities.find(a => a.id === id);
        if (!activity) return;

        // Create a date picker dialog
        const newStartDate = prompt(`Edit start date for "${activity.name}" (YYYY-MM-DD):`, 
            activity.startDate ? activity.startDate.toISODate() : '');
        
        if (newStartDate && newStartDate.match(/^\d{4}-\d{2}-\d{2}$/)) {
            const startDate = DateTime.fromISO(newStartDate);
            const endDate = calculateEndDate(startDate, activity.duration);
            
            // Update activity dates
            activity.startDate = startDate;
            activity.endDate = endDate;
            
            // Update schedule if this activity is scheduled
            const scheduleIndex = state.schedule.findIndex(a => a.id === id);
            if (scheduleIndex !== -1) {
                state.schedule[scheduleIndex].startDate = startDate;
                state.schedule[scheduleIndex].endDate = endDate;
            }
            
            // Update UI
            renderActivitiesList();
            renderScheduleTimeline();
            renderCalendar();
        } else if (newStartDate !== null) {
            alert('Please enter a valid date in YYYY-MM-DD format');
        }
    };

    // Function to calculate end date based on start date and duration
    function calculateEndDate(startDate, duration) {
        let currentDate = startDate;
        let daysScheduled = 0;
        
        while (daysScheduled < duration) {
            if (!isWorkingDay(currentDate)) {
                currentDate = currentDate.plus({ days: 1 });
                continue;
            }
            daysScheduled++;
            if (daysScheduled === duration) break;
            currentDate = currentDate.plus({ days: 1 });
        }
        return currentDate;
    }

    // Function to update dependency select dropdown
    function updateDependencySelect() {
        dependencySelect.innerHTML = '<option value="">None</option>';
        
        state.activities.forEach(activity => {
            const option = document.createElement('option');
            option.value = activity.id;
            option.textContent = activity.name;
            dependencySelect.appendChild(option);
        });
    }

    // Function to get activity name by ID
    function getActivityName(id) {
        const activity = state.activities.find(a => a.id === id);
        return activity ? activity.name : 'Unknown';
    }

    // Enhanced function to remove an activity
    window.removeActivity = function(id) {
        // Check if any activity depends on this one
        const dependentActivities = state.activities.filter(a => a.dependency === id);
        
        if (dependentActivities.length > 0) {
            const dependentNames = dependentActivities.map(a => a.name).join(', ');
            if (!confirm(`The following activities depend on this one: ${dependentNames}. Do you still want to remove it?`)) {
                return;
            }
        }

        // Remove the activity
        state.activities = state.activities.filter(a => a.id !== id);
        
        // Remove any dependencies pointing to this activity
        state.activities.forEach(a => {
            if (a.dependency === id) {
                a.dependency = null;
            }
        });

        // Remove from schedule
        state.schedule = state.schedule.filter(a => a.id !== id);

        // Update UI
        renderActivitiesList();
        updateDependencySelect();
        renderScheduleTimeline();
        renderCalendar();
    };

    // Function to generate schedule
    function generateSchedule() {
        if (state.activities.length === 0) {
            alert('Please add at least one activity');
            return;
        }

        const startDateStr = startDateInput.value;
        if (!startDateStr) {
            alert('Please select a start date');
            return;
        }

        state.startDate = DateTime.fromISO(startDateStr);
        
        try {
            calculateSchedule();
            renderScheduleTimeline();
            renderCalendar();
        } catch (error) {
            alert('Error generating schedule: ' + error.message);
            console.error(error);
        }
    }

    // Function to calculate schedule considering dependencies and holidays
    function calculateSchedule() {
        // Clear existing schedule
        state.schedule = [];
        
        // Create a copy of activities to process
        const activitiesToSchedule = [...state.activities];
        const scheduledActivities = new Set();
        
        // Initialize all activities
        activitiesToSchedule.forEach(activity => {
            // Only reset dates if they weren't manually set
            if (!activity.startDate) {
                activity.startDate = null;
                activity.endDate = null;
            }
        });

        // Function to schedule an activity
        const scheduleActivity = (activity, startDate) => {
            let currentDate = startDate;
            let daysScheduled = 0;
            
            while (daysScheduled < activity.duration) {
                // Skip weekends and holidays
                if (!isWorkingDay(currentDate)) {
                    currentDate = currentDate.plus({ days: 1 });
                    continue;
                }
                
                daysScheduled++;
                if (daysScheduled === activity.duration) {
                    break;
                }
                currentDate = currentDate.plus({ days: 1 });
            }
            
            activity.startDate = startDate;
            activity.endDate = currentDate;
            scheduledActivities.add(activity.id);
            state.schedule.push({ ...activity });
            
            return currentDate.plus({ days: 1 }); // Next available date
        };

        // Separate activities with manually set dates
        const manuallyScheduled = activitiesToSchedule.filter(a => a.startDate !== null);
        const toAutoSchedule = activitiesToSchedule.filter(a => a.startDate === null);
        
        // Add manually scheduled activities to schedule
        manuallyScheduled.forEach(activity => {
            scheduledActivities.add(activity.id);
            state.schedule.push({ ...activity });
        });

        // Find activities with no dependencies to start
        let availableActivities = toAutoSchedule.filter(a => !a.dependency);
        let currentDate = state.startDate;

        while (availableActivities.length > 0) {
            // Sort by duration (shortest first) for better scheduling
            availableActivities.sort((a, b) => a.duration - b.duration);
            
            // Schedule all available activities
            for (const activity of availableActivities) {
                if (!scheduledActivities.has(activity.id)) {
                    currentDate = scheduleActivity(activity, currentDate);
                }
            }

            // Update available activities
            availableActivities = toAutoSchedule.filter(a => 
                !scheduledActivities.has(a.id) && 
                (a.dependency === null || scheduledActivities.has(a.dependency))
            );
        }

        // Check for circular dependencies
        if (scheduledActivities.size < state.activities.length) {
            const unscheduled = state.activities.filter(a => !scheduledActivities.has(a.id));
            throw new Error(`Circular dependency detected. Unscheduled activities: ${unscheduled.map(a => a.name).join(', ')}`);
        }

        // Sort schedule by start date
        state.schedule.sort((a, b) => a.startDate.valueOf() - b.startDate.valueOf());
    }

    // Function to check if a day is a working day (not weekend or holiday)
    function isWorkingDay(date) {
        // Check if it's a weekend (Saturday = 6, Sunday = 7 in our DateUtils)
        const weekday = date.weekday;
        if (weekday === 6 || weekday === 7) { // Saturday or Sunday
            return false;
        }
        
        // Check if it's a Hong Kong public holiday
        if (isHongKongHoliday(date.toJSDate())) {
            return false;
        }
        
        return true;
    }

    // Function to render schedule timeline
    function renderScheduleTimeline() {
        if (state.schedule.length === 0) {
            scheduleTimelineElement.innerHTML = '<p class="empty-message">No schedule generated yet. Add activities and click "Generate Schedule".</p>';
            return;
        }

        scheduleTimelineElement.innerHTML = '';

        state.schedule.forEach(activity => {
            const timelineItem = document.createElement('div');
            timelineItem.className = 'timeline-item';
            
            const startDateStr = activity.startDate ? activity.startDate.toLocaleString() : 'Not scheduled';
            const endDateStr = activity.endDate ? activity.endDate.toLocaleString() : 'Not scheduled';
            
            timelineItem.innerHTML = `
                <div>
                    <h4>${activity.name}</h4>
                    <p>Duration: ${activity.duration} day${activity.duration > 1 ? 's' : ''}</p>
                    ${activity.dependency ? `<p>Depends on: ${getActivityName(activity.dependency)}</p>` : ''}
                </div>
                <div class="timeline-dates">
                    ${startDateStr} - ${endDateStr}
                </div>
            `;
            
            scheduleTimelineElement.appendChild(timelineItem);
        });
    }

    // Enhanced function to render calendar with clickable days
    function renderCalendar() {
        const year = state.calendarMonth.year;
        const month = state.calendarMonth.month;
        
        // Update month display
        currentMonthElement.textContent = state.calendarMonth.toLocaleString({ month: 'long', year: 'numeric' });
        
        // Clear calendar
        calendarElement.innerHTML = '';
        
        // Add day headers
        const daysOfWeek = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
        daysOfWeek.forEach(day => {
            const dayHeader = document.createElement('div');
            dayHeader.className = 'calendar-day-header';
            dayHeader.textContent = day;
            calendarElement.appendChild(dayHeader);
        });
        
        // Calculate first day of month and padding
        const firstDayOfMonth = DateTime.local(year, month, 1);
        const startPadding = (firstDayOfMonth.weekday - 1 + 7) % 7;
        
        // Add padding for days before the first day of month
        for (let i = 0; i < startPadding; i++) {
            const emptyDay = document.createElement('div');
            emptyDay.className = 'calendar-day empty';
            calendarElement.appendChild(emptyDay);
        }
        
        // Get holidays for this month
        const holidays = getHolidaysForMonth(year, month - 1);
        
        // Add days of the month
        const daysInMonth = state.calendarMonth.daysInMonth;
        for (let day = 1; day <= daysInMonth; day++) {
            const currentDate = DateTime.local(year, month, day);
            const dayElement = document.createElement('div');
            dayElement.className = 'calendar-day';
            dayElement.dataset.date = currentDate.toISODate();
            
            // Make calendar days clickable for date editing
            dayElement.addEventListener('click', function() {
                handleCalendarDayClick(this.dataset.date);
            });
            
            // Check for weekend
            if (currentDate.weekday === 6 || currentDate.weekday === 7) {
                dayElement.classList.add('weekend');
            }
            
            // Check for holiday
            const holiday = holidays.find(h => {
                const holidayDate = new Date(h.date);
                return holidayDate.getDate() === day;
            });
            
            if (holiday) {
                dayElement.classList.add('holiday');
            }
            
            // Check for scheduled activities
            const scheduledActivities = state.schedule.filter(activity => {
                const activityStart = activity.startDate ? activity.startDate.startOf('day') : null;
                const activityEnd = activity.endDate ? activity.endDate.startOf('day') : null;
                const currentDay = currentDate.startOf('day');
                
                if (!activityStart || !activityEnd) return false;
                
                return DateTime.isBetween(currentDay, activityStart, activityEnd);
            });
            
            if (scheduledActivities.length > 0) {
                dayElement.classList.add('scheduled');
                dayElement.title = `Scheduled activities: ${scheduledActivities.map(a => a.name).join(', ')}`;
            }
            
            // Add day number
            const dayNumber = document.createElement('div');
            dayNumber.className = 'calendar-day-number';
            dayNumber.textContent = day;
            dayElement.appendChild(dayNumber);
            
            // Add holiday name
            if (holiday) {
                const holidayName = document.createElement('div');
                holidayName.className = 'calendar-day-content';
                holidayName.textContent = holiday.name;
                holidayName.style.color = 'var(--holiday-color)';
                holidayName.style.fontWeight = 'bold';
                dayElement.appendChild(holidayName);
            }
            
            // Add scheduled activities
            scheduledActivities.forEach(activity => {
                const activityElement = document.createElement('div');
                activityElement.className = 'calendar-day-content';
                activityElement.textContent = activity.name;
                activityElement.style.color = 'var(--scheduled-color)';
                activityElement.style.marginTop = '2px';
                activityElement.style.fontSize = '0.7rem';
                dayElement.appendChild(activityElement);
            });
            
            calendarElement.appendChild(dayElement);
        }
    }

    // Function to handle calendar day clicks
    function handleCalendarDayClick(dateString) {
        // Find activities that occur on this date
        const clickedDate = DateTime.fromISO(dateString);
        const activitiesOnDate = state.schedule.filter(activity => {
            const activityStart = activity.startDate ? activity.startDate.startOf('day') : null;
            const activityEnd = activity.endDate ? activity.endDate.startOf('day') : null;
            const currentDay = clickedDate.startOf('day');
            
            if (!activityStart || !activityEnd) return false;
            
            return DateTime.isBetween(currentDay, activityStart, activityEnd);
        });
        
        if (activitiesOnDate.length > 0) {
            // Show menu to edit activity dates
            const activityNames = activitiesOnDate.map(a => a.name).join(', ');
            const action = prompt(`Activities on ${dateString}: ${activityNames}\n\nEnter 'edit' to edit dates or activity name to edit specific activity:`);
            
            if (action && action.toLowerCase() === 'edit') {
                // Edit all activities on this date
                activitiesOnDate.forEach(activity => {
                    editActivityDate(activity.id);
                });
            } else if (action) {
                // Find specific activity by name
                const activity = activitiesOnDate.find(a => a.name.toLowerCase().includes(action.toLowerCase()));
                if (activity) {
                    editActivityDate(activity.id);
                } else {
                    alert(`Activity "${action}" not found on this date.`);
                }
            }
        } else {
            // No activities on this date - offer to schedule one
            if (state.activities.length > 0) {
                const activityNames = state.activities.map(a => a.name).join(', ');
                const activityName = prompt(`No activities scheduled on ${dateString}.\n\nAvailable activities: ${activityNames}\nEnter activity name to schedule on this date:`);
                
                if (activityName) {
                    const activity = state.activities.find(a => a.name.toLowerCase() === activityName.toLowerCase());
                    if (activity) {
                        const startDate = DateTime.fromISO(dateString);
                        const endDate = calculateEndDate(startDate, activity.duration);
                        
                        activity.startDate = startDate;
                        activity.endDate = endDate;
                        
                        // Update schedule
                        const scheduleIndex = state.schedule.findIndex(a => a.id === activity.id);
                        if (scheduleIndex !== -1) {
                            state.schedule[scheduleIndex].startDate = startDate;
                            state.schedule[scheduleIndex].endDate = endDate;
                        } else {
                            state.schedule.push({ ...activity });
                        }
                        
                        // Update UI
                        renderActivitiesList();
                        renderScheduleTimeline();
                        renderCalendar();
                    } else {
                        alert(`Activity "${activityName}" not found.`);
                    }
                }
            }
        }
    }

    // Function to go to previous month
    function previousMonth() {
        state.calendarMonth = state.calendarMonth.minus({ months: 1 });
        renderCalendar();
    }

    // Function to go to next month
    function nextMonth() {
        state.calendarMonth = state.calendarMonth.plus({ months: 1 });
        renderCalendar();
    }

    // Function to clear all activities and schedule
    function clearAll() {
        if (state.activities.length === 0) {
            return;
        }
        
        if (!confirm('Are you sure you want to clear all activities and schedule?')) {
            return;
        }
        
        state.activities = [];
        state.schedule = [];
        state.startDate = null;
        
        renderActivitiesList();
        updateDependencySelect();
        renderScheduleTimeline();
        renderCalendar();
        
        // Reset start date to today
        startDateInput.value = today;
    }

    // Template Management Functions
    function saveTemplate() {
        if (state.activities.length === 0) {
            alert('No activities to save as template');
            return;
        }
        
        const templateName = prompt('Enter a name for this template:');
        if (!templateName) return;
        
        // Create template object without IDs (they will be regenerated on load)
        const template = {
            name: templateName,
            activities: state.activities.map(activity => ({
                name: activity.name,
                duration: activity.duration,
                dependency: null // Reset dependencies for templates
            })),
            createdAt: new Date().toISOString()
        };
        
        // Save to templates
        state.templates.push(template);
        saveTemplatesToStorage(state.templates);
        updateTemplatesDropdown();
        
        alert(`Template "${templateName}" saved successfully!`);
    }

    function loadTemplate() {
        const selectedTemplateName = templateSelect.value;
        if (!selectedTemplateName) {
            alert('Please select a template first');
            return;
        }
        
        if (!confirm('Loading a template will replace your current activities. Continue?')) {
            return;
        }
        
        const template = state.templates.find(t => t.name === selectedTemplateName);
        if (!template) {
            alert('Template not found');
            return;
        }
        
        // Clear current activities
        state.activities = [];
        
        // Load template activities with new IDs
        template.activities.forEach(activityData => {
            const activity = {
                id: generateId(),
                name: activityData.name,
                duration: activityData.duration,
                dependency: null,
                startDate: null,
                endDate: null
            };
            state.activities.push(activity);
        });
        
        // Clear schedule
        state.schedule = [];
        state.startDate = null;
        
        // Update UI
        renderActivitiesList();
        updateDependencySelect();
        renderScheduleTimeline();
        renderCalendar();
        
        alert(`Template "${template.name}" loaded successfully!`);
    }

    function handleTemplateSelect() {
        // Optional: Show template preview
    }

    function updateTemplatesDropdown() {
        templateSelect.innerHTML = '<option value="">Select a template...</option>';
        
        state.templates.forEach(template => {
            const option = document.createElement('option');
            option.value = template.name;
            option.textContent = `${template.name} (${template.activities.length} activities)`;
            templateSelect.appendChild(option);
        });
    }

    // Import/Export Functions
    function exportActivities() {
        if (state.activities.length === 0) {
            alert('No activities to export');
            return;
        }
        
        // Prepare data for export
        const exportData = {
            activities: state.activities.map(activity => ({
                name: activity.name,
                duration: activity.duration,
                dependency: activity.dependency
            })),
            exportedAt: new Date().toISOString(),
            version: '1.0'
        };
        
        // Create and download JSON file
        const dataStr = JSON.stringify(exportData, null, 2);
        const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
        const exportFileDefaultName = `activities-${new Date().toISOString().slice(0,10)}.json`;
        
        const linkElement = document.createElement('a');
        linkElement.setAttribute('href', dataUri);
        linkElement.setAttribute('download', exportFileDefaultName);
        linkElement.click();
    }

    function exportSchedule() {
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
                dependency: activity.dependency
            })),
            exportedAt: new Date().toISOString(),
            version: '1.0'
        };
        
        // Create and download JSON file
        const dataStr = JSON.stringify(exportData, null, 2);
        const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
        const exportFileDefaultName = `schedule-${new Date().toISOString().slice(0,10)}.json`;
        
        const linkElement = document.createElement('a');
        linkElement.setAttribute('href', dataUri);
        linkElement.setAttribute('download', exportFileDefaultName);
        linkElement.click();
    }

    function handleFileImport(event) {
        const file = event.target.files[0];
        if (!file) return;
        
        const reader = new FileReader();
        reader.onload = function(e) {
            try {
                const importData = JSON.parse(e.target.result);
                
                if (!confirm('Importing data will replace your current activities. Continue?')) {
                    return;
                }
                
                // Clear current state
                state.activities = [];
                state.schedule = [];
                state.startDate = null;
                
                // Check if it's activities or schedule data
                if (importData.activities) {
                    // Import activities
                    importData.activities.forEach(activityData => {
                        const activity = {
                            id: generateId(),
                            name: activityData.name,
                            duration: activityData.duration,
                            dependency: activityData.dependency || null,
                            startDate: null,
                            endDate: null
                        };
                        state.activities.push(activity);
                    });
                    
                    alert(`Successfully imported ${importData.activities.length} activities!`);
                } else if (importData.schedule) {
                    // Import schedule
                    importData.schedule.forEach(scheduleData => {
                        const activity = {
                            id: generateId(),
                            name: scheduleData.name,
                            duration: scheduleData.duration,
                            dependency: scheduleData.dependency || null,
                            startDate: scheduleData.startDate ? DateTime.fromISO(scheduleData.startDate) : null,
                            endDate: scheduleData.endDate ? DateTime.fromISO(scheduleData.endDate) : null
                        };
                        state.activities.push(activity);
                        if (activity.startDate) {
                            state.schedule.push({ ...activity });
                        }
                    });
                    
                    alert(`Successfully imported ${importData.schedule.length} scheduled activities!`);
                } else {
                    throw new Error('Invalid file format');
                }
                
                // Update UI
                renderActivitiesList();
                updateDependencySelect();
                renderScheduleTimeline();
                renderCalendar();
                
            } catch (error) {
                alert('Error importing file: ' + error.message);
                console.error(error);
            }
            
            // Reset file input
            event.target.value = '';
        };
        
        reader.readAsText(file);
    }

    // Storage Functions
    function loadTemplatesFromStorage() {
        try {
            const templatesJson = localStorage.getItem('activityTemplates');
            return templatesJson ? JSON.parse(templatesJson) : [];
        } catch (error) {
            console.error('Error loading templates from storage:', error);
            return [];
        }
    }

    function saveTemplatesToStorage(templates) {
        try {
            localStorage.setItem('activityTemplates', JSON.stringify(templates));
        } catch (error) {
            console.error('Error saving templates to storage:', error);
        }
    }

    // Helper function to generate unique ID
    function generateId() {
        return Date.now().toString(36) + Math.random().toString(36).substr(2);
    }
});