// Enhanced Task Scheduler with Import/Export and Date Editing
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
        calendarExpanded: false
    };

    // DOM Elements
    const activityNameInput = document.getElementById('activityName');
    const durationInput = document.getElementById('duration');
    const dependenciesSelect = document.getElementById('dependencies');
    const allowNonWorkingDaysSelect = document.getElementById('allowNonWorkingDays');
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
    // Type-related elements
    const typeInput = document.getElementById('activityType');
    const typeFilterSelect = document.getElementById('typeFilter');
    const typeOptionsDatalist = document.getElementById('typeOptions');
    
    // New DOM Elements for enhanced features
    const exportActivitiesBtn = document.getElementById('exportActivities');
    const importActivitiesBtn = document.getElementById('importActivities');
    const exportScheduleBtn = document.getElementById('exportSchedule');
    const importFileInput = document.getElementById('importFile');
    const expandCalendarBtn = document.getElementById('expandCalendar');

    // Initialize date picker with today's date
    const today = DateTime.now().toISODate();
    startDateInput.value = today;
    startDateInput.min = today;


    // Event Listeners
    addActivityBtn.addEventListener('click', addActivity);
    generateScheduleBtn.addEventListener('click', generateSchedule);
    clearAllBtn.addEventListener('click', clearAll);
    prevMonthBtn.addEventListener('click', previousMonth);
    nextMonthBtn.addEventListener('click', nextMonth);
    // Type filter event listener
    typeFilterSelect.addEventListener('change', function() {
        renderActivitiesList();
    });
    // Quick delete type button
    const quickDeleteTypeBtn = document.getElementById('quickDeleteType');
    if (quickDeleteTypeBtn) {
        quickDeleteTypeBtn.addEventListener('click', deleteAllOfSelectedType);
    }
    
    // Enhanced feature event listeners
    exportActivitiesBtn.addEventListener('click', exportActivities);
    importActivitiesBtn.addEventListener('click', () => importFileInput.click());
    exportScheduleBtn.addEventListener('click', exportSchedule);
    importFileInput.addEventListener('change', handleFileImport);
    
    // Expand calendar button
    if (expandCalendarBtn) {
        expandCalendarBtn.addEventListener('click', toggleExpandCalendar);
    }

    // Initialize calendar
    renderCalendar();
    updateDependenciesSelect();
    updateTypeFilterAndSuggestions();

    // Function to add a new activity
    function addActivity() {
        const name = activityNameInput.value.trim();
        const duration = parseInt(durationInput.value);
        const dependency = dependenciesSelect.value || null;
        const type = typeInput.value.trim() || 'Default';
        const allowNonWorkingDays = allowNonWorkingDaysSelect.value === 'true';
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
            type,
            dependency: dependency,
            allowNonWorkingDays: allowNonWorkingDays,
            startDate: null,
            endDate: null
        };

        // Add to state
        state.activities.push(activity);

        // Clear inputs
        activityNameInput.value = '';
        durationInput.value = '1';
        typeInput.value = '';

        // Update UI
        renderActivitiesList();
    updateDependenciesSelect();
        updateTypeFilterAndSuggestions();

        console.log('Activity added:', activity);
    }

    // Enhanced function to render activities list with edit buttons
            function renderActivitiesList() {
        // Get the selected type filter
        const selectedType = typeFilterSelect.value;
        
        // Filter activities by type if a type is selected
        let activitiesToShow = state.activities;
        if (selectedType) {
            activitiesToShow = state.activities.filter(a => (a.type || 'Default') === selectedType);
        }

        if (activitiesToShow.length === 0) {
            activitiesContainer.innerHTML = '<p class="empty-message">No activities ' + (selectedType ? 'of type "' + selectedType + '" ' : '') + 'added yet. Add your first activity above.</p>';
            return;
        }

        activitiesContainer.innerHTML = '';

        activitiesToShow.forEach(activity => {
            const activityElement = document.createElement('div');
            activityElement.className = 'activity-item';
            
            // Build HTML string using concatenation
            let html = '';
            html += '<div class="activity-info">';
            html += '<h4>' + escapeHtml(activity.name) + '</h4>';
            html += '<p>Duration: ' + activity.duration + ' day' + (activity.duration > 1 ? 's' : '') + '</p>';
            html += '<p>Type: ' + escapeHtml(activity.type || 'Default') + '</p>';
            let depsText = 'None';
            if (activity.dependency) {
                depsText = escapeHtml(getActivityName(activity.dependency));
            }
            html += '<p>Dependency: ' + depsText + '</p>';
            if (activity.startDate) {
                html += '<p>Schedule: ' + formatDate(activity.startDate) + ' - ' + formatDate(activity.endDate) + '</p>';
            }
            html += '</div>';
            html += '<div class="activity-actions">';
            html += '<button class="btn-secondary edit-activity-btn" onclick="editActivity(\'' + activity.id + '\')">';
            html += '<i class="fas fa-edit"></i> Edit';
            html += '</button>';
            html += '<button class="btn-secondary edit-date-btn" onclick="editActivityDate(\'' + activity.id + '\')">';
            html += '<i class="fas fa-calendar-edit"></i> Edit Date';
            html += '</button>';
            html += '<button class="btn-danger" onclick="removeActivity(\'' + activity.id + '\')">';
            html += '<i class="fas fa-trash"></i> Remove';
            html += '</button>';
            html += '</div>';
            
            activityElement.innerHTML = html;
            activitiesContainer.appendChild(activityElement);
        });
    }

    // Function to format date for display
    function formatDate(dateObj) {
        if (!dateObj) return 'Not scheduled';
        return dateObj.toLocaleString();
    }
    // Helper to escape HTML special characters
    function escapeHtml(text) {
        if (typeof text !== 'string') return text;
        return text
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }

    // Function to edit activity date (exposed to window)
    window.editActivityDate = function(id) {
    try {
    console.log("Function called with id:", id);
        const activity = state.activities.find(a => a.id === id);
        if (!activity) return;

        // Create a date picker dialog
        const newStartDate = prompt(`Edit start date for "${activity.name}" (YYYY-MM-DD):`, 
            activity.startDate ? activity.startDate.toISODate() : '');
        
        if (newStartDate && newStartDate.match(/^\d{4}-\d{2}-\d{2}$/)) {
            const startDate = DateTime.fromISO(newStartDate);
            const endDate = calculateEndDate(startDate, activity);
            
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
    } catch (error) {
        console.error(error);
        return;
    }
    }
    // Function to edit activity (name, duration, dependency, allowNonWorkingDays) (exposed to window)
    window.editActivity = function(id) {
    try {
    console.log("Function called with id:", id);
        const activity = state.activities.find(a => a.id === id);
        if (!activity) return;

        // Create a form for editing
        const newName = prompt('Edit activity name:', activity.name);
        if (newName === null) return; // User cancelled

        const newDuration = prompt('Edit duration (days):', activity.duration);
        if (newDuration === null) return;

        const duration = parseInt(newDuration);
        if (isNaN(duration) || duration < 1) {
            alert('Duration must be a positive number');
            return;
        }

        // Show current dependency and let user edit
        let currentDep = '';
        let currentDepName = '';
        if (activity.dependency) {
            currentDep = activity.dependency;
            currentDepName = getActivityName(activity.dependency);
        }
        const depsPrompt = prompt('Edit dependency (enter activity ID, leave empty for none).\nCurrent dependency ID: ' + currentDep + ' (' + currentDepName + ')\n\nYou can copy the ID from the input below.\n\nAvailable activities:\n' + 
            state.activities.filter(a => a.id !== id).map(a => a.id + ': ' + a.name).join('\n'), 
            activity.dependency || '');
        
        let newDependency = null;
        if (depsPrompt !== null && depsPrompt.trim() !== '') {
            const depId = depsPrompt.trim();
            // Validate ID exists
            if (!state.activities.find(a => a.id === depId)) {
                alert('Invalid activity ID: ' + depId);
                return;
            }
            newDependency = depId;
        }

        // Prompt for allowNonWorkingDays
        const currentAllow = activity.allowNonWorkingDays || false;
        const newAllow = confirm('Allow on non-working days?\n\nCurrent: ' + (currentAllow ? 'Yes' : 'No') + '\n\nClick OK for Yes, Cancel for No.');
        
        // Update activity
        activity.name = newName.trim();
        activity.duration = duration;
        activity.dependency = newDependency;
        activity.allowNonWorkingDays = newAllow;

        // If the activity is scheduled, we need to reschedule
        // For now, we'll remove the schedule and let the user regenerate
        // Remove from schedule
        state.schedule = state.schedule.filter(a => a.id !== id);
        activity.startDate = null;
        activity.endDate = null;

        // Update UI
        renderActivitiesList();
        updateDependenciesSelect();
        updateTypeFilterAndSuggestions();
        renderScheduleTimeline();
        renderCalendar();
    } catch (error) {
        console.error(error);
        return;
    }
    };

    // Function to calculate end date based on start date and activity
    function calculateEndDate(startDate, activity) {
        let currentDate = startDate;
        let daysScheduled = 0;
        
        while (daysScheduled < activity.duration) {
            if (!isDayAllowedForActivity(currentDate, activity)) {
                currentDate = currentDate.plus({ days: 1 });
                continue;
            }
            daysScheduled++;
            if (daysScheduled === activity.duration) break;
            currentDate = currentDate.plus({ days: 1 });
        }
        return currentDate;
    }

    // Function to update dependency select dropdown
function updateDependenciesSelect() {
        dependenciesSelect.innerHTML = '<option value="">None</option>';
        
        state.activities.forEach(activity => {
            const option = document.createElement('option');
            option.value = activity.id;
            option.textContent = activity.name;
            dependenciesSelect.appendChild(option);
        });
    }

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
        if (typeOptionsDatalist) {
            typeOptionsDatalist.innerHTML = '';
            // Also include some default options if there are no types yet
            if (types.length === 0) {
                const defaultTypes = ['Development', 'Design', 'Meeting', 'Testing', 'Documentation', 'Other'];
                defaultTypes.forEach(type => {
                    const option = document.createElement('option');
                    option.value = type;
                    typeOptionsDatalist.appendChild(option);
                });
            } else {
                types.forEach(type => {
                    const option = document.createElement('option');
                    option.value = type;
                    typeOptionsDatalist.appendChild(option);
                });
            }
        }
    }

    // Function to delete all activities of the selected type
    function deleteAllOfSelectedType() {
        const selectedType = typeFilterSelect.value;
        if (!selectedType) {
            alert('Please select a type to delete');
            return;
        }

        // Filter activities of the selected type
        const activitiesToDelete = state.activities.filter(a => (a.type || 'Default') === selectedType);
        if (activitiesToDelete.length === 0) {
            alert(`No activities of type "${selectedType}" found`);
            return;
        }

        // Check for dependencies: if any activity of other types depends on these activities
        const dependentActivities = [];
        activitiesToDelete.forEach(activity => {
            const deps = state.activities.filter(a => a.dependency === activity.id);
            deps.forEach(dep => {
                if (!activitiesToDelete.some(a => a.id === dep.id)) {
                    dependentActivities.push(dep);
                }
            });
        });

        if (dependentActivities.length > 0) {
            const depNames = dependentActivities.map(a => a.name).join(', ');
            if (!confirm(`The following activities depend on activities of type "${selectedType}": ${depNames}. Deleting these activities will break dependencies. Do you still want to proceed?`)) {
                return;
            }
        }

        // Remove the activities
        const idsToDelete = new Set(activitiesToDelete.map(a => a.id));
        state.activities = state.activities.filter(a => !idsToDelete.has(a.id));
        state.schedule = state.schedule.filter(a => !idsToDelete.has(a.id));

        // Update UI
        renderActivitiesList();
        updateDependenciesSelect();
        updateTypeFilterAndSuggestions();
        renderScheduleTimeline();
        renderCalendar();

        alert(`Deleted ${activitiesToDelete.length} activities of type "${selectedType}"`);
    }

    // Function to get activity name by ID
    function getActivityName(id) {
        const activity = state.activities.find(a => a.id === id);
        return activity ? activity.name : 'Unknown';
    }

    // Enhanced function to remove an activity
    window.removeActivity = function(id) {
    try {
    console.log("Function called with id:", id);
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
    updateDependenciesSelect();
        updateTypeFilterAndSuggestions();
        renderScheduleTimeline();
        renderCalendar();
    } catch (error) {
        console.error(error);
        return;
    }
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
                // Skip weekends and holidays unless activity allows non-working days
                if (!isDayAllowedForActivity(currentDate, activity)) {
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

        let currentDate = state.startDate;
        let availableActivities = toAutoSchedule.filter(a => 
            !scheduledActivities.has(a.id) && 
            (a.dependency === null || scheduledActivities.has(a.dependency))
        );

        while (availableActivities.length > 0) {
            // Sort by duration (shortest first) for better scheduling
            availableActivities.sort((a, b) => a.duration - b.duration);
            
            // Schedule all available activities
            for (const activity of availableActivities) {
                currentDate = scheduleActivity(activity, currentDate);
            }

            // Update available activities
            availableActivities = toAutoSchedule.filter(a => 
                !scheduledActivities.has(a.id) && 
                (a.dependency === null || scheduledActivities.has(a.dependency))
            );
        }

        // Check for unscheduled activities
        if (scheduledActivities.size < state.activities.length) {
            const unscheduled = state.activities.filter(a => !scheduledActivities.has(a.id));
            // Check if any unscheduled activities have missing dependencies
            const missingDeps = unscheduled.filter(a => a.dependency && !state.activities.find(b => b.id === a.dependency));
            if (missingDeps.length > 0) {
                throw new Error(`Cannot schedule activities because their dependencies are missing: ${missingDeps.map(a => a.name).join(', ')}`);
            }
            // Otherwise, assume circular dependency
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

    // Function to check if a day is allowed for an activity
    function isDayAllowedForActivity(date, activity) {
        if (activity.allowNonWorkingDays) {
            return true; // Activity can be scheduled on any day
        }
        return isWorkingDay(date);
    }

    // Function to check if a day is actually scheduled for an activity
    function isDayScheduledForActivity(date, activity) {
        if (!activity.startDate || !activity.endDate) return false;
        const start = activity.startDate.startOf('day');
        const end = activity.endDate.startOf('day');
        const current = date.startOf('day');
        if (!DateTime.isBetween(current, start, end)) return false;
        return isDayAllowedForActivity(date, activity);
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
            
            let timelineHTML = '';
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
            timelineItem.innerHTML = timelineHTML;
            
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
            const scheduledActivities = state.schedule.filter(activity => 
                isDayScheduledForActivity(currentDate, activity)
            );
            
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
        const activitiesOnDate = state.schedule.filter(activity => 
            isDayScheduledForActivity(clickedDate, activity)
        );
        
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
                        const endDate = calculateEndDate(startDate, activity);
                        
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
    updateDependenciesSelect();
        updateTypeFilterAndSuggestions();
        renderScheduleTimeline();
        renderCalendar();
        
        // Reset start date to today
        startDateInput.value = today;
    }

    // Import/Export Functions
    function exportActivities() {
        if (state.activities.length === 0) {
            alert('No activities to export');
            return;
        }
        
        // Prepare data for export - include IDs to preserve dependencies
        const exportData = {
            activities: state.activities.map(activity => ({
                id: activity.id,
                name: activity.name,
                duration: activity.duration,
                dependency: activity.dependency,
                type: activity.type || 'Default',
                allowNonWorkingDays: activity.allowNonWorkingDays || false
            })),
            exportedAt: new Date().toISOString(),
            version: '2.0'
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
                    // Check version to determine if IDs are included
                    const hasIds = importData.version === '2.0' && importData.activities.every(a => a.id);
                    
                    // First, collect all imported activities in a temporary array
                    const importedActivities = [];
                    const idMap = {};
                    
                    importData.activities.forEach(activityData => {
                        const activity = {
                            id: hasIds ? activityData.id : generateId(),
                            name: activityData.name,
                            duration: activityData.duration,
                            dependency: activityData.dependency || null,
                            type: activityData.type || 'Default',
                            allowNonWorkingDays: activityData.allowNonWorkingDays || false,
                            startDate: null,
                            endDate: null
                        };
                        importedActivities.push(activity);
                        idMap[activity.id] = activity;
                    });
                    
                    // Resolve dependencies for new version (by ID)
                    if (hasIds) {
                        importedActivities.forEach(activity => {
                            if (activity.dependency && !idMap[activity.dependency]) {
                                // Dependency ID not found in imported set
                                activity.dependency = null;
                            }
                        });
                    } else {
                        // Old version: dependencies are stored as names
                        // Create a mapping from activity name to ID (assuming names are unique)
                        const nameToId = {};
                        importedActivities.forEach(activity => {
                            nameToId[activity.name] = activity.id;
                        });
                        
                        // Update dependencies
                        importedActivities.forEach(activity => {
                            if (activity.dependency) {
                                // Find the dependency by name
                                const depActivity = importedActivities.find(a => a.name === activity.dependency);
                                if (depActivity) {
                                    activity.dependency = depActivity.id;
                                } else {
                                    activity.dependency = null;
                                }
                            }
                        });
                    }
                    
                    // Add to state
                    importedActivities.forEach(activity => state.activities.push(activity));
                    
                    alert(`Successfully imported ${importData.activities.length} activities!`);
                } else if (importData.schedule) {
                    // Import schedule - preserve IDs if available
                    const hasIds = importData.version === '2.0' && importData.schedule.every(a => a.id);
                    importData.schedule.forEach(scheduleData => {
                        const activity = {
                            id: hasIds ? scheduleData.id : generateId(),
                            name: scheduleData.name,
                            duration: scheduleData.duration,
                            dependency: scheduleData.dependency || null,
                            type: scheduleData.type || 'Default',
                            allowNonWorkingDays: scheduleData.allowNonWorkingDays || false,
                            startDate: scheduleData.startDate ? DateTime.fromISO(scheduleData.startDate) : null,
                            endDate: scheduleData.endDate ? DateTime.fromISO(scheduleData.endDate) : null
                        };
                        state.activities.push(activity);
                        if (activity.startDate) {
                            state.schedule.push({ ...activity });
                        }
                    });
                    
                    // Fix dependencies for old version
                    if (!hasIds) {
                        const nameToId = {};
                        state.activities.forEach(activity => {
                            nameToId[activity.name] = activity.id;
                        });
                        state.activities.forEach(activity => {
                            if (activity.dependency) {
                                const depActivity = state.activities.find(a => a.name === activity.dependency);
                                if (depActivity) {
                                    activity.dependency = depActivity.id;
                                } else {
                                    activity.dependency = null;
                                }
                            }
                        });
                        state.schedule.forEach(activity => {
                            if (activity.dependency) {
                                const depActivity = state.activities.find(a => a.name === activity.dependency);
                                if (depActivity) {
                                    activity.dependency = depActivity.id;
                                } else {
                                    activity.dependency = null;
                                }
                            }
                        });
                    }
                    
                    alert(`Successfully imported ${importData.schedule.length} scheduled activities!`);
                } else {
                    throw new Error('Invalid file format');
                }
                
                // Update UI
                renderActivitiesList();
                updateDependenciesSelect();
                updateTypeFilterAndSuggestions();
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


    // Helper function to generate unique ID
    function generateId() {
        return Date.now().toString(36) + Math.random().toString(36).substr(2);
    }

    // Function to toggle calendar expanded view
    function toggleExpandCalendar() {
        state.calendarExpanded = !state.calendarExpanded;
        calendarElement.classList.toggle('expanded', state.calendarExpanded);
        
        // Update button text and icon
        if (expandCalendarBtn) {
            if (state.calendarExpanded) {
                expandCalendarBtn.innerHTML = '<i class="fas fa-compress"></i> Compress';
            } else {
                expandCalendarBtn.innerHTML = '<i class="fas fa-expand"></i> Expand';
            }
        }
    }
});
