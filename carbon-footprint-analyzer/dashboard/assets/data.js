// Carbon Footprint Data
const carbonData = {
    summary: {
        totalFilesAnalyzed: 35,
        linesOfCode: 4850,
        totalEnergyConsumptionKwh: 0.218859,
        estimatedCo2EmissionsKg: 0.109429,
        totalDependencies: 26,
        highImpactFilesCount: 6
    },
    
    energyBreakdown: {
        staticAnalysis: { value: 0.213500, percentage: 97.6 },
        runtimeOperations: { value: 0.000000, percentage: 0.0 },
        memoryUsage: { value: 0.004909, percentage: 2.2 },
        networkTransfer: { value: 0.000450, percentage: 0.2 }
    },
    
    fileAnalysis: [
        {
            file: "backend/server.js",
            lines: 497,
            impactScore: 238.97,
            complexity: {
                loops: 58,
                functions: 14,
                asyncOperations: 24,
                apiCalls: 8,
                fileOperations: 0
            },
            issues: ["High async operations", "Multiple API calls"],
            recommendations: [
                "🔄 High async operations detected - consider connection pooling",
                "⚡ Consider implementing request rate limiting"
            ]
        },
        {
            file: "frontend/src/RevenueFteTab.js",
            lines: 884,
            impactScore: 241.84,
            complexity: {
                loops: 91,
                functions: 5,
                asyncOperations: 14,
                apiCalls: 1,
                fileOperations: 0
            },
            issues: ["Heavy data processing", "Many loops"],
            recommendations: [
                "🔄 Heavy data processing - consider virtualization",
                "📊 Implement data pagination for large datasets",
                "💾 Add memoization for expensive calculations"
            ]
        },
        {
            file: "frontend/src/IdeasTab.js",
            lines: 935,
            impactScore: 147.35,
            complexity: {
                loops: 50,
                functions: 1,
                asyncOperations: 11,
                apiCalls: 1,
                fileOperations: 0
            },
            issues: ["Heavy data processing", "Large file"],
            recommendations: [
                "🔄 Heavy data processing - consider virtualization",
                "📊 Implement data pagination for large datasets",
                "💾 Add memoization for expensive calculations"
            ]
        },
        {
            file: "frontend/src/TrainingTab.js",
            lines: 857,
            impactScore: 126.57,
            complexity: {
                loops: 49,
                functions: 1,
                asyncOperations: 5,
                apiCalls: 1,
                fileOperations: 0
            },
            issues: ["Heavy data processing", "Large file"],
            recommendations: [
                "🔄 Heavy data processing - consider virtualization",
                "📊 Implement data pagination for large datasets",
                "💾 Add memoization for expensive calculations"
            ]
        },
        {
            file: "frontend/src/App.js",
            lines: 576,
            impactScore: 56.76,
            complexity: {
                loops: 10,
                functions: 1,
                asyncOperations: 10,
                apiCalls: 0,
                fileOperations: 0
            },
            issues: ["No major issues"],
            recommendations: [
                "⚛️ Implement React.lazy for code splitting"
            ]
        },
        {
            file: "server.js",
            lines: 53,
            impactScore: 11.53,
            complexity: {
                loops: 1,
                functions: 0,
                asyncOperations: 3,
                apiCalls: 0,
                fileOperations: 0
            },
            issues: ["No major issues"],
            recommendations: [
                "⚡ Consider implementing request rate limiting"
            ]
        }
    ],
    
    recommendations: [
        {
            id: 1,
            title: "Excel Processing Optimization",
            description: "Cache processed data to avoid re-computation and reduce CPU usage",
            priority: "high",
            impact: "High",
            effort: "Medium",
            category: "Performance"
        },
        {
            id: 2,
            title: "Data Grid Virtualization",
            description: "Implement virtual scrolling for large datasets to reduce memory usage",
            priority: "high",
            impact: "High",
            effort: "High",
            category: "Memory"
        },
        {
            id: 3,
            title: "API Request Batching",
            description: "Batch similar requests and implement request debouncing",
            priority: "medium",
            impact: "Medium",
            effort: "Low",
            category: "Network"
        },
        {
            id: 4,
            title: "React Component Optimization",
            description: "Use React.memo for heavy components to prevent unnecessary re-renders",
            priority: "medium",
            impact: "Medium",
            effort: "Low",
            category: "Performance"
        },
        {
            id: 5,
            title: "Bundle Code Splitting",
            description: "Implement code splitting for different tabs (Training, Ideas, Revenue)",
            priority: "medium",
            impact: "Medium",
            effort: "Medium",
            category: "Bundle Size"
        },
        {
            id: 6,
            title: "Background Processing",
            description: "Move heavy calculations to background workers",
            priority: "low",
            impact: "High",
            effort: "High",
            category: "Performance"
        },
        {
            id: 7,
            title: "Dependency Audit",
            description: "Consider lighter alternatives to heavy packages like ExcelJS",
            priority: "low",
            impact: "Medium",
            effort: "High",
            category: "Dependencies"
        },
        {
            id: 8,
            title: "Data Pagination",
            description: "Implement data pagination and lazy loading for better performance",
            priority: "medium",
            impact: "Medium",
            effort: "Medium",
            category: "Performance"
        }
    ],
    
    implementationGuide: {
        quick: [
            {
                title: "Enable React.memo",
                description: "Wrap heavy components with React.memo to prevent unnecessary re-renders",
                code: "const MyComponent = React.memo(({ data }) => { ... });",
                timeToImplement: "1-2 hours",
                impact: "Immediate 10-15% performance improvement"
            },
            {
                title: "Add Request Debouncing",
                description: "Implement debouncing for search and filter operations",
                code: "const debouncedSearch = useMemo(() => debounce(searchFunction, 300), []);",
                timeToImplement: "30 minutes",
                impact: "Reduces API calls by 60-80%"
            },
            {
                title: "Compress API Responses",
                description: "Enable gzip compression in Express server",
                code: "app.use(compression());",
                timeToImplement: "15 minutes",
                impact: "Reduces network usage by 70%"
            }
        ],
        medium: [
            {
                title: "Implement Virtual Scrolling",
                description: "Use react-window for large data grids",
                timeToImplement: "1-2 days",
                impact: "Handles 10,000+ rows efficiently"
            },
            {
                title: "Code Splitting by Route",
                description: "Split bundles for different application tabs",
                timeToImplement: "2-3 days",
                impact: "Reduces initial bundle size by 40%"
            },
            {
                title: "Excel Processing Cache",
                description: "Implement Redis cache for processed Excel data",
                timeToImplement: "1 week",
                impact: "Eliminates re-processing, 90% faster"
            }
        ],
        long: [
            {
                title: "Microservices Architecture",
                description: "Split Excel processing into separate service",
                timeToImplement: "2-4 weeks",
                impact: "Scalable processing, better resource management"
            },
            {
                title: "Progressive Web App",
                description: "Convert to PWA with offline capabilities",
                timeToImplement: "3-6 weeks",
                impact: "Reduces server load, better user experience"
            },
            {
                title: "Edge Computing",
                description: "Deploy processing closer to users",
                timeToImplement: "4-8 weeks",
                impact: "Reduces latency and energy consumption"
            }
        ]
    },
    
    // Mock trend data for demonstration
    trendData: {
        daily: [
            { date: '2025-11-01', co2: 0.125, energy: 0.25 },
            { date: '2025-11-02', co2: 0.118, energy: 0.236 },
            { date: '2025-11-03', co2: 0.122, energy: 0.244 },
            { date: '2025-11-04', co2: 0.115, energy: 0.23 },
            { date: '2025-11-05', co2: 0.111, energy: 0.222 },
            { date: '2025-11-06', co2: 0.108, energy: 0.216 },
            { date: '2025-11-07', co2: 0.109, energy: 0.218 },
            { date: '2025-11-08', co2: 0.109, energy: 0.219 }
        ]
    },
    
    dependencies: {
        frontend: [
            { name: "@emotion/react", category: "heavy", reason: "Large bundle size" },
            { name: "@mui/material", category: "heavy", reason: "UI framework overhead" },
            { name: "@mui/x-data-grid", category: "heavy", reason: "Data grid complexity" },
            { name: "exceljs", category: "heavy", reason: "Excel processing" },
            { name: "react", category: "heavy", reason: "Core framework" },
            { name: "react-dom", category: "heavy", reason: "DOM manipulation" }
        ],
        backend: [
            { name: "exceljs", category: "heavy", reason: "CPU intensive Excel processing" },
            { name: "multer", category: "heavy", reason: "File upload processing" },
            { name: "express", category: "medium", reason: "Server framework" },
            { name: "cors", category: "light", reason: "Simple middleware" }
        ]
    }
};

// Utility functions
function formatBytes(bytes) {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function formatNumber(num) {
    return new Intl.NumberFormat().format(num);
}

function formatCO2(kg) {
    if (kg < 0.001) {
        return (kg * 1000000).toFixed(0) + ' mg';
    } else if (kg < 1) {
        return (kg * 1000).toFixed(0) + ' g';
    } else {
        return kg.toFixed(3) + ' kg';
    }
}

function getImpactLevel(score) {
    if (score > 200) return 'high';
    if (score > 100) return 'medium';
    return 'low';
}

function getPriorityColor(priority) {
    const colors = {
        high: '#ff5252',
        medium: '#ff9800',
        low: '#4CAF50'
    };
    return colors[priority] || '#666';
}

// Export for use in other files
window.carbonData = carbonData;
window.formatBytes = formatBytes;
window.formatNumber = formatNumber;
window.formatCO2 = formatCO2;
window.getImpactLevel = getImpactLevel;
window.getPriorityColor = getPriorityColor;