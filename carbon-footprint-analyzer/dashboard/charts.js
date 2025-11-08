// Chart rendering logic
function renderCharts() {
  // Energy Breakdown Pie Chart
  const energyLabels = Object.keys(reportData.energy_breakdown);
  const energyValues = Object.values(reportData.energy_breakdown);
  new Chart(document.getElementById('energyChart').getContext('2d'), {
    type: 'doughnut',
    data: {
      labels: energyLabels,
      datasets: [{
        data: energyValues,
        backgroundColor: ['#4CAF50', '#FF9800', '#2196F3', '#9C27B0'],
        borderWidth: 2,
        borderColor: '#fff'
      }]
    },
    options: {
      plugins: {
        legend: { position: 'bottom' }
      }
    }
  });

  // File Impact Bar Chart
  const fileNames = Object.keys(reportData.file_analysis);
  const fileScores = fileNames.map(f => reportData.file_analysis[f].carbon_impact_score);
  new Chart(document.getElementById('fileImpactChart').getContext('2d'), {
    type: 'bar',
    data: {
      labels: fileNames,
      datasets: [{
        label: 'Impact Score',
        data: fileScores,
        backgroundColor: 'rgba(76, 175, 80, 0.7)',
        borderColor: '#4CAF50',
        borderWidth: 2
      }]
    },
    options: {
      plugins: { legend: { display: false } },
      scales: { y: { beginAtZero: true } }
    }
  });

  // Complexity Radar Chart
  const complexityTotals = { loops: 0, functions: 0, async_operations: 0, api_calls: 0, file_operations: 0 };
  Object.values(reportData.file_analysis).forEach(a => {
    Object.keys(complexityTotals).forEach(k => complexityTotals[k] += a.complexity[k] || 0);
  });
  new Chart(document.getElementById('complexityChart').getContext('2d'), {
    type: 'radar',
    data: {
      labels: Object.keys(complexityTotals),
      datasets: [{
        label: 'Total Count',
        data: Object.values(complexityTotals),
        backgroundColor: 'rgba(33, 150, 243, 0.2)',
        borderColor: '#2196F3',
        borderWidth: 2
      }]
    },
    options: {
      plugins: { legend: { display: false } }
    }
  });

  // Scatter Chart: Lines vs Impact
  const scatterData = fileNames.map(f => ({ x: reportData.file_analysis[f].lines, y: reportData.file_analysis[f].carbon_impact_score }));
  new Chart(document.getElementById('scatterChart').getContext('2d'), {
    type: 'scatter',
    data: {
      datasets: [{
        label: 'Files',
        data: scatterData,
        backgroundColor: 'rgba(255, 152, 0, 0.7)',
        borderColor: '#FF9800',
        borderWidth: 2,
        pointRadius: 6
      }]
    },
    options: {
      plugins: { legend: { display: false } },
      scales: {
        x: { title: { display: true, text: 'Lines of Code' }, beginAtZero: true },
        y: { title: { display: true, text: 'Impact Score' }, beginAtZero: true }
      }
    }
  });
}
