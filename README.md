# Task Scheduler with Calendar

A modern, offline-capable web application for scheduling activities with dependencies, accounting for Hong Kong public holidays.

## Features

1. **Activity Management**
   - Add activities with names and durations
   - Set dependencies between activities
   - Remove activities with dependency validation

2. **Schedule Generation**
   - Automatic scheduling based on dependencies
   - Skips weekends and Hong Kong public holidays
   - Visual timeline of scheduled activities

3. **Calendar View**
   - Monthly calendar with color-coded days
   - Shows Hong Kong public holidays
   - Highlights scheduled activities
   - Navigate between months

4. **Hong Kong Public Holidays**
   - Includes holiday data for 2024-2026
   - Automatically excludes holidays from working days

5. **Offline Capability**
   - No external dependencies required
   - Uses built-in date utilities
   - Unicode icons as fallbacks

## Files Structure

- `index.html` - Main application interface
- `style.css` - Modern, responsive styling
- `holidays.js` - Hong Kong public holiday data (2024-2026)
- `date-utils.js` - Custom date manipulation library
- `script-offline.js` - Main application logic
- `script.js` - Original Luxon-based version (optional)

## How to Use

1. **Add Activities**
   - Enter activity name and duration (in days)
   - Select optional dependency from existing activities
   - Click "Add Activity"

2. **Generate Schedule**
   - Select start date for first activity
   - Click "Generate Schedule"

3. **View Results**
   - Calendar shows scheduled days (blue highlight)
   - Timeline lists activities with dates
   - Holidays are marked in red, weekends in yellow

4. **Navigation**
   - Use arrow buttons to navigate months
   - Click "Clear All" to reset everything

## Technical Details

- **Pure HTML/CSS/JavaScript** - No frameworks required
- **Responsive Design** - Works on mobile and desktop
- **Modern UI** - Clean, card-based interface with shadows and gradients
- **Offline Date Handling** - Custom DateUtils replaces Luxon library
- **Local Storage** - No data persistence needed (session-only)

## Running the Application

Open `index.html` in any modern web browser. The application runs entirely offline - no internet connection required.

Alternatively, serve the files using a simple HTTP server:
```bash
python3 -m http.server 3000
```
Then open `http://localhost:3000` in your browser.

## Requirements

- Modern web browser (Chrome, Firefox, Safari, Edge)
- No additional software or libraries needed

## License

Free to use and modify. Hong Kong public holiday data based on official government announcements.

## Credits

Created as a task scheduler and calendar planner with Hong Kong public holiday integration.