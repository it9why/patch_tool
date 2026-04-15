// Main application logic for Task Scheduler
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Luxon DateTime for date manipulation
    const DateTime = luxon.DateTime;
    
    // State management
    const state = {
        activities: [],
        schedule: [],
        currentDate: DateTime.now(),
        calendarMonth: DateTime.now(),
        startDate: null
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

    // Function to render activities list
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
                </div>
                <div class="activity-actions">
                    <button class="btn-danger" onclick="removeActivity('${activity.id}')">
                        <i class="fas fa-trash"></i> Remove
                    </button>
                </div>
            `;
            activitiesContainer.appendChild(activityElement);
        });
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

    // Function to remove an activity
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

        // Update UI
        renderActivitiesList();
        updateDependencySelect();
        clearSchedule();
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
            activity.startDate = null;
            activity.endDate = null;
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

        // Find activities with no dependencies to start
        let availableActivities = activitiesToSchedule.filter(a => !a.dependency);
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
            availableActivities = activitiesToSchedule.filter(a => 
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
        state.schedule.sort((a, b) => a.startDate - b.startDate);
    }

    // Function to check if a day is a working day (not weekend or holiday)
    function isWorkingDay(date) {
        // Check if it's a weekend (Saturday = 6, Sunday = 0 in Luxon)
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
            
            const startDateStr = activity.startDate.toLocaleString(DateTime.DATE_SHORT);
            const endDateStr = activity.endDate.toLocaleString(DateTime.DATE_SHORT);
            
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

    // Function to render calendar
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
                const activityStart = activity.startDate.startOf('day');
                const activityEnd = activity.endDate.startOf('day');
                const currentDay = currentDate.startOf('day');
                return currentDay >= activityStart && currentDay <= activityEnd;
            });
            
            if (scheduledActivities.length > 0) {
                dayElement.classList.add('scheduled');
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

    // Function to clear schedule only
    function clearSchedule() {
        state.schedule = [];
        state.startDate = null;
        renderScheduleTimeline();
        renderCalendar();
    }

    // Helper function to generate unique ID
    function generateId() {
        return Date.now().toString(36) + Math.random().toString(36).substr(2);
    }
});