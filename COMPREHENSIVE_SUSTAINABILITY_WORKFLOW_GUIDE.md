# 🌱 Comprehensive Sustainability Analysis GitHub Workflow Guide

## Overview

This guide explains how to run the **Comprehensive Sustainability Evaluator** in GitHub Actions to generate advanced sustainability reports with interactive visualizations, carbon impact assessments, and detailed recommendations.

## Workflow Configuration

### File Location
```
.github/workflows/sustainability-analysis.yml
```

### Trigger Events
The workflow runs automatically on:
- ✅ **Push to main/develop branches**
- ✅ **Pull requests to main branch** 
- ✅ **Weekly schedule** (Mondays at 2 AM UTC)
- ✅ **Manual trigger** (workflow_dispatch)

### Environment Variables
```yaml
env:
  SUSTAINABILITY_THRESHOLD: 75    # Quality gate threshold
  PYTHON_VERSION: '3.9'          # Python version for analysis
```

## Generated Reports

### 1. Interactive HTML Report
- **File**: `comprehensive_sustainability_report.html`
- **Features**: Chart.js visualizations, tabbed interface, responsive design
- **Contains**: Radar charts, progress bars, detailed metrics breakdown
- **Access**: Download from workflow artifacts

### 2. Comprehensive JSON Data
- **File**: `comprehensive_sustainability_data.json`
- **Features**: Machine-readable detailed analysis
- **Contains**: All metrics, code patterns, recommendations, carbon impact
- **Use Case**: Integration with other tools, custom reporting

### 3. Executive Summary
- **File**: `COMPREHENSIVE_SUSTAINABILITY_SUMMARY.md`
- **Features**: Dashboard-style markdown with tables
- **Contains**: Action plans, benchmarking, timeline projections
- **Use Case**: Management reporting, strategic planning

## Key Metrics Analyzed

### Core Sustainability Scores
| Metric | Description | Weight |
|--------|-------------|--------|
| **Overall Sustainability** | Combined sustainability score | 100% |
| **Energy Efficiency** | Computational overhead analysis | 25% |
| **Resource Utilization** | Memory and storage optimization | 25% |
| **Code Maintainability** | Long-term maintenance impact | 25% |
| **Security Compliance** | Security best practices | 25% |

### Performance Issues Detection
- **Loop Patterns**: Identifies potentially inefficient loops
- **Async Operations**: Analyzes concurrent programming patterns
- **Console Logs**: Detects debug code left in production
- **Memory Patterns**: Identifies memory management issues

### Carbon Impact Assessment
- **Total CO2 Footprint**: Estimated environmental impact
- **Compute Efficiency**: Resource utilization efficiency
- **Energy Waste Factor**: Optimization opportunity indicator

## Workflow Steps Breakdown

### Step 1: Environment Setup
```yaml
- name: Checkout Repository
  uses: actions/checkout@v4
  with:
    fetch-depth: 0  # Full history for analysis

- name: Setup Python Environment  
  uses: actions/setup-python@v5
  with:
    python-version: '3.9'
    cache: 'pip'
```

### Step 2: Dependencies Installation
```yaml
- name: Install Analysis Dependencies
  run: |
    python -m pip install --upgrade pip
    pip install radon xenon bandit safety pylint flake8 mypy
```

### Step 3: Comprehensive Analysis Generation
```yaml
- name: Generate Comprehensive Sustainability Report
  run: |
    chmod +x comprehensive_sustainability_evaluator.py
    
    # Generate JSON data
    python3 comprehensive_sustainability_evaluator.py --path . --format json --output comprehensive_sustainability_data.json
    
    # Generate HTML report with visualizations
    python3 comprehensive_sustainability_evaluator.py --path . --format html --output comprehensive_sustainability_report.html
```

### Step 4: Quality Gate Evaluation
```yaml
- name: Quality Gate Evaluation
  run: |
    OVERALL_SCORE=$(python3 -c "
    import json
    with open('comprehensive_sustainability_data.json', 'r') as f:
        data = json.load(f)
    print(data['comprehensive_metrics']['overall_sustainability_score'])
    ")
    
    if (( $(echo "$OVERALL_SCORE >= 75" | bc -l) )); then
      echo "Quality gate PASSED!"
    else
      echo "Quality gate FAILED!"
      exit 1
    fi
```

### Step 5: GitHub Actions Job Summary
Creates a comprehensive dashboard in the GitHub Actions interface with:
- Overall sustainability score with visual progress bars
- Detailed metrics breakdown
- Performance issues analysis
- Carbon impact assessment
- Priority action items
- Links to downloadable reports

### Step 6: Artifact Upload
```yaml
- name: Upload Comprehensive Reports
  uses: actions/upload-artifact@v4
  with:
    name: comprehensive-reports
    path: |
      comprehensive_sustainability_data.json
      comprehensive_sustainability_report.html
      COMPREHENSIVE_SUSTAINABILITY_SUMMARY.md
    retention-days: 30
```

### Step 7: Pull Request Comments
Automatically comments on PRs with:
- Overall sustainability score and quality gate status
- Detailed metrics table
- Environmental impact summary
- Code pattern analysis
- Links to full reports

## Usage Examples

### Manual Trigger
1. Go to **Actions** tab in GitHub
2. Select **Comprehensive Sustainability Analysis**
3. Click **Run workflow**
4. Choose branch and click **Run workflow**

### Viewing Results

#### In GitHub Actions Interface
1. Go to workflow run
2. Check **Job Summary** for dashboard view
3. Scroll down to see comprehensive metrics

#### Downloading Reports
1. Go to workflow run
2. Scroll to **Artifacts** section
3. Download **comprehensive-reports** package
4. Extract and view HTML report in browser

#### Accessing JSON Data
```bash
# Download and extract artifacts
curl -H "Authorization: token $GITHUB_TOKEN" \
     -L -o reports.zip \
     "$GITHUB_API_URL/repos/owner/repo/actions/artifacts/$ARTIFACT_ID/zip"

unzip reports.zip
```

## Quality Gates and Thresholds

### Overall Score Thresholds
- **90-100**: 🏆 Excellent - Optimal sustainability
- **75-89**: ✅ Good - Meets quality standards
- **60-74**: ⚠️ Fair - Improvement needed
- **0-59**: ❌ Needs Work - Critical issues

### Performance Issues Thresholds
- **0-99**: 🟢 Clean - Minimal issues
- **100-499**: 🟡 Minor - Some optimization opportunities
- **500-999**: 🟠 Moderate - Significant improvements needed
- **1000+**: 🔴 Critical - Major performance concerns

### Carbon Impact Levels
- **< 0.01kg CO2**: 🟢 Low impact
- **0.01-0.1kg CO2**: 🟡 Medium impact
- **> 0.1kg CO2**: 🔴 High impact

## Integration with CI/CD

### Failing Builds on Low Scores
The workflow will fail if the overall sustainability score is below the threshold (75):

```yaml
- name: Fail if Quality Gate Failed
  if: env.QUALITY_GATE_PASSED == 'false'
  run: exit 1
```

### Branch Protection Rules
Configure branch protection to require sustainability checks:
1. Go to **Settings** → **Branches**
2. Add rule for `main` branch
3. Enable **Require status checks to pass**
4. Select **comprehensive-sustainability** check

### Customizing Thresholds
Modify the workflow file:
```yaml
env:
  SUSTAINABILITY_THRESHOLD: 80  # Increase for stricter requirements
```

## Advanced Configuration

### Custom Analysis Parameters
Modify the analysis command:
```bash
# Focus on specific file patterns
python3 comprehensive_sustainability_evaluator.py \
  --path ./src \
  --format html \
  --exclude "*.test.js,*.spec.js"
```

### Multiple Environment Analysis
```yaml
strategy:
  matrix:
    python-version: [3.8, 3.9, '3.10']
    path: ['./frontend', './backend', '.']
```

### Scheduled Deep Analysis
```yaml
# Weekly comprehensive analysis
- cron: '0 2 * * 1'   # Monday 2 AM UTC

# Daily quick analysis  
- cron: '0 6 * * *'    # Daily 6 AM UTC
```

## Troubleshooting

### Common Issues

#### 1. Analysis Timeout
```yaml
timeout-minutes: 15  # Increase for large codebases
```

#### 2. Memory Issues
```yaml
env:
  NODE_OPTIONS: --max-old-space-size=4096
```

#### 3. Missing Dependencies
```bash
# Add missing tools
pip install additional-package
```

#### 4. File Access Issues
```yaml
- name: Fix Permissions
  run: |
    chmod +x comprehensive_sustainability_evaluator.py
    chmod +x sustainability-analyzer/analyzer/sustainability_analyzer.py
```

### Debug Mode
Enable verbose logging:
```bash
python3 comprehensive_sustainability_evaluator.py --path . --format html --verbose
```

### Manual Local Testing
```bash
# Test locally before pushing
./comprehensive_sustainability_evaluator.py --path . --format html
```

## Best Practices

### 1. Regular Monitoring
- Set up weekly scheduled runs
- Monitor trend over time
- Set up notifications for score drops

### 2. Incremental Improvements
- Focus on one metric at a time
- Address highest-impact issues first
- Track progress with each PR

### 3. Team Integration
- Include sustainability score in PR reviews
- Set team goals for sustainability improvements
- Share reports in team meetings

### 4. Documentation
- Document sustainability decisions
- Create improvement roadmaps
- Share best practices across teams

## Report Interpretation

### HTML Interactive Report
- **Radar Chart**: Visual representation of all metrics
- **Progress Bars**: Individual metric scores
- **Tabbed Interface**: Organized by analysis category
- **Responsive Design**: Works on mobile and desktop

### JSON Data Structure
```json
{
  "comprehensive_metrics": {
    "overall_sustainability_score": 30.2,
    "energy_efficiency": 0.0,
    "resource_utilization": 0.0,
    "maintainability_score": 65.0,
    "security_score": 85.0,
    "performance_issues_detected": 1338
  },
  "carbon_impact": {
    "total_estimated_co2_kg": 0.1245,
    "compute_efficiency": 45.3,
    "energy_waste_factor": 2.1
  },
  "code_patterns": {
    "loops_detected": 604,
    "async_patterns": 65,
    "console_logs": 146
  }
}
```

## Support and Resources

- **Documentation**: [Comprehensive Sustainability Summary](./COMPREHENSIVE_SUSTAINABILITY_SUMMARY.md)
- **Issues**: Report problems in GitHub Issues
- **Contributions**: Submit improvements via Pull Requests
- **Questions**: Use GitHub Discussions for questions

---

## Quick Start Checklist

- [ ] Add workflow file to `.github/workflows/`
- [ ] Ensure `comprehensive_sustainability_evaluator.py` is in repository root
- [ ] Make evaluator executable: `chmod +x comprehensive_sustainability_evaluator.py`
- [ ] Commit and push to trigger first run
- [ ] Check Actions tab for results
- [ ] Download and review HTML report
- [ ] Set up branch protection rules (optional)
- [ ] Configure team notifications (optional)

**🌱 Start improving your code's sustainability today with comprehensive analysis and actionable insights!**