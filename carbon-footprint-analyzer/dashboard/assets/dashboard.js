// Main Dashboard JavaScript functionality

// Global state
let currentTab = 'overview';
let filteredRecommendations = carbonData.recommendations;
let sortedFiles = [...carbonData.fileAnalysis];

// DOM Elements
const tabButtons = document.querySelectorAll('.nav-btn');
const tabContents = document.querySelectorAll('.tab-content');

// Initialize dashboard on DOM load
document.addEventListener('DOMContentLoaded', function() {
    initializeDashboard();
});

function initializeDashboard() {
    updateTimestamp();
    setupTabNavigation();
    populateSummaryCards();
    populateFileTable();
    populateRecommendations();
    setupEventListeners();
    
    // Initialize charts after DOM is ready
    setTimeout(() => {
        initializeCharts();
    }, 100);
}

function updateTimestamp() {
    const timestampEl = document.getElementById('lastUpdated');
    if (timestampEl) {
        const now = new Date();
        timestampEl.textContent = `Updated: ${now.toLocaleDateString()} ${now.toLocaleTimeString()}`;
    }
}

function setupTabNavigation() {
    tabButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            const tabName = e.currentTarget.dataset.tab;
            switchTab(tabName);
        });
    });
}

function switchTab(tabName) {
    // Update button states
    tabButtons.forEach(btn => btn.classList.remove('active'));
    document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
    
    // Update content visibility
    tabContents.forEach(content => content.classList.remove('active'));
    document.getElementById(tabName).classList.add('active');
    
    currentTab = tabName;
    
    // Initialize tab-specific functionality
    if (tabName === 'trends') {
        setTimeout(() => createTrendsChart(), 100);
    } else if (tabName === 'recommendations') {
        populateImplementationGuide();
    }
}

function populateSummaryCards() {
    const summary = carbonData.summary;
    
    // Update summary card values
    if (document.getElementById('co2Value')) {
        document.getElementById('co2Value').textContent = formatCO2(summary.estimatedCo2EmissionsKg);
    }
    if (document.getElementById('energyValue')) {
        document.getElementById('energyValue').textContent = summary.totalEnergyConsumptionKwh.toFixed(3);
    }
    if (document.getElementById('filesValue')) {
        document.getElementById('filesValue').textContent = summary.totalFilesAnalyzed;
    }
    if (document.getElementById('depsValue')) {
        document.getElementById('depsValue').textContent = summary.totalDependencies;
    }
}

function populateFileTable() {
    const tbody = document.getElementById('fileTableBody');
    if (!tbody) return;
    
    tbody.innerHTML = '';
    
    sortedFiles.forEach((file, index) => {
        const row = createFileTableRow(file, index);
        tbody.appendChild(row);
    });
}

function createFileTableRow(file, index) {
    const row = document.createElement('tr');
    const impactLevel = getImpactLevel(file.impactScore);
    
    row.innerHTML = `
        <td>
            <div class="file-name">${file.file}</div>
        </td>
        <td>${file.lines.toLocaleString()}</td>
        <td>
            <span class="impact-score impact-${impactLevel}">
                ${file.impactScore.toFixed(1)}
            </span>
        </td>
        <td>
            <div class="complexity-badges">
                ${Object.entries(file.complexity)
                    .filter(([key, value]) => value > 0)
                    .map(([key, value]) => 
                        `<span class="complexity-badge">${key.replace(/([A-Z])/g, ' $1')}: ${value}</span>`
                    ).join('')}
            </div>
        </td>
        <td>${file.issues.join(', ')}</td>
        <td>
            <button class="action-btn" onclick="showFileDetails(${index})">
                <i class="fas fa-info-circle"></i> Details
            </button>
        </td>
    `;
    
    return row;
}

function showFileDetails(index) {
    const file = sortedFiles[index];
    const modal = document.getElementById('fileModal');
    const fileName = document.getElementById('modalFileName');
    const modalBody = document.getElementById('modalBody');
    
    fileName.textContent = file.file;
    
    modalBody.innerHTML = `
        <div class="file-details">
            <div class="detail-section">
                <h4><i class="fas fa-chart-bar"></i> Metrics</h4>
                <div class="metrics-grid">
                    <div class="metric-item">
                        <span class="metric-label">Lines of Code</span>
                        <span class="metric-value">${file.lines.toLocaleString()}</span>
                    </div>
                    <div class="metric-item">
                        <span class="metric-label">Carbon Impact Score</span>
                        <span class="metric-value">${file.impactScore.toFixed(2)}</span>
                    </div>
                </div>
            </div>
            
            <div class="detail-section">
                <h4><i class="fas fa-cogs"></i> Complexity Analysis</h4>
                <div class="complexity-details">
                    ${Object.entries(file.complexity).map(([key, value]) => 
                        `<div class="complexity-item">
                            <span>${key.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase())}</span>
                            <span class="complexity-value">${value}</span>
                        </div>`
                    ).join('')}
                </div>
            </div>
            
            <div class="detail-section">
                <h4><i class="fas fa-exclamation-triangle"></i> Issues Identified</h4>
                <ul class="issues-list">
                    ${file.issues.map(issue => `<li>${issue}</li>`).join('')}
                </ul>
            </div>
            
            <div class="detail-section">
                <h4><i class="fas fa-lightbulb"></i> Recommendations</h4>
                <ul class="recommendations-list">
                    ${file.recommendations.map(rec => `<li>${rec}</li>`).join('')}
                </ul>
            </div>
        </div>
    `;
    
    modal.style.display = 'block';
}

function closeFileModal() {
    document.getElementById('fileModal').style.display = 'none';
}

function populateRecommendations() {
    const grid = document.getElementById('recommendationsGrid');
    if (!grid) return;
    
    grid.innerHTML = '';
    
    filteredRecommendations.forEach(rec => {
        const card = createRecommendationCard(rec);
        grid.appendChild(card);
    });
}

function createRecommendationCard(rec) {
    const card = document.createElement('div');
    card.className = `recommendation-card priority-${rec.priority}`;
    card.dataset.priority = rec.priority;
    
    card.innerHTML = `
        <div class="rec-header">
            <div class="rec-title">${rec.title}</div>
            <span class="priority-badge priority-${rec.priority}">${rec.priority}</span>
        </div>
        <div class="rec-description">${rec.description}</div>
        <div class="rec-meta">
            <span class="rec-impact">Impact: ${rec.impact}</span>
            <span class="rec-effort">Effort: ${rec.effort}</span>
            <span class="rec-category">Category: ${rec.category}</span>
        </div>
    `;
    
    return card;
}

function populateImplementationGuide() {
    const guideContent = document.getElementById('guideContent');
    if (!guideContent) return;
    
    // Default to quick wins
    showImplementationGuide('quick');
}

function showImplementationGuide(type) {
    const guideContent = document.getElementById('guideContent');
    const guides = carbonData.implementationGuide[type];
    
    // Update tab states
    document.querySelectorAll('.guide-tab').forEach(tab => {
        tab.classList.toggle('active', tab.dataset.guide === type);
    });
    
    guideContent.innerHTML = guides.map(guide => `
        <div class="guide-item">
            <h4>${guide.title}</h4>
            <p>${guide.description}</p>
            ${guide.code ? `<div class="code-block"><code>${guide.code}</code></div>` : ''}
            <div class="guide-meta">
                <span class="time-estimate">⏱️ ${guide.timeToImplement}</span>
                <span class="impact-estimate">📈 ${guide.impact}</span>
            </div>
        </div>
    `).join('');
}

function setupEventListeners() {
    // File search functionality
    const fileSearch = document.getElementById('fileSearch');
    if (fileSearch) {
        fileSearch.addEventListener('input', handleFileSearch);
    }
    
    // File sort functionality
    const sortBy = document.getElementById('sortBy');
    if (sortBy) {
        sortBy.addEventListener('change', handleFileSort);
    }
    
    // Priority filter buttons
    const filterButtons = document.querySelectorAll('.filter-btn');
    filterButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            const priority = e.target.dataset.priority;
            filterRecommendations(priority);
        });
    });
    
    // Implementation guide tabs
    const guideTabs = document.querySelectorAll('.guide-tab');
    guideTabs.forEach(tab => {
        tab.addEventListener('click', (e) => {
            const guideType = e.target.dataset.guide;
            showImplementationGuide(guideType);
        });
    });
    
    // Modal close on background click
    const modal = document.getElementById('fileModal');
    if (modal) {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                closeFileModal();
            }
        });
    }
    
    // Complexity metric selector
    const complexityMetric = document.getElementById('complexityMetric');
    if (complexityMetric) {
        complexityMetric.addEventListener('change', updateComplexityChart);
    }
}

function handleFileSearch(e) {
    const searchTerm = e.target.value.toLowerCase();
    
    if (searchTerm === '') {
        sortedFiles = [...carbonData.fileAnalysis];
    } else {
        sortedFiles = carbonData.fileAnalysis.filter(file => 
            file.file.toLowerCase().includes(searchTerm) ||
            file.issues.some(issue => issue.toLowerCase().includes(searchTerm))
        );
    }
    
    populateFileTable();
}

function handleFileSort(e) {
    const sortBy = e.target.value;
    
    sortedFiles.sort((a, b) => {
        switch (sortBy) {
            case 'impact':
                return b.impactScore - a.impactScore;
            case 'lines':
                return b.lines - a.lines;
            case 'complexity':
                const aComplexity = Object.values(a.complexity).reduce((sum, val) => sum + val, 0);
                const bComplexity = Object.values(b.complexity).reduce((sum, val) => sum + val, 0);
                return bComplexity - aComplexity;
            default:
                return 0;
        }
    });
    
    populateFileTable();
}

function filterRecommendations(priority) {
    // Update filter button states
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.priority === priority);
    });
    
    if (priority === 'all') {
        filteredRecommendations = carbonData.recommendations;
    } else {
        filteredRecommendations = carbonData.recommendations.filter(rec => rec.priority === priority);
    }
    
    populateRecommendations();
}

function updateComplexityChart() {
    const metric = document.getElementById('complexityMetric').value;
    
    if (metric === 'all') {
        createComplexityChart();
    } else {
        // Create filtered complexity chart
        // Implementation would depend on specific requirements
        createComplexityChart();
    }
}

// Export functions for global access
window.switchTab = switchTab;
window.showFileDetails = showFileDetails;
window.closeFileModal = closeFileModal;
window.showImplementationGuide = showImplementationGuide;
window.filterRecommendations = filterRecommendations;

// Add some CSS for the additional elements
const additionalStyles = `
    <style>
    .file-details {
        max-height: 60vh;
        overflow-y: auto;
    }
    
    .detail-section {
        margin-bottom: 2rem;
    }
    
    .detail-section h4 {
        color: var(--primary-green);
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .complexity-details {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 0.5rem;
    }
    
    .complexity-item {
        display: flex;
        justify-content: space-between;
        padding: 0.5rem;
        background: var(--background);
        border-radius: 6px;
    }
    
    .complexity-value {
        font-weight: 600;
        color: var(--primary-green);
    }
    
    .issues-list,
    .recommendations-list {
        list-style: none;
        padding: 0;
    }
    
    .issues-list li,
    .recommendations-list li {
        padding: 0.5rem 0;
        border-bottom: 1px solid var(--border-color);
    }
    
    .issues-list li:last-child,
    .recommendations-list li:last-child {
        border-bottom: none;
    }
    
    .guide-item {
        background: var(--background);
        padding: 1.5rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        border-left: 4px solid var(--light-green);
    }
    
    .guide-item h4 {
        color: var(--primary-green);
        margin-bottom: 0.5rem;
    }
    
    .code-block {
        background: #f4f4f4;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
        font-family: 'Monaco', 'Menlo', monospace;
        font-size: 0.85rem;
        overflow-x: auto;
    }
    
    .guide-meta {
        display: flex;
        gap: 1rem;
        margin-top: 1rem;
        font-size: 0.85rem;
        color: var(--text-secondary);
    }
    
    .rec-meta {
        display: flex;
        gap: 1rem;
        margin-top: 1rem;
        font-size: 0.8rem;
        color: var(--text-secondary);
    }
    </style>
`;

document.head.insertAdjacentHTML('beforeend', additionalStyles);