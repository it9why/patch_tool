// Hong Kong Public Holidays Data for 2024-2026
// This data can be used offline

const hongKongHolidays = {
    "2024": [
        { date: "2024-01-01", name: "New Year's Day" },
        { date: "2024-02-10", name: "Chinese New Year (Day 1)" },
        { date: "2024-02-11", name: "Chinese New Year (Day 2)" },
        { date: "2024-02-12", name: "Chinese New Year (Day 3)" },
        { date: "2024-03-29", name: "Good Friday" },
        { date: "2024-03-30", name: "Holy Saturday" },
        { date: "2024-04-01", name: "Easter Monday" },
        { date: "2024-04-04", name: "Ching Ming Festival" },
        { date: "2024-05-01", name: "Labour Day" },
        { date: "2024-05-15", name: "Buddha's Birthday" },
        { date: "2024-06-10", name: "Tuen Ng (Dragon Boat) Festival" },
        { date: "2024-07-01", name: "Hong Kong Special Administrative Region Establishment Day" },
        { date: "2024-09-18", name: "Day after Mid-Autumn Festival" },
        { date: "2024-10-01", name: "National Day" },
        { date: "2024-10-11", name: "Chung Yeung Festival" },
        { date: "2024-12-25", name: "Christmas Day" },
        { date: "2024-12-26", name: "Boxing Day" }
    ],
    "2025": [
        { date: "2025-01-01", name: "New Year's Day" },
        { date: "2025-01-29", name: "Chinese New Year (Day 1)" },
        { date: "2025-01-30", name: "Chinese New Year (Day 2)" },
        { date: "2025-01-31", name: "Chinese New Year (Day 3)" },
        { date: "2025-04-18", name: "Good Friday" },
        { date: "2025-04-19", name: "Holy Saturday" },
        { date: "2025-04-21", name: "Easter Monday" },
        { date: "2025-04-04", name: "Ching Ming Festival" },
        { date: "2025-05-01", name: "Labour Day" },
        { date: "2025-05-05", name: "Buddha's Birthday" },
        { date: "2025-05-31", name: "Tuen Ng (Dragon Boat) Festival" },
        { date: "2025-07-01", name: "Hong Kong Special Administrative Region Establishment Day" },
        { date: "2025-10-06", name: "Day after Mid-Autumn Festival" },
        { date: "2025-10-01", name: "National Day" },
        { date: "2025-10-30", name: "Chung Yeung Festival" },
        { date: "2025-12-25", name: "Christmas Day" },
        { date: "2025-12-26", name: "Boxing Day" }
    ],
    "2026": [
        { date: "2026-01-01", name: "The first day of January" },
        { date: "2026-02-17", name: "Lunar New Year's Day" },
        { date: "2026-02-18", name: "The second day of Lunar New Year" },
        { date: "2026-02-19", name: "The third day of Lunar New Year" },
        { date: "2026-04-03", name: "Good Friday" },
        { date: "2026-04-04", name: "The day following Good Friday" },
        { date: "2026-04-06", name: "The day following Ching Ming Festival" },
        { date: "2026-04-07", name: "The day following Easter Monday" },
        { date: "2026-05-01", name: "Labour Day" },
        { date: "2026-05-25", name: "The day following the Birthday of the Buddha" },
        { date: "2026-06-19", name: "Tuen Ng Festival" },
        { date: "2026-07-01", name: "Hong Kong Special Administrative Region Establishment Day" },
        { date: "2026-09-26", name: "The day following the Chinese Mid-Autumn Festival" },
        { date: "2026-10-01", name: "National Day" },
        { date: "2026-10-19", name: "The day following Chung Yeung Festival" },
        { date: "2026-12-25", name: "Christmas Day" },
        { date: "2026-12-26", name: "The first weekday after Christmas Day" }
    ]
};

// Helper function to format a Date as YYYY-MM-DD using LOCAL date components
// (toISOString uses UTC which can shift the date in timezones like Hong Kong UTC+8)
function formatLocalDate(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}

// Function to check if a date is a Hong Kong public holiday
function isHongKongHoliday(date) {
    const dateString = formatLocalDate(date);
    const year = date.getFullYear().toString();
    
    if (hongKongHolidays[year]) {
        return hongKongHolidays[year].some(holiday => holiday.date === dateString);
    }
    return false;
}

// Function to get holiday name for a date
function getHolidayName(date) {
    const dateString = formatLocalDate(date);
    const year = date.getFullYear().toString();
    
    if (hongKongHolidays[year]) {
        const holiday = hongKongHolidays[year].find(h => h.date === dateString);
        return holiday ? holiday.name : null;
    }
    return null;
}

// Function to get all holidays for a month
function getHolidaysForMonth(year, month) {
    const yearStr = year.toString();
    if (!hongKongHolidays[yearStr]) return [];
    
    return hongKongHolidays[yearStr].filter(holiday => {
        const parts = holiday.date.split('-').map(Number);
        return parts[0] === year && (parts[1] - 1) === month;
    });
}

// Export for use in script.js
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        hongKongHolidays,
        isHongKongHoliday,
        getHolidayName,
        getHolidaysForMonth
    };
}