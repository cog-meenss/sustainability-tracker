# 📊 How to View Sustainability Reports in GitHub

## Method 1: GitHub Actions Job Summary (Recommended)

### Setup:
Your GitHub Actions workflow automatically generates visual reports that appear directly in the GitHub interface.

### How to Access:
1. **Go to**: https://github.com/cog-meenss/sustainability-tracker/actions
2. **Click**: Any completed "Sustainability Analysis" workflow run
3. **Scroll down**: Look for the "Job Summary" section
4. **View**: Interactive charts, metrics, and recommendations

### What You'll See:
- 📊 Overall sustainability score with color-coded status
- 📈 Detailed metrics breakdown table
- 🎯 Quality gate pass/fail status
- 📁 File analysis by language
- 💡 Top 3 actionable recommendations
- 📊 Progress bars and visual indicators

## Method 2: Downloadable Artifacts

### How to Access:
1. **Go to**: Completed workflow run
2. **Scroll down**: Find "Artifacts" section
3. **Download**: "sustainability-dashboard" (HTML files)
4. **Extract**: ZIP file and open `dashboard.html` in browser

### What You Get:
- 🎨 Interactive Chart.js visualizations
- 📊 Radar charts showing multi-dimensional metrics
- 📈 Bar charts and progress indicators
- 💡 Detailed recommendations with priority levels
- 📱 Responsive design works on mobile

## Method 3: GitHub Pages Integration

### Setup (One-time):
1. **Enable GitHub Pages**: Repository Settings → Pages
2. **Source**: Deploy from `/docs` folder
3. **Auto-update**: Workflow publishes reports to docs/

### Benefits:
- 🌐 Public URL for sharing reports
- 📊 Always shows latest analysis
- 🔄 Automatically updates on each push
- 📱 Mobile-friendly interface

## Method 4: Pull Request Comments

### Automatic Feature:
- 📝 Bot comments on PRs with sustainability impact
- 📊 Before/after score comparisons
- 💡 Specific recommendations for changes
- 🎯 Quality gate results

## Quick Start Guide:

### 1. Trigger Analysis:
```bash
# Manual trigger
git commit --allow-empty -m "Trigger sustainability analysis"
git push origin main
```

### 2. View Results:
- **GitHub Actions**: https://github.com/cog-meenss/sustainability-tracker/actions
- **Latest Run**: Click the most recent "Sustainability Analysis"
- **Job Summary**: Scroll down to see visual metrics

### 3. Download Detailed Reports:
- **Artifacts Section**: Download "sustainability-dashboard"
- **Extract & Open**: `dashboard.html` for full interactive experience

## Live Example URLs:

- **Actions Dashboard**: https://github.com/cog-meenss/sustainability-tracker/actions
- **Workflow File**: https://github.com/cog-meenss/sustainability-tracker/blob/main/.github/workflows/sustainability-analysis.yml
- **Repository**: https://github.com/cog-meenss/sustainability-tracker

## Visual Report Features:

### Job Summary Includes:
```
🌱 Sustainability Analysis Results

📊 Overall Score: 75/100 ✅ PASS
┌─────────────────────────────┬────────┬────────┐
│ Metric                      │ Score  │ Status │
├─────────────────────────────┼────────┼────────┤
│ Energy Efficiency           │ 82/100 │ ✅ Good │
│ Resource Utilization        │ 78/100 │ ✅ Good │
│ Carbon Footprint           │ 65/100 │ ⚠️  Fair │
│ Performance Optimization   │ 88/100 │ ✅ Excellent │
│ Sustainable Practices      │ 71/100 │ ⚠️  Fair │
└─────────────────────────────┴────────┴────────┘

🎯 Quality Gates: ✅ 4/5 PASSED

💡 Top Recommendations:
1. Optimize async patterns (HIGH priority)
2. Reduce bundle size (MEDIUM priority)  
3. Implement caching (LOW priority)
```

### Interactive Dashboard Features:
- 📊 **Radar Chart**: Multi-dimensional sustainability view
- 📈 **Trend Analysis**: Score changes over time
- 🎯 **Drill-down**: Click metrics for detailed breakdown
- 📁 **File Explorer**: See per-file sustainability scores
- 💡 **Action Items**: Prioritized improvement suggestions

## Next Steps:

1. **Trigger First Analysis**: Push code or manually trigger workflow
2. **Check GitHub Actions**: Look for job summary with visual metrics  
3. **Download Dashboard**: Get full interactive HTML report
4. **Set Up GitHub Pages**: For permanent public reporting URL
5. **Monitor Trends**: Track improvements over time

Your sustainability reports are now fully integrated with GitHub! 🚀