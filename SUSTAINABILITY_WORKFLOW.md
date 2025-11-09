# 🌱 Automated Sustainability Analysis

This repository includes automated sustainability analysis that runs on every commit to generate comprehensive green coding reports.

## 🚀 Workflow Features

[![Sustainability Analysis](https://github.com/USERNAME/REPO/workflows/Automated%20Sustainability%20Analysis%20&%20Report%20Generation/badge.svg)](https://github.com/USERNAME/REPO/actions)

### 📊 What Gets Generated

**On Every Commit:**
- 🎯 **Interactive HTML Dashboard** with real-time metrics
- 📋 **Detailed JSON Report** with raw analysis data
- 📝 **Analysis Summary** with key insights and recommendations
- 💬 **PR Comments** with sustainability scores (for pull requests)

### 🔄 Trigger Conditions

The workflow automatically runs when:
- **Push to main/develop** branches
- **Pull requests** to main branch  
- **Manual workflow dispatch** with custom parameters
- **Code changes** in supported languages (Python, JavaScript, TypeScript, etc.)

### 📁 Report Generation

```bash
# Generated files are saved to:
sustainability-reports/
├── sustainability-report-{commit}-{timestamp}.html   # Interactive dashboard
├── sustainability-report-{commit}-{timestamp}.json   # Raw data
└── analysis-summary.md                               # Executive summary
```

### 🎯 Quality Gates

The workflow includes built-in quality gates:
- **Minimum Sustainability Score:** 50/100
- **Automatic Failure:** If score falls below threshold
- **PR Blocking:** Quality gate failures prevent merging

### 📈 Metrics Tracked

**Core Sustainability Metrics:**
- Overall Sustainability Score (0-100)
- Energy Efficiency Rating (0-100) 
- Green Coding Score (0-100)
- Resource Utilization (0-100)
- Code Quality Assessment (0-100)

**Green Coding Analysis:**
- CPU Efficiency Patterns
- Memory Optimization Practices
- Energy Saving Implementations
- Carbon Footprint Projections

**File-Level Analysis:**
- Issue Detection with Line Numbers
- Code Pattern Recognition
- Language-Specific Optimizations
- Actionable Improvement Suggestions

### 🛠️ Manual Workflow Execution

You can manually trigger the workflow with custom parameters:

1. Go to **Actions** tab in GitHub
2. Select **"Automated Sustainability Analysis & Report Generation"**
3. Click **"Run workflow"**
4. Optionally set:
   - **Analysis Path:** Specific directory to analyze (default: entire repo)
   - **Output Name:** Custom filename for reports

### 📥 Accessing Reports

**Method 1: Artifacts (Recommended)**
- Go to the workflow run in GitHub Actions
- Download the "sustainability-reports-{sha}" artifact
- Extract and open the HTML dashboard

**Method 2: Repository Files**
- Reports are auto-committed to `sustainability-reports/` directory
- View directly in GitHub or clone repository

**Method 3: GitHub Pages (if enabled)**
- Latest report automatically published to GitHub Pages
- Access via: `https://username.github.io/repo/sustainability-reports/`

### 🔧 Configuration Options

**Environment Variables:**
- `PYTHON_VERSION`: Python version for analysis (default: 3.9)
- `REPORT_PATH`: Directory for generated reports (default: sustainability-reports)

**Quality Gate Thresholds:**
- Modify `MIN_SCORE` in the workflow file to adjust quality standards
- Current minimum: 50/100 overall sustainability score

### 💡 Understanding Your Reports

**HTML Dashboard Includes:**
- 🎨 **Visual Metrics** - Interactive charts and progress bars
- 📊 **Real-time Controls** - Refresh buttons and auto-update toggles  
- 📁 **File Analysis** - Specific issues with line numbers and code snippets
- 💡 **Recommendations** - Prioritized suggestions with energy impact estimates
- 🌍 **Carbon Footprint** - Environmental impact projections and metrics

**JSON Report Contains:**
- Raw analysis data for programmatic access
- Complete metric breakdowns
- File-by-file issue listings
- Detailed recommendation objects
- Metadata and execution timing

### 🚨 Troubleshooting

**Common Issues:**

1. **Workflow Fails on Dependencies**
   ```yaml
   # Add required dependencies to workflow
   - name: Install Additional Dependencies  
     run: pip install your-package-name
   ```

2. **Quality Gate Failures**
   - Review generated recommendations
   - Address high-priority sustainability issues
   - Consider adjusting minimum score threshold

3. **Large Repository Analysis**
   - Use manual workflow with specific `analysis_path`
   - Exclude large directories in sustainability_evaluator.py

### 📞 Support

For issues with the sustainability analysis workflow:
- Check workflow logs in GitHub Actions
- Review generated error reports
- Ensure sustainability_evaluator.py is present in repository root

---

**Next Steps:**
1. Commit this workflow to trigger your first automated analysis
2. Review the generated HTML dashboard
3. Implement recommended sustainability improvements
4. Watch your green coding scores improve over time! 🌱✨