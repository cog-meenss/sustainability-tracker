// Example data structure - Replace with actual analyzer output
// 
// To use with real data:
// 1. Run: python cli.py /path/to/project --format json --output ./dashboard/
// 2. Load the generated complete_analysis.json file
// 3. Map the analyzer output fields to this structure
// 
// This example shows the expected data format for the Tracker project analysis
const reportData = {
  summary: {
    total_files_analyzed: 35,
    lines_of_code: 4850,
    total_energy_consumption_kwh: 0.218859,
    estimated_co2_emissions_kg: 0.109429,
    total_dependencies: 26,
    high_impact_files_count: 6
  },
  energy_breakdown: {
    'Static Analysis': 0.2135,
    'Runtime Operations': 0.0000,
    'Memory Usage': 0.004909,
    'Network Transfer': 0.00045
  },
  file_analysis: {
    'server.js': {lines: 53, carbon_impact_score: 11.53, complexity: {loops: 1, functions: 0, async_operations: 3, api_calls: 0, file_operations: 0}},
    'backend/server.js': {lines: 497, carbon_impact_score: 238.97, complexity: {loops: 58, functions: 14, async_operations: 24, api_calls: 8, file_operations: 0}},
    'frontend/src/App.js': {lines: 576, carbon_impact_score: 56.76, complexity: {loops: 10, functions: 1, async_operations: 10, api_calls: 0, file_operations: 0}},
    'frontend/src/RevenueFteTab.js': {lines: 884, carbon_impact_score: 241.84, complexity: {loops: 91, functions: 5, async_operations: 14, api_calls: 1, file_operations: 0}},
    'frontend/src/TrainingTab.js': {lines: 857, carbon_impact_score: 126.57, complexity: {loops: 49, functions: 1, async_operations: 5, api_calls: 1, file_operations: 0}},
    'frontend/src/IdeasTab.js': {lines: 935, carbon_impact_score: 147.35, complexity: {loops: 50, functions: 1, async_operations: 11, api_calls: 1, file_operations: 0}}
  },
  recommendations: [
    "Heavy packages detected: exceljs, multer, @emotion/react... - Consider lighter alternatives",
    "High memory usage estimated - implement data pagination and lazy loading",
    "Excel Processing: Cache processed data to avoid re-computation",
    "Data Grid: Implement virtual scrolling for large datasets",
    "API Optimization: Batch similar requests and implement request debouncing",
    "Frontend: Use React.memo for heavy components to prevent unnecessary re-renders",
    "Bundle Optimization: Implement code splitting for different tabs (Training, Ideas, Revenue)",
    "Data Management: Consider moving heavy calculations to background workers"
  ]
};
