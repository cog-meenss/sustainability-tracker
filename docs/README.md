# Tracker Application Documentation

Welcome to the Tracker Application documentation. This folder contains guides and documentation for various features and components.

## 📚 Available Documentation

### Features Documentation
- **[AI Idea Ranking Guide](./AI-Idea-Ranking-Guide.md)** - Complete guide for the AI-powered idea evaluation and ranking system

### Development Documentation
- **[Copilot Instructions](../.github/copilot-instructions.md)** - AI coding assistant guidelines for the project

### Carbon Footprint Analysis
- **[Carbon Dashboard](../carbon-dashboard/)** - Interactive dashboard for analyzing application carbon footprint
- **Carbon Analyzer Scripts** - Python scripts for environmental impact analysis

## 🏗️ Project Structure

```
Tracker/
├── docs/ # Documentation (you are here)
│ ├── README.md # This file
│ └── AI-Idea-Ranking-Guide.md # AI evaluation system docs
├── frontend/ # React application
├── backend/ # Express.js server
├── carbon-dashboard/ # Environmental impact dashboard
└── .github/ # GitHub/development configs
```

## Quick Start Guides

### For Users
1. **Training Tab** - Upload and analyze training records
2. **Ideas Tab** - Upload ideas and use AI evaluation system
3. **Revenue & FTE Tab** - Upload leave/people data for calculations

### For Developers
1. Review **[Copilot Instructions](../.github/copilot-instructions.md)** for architecture patterns
2. See **[AI Idea Ranking Guide](./AI-Idea-Ranking-Guide.md)** for AI integration examples
3. Check **[Carbon Dashboard](../carbon-dashboard/)** for visualization techniques

## Features Overview

### Core Functionality
- **Excel File Processing** - Upload and process various Excel formats
- **Data Visualization** - Interactive grids and charts using Material-UI
- **Multi-tab Architecture** - Separate modules for different business domains

### Advanced Features
- **AI-Powered Idea Ranking** - OpenAI integration for intelligent evaluation
- **Carbon Footprint Analysis** - Environmental impact assessment tools
- **Persistent State Management** - Local storage for user preferences

### Technical Stack
- **Frontend**: React.js with Material-UI components
- **Backend**: Node.js with Express.js
- **Data Processing**: ExcelJS for file parsing
- **AI Integration**: OpenAI API for intelligent analysis
- **Visualization**: Chart.js and MUI Data Grid

## Configuration

### Environment Setup
```bash
# Backend
cd backend && npm install && npm start

# Frontend 
cd frontend && npm install && npm start
```

### API Keys
- OpenAI API key for AI idea evaluation (optional)
- UK Holidays API for working days calculation

## Future Documentation

As the project grows, this documentation will expand to include:
- API Reference
- Component Library
- Deployment Guides
- Testing Documentation
- Performance Optimization

---

*Last updated: November 2025*