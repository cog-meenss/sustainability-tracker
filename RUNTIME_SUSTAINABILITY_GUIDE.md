# 🔄 Runtime Sustainability Analysis System

## Overview

This system generates **runtime sustainability reports** instead of static files. All analysis is performed on-demand, ensuring fresh results every time without cluttering your repository with generated files.

## 🚀 Quick Start

### 1. Generate Runtime Report (Command Line)

```bash
# Console output
python3 runtime_sustainability_reporter.py --path . --format console

# Generate HTML report
python3 runtime_sustainability_reporter.py --path . --format html --output report.html

# Generate JSON data
python3 runtime_sustainability_reporter.py --path . --format json --output data.json

# Generate Markdown report
python3 runtime_sustainability_reporter.py --path . --format markdown --output report.md
```

### 2. Start Web Server (Live Dashboard)

```bash
# Start server on default port 8000
python3 runtime_report_server.py

# Start server on custom port
python3 runtime_report_server.py --port 8080

# Start server accessible from other machines
python3 runtime_report_server.py --host 0.0.0.0 --port 8080
```

## 🌐 Web Server Features

### Dashboard URLs
- **Main Dashboard:** `http://localhost:8000/`
- **API Endpoint:** `http://localhost:8000/api/report?format=json`
- **Server Status:** `http://localhost:8000/api/status`
- **Force Refresh:** `http://localhost:8000/refresh`

### API Formats
- HTML: `/api/report?format=html`
- JSON: `/api/report?format=json`
- Markdown: `/api/report?format=markdown`
- Console: `/api/report?format=console`

### Key Features
- ✅ **Real-time Generation** - Fresh analysis on every request
- ✅ **Auto-refresh** - Dashboard updates every 5 minutes
- ✅ **Multiple Formats** - HTML, JSON, Markdown, Console output
- ✅ **No Static Files** - Everything generated at runtime
- ✅ **Interactive Dashboard** - Visual charts and metrics
- ✅ **Manual Refresh** - Click button to regenerate instantly

## 📊 GitHub Actions Integration

The system integrates seamlessly with GitHub Actions for CI/CD sustainability analysis:

### Workflow Features
- **Runtime Reports:** Generated fresh on every workflow run
- **Multiple Formats:** HTML, JSON, and Markdown reports available as artifacts
- **Quality Gates:** Configurable sustainability thresholds
- **PR Comments:** Automatic sustainability feedback on pull requests
- **Visual Summaries:** Rich GitHub Actions job summaries with progress bars

### View Results
1. **GitHub Actions Tab:** See job summaries with visual metrics
2. **Download Artifacts:** Get HTML, JSON, and Markdown reports
3. **PR Comments:** Automatic sustainability feedback on pull requests

## 🎯 Key Metrics

### Sustainability Scores
- **Overall Score:** Comprehensive sustainability rating (0-100)
- **Energy Efficiency:** Computational overhead analysis
- **Resource Utilization:** Memory and storage efficiency
- **Performance Optimization:** Runtime performance metrics
- **Sustainable Practices:** Code quality and best practices

### Quality Gates
- **Threshold:** 75/100 (configurable)
- **Pass/Fail:** Automatic quality gate evaluation
- **Recommendations:** Priority-based improvement suggestions

## 🔧 Configuration

### Environment Variables
```bash
export SUSTAINABILITY_THRESHOLD=75  # Quality gate threshold
export PYTHON_VERSION=3.9           # Python version for analysis
```

### Custom Analysis
The system automatically detects and analyzes:
- **Python files** - Resource utilization patterns
- **JavaScript/TypeScript** - Energy efficiency patterns
- **JSON/CSS** - Minimal overhead analysis
- **Project structure** - Overall sustainability assessment

## 💡 Best Practices

### For Development
1. **Regular Monitoring** - Run analysis frequently during development
2. **Quality Gates** - Set appropriate sustainability thresholds
3. **Optimization Focus** - Address high-priority recommendations first
4. **Runtime Efficiency** - Keep analysis fast for frequent use

### For CI/CD
1. **Automated Analysis** - Include in all major workflows
2. **PR Feedback** - Enable automatic pull request comments
3. **Artifact Storage** - Download reports for historical tracking
4. **Threshold Management** - Adjust quality gates based on project maturity

## 🚀 Advanced Usage

### Custom Web Server
```python
from runtime_report_server import RuntimeReportHandler
from http.server import HTTPServer

# Custom server with your own handler
server = HTTPServer(('localhost', 8000), RuntimeReportHandler)
server.serve_forever()
```

### Programmatic Analysis
```python
from runtime_sustainability_reporter import RuntimeSustainabilityReporter

reporter = RuntimeSustainabilityReporter("/path/to/project")
result = reporter.generate_runtime_report(format_type="json")
print(f"Overall Score: {result['sustainability_metrics']['overall_score']}")
```

## 📈 Continuous Improvement

### Monitoring Trends
- Track sustainability scores over time
- Monitor quality gate pass/fail rates
- Focus on high-impact recommendations
- Regular threshold adjustments

### Performance Optimization
- Analysis typically completes in < 1 second
- Web server responds in < 2 seconds
- GitHub Actions integration adds < 30 seconds to workflows
- No repository bloat from static files

## 🔗 Integration Examples

### GitHub Actions Workflow
```yaml
- name: 🔄 Generate Runtime Sustainability Report
  run: |
    python3 runtime_sustainability_reporter.py --path . --format json --output report.json
    python3 runtime_sustainability_reporter.py --path . --format html --output dashboard.html
```

### Local Development
```bash
# Quick check during development
python3 runtime_sustainability_reporter.py --path . --format console

# Start live dashboard for monitoring
python3 runtime_report_server.py --port 3001
```

---

## 📋 Available Commands Summary

| Command | Purpose | Output |
|---------|---------|--------|
| `python3 runtime_sustainability_reporter.py --format console` | Quick CLI analysis | Terminal output |
| `python3 runtime_sustainability_reporter.py --format html --output report.html` | Generate HTML report | HTML file |
| `python3 runtime_report_server.py` | Start web dashboard | Live server at :8000 |
| `python3 runtime_report_server.py --port 8080` | Custom port server | Live server at :8080 |

**🔄 No static files needed - everything generated at runtime!**