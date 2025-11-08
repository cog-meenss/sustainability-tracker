// Dashboard rendering logic
function renderSummary() {
  const s = reportData.summary;
  document.getElementById('summary').innerHTML = `
    <div class="summary-grid">
      <div class="summary-card"><h3>Total Files</h3><div class="value">${s.total_files_analyzed}</div></div>
      <div class="summary-card"><h3>Lines of Code</h3><div class="value">${s.lines_of_code}</div></div>
      <div class="summary-card"><h3>Energy (kWh)</h3><div class="value">${s.total_energy_consumption_kwh.toFixed(4)}</div></div>
      <div class="summary-card"><h3>CO₂ (kg)</h3><div class="value">${s.estimated_co2_emissions_kg.toFixed(3)}</div></div>
      <div class="summary-card"><h3>Dependencies</h3><div class="value">${s.total_dependencies}</div></div>
      <div class="summary-card"><h3>High-Impact Files</h3><div class="value">${s.high_impact_files_count}</div></div>
    </div>
  `;
}

function renderFileTable() {
  const table = document.createElement('table');
  table.innerHTML = `
    <thead><tr><th>File</th><th>Lines</th><th>Impact</th><th>Complexity</th></tr></thead>
    <tbody>
      ${Object.entries(reportData.file_analysis).map(([file, a]) => `
        <tr>
          <td>${file}</td>
          <td>${a.lines}</td>
          <td>${a.carbon_impact_score.toFixed(1)}</td>
          <td>${Object.entries(a.complexity).map(([k, v]) => `${k}: ${v}`).join(', ')}</td>
        </tr>
      `).join('')}
    </tbody>
  `;
  document.getElementById('fileTable').appendChild(table);
}

function renderRecommendations() {
  document.getElementById('recommendations').innerHTML = `
    <h2>💡 Recommendations</h2>
    <ul>
      ${reportData.recommendations.map(r => `<li>${r}</li>`).join('')}
    </ul>
  `;
}

document.addEventListener('DOMContentLoaded', () => {
  renderSummary();
  renderCharts();
  renderFileTable();
  renderRecommendations();
});
