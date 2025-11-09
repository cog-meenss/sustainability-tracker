# 🌱 Sustainability Code Evaluation Analyzer

A comprehensive code analysis tool that evaluates software sustainability metrics and integrates with Azure DevOps pipelines for automated reporting.

## 🎯 Overview

This analyzer evaluates code repositories for sustainability metrics including energy efficiency, resource utilization, carbon footprint indicators, and sustainable coding practices. It generates detailed reports in multiple formats and integrates seamlessly with Azure DevOps pipelines.

## ✨ Key Features

### 📊 Sustainability Metrics Analysis
- **Energy Efficiency Score** - Algorithmic complexity and performance patterns
- **Resource Utilization Index** - Memory, CPU, and I/O efficiency analysis
- **Carbon Footprint Indicator** - Estimated environmental impact of code execution
- **Performance Optimization Score** - Identification of optimization opportunities
- **Sustainable Practices Rating** - Code quality and maintainability assessment

### 🔍 Multi-Language Support
- **Python** - Energy-efficient libraries, async patterns, memory management
- **JavaScript/Node.js** - Bundle size, runtime performance, async optimization
- **Java** - JVM optimization, garbage collection efficiency, resource management  
- **C#/.NET** - Memory management, async patterns, performance optimization
- **Go** - Concurrency patterns, resource efficiency, compilation optimization
- **Rust** - Zero-cost abstractions, memory safety, performance analysis

### 📈 Report Generation
- **Interactive HTML Dashboard** - Visual metrics with charts and recommendations
- **JSON API Format** - Structured data for integrations and APIs
- **Azure DevOps Reports** - Native pipeline integration with artifacts
- **Executive Summary** - High-level sustainability assessment
- **Trend Analysis** - Historical performance and improvement tracking

### 🔧 Azure Pipeline Integration
- **Automated Triggers** - Analysis on PR, commits, and scheduled runs
- **Report Publishing** - Artifacts integrated with Azure DevOps reporting
- **Quality Gates** - Configurable sustainability thresholds
- **Notifications** - Teams/email integration for sustainability alerts

## 🚀 Quick Start

### 1. Installation
```bash
# Clone and install dependencies
git clone <repository-url>
cd sustainability-analyzer
npm install
pip install -r requirements.txt
```

### 2. Basic Analysis
```bash
# Analyze current directory
python analyzer/sustainability_analyzer.py --path . --output reports/

# Generate HTML dashboard
python analyzer/generate_dashboard.py --input reports/analysis.json --output dashboard/
```

### 3. Azure Pipeline Setup
```yaml
# Add to azure-pipelines.yml
- task: PythonScript@0
  displayName: 'Sustainability Analysis'
  inputs:
    scriptSource: 'filePath'
    scriptPath: 'sustainability-analyzer/pipeline/run_analysis.py'
    arguments: '--path $(Build.SourcesDirectory) --output $(Build.ArtifactStagingDirectory)/sustainability-reports'
```

## 📋 Configuration

### Analysis Configuration (`config/analyzer_config.json`)
```json
{
  "sustainability_thresholds": {
    "energy_efficiency_min": 75,
    "resource_utilization_max": 85,
    "carbon_footprint_max": 50,
    "performance_optimization_min": 80
  },
  "languages": {
    "python": {
      "rules": ["async_usage", "memory_efficiency", "algorithmic_complexity"],
      "weight": 1.0
    },
    "javascript": {
      "rules": ["bundle_optimization", "async_patterns", "dom_efficiency"],
      "weight": 1.0
    }
  },
  "reporting": {
    "formats": ["html", "json", "azure_devops"],
    "include_trends": true,
    "generate_recommendations": true
  }
}
```

## 🔬 Analysis Components

### Core Analyzer Engine
- **Language Detectors** - Automatic language identification and rule selection
- **Metrics Calculators** - Sustainability score computation algorithms  
- **Pattern Analyzers** - Code pattern recognition for sustainability assessment
- **Recommendation Engine** - Actionable improvement suggestions

### Report Generators
- **HTML Dashboard** - Interactive visualization with Chart.js integration
- **JSON Exporter** - Structured data for API consumption
- **Azure DevOps Publisher** - Native pipeline report integration
- **PDF Generator** - Executive summary reports

### Pipeline Integration
- **Azure DevOps Tasks** - Custom tasks for pipeline integration
- **Quality Gates** - Configurable pass/fail criteria
- **Artifact Publishing** - Report storage and historical tracking
- **Notification System** - Alert integration for sustainability issues

## 📊 Metrics Details

### Energy Efficiency (0-100)
- **Algorithmic Complexity** - Big O analysis and optimization opportunities
- **Library Usage** - Efficient vs. resource-heavy library selection
- **Async Patterns** - Non-blocking operation implementation
- **CPU Optimization** - Computation efficiency analysis

### Resource Utilization (0-100) 
- **Memory Management** - Leak detection and optimization patterns
- **I/O Efficiency** - File system and network operation optimization
- **Database Queries** - Query efficiency and connection management
- **Caching Strategies** - Resource reuse and performance optimization

### Carbon Footprint (0-100, lower is better)
- **Execution Time Estimation** - Runtime performance prediction
- **Resource Consumption** - Memory and CPU usage patterns
- **Network Traffic** - Data transfer efficiency analysis
- **Deployment Impact** - Build and deployment resource usage

## 🏗️ Architecture

```
sustainability-analyzer/
├── analyzer/                 # Core analysis engine
│   ├── sustainability_analyzer.py
│   ├── language_analyzers/
│   ├── metrics/
│   └── rules/
├── reports/                  # Report generation
│   ├── html_generator.py
│   ├── json_exporter.py
│   └── azure_publisher.py
├── dashboard/                # Interactive dashboard  
│   ├── index.html
│   ├── assets/
│   └── templates/
├── pipeline/                 # Azure DevOps integration
│   ├── azure-pipelines.yml
│   ├── tasks/
│   └── scripts/
├── config/                   # Configuration files
└── examples/                 # Integration examples
```

## 🔄 Integration Examples

### GitHub Actions Integration
```yaml
name: Sustainability Analysis
on: [push, pull_request]
jobs:
  sustainability:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Sustainability Analysis
        run: |
          python sustainability-analyzer/analyzer/sustainability_analyzer.py
          python sustainability-analyzer/reports/html_generator.py
```

### Jenkins Integration  
```groovy
pipeline {
    agent any
    stages {
        stage('Sustainability Analysis') {
            steps {
                script {
                    sh 'python sustainability-analyzer/pipeline/run_analysis.py'
                    publishHTML([
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'reports',
                        reportFiles: 'sustainability_dashboard.html',
                        reportName: 'Sustainability Report'
                    ])
                }
            }
        }
    }
}
```

## 📈 Continuous Monitoring

### Trend Analysis
- Historical sustainability score tracking
- Performance regression detection  
- Improvement opportunity identification
- Team/project sustainability benchmarking

### Alerts and Notifications
- Configurable threshold-based alerts
- Integration with Teams, Slack, email
- Pull request sustainability checks
- Dashboard-based monitoring

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/sustainability-enhancement`)
3. Commit your changes (`git commit -am 'Add sustainability feature'`)
4. Push to the branch (`git push origin feature/sustainability-enhancement`)
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For issues and questions:
- 📧 Email: sustainability-analyzer@company.com  
- 📖 Documentation: [Wiki](wiki-url)
- 🐛 Bug Reports: [Issues](issues-url)