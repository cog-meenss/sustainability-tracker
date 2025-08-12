# Tracker Backend

This folder contains the Node.js Express backend for the Tracker application.

## Overview

The backend is responsible for:
- Handling Excel file uploads (for Training, Ideas, Revenue & FTE tabs)
- Parsing and processing Excel files
- Serving API endpoints for frontend data requests
- Serving static files (if needed)

## Features
- **Excel File Upload API**: Accepts `.xlsx` and `.xls` files for analysis
- **Data Extraction**: Parses uploaded Excel files and returns structured data for frontend display
- **Error Handling**: Returns clear error messages for invalid uploads or processing errors
- **CORS Support**: Allows frontend (React) to communicate with the backend

## Getting Started

### Prerequisites
- Node.js (v16 or later recommended)
- npm (Node Package Manager)

### Setup
1. Install dependencies:
   ```bash
   npm install
   ```
2. Start the backend server:
   ```bash
   npm start
   ```
   By default, the server runs on `http://localhost:4000`.

## API Endpoints

### File Upload
- **POST** `/api/training-upload` — Upload Training Excel file
- **POST** `/api/ideas-upload` — Upload Ideas Excel file
- **POST** `/api/revenuefte-upload` — Upload Revenue & FTE Excel files (multi-file)

**Example (single file):**
```
POST /api/training-upload
Content-Type: multipart/form-data
Body: { excel: <file> }
```

**Example (multi-file):**
```
POST /api/revenuefte-upload
Content-Type: multipart/form-data
Body: { leave: <file>, people: <file> }
```

### Static Files
- Static files (if any) are served from the `public/` folder.

## Project Structure
```
backend/
├── public/           # Static assets (optional)
├── routes/           # Express route handlers
├── uploads/          # Temporary uploaded files (gitignored)
├── app.js            # Main Express app
├── package.json      # Dependencies and scripts
└── README.md         # This file
```

## Troubleshooting
- **Port in use:** Change the port in `app.js` if `4000` is occupied.
- **CORS errors:** Ensure the frontend is running on a different port (e.g., 3000) and CORS is enabled in the backend.
- **Excel parsing errors:** Check that files are valid `.xlsx` or `.xls` and not open in another program.

## Security Notes
- Uploaded files are processed and deleted after parsing.
- Do not expose sensitive data or credentials in the backend code.

## License
MIT

---
For questions or issues, please contact the project maintainer.

