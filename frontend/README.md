# Tracker Frontend

This folder contains the React-based frontend for the Tracker application.

## Overview
The frontend provides a modern, user-friendly interface for uploading, analyzing, and visualizing data from Excel files. It interacts with the backend API to process files and display results for Training, Ideas, and Revenue & FTE management.

## Features
- **Excel Upload:** Upload and process `.xlsx`/`.xls` files for multiple business domains.
- **Dynamic Tables:** Interactive data grids for filtering, sorting, and viewing results.
- **Saved Views:** Save, load, and manage custom column configurations for each tab.
- **Multi-Tab Navigation:** Switch between Training, Ideas, and Revenue & FTE modules.
- **Real-Time Feedback:** Displays upload progress, errors, and processing status.
- **Chat Help:** Built-in chat assistant for app usage guidance.

## Getting Started

### Prerequisites
- Node.js (v16 or later recommended)
- npm (Node Package Manager)
- Backend server running (see `../backend/README.md`)

### Setup
1. Install dependencies:
   ```bash
   npm install
   ```
2. Start the frontend server:
   ```bash
   npm start
   ```
   The app will run on `http://localhost:3000` by default.

## Usage
- Upload Excel files in the relevant tab (Training, Ideas, Revenue & FTE)
- Use the column selector to customize table views
- Save or load custom views as needed
- Use the built-in chat for help or tips

## Project Structure
```
frontend/
├── public/             # Static assets
├── src/
│   ├── App.js          # Main app entry
│   ├── TrainingTab.js  # Training tab logic
│   ├── IdeasTab.js     # Ideas tab logic
│   ├── RevenueFteTab.js# Revenue & FTE tab logic
│   ├── ChatSection.js  # Chat UI
│   ├── store.js        # Redux/store setup
│   └── ...             # Other components/utilities
├── package.json        # Dependencies and scripts
└── README.md           # This file
```

## API Integration
- Communicates with the backend via HTTP (see backend API docs)
- All file uploads and data requests are sent to `http://localhost:4000/api/*`

## Troubleshooting
- **CORS errors:** Ensure backend is running and CORS is enabled
- **Upload issues:** Check file format and size; refresh if needed
- **State not persisting:** Saved views and selections are stored in browser localStorage
- **Port conflicts:** Change frontend port in `.env` or `package.json` if needed

## Customization
- UI built with [Material-UI (MUI)](https://mui.com/)
- Responsive design for desktop and mobile
- Easily extendable for new tabs or data sources

## License
MIT

---
For questions or issues, please contact the project maintainer.
