# Tracker Application - AI Coding Guide

## Architecture Overview
This is a React + Express full-stack Excel processing application with:
- **Frontend**: React app (`frontend/`) using Material-UI components and MUI Data Grid
- **Backend**: Express server (`backend/server.js`) handling Excel file uploads and processing  
- **Deployment**: Single-server approach where Express serves both API routes and built React files
- **Domain**: Business data tracker for Training records, Ideas management, and Revenue/FTE analysis

## Key Architectural Patterns

### Tab-Based Module Architecture
Each business domain is implemented as a separate tab component:
- `TrainingTab.js` - Training records upload/analysis
- `IdeasTab.js` - Ideas tracking and management  
- `RevenueFteTab.js` - Revenue and FTE calculations
- `ChatSection.js` - Built-in help chat system

All tabs follow the same pattern: file upload → Excel processing → data grid display with filtering/sorting.

### State Management Strategy
- **Local state**: Component-level with `useState` for UI interactions
- **Persistence**: Direct `localStorage` for user preferences (views, filters, tab states)
- **Redux store**: Configured but minimally used (`store.js` has basic setup)
- **No global state sharing**: Each tab manages its own data independently

### Data Processing Flow
1. User uploads Excel files via Material-UI file inputs
2. Files sent to specific API endpoints (`/api/training-upload`, `/api/ideas-upload`, `/api/upload`)
3. Backend uses `XLSX` library to parse Excel → JSON conversion
4. Frontend displays data in MUI DataGrid with custom filtering/sorting
5. Results cached in localStorage for persistence across sessions

## Critical Development Patterns

### File Upload Implementation
```javascript
// Standard pattern in all tab components:
const formData = new FormData();
formData.append('excel', file);
const response = await fetch('/api/training-upload', {
  method: 'POST',
  body: formData
});
```

### Custom View System
Each tab implements a "saved views" system for column configurations:
- Views stored in `localStorage` as `{viewName: {columns: [], filters: {}, sort: {}}}`
- Pattern: `handleSelectView()`, `handleSaveView()`, `handleDeleteView()` methods
- Always check for view persistence on component mount

### Working Days Calculation
Business logic includes UK working days calculations with holiday exclusions:
- `utils/ukWorkingDays2025.js` - Static 2025 working days
- `backend/server.js` - Dynamic holiday API integration via `date.nager.at`
- Pattern: Filter weekends + UK public holidays for England & Wales only

## Development Workflows

### Local Development Setup
```bash
# Backend (runs on :4000)
cd backend && npm install && npm start

# Frontend (runs on :3000) 
cd frontend && npm install && npm start
```

### Production Deployment
- Build frontend: `cd frontend && npm run build`
- Backend serves built files from `../frontend/build`
- Single Express server handles both API and static file serving
- Fallback route `app.get('*')` serves React app for client-side routing

### Testing Approach
- `backend/calculationTest.js` contains manual calculation verification
- No automated test suite - testing is done via manual Excel upload verification
- Focus on data accuracy: upload known Excel files and verify calculations

## Excel Processing Conventions

### Column Mapping Strategy
- Headers read from first Excel row: `const columns = json[0]`
- Dynamic column detection - no hardcoded column assumptions
- UI allows users to select which columns to display via checkboxes
- Column visibility state persisted per tab in localStorage

### Multi-file Upload Pattern
RevenueFteTab handles multiple files differently:
```javascript
// Uses multer.fields() for multiple file types:
app.post('/api/upload', upload.fields([
  { name: 'leave' }, 
  { name: 'people' }
]), ...)
```

### CWR Detection Logic
Special business rule for "CWR" (Cognizant Work from Remote) entries:
- Backend function `isCWRRow()` checks multiple fields for CWR indicators
- Used for filtering and special processing in calculations

## Integration Points

### External APIs
- **UK Holidays API**: `https://date.nager.at/api/v3/PublicHolidays/{year}/GB`
- Cached in `holidaysCache` object to avoid repeated requests
- Filters to England & Wales only: `h.counties === null || counties.includes('GB-ENG')`

### Material-UI Components
- Heavy usage of MUI Data Grid for all tabular data
- Custom toolbar integration: `GridToolbar` component
- Consistent theming with Material-UI icons (`@mui/icons-material`)

### Chart Integration
- `@mui/x-charts` for data visualization
- Chart columns configurable per tab via dropdown selectors
- Pattern: `chartColumns` state tracks which data columns to visualize

## File Structure Conventions
- `src/` contains all React components (flat structure, no folders)
- `utils/` for pure utility functions (CSV export, date calculations)
- `assets/` for static resources (logo.png)
- Backend logic concentrated in single `server.js` file
- No separate routes/controllers - all API handlers in main server file