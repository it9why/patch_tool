// Date utilities to replace Luxon for offline functionality
const DateUtils = {
    // Create a DateTime-like object from a JavaScript Date
    fromDate(date) {
        return {
            date: new Date(date.getTime()),
            
            // Get ISO date string (YYYY-MM-DD)
            toISODate() {
                const year = this.date.getFullYear();
                const month = String(this.date.getMonth() + 1).padStart(2, '0');
                const day = String(this.date.getDate()).padStart(2, '0');
                return `${year}-${month}-${day}`;
            },
            
            // Get localized date string
            toLocaleString(format) {
                if (format && format.month === 'long' && format.year === 'numeric') {
                    const options = { month: 'long', year: 'numeric' };
                    return this.date.toLocaleDateString('en-US', options);
                }
                // Default to short date
                return this.date.toLocaleDateString('en-US');
            },
            
            // Add days to date
            plus({ days = 0, months = 0, years = 0 }) {
                const newDate = new Date(this.date.getTime());
                newDate.setDate(newDate.getDate() + days);
                newDate.setMonth(newDate.getMonth() + months);
                newDate.setFullYear(newDate.getFullYear() + years);
                return DateUtils.fromDate(newDate);
            },
            
            // Subtract months from date
            minus({ days = 0, months = 0, years = 0 }) {
                return this.plus({ days: -days, months: -months, years: -years });
            },
            
            // Get weekday (1 = Monday, 7 = Sunday)
            get weekday() {
                const jsWeekday = this.date.getDay(); // 0 = Sunday, 6 = Saturday
                return jsWeekday === 0 ? 7 : jsWeekday;
            },
            
            // Get year
            get year() {
                return this.date.getFullYear();
            },
            
            // Get month (1-12)
            get month() {
                return this.date.getMonth() + 1;
            },
            
            // Get day of month
            get day() {
                return this.date.getDate();
            },
            
            // Get days in month
            get daysInMonth() {
                const year = this.year;
                const month = this.month;
                return new Date(year, month, 0).getDate();
            },
            
            // Start of day (set time to 00:00:00)
            startOf(unit) {
                if (unit === 'day') {
                    const newDate = new Date(this.date.getTime());
                    newDate.setHours(0, 0, 0, 0);
                    return DateUtils.fromDate(newDate);
                }
                return this;
            },
            
            // Convert to JavaScript Date
            toJSDate() {
                return new Date(this.date.getTime());
            },
            
            // Compare dates
            valueOf() {
                return this.date.getTime();
            }
        };
    },
    
    // Create from ISO string (YYYY-MM-DD)
    fromISO(isoString) {
        const [year, month, day] = isoString.split('-').map(Number);
        const date = new Date(year, month - 1, day);
        return this.fromDate(date);
    },
    
    // Create from year, month, day
    local(year, month, day) {
        const date = new Date(year, month - 1, day);
        return this.fromDate(date);
    },
    
    // Get current date/time
    now() {
        return this.fromDate(new Date());
    },
    
    // Check if two date objects represent the same day
    isSameDay(date1, date2) {
        return date1.toISODate() === date2.toISODate();
    },
    
    // Check if date1 is before date2 (by day)
    isBefore(date1, date2) {
        const d1 = date1.startOf('day').valueOf();
        const d2 = date2.startOf('day').valueOf();
        return d1 < d2;
    },
    
    // Check if date1 is after date2 (by day)
    isAfter(date1, date2) {
        const d1 = date1.startOf('day').valueOf();
        const d2 = date2.startOf('day').valueOf();
        return d1 > d2;
    },
    
    // Check if date is between start and end (inclusive)
    isBetween(date, start, end) {
        const d = date.startOf('day').valueOf();
        const s = start.startOf('day').valueOf();
        const e = end.startOf('day').valueOf();
        return d >= s && d <= e;
    }
};

// Export for use in browser
if (typeof window !== 'undefined') {
    window.DateUtils = DateUtils;
}

// Export for Node.js
if (typeof module !== 'undefined' && module.exports) {
    module.exports = DateUtils;
}