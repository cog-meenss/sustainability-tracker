# Sustainability Tracker

A comprehensive code sustainability analysis tool with automated CI/CD integration for business applications.

## 🚀 Features

### 📊 Sustainability Analysis
- **Multi-language support**: Python, JavaScript, TypeScript, Java, C#, Go, Rust
- **40+ sustainability rules** covering energy efficiency, resource optimization, and carbon footprint
- **Interactive dashboards** with Chart.js visualizations
- **Quality gates** with configurable thresholds

### 🤖 CI/CD Integration  
- **GitHub Actions**: Full-featured pipeline with PR comments and job summaries
- **Azure DevOps**: Complete YAML pipeline (requires parallelism grant)
- **Automated scheduling**: Weekly sustainability reports
- **Artifact publishing**: Download reports and dashboards

### 📈 Business Intelligence
- **Training Tracker**: Excel upload and analysis for employee training records
- **Ideas Management**: Innovation tracking and evaluation system
- **Revenue/FTE Analysis**: Financial metrics with working days calculations
- **Executive Dashboards**: Visual reporting with export capabilities

## 🏃‍♂️ Quick Start

### GitHub Actions (Recommended)
1. **Fork/Clone** this repository
2. **Enable Actions** in repository settings
3. **Push changes** to trigger analysis
4. **View results** in Actions tab with interactive reports

### Local Development
```bash
# Install dependencies
cd sustainability-analyzer
pip install -r requirements.txt

# Run analysis
python analyzer/sustainability_analyzer.py --path ../frontend --format json

# Generate dashboard  
python reports/html_generator.py --input analysis.json --output dashboard.html
```

### Business Application
```bash
# Backend server
cd backend && npm install && npm start

# Frontend application  
cd frontend && npm install && npm start
```

## 📊 Pipeline Status

![Sustainability Analysis](https://github.com/cog-meenss/sustainability-tracker/workflows/🌱%20Sustainability%20Analysis/badge.svg)
![Simple Check](https://github.com/cog-meenss/sustainability-tracker/workflows/🌱%20Simple%20Sustainability%20Check/badge.svg)

## 📁 Project Structure

```
├── .github/workflows/          # GitHub Actions pipelines
├── sustainability-analyzer/    # Core analysis engine
│   ├── analyzer/              # Python analysis modules  
│   ├── reports/               # Report generators
│   └── dashboard/             # Interactive dashboards
├── frontend/                  # React business application
├── backend/                   # Express.js API server
└── docs/                      # Documentation
```

## 🎯 Analysis Metrics

- **Energy Efficiency**: Code patterns that minimize computational overhead
- **Resource Utilization**: Memory and storage optimization practices  
- **Carbon Footprint**: Environmental impact assessment
- **Quality Gates**: Automated pass/fail thresholds

## 🔧 Configuration

### GitHub Actions Variables
Set these in your repository settings → Secrets and variables → Actions:

| Variable | Default | Description |
|----------|---------|-------------|
| `SUSTAINABILITY_THRESHOLD` | 75 | Minimum score for quality gate |
| `PYTHON_VERSION` | 3.9 | Python version for analysis |

### Quality Thresholds
- **Excellent**: 90+ (Green)
- **Good**: 75-89 (Yellow) 
- **Needs Improvement**: <75 (Red)

## 📈 Reports & Dashboards

- **Interactive Dashboard**: HTML with Chart.js radar charts
- **Executive Summary**: PDF with key insights and recommendations
- **Detailed Analysis**: JSON with complete metrics and file-level data
- **PR Comments**: Automatic analysis results on pull requests

## 🌍 Sustainability Focus

This project demonstrates sustainable software development practices:
- Efficient algorithms and data structures
- Minimal resource consumption patterns
- Carbon-aware development practices
- Automated sustainability monitoring

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`) 
5. Open Pull Request (automatic sustainability analysis included!)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- **Documentation**: [Setup Guides](GITHUB_ACTIONS_SETUP.md)
- **Demo**: [Repository](https://github.com/cog-meenss/sustainability-tracker)

---

**🌱 Built with sustainability in mind** • Automated analysis • Continuous improvement
=======
# sustainability-tracker
Code sustainability analysis and business data tracker
Report updated: Fri Dec 12 10:00:00 GMT 2025
