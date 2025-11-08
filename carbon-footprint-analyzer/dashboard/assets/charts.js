// Chart.js configurations and chart creation functions

// Chart color palette
const chartColors = {
    primary: '#4CAF50',
    secondary: '#2196F3',
    warning: '#FF9800',
    danger: '#F44336',
    success: '#4CAF50',
    info: '#00BCD4',
    purple: '#9C27B0',
    gradient: {
        green: ['#66BB6A', '#4CAF50', '#388E3C'],
        blue: ['#64B5F6', '#2196F3', '#1976D2'],
        orange: ['#FFB74D', '#FF9800', '#F57C00'],
        red: ['#EF5350', '#F44336', '#D32F2F']
    }
};

// Chart default options
Chart.defaults.font.family = "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif";
Chart.defaults.color = '#666666';
Chart.defaults.plugins.legend.labels.usePointStyle = true;
Chart.defaults.plugins.legend.labels.padding = 20;

let charts = {}; // Store chart instances

// Energy Breakdown Pie Chart
function createEnergyChart() {
    const ctx = document.getElementById('energyChart').getContext('2d');
    
    const data = carbonData.energyBreakdown;
    const labels = Object.keys(data).map(key => 
        key.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase())
    );
    const values = Object.values(data).map(item => item.percentage);
    
    charts.energy = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: [
                    chartColors.success,
                    chartColors.warning,
                    chartColors.info,
                    chartColors.purple
                ],
                borderWidth: 3,
                borderColor: '#ffffff',
                hoverBorderWidth: 5,
                hoverBorderColor: '#ffffff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '60%',
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 20,
                        font: {
                            size: 12,
                            weight: '500'
                        }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const percentage = context.parsed + '%';
                            const energyValue = Object.values(carbonData.energyBreakdown)[context.dataIndex].value;
                            return `${label}: ${percentage} (${energyValue.toFixed(6)} kWh)`;
                        }
                    },
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    titleColor: '#ffffff',
                    bodyColor: '#ffffff',
                    borderColor: chartColors.primary,
                    borderWidth: 1
                }
            },
            animation: {
                animateRotate: true,
                duration: 1000
            }
        }
    });
}

// File Impact Bar Chart
function createFileImpactChart() {
    const ctx = document.getElementById('fileImpactChart').getContext('2d');
    
    const files = carbonData.fileAnalysis;
    const labels = files.map(file => file.file.split('/').pop());
    const scores = files.map(file => file.impactScore);
    const colors = scores.map(score => {
        if (score > 200) return chartColors.danger;
        if (score > 100) return chartColors.warning;
        return chartColors.success;
    });
    
    charts.fileImpact = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Carbon Impact Score',
                data: scores,
                backgroundColor: colors.map(color => color + '80'),
                borderColor: colors,
                borderWidth: 2,
                borderRadius: 4,
                borderSkipped: false,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Carbon Impact Score',
                        font: {
                            size: 12,
                            weight: '600'
                        }
                    },
                    grid: {
                        color: '#f0f0f0'
                    }
                },
                x: {
                    ticks: {
                        maxRotation: 45,
                        font: {
                            size: 10
                        }
                    },
                    grid: {
                        display: false
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        title: function(context) {
                            const fileIndex = context[0].dataIndex;
                            return carbonData.fileAnalysis[fileIndex].file;
                        },
                        afterLabel: function(context) {
                            const fileIndex = context.dataIndex;
                            const file = carbonData.fileAnalysis[fileIndex];
                            return [
                                `Lines of Code: ${file.lines.toLocaleString()}`,
                                `Issues: ${file.issues.join(', ')}`
                            ];
                        }
                    },
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    titleColor: '#ffffff',
                    bodyColor: '#ffffff'
                }
            },
            animation: {
                delay: (context) => context.dataIndex * 100
            }
        }
    });
}

// Complexity Radar Chart
function createComplexityChart() {
    const ctx = document.getElementById('complexityChart').getContext('2d');
    
    // Aggregate complexity metrics across all files
    const complexityTotals = {
        loops: 0,
        functions: 0,
        asyncOperations: 0,
        apiCalls: 0,
        fileOperations: 0
    };
    
    carbonData.fileAnalysis.forEach(file => {
        Object.keys(complexityTotals).forEach(key => {
            complexityTotals[key] += file.complexity[key] || 0;
        });
    });
    
    const labels = Object.keys(complexityTotals).map(key => 
        key.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase())
    );
    const values = Object.values(complexityTotals);
    
    charts.complexity = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Complexity Metrics',
                data: values,
                backgroundColor: chartColors.info + '30',
                borderColor: chartColors.info,
                borderWidth: 3,
                pointBackgroundColor: chartColors.info,
                pointBorderColor: '#ffffff',
                pointBorderWidth: 2,
                pointRadius: 6,
                pointHoverRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                r: {
                    beginAtZero: true,
                    grid: {
                        color: '#f0f0f0'
                    },
                    angleLines: {
                        color: '#e0e0e0'
                    },
                    pointLabels: {
                        font: {
                            size: 11,
                            weight: '500'
                        }
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    titleColor: '#ffffff',
                    bodyColor: '#ffffff'
                }
            },
            animation: {
                duration: 1500
            }
        }
    });
}

// Trends Line Chart
function createTrendsChart() {
    const ctx = document.getElementById('trendsChart');
    if (!ctx) return; // Chart not on current tab
    
    const context = ctx.getContext('2d');
    const trendData = carbonData.trendData.daily;
    
    charts.trends = new Chart(context, {
        type: 'line',
        data: {
            labels: trendData.map(item => {
                const date = new Date(item.date);
                return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
            }),
            datasets: [{
                label: 'CO₂ Emissions (kg)',
                data: trendData.map(item => item.co2),
                borderColor: chartColors.danger,
                backgroundColor: chartColors.danger + '20',
                borderWidth: 3,
                fill: true,
                tension: 0.4,
                pointRadius: 5,
                pointHoverRadius: 7,
                pointBackgroundColor: chartColors.danger,
                pointBorderColor: '#ffffff',
                pointBorderWidth: 2
            }, {
                label: 'Energy Consumption (kWh)',
                data: trendData.map(item => item.energy),
                borderColor: chartColors.warning,
                backgroundColor: chartColors.warning + '20',
                borderWidth: 3,
                fill: true,
                tension: 0.4,
                pointRadius: 5,
                pointHoverRadius: 7,
                pointBackgroundColor: chartColors.warning,
                pointBorderColor: '#ffffff',
                pointBorderWidth: 2,
                yAxisID: 'y1'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                intersect: false,
                mode: 'index'
            },
            scales: {
                x: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Date',
                        font: {
                            size: 12,
                            weight: '600'
                        }
                    },
                    grid: {
                        color: '#f0f0f0'
                    }
                },
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    title: {
                        display: true,
                        text: 'CO₂ Emissions (kg)',
                        color: chartColors.danger,
                        font: {
                            size: 12,
                            weight: '600'
                        }
                    },
                    grid: {
                        color: '#f0f0f0'
                    }
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    title: {
                        display: true,
                        text: 'Energy (kWh)',
                        color: chartColors.warning,
                        font: {
                            size: 12,
                            weight: '600'
                        }
                    },
                    grid: {
                        drawOnChartArea: false
                    }
                }
            },
            plugins: {
                legend: {
                    position: 'top'
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    titleColor: '#ffffff',
                    bodyColor: '#ffffff',
                    callbacks: {
                        afterLabel: function(context) {
                            if (context.datasetIndex === 0) {
                                const energy = trendData[context.dataIndex].energy;
                                return `Energy: ${energy.toFixed(3)} kWh`;
                            }
                            return '';
                        }
                    }
                }
            },
            animation: {
                duration: 2000,
                easing: 'easeInOutQuart'
            }
        }
    });
}

// Create scatter chart for lines vs impact
function createScatterChart() {
    const scatterData = carbonData.fileAnalysis.map(file => ({
        x: file.lines,
        y: file.impactScore,
        label: file.file.split('/').pop()
    }));
    
    // This would be used if we had a scatter chart element
    // Implementation would go here
}

// Function to download chart as image
function downloadChart(chartId) {
    const chart = charts[chartId.replace('Chart', '')];
    if (chart) {
        const link = document.createElement('a');
        link.download = `${chartId}_${new Date().toISOString().split('T')[0]}.png`;
        link.href = chart.toBase64Image();
        link.click();
    }
}

// Function to update chart data
function updateChartData(chartType, newData) {
    const chart = charts[chartType];
    if (chart) {
        chart.data = newData;
        chart.update();
    }
}

// Function to destroy all charts (useful for cleanup)
function destroyAllCharts() {
    Object.values(charts).forEach(chart => {
        if (chart && typeof chart.destroy === 'function') {
            chart.destroy();
        }
    });
    charts = {};
}

// Initialize all charts
function initializeCharts() {
    // Destroy existing charts if any
    destroyAllCharts();
    
    // Create charts that are currently visible
    if (document.getElementById('energyChart')) {
        createEnergyChart();
    }
    if (document.getElementById('fileImpactChart')) {
        createFileImpactChart();
    }
    if (document.getElementById('complexityChart')) {
        createComplexityChart();
    }
    if (document.getElementById('trendsChart')) {
        createTrendsChart();
    }
}

// Export functions
window.createEnergyChart = createEnergyChart;
window.createFileImpactChart = createFileImpactChart;
window.createComplexityChart = createComplexityChart;
window.createTrendsChart = createTrendsChart;
window.downloadChart = downloadChart;
window.initializeCharts = initializeCharts;
window.destroyAllCharts = destroyAllCharts;