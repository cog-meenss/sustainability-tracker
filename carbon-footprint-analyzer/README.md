# 🌱 Universal Carbon Footprint Analyzer

A comprehensive, language-agnostic tool for analyzing and optimizing the carbon footprint of software projects. This analyzer provides detailed insights into your code's environmental impact and offers actionable recommendations for reducing energy consumption.

## 🚀 Features

### 🔍 **Multi-Language Support**
- **Web Technologies**: JavaScript, TypeScript, HTML, CSS, Vue, React
- **Backend Languages**: Python, Java, Go, C#, PHP, Ruby  
- **Mobile Development**: Swift, Kotlin, Dart, Objective-C
- **Systems Programming**: C, C++, Rust
- **Data Science**: Python, R, MATLAB, Jupyter Notebooks
- **And 40+ more languages with generic analysis fallback**

### 📊 **Comprehensive Analysis**
- **Language Detection**: Automatically identifies programming languages and frameworks
- **Code Complexity**: Calculates cyclomatic complexity, depth metrics, and patterns
- **Dependency Analysis**: Evaluates impact of third-party libraries and packages
- **Framework Detection**: Identifies and analyzes framework-specific optimizations
- **Energy Modeling**: Converts code metrics to energy consumption estimates
- **Carbon Calculation**: Maps energy usage to CO2 emissions based on electricity grids

### 📈 **Rich Reporting**
- **Multiple Formats**: JSON, HTML, Markdown, CSV outputs
- **Interactive Dashboards**: Web-based visualization with charts and graphs
- **Executive Summaries**: High-level overviews for stakeholders  
- **Technical Details**: In-depth analysis for developers
- **Optimization Guides**: Actionable recommendations with implementation steps
- **Example Dashboard**: Sample HTML visualization in `dashboard/` folder

### 🔧 **Developer Integration**
- **Command Line Interface**: Full-featured CLI with extensive options
- **CI/CD Integration**: GitHub Actions, Jenkins, GitLab pipelines
- **IDE Extensions**: VS Code integration (examples provided)
- **Pre-commit Hooks**: Automatic analysis on code changes
- **API Access**: Programmatic analysis for custom workflows

## 📦 Installation

### Quick Install
```bash
git clone https://github.com/your-org/carbon-footprint-analyzer.git
cd carbon-footprint-analyzer
pip install -e .
```

### Dependencies
- Python 3.8+
- No external API keys required
- Works completely offline

## 🏃 Quick Start

### Command Line Usage

```bash
# Basic analysis
python cli.py /path/to/your/project

# Generate HTML and JSON reports
python cli.py /path/to/project --format html json --output ./reports

# Use project-specific configuration
python cli.py /path/to/project --config web_app_config.json

# Compare multiple projects
python cli.py --compare project1/ project2/ project3/ --output ./comparison

# Analyze code snippet
python cli.py --code "console.log('hello')" --language javascript
```

### Python API Usage

```python
# Add to your Python path
import sys
sys.path.insert(0, 'carbon-footprint-analyzer/src')

from carbon_analyzer import CarbonAnalyzer

# Initialize analyzer
analyzer = CarbonAnalyzer()

# Analyze project
results = analyzer.analyze_project(
    project_path='/path/to/project',
    output_path='./reports',
    report_formats=['html', 'json']
)

print(f"Carbon footprint: {results['carbon_footprint']['total_carbon_kg']:.6f} kg CO2")
```

## ✅ Validated Results

### Tracker Project Analysis
When run on the included Tracker project (React + Express Excel processor):

```
🌱 CARBON FOOTPRINT ANALYSIS SUMMARY
====================================
🎯 Project: Tracker
💻 Primary Language: JavaScript  
📁 Total Files: 66
🔧 Complexity: Medium

🌱 CARBON IMPACT:
   • Total Emissions: 0.008075 kg CO2
   • Energy Consumption: 0.017000 kWh
   • Impact Level: Low

📊 BREAKDOWN:
   • Code Execution: 41.2%
   • Dependencies: 29.4%  
   • Frameworks: 23.5%
   • Build System: 5.9%

🌍 REAL-WORLD COMPARISONS:
   • Equivalent to 807.5 smartphone charges
   • Equivalent to 0.020 km by car

💡 TOP RECOMMENDATIONS:
   1. 📦 Consider reducing bundle size by removing unused dependencies
   2. ⚡ Implement code splitting for better performance  
   3. 🔄 Use React.memo for component optimization
```

## 🛠 Configuration

The analyzer supports project-specific configurations:

- **`examples/configs/web_app_config.json`**: React, Vue, Angular web applications
- **`examples/configs/api_service_config.json`**: REST APIs, microservices
- **`examples/configs/mobile_app_config.json`**: React Native, Flutter apps
- **`examples/configs/data_science_config.json`**: ML projects, Jupyter notebooks
- **`examples/configs/basic_config.json`**: Minimal configuration

## 🔌 Integration Examples

### GitHub Actions
See `examples/integrations/.github_workflows_carbon_analysis.yml`

### Jenkins Pipeline  
See `examples/integrations/jenkins_integration.py`

### Pre-commit Hook
See `examples/integrations/pre_commit_hook.py`

### VS Code Extension
See `examples/integrations/vscode_extension.py`

## 📊 Example Dashboard

The `dashboard/` folder contains a complete HTML dashboard example showing how to visualize carbon footprint analysis results:

```bash
cd dashboard
python3 serve_dashboard.py
# Open http://localhost:8080 to view interactive dashboard
```

**Features**:
- 📈 **Interactive Charts**: Energy breakdown, file impact scores, complexity metrics
- 📋 **Summary Cards**: Key metrics and comparisons at a glance
- 🎯 **Optimization Guide**: Actionable recommendations with priority rankings
- 📊 **Data Tables**: Detailed file-by-file analysis results
- 🌍 **Real-World Comparisons**: Smartphone charges, car distance equivalents

This dashboard demonstrates how to integrate the analyzer's JSON output into custom web interfaces for stakeholders and management reporting.

## 🧪 Testing

Run the test suite to validate functionality:

```bash
cd carbon-footprint-analyzer
python simple_test.py
```

This will analyze the Tracker project and generate sample reports in `simple_test_results/`.

## 🚀 Getting Started

1. **Clone this repository**
2. **Run the test**: `python simple_test.py`
3. **Analyze your project**: `python cli.py /path/to/your/project`
4. **View the HTML report** for detailed insights
5. **Implement the recommendations** to reduce carbon footprint

## 📊 Understanding Results

- **Carbon Emissions (kg CO2)**: Direct environmental impact
- **Energy Consumption (kWh)**: Computational energy usage
- **Impact Level**: Categorical assessment (Low/Medium/High)
- **Optimization Potential**: Percentage reduction possible
- **Component Breakdown**: Where energy is consumed
- **Language Analysis**: Per-language carbon footprint
- **Recommendations**: Actionable optimization steps

## 🌍 Environmental Impact

This analyzer helps developers:
- **Measure** the carbon footprint of their code
- **Optimize** for energy efficiency 
- **Track** improvements over time
- **Compare** different approaches
- **Learn** sustainable coding practices

*Built for a more sustainable digital future* 🌱

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/Version-1.0.0-blue.svg)]()
[![Language Support](https://img.shields.io/badge/Languages-Universal-green.svg)]()

## 🎯 **Universal Support**

This package analyzes carbon footprint for projects in **any programming language**:

- ✅ **JavaScript/TypeScript** (Node.js, React, Vue, Angular)
- ✅ **Python** (Django, Flask, FastAPI, Data Science)
- ✅ **Java** (Spring, Maven, Gradle projects) 
- ✅ **C#/.NET** (ASP.NET, .NET Core)
- ✅ **Go** (Standard library, frameworks)
- ✅ **Ruby** (Rails, Sinatra)
- ✅ **PHP** (Laravel, Symfony)
- ✅ **Rust** (Cargo projects)
- ✅ **C/C++** (CMake, Make projects)
- ✅ **And more...** (Generic file-based analysis)

## 🚀 **Quick Start**

### 1. **Install & Run Analysis**

```bash
# Clone or download this package
git clone <your-repo>/carbon-footprint-analyzer
cd carbon-footprint-analyzer

# Analyze any project
python src/analyzer.py --project-path /path/to/your/project --language auto

# Start interactive dashboard
python dashboard/server.py --port 8080
```

### 2. **Language-Specific Examples**

#### **JavaScript/Node.js Project:**
```bash
python src/analyzer.py --project-path ./my-react-app --language javascript --framework react
```

#### **Python Project:**
```bash  
python src/analyzer.py --project-path ./my-django-app --language python --framework django
```

#### **Java Project:**
```bash
python src/analyzer.py --project-path ./my-spring-app --language java --framework spring
```

#### **Any Project (Auto-detect):**
```bash
python src/analyzer.py --project-path ./any-project --language auto
```

### 3. **View Results**
- 📊 **Interactive Dashboard**: `http://localhost:8080`
- 📄 **JSON Report**: `./reports/carbon_report_YYYYMMDD.json`
- 📋 **CSV Export**: `./reports/carbon_summary_YYYYMMDD.csv`

## 📊 **Features**

### **🔍 Analysis Capabilities**
- **Multi-language Support** - Automatic language detection
- **Framework Recognition** - Specialized analysis for popular frameworks
- **Dependency Analysis** - Package/library carbon impact assessment
- **Code Complexity** - Computational complexity scoring
- **Energy Estimation** - Runtime energy consumption prediction
- **CO2 Calculations** - Environmental impact quantification

### **📈 Interactive Dashboard**
- **Real-time Charts** - Energy breakdown, file impact scores
- **Comparative Analysis** - Before/after optimization comparisons
- **Drill-down Reports** - File-level and function-level analysis
- **Export Options** - PDF, CSV, JSON formats
- **Responsive Design** - Works on desktop and mobile

### **🛠️ Customization**
- **Configurable Metrics** - Define custom carbon factors
- **Plugin Architecture** - Add analyzers for new languages
- **Template System** - Customize report formats
- **API Integration** - Embed in CI/CD pipelines

## 🏗️ **Architecture**

```
carbon-footprint-analyzer/
├── src/
│   ├── analyzer.py              # Main analysis engine
│   ├── analyzers/               # Language-specific analyzers
│   │   ├── javascript.py        # JS/TS/Node.js analysis
│   │   ├── python.py           # Python analysis
│   │   ├── java.py             # Java analysis
│   │   ├── csharp.py           # C# analysis
│   │   ├── generic.py          # Universal file analyzer
│   │   └── ...                 # More language analyzers
│   ├── core/
│   │   ├── metrics.py          # Carbon calculation engine
│   │   ├── detector.py         # Language/framework detection
│   │   └── reporter.py         # Report generation
│   └── utils/
│       ├── file_scanner.py     # File system analysis
│       └── complexity.py       # Code complexity metrics
├── dashboard/
│   ├── server.py               # Dashboard web server
│   ├── assets/                 # CSS, JS, templates
│   │   ├── styles.css         # Universal styling
│   │   ├── charts.js          # Chart configurations
│   │   └── dashboard.js       # Interactive functionality
│   └── templates/             # HTML templates
├── configs/                    # Configuration files
│   ├── languages.json         # Language-specific settings
│   ├── frameworks.json        # Framework detection rules
│   ├── carbon_factors.json    # Energy conversion factors
│   └── default.json          # Default configuration
├── templates/                  # Report templates
│   ├── html_report.html       # Interactive HTML report
│   ├── pdf_template.html      # PDF export template
│   └── csv_template.csv       # CSV export format
└── examples/                   # Example projects and configs
    ├── javascript_example/
    ├── python_example/
    └── java_example/
```

## 🔧 **Configuration**

### **Language Detection Rules** (`configs/languages.json`)
```json
{
  "javascript": {
    "extensions": [".js", ".jsx", ".ts", ".tsx", ".mjs"],
    "indicators": ["package.json", "node_modules/", "yarn.lock"],
    "frameworks": {
      "react": ["react", "react-dom"],
      "vue": ["vue", "@vue/"],
      "angular": ["@angular/"],
      "node": ["express", "fastify", "koa"]
    }
  },
  "python": {
    "extensions": [".py", ".pyx", ".pyi"],
    "indicators": ["requirements.txt", "setup.py", "pyproject.toml"],
    "frameworks": {
      "django": ["django"],
      "flask": ["flask"],
      "fastapi": ["fastapi"]
    }
  }
}
```

### **Carbon Factors** (`configs/carbon_factors.json`)
```json
{
  "energy_factors": {
    "cpu_per_second": 0.0001,
    "memory_per_mb": 0.00001,
    "network_per_mb": 0.00005,
    "storage_per_gb": 0.002
  },
  "co2_factors": {
    "kwh_to_kg_co2": 0.5,
    "server_efficiency": 1.2,
    "cloud_overhead": 1.1
  },
  "language_multipliers": {
    "javascript": 1.0,
    "python": 1.2,
    "java": 1.5,
    "c": 0.8,
    "rust": 0.9
  }
}
```

## 📋 **Usage Examples**

### **1. Basic Analysis**

```bash
# Analyze current directory
python src/analyzer.py

# Analyze specific project
python src/analyzer.py --project-path /path/to/project

# Auto-detect language and generate dashboard
python src/analyzer.py --project-path ./my-app --output dashboard
```

### **2. Advanced Configuration**

```bash
# Custom configuration
python src/analyzer.py \
  --project-path ./my-app \
  --language python \
  --framework django \
  --config configs/custom.json \
  --output-format json,html,csv

# CI/CD Integration
python src/analyzer.py \
  --project-path . \
  --threshold 0.5 \
  --fail-on-threshold \
  --output reports/
```

### **3. API Usage**

```python
from src.analyzer import CarbonAnalyzer

# Initialize analyzer
analyzer = CarbonAnalyzer(
    project_path="./my-project",
    language="auto",
    config_file="configs/default.json"
)

# Run analysis
results = analyzer.analyze()

# Generate dashboard
analyzer.generate_dashboard(port=8080)

# Export results
analyzer.export_report(format="json", output="./report.json")
```

### **4. Programmatic Integration**

```javascript
// Node.js integration example
const { spawn } = require('child_process');

const runCarbonAnalysis = async (projectPath) => {
  return new Promise((resolve, reject) => {
    const analyzer = spawn('python', [
      'carbon-footprint-analyzer/src/analyzer.py',
      '--project-path', projectPath,
      '--output-format', 'json'
    ]);
    
    analyzer.on('close', (code) => {
      if (code === 0) resolve('Analysis complete');
      else reject('Analysis failed');
    });
  });
};
```

## 🎨 **Dashboard Features**

### **Interactive Visualizations**
- **Energy Breakdown** - Pie charts showing energy distribution
- **File Impact Scores** - Bar charts of high-carbon files
- **Timeline Analysis** - Historical carbon footprint trends
- **Comparison Views** - Before/after optimization metrics

### **Detailed Reports**
- **File-level Analysis** - Carbon impact per source file
- **Dependency Impact** - Third-party library carbon costs  
- **Optimization Recommendations** - Actionable improvement suggestions
- **Performance Metrics** - Runtime efficiency correlations

### **Export Options**
- **PDF Reports** - Professional formatted documents
- **CSV Data** - Spreadsheet-compatible data export
- **JSON API** - Machine-readable results
- **PNG Charts** - High-quality chart images

## 🔌 **Plugin System**

### **Create Custom Language Analyzer**

```python
# src/analyzers/my_language.py
from .base_analyzer import BaseAnalyzer

class MyLanguageAnalyzer(BaseAnalyzer):
    def __init__(self, project_path):
        super().__init__(project_path)
        self.language = "my_language"
    
    def analyze_files(self):
        # Custom file analysis logic
        pass
    
    def calculate_complexity(self, file_content):
        # Language-specific complexity calculation
        pass
    
    def estimate_energy(self, complexity_metrics):
        # Custom energy estimation
        pass
```

### **Register Plugin**

```python
# Register in src/analyzer.py
from analyzers.my_language import MyLanguageAnalyzer

LANGUAGE_ANALYZERS = {
    'javascript': JavaScriptAnalyzer,
    'python': PythonAnalyzer,
    'my_language': MyLanguageAnalyzer,  # Add custom analyzer
}
```

## 📦 **Installation & Dependencies**

### **Requirements**
- **Python 3.8+** (for analysis engine)
- **Web Browser** (for dashboard viewing)
- **Optional**: Node.js (for advanced JS analysis)

### **Dependencies**
```bash
pip install -r requirements.txt
```

**Core dependencies:**
- `pathlib` - File system operations
- `json` - Configuration and data handling  
- `argparse` - Command-line interface
- `http.server` - Dashboard web server
- `re` - Pattern matching for code analysis

**Optional dependencies:**
- `matplotlib` - Advanced chart generation
- `pandas` - Data analysis and export
- `requests` - API integrations
- `beautifulsoup4` - HTML parsing

## 🚀 **Integration Examples**

### **GitHub Actions**
```yaml
name: Carbon Footprint Analysis
on: [push, pull_request]

jobs:
  carbon-analysis:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run Carbon Analysis
        run: |
          python carbon-footprint-analyzer/src/analyzer.py \
            --project-path . \
            --threshold 0.5 \
            --output reports/
      - name: Upload Results
        uses: actions/upload-artifact@v2
        with:
          name: carbon-report
          path: reports/
```

### **Docker Container**
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY carbon-footprint-analyzer/ ./

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "src/analyzer.py"]
CMD ["--help"]
```

### **NPM Package Integration**
```json
{
  "scripts": {
    "analyze-carbon": "python carbon-footprint-analyzer/src/analyzer.py --project-path .",
    "carbon-dashboard": "python carbon-footprint-analyzer/dashboard/server.py"
  }
}
```

## 📈 **Roadmap**

### **v1.1 - Enhanced Language Support**
- Go, Rust, Kotlin analyzers
- Advanced framework detection
- Cloud deployment analysis

### **v1.2 - AI Integration** 
- Machine learning for optimization suggestions
- Predictive carbon footprint modeling
- Automated code refactoring recommendations

### **v1.3 - Enterprise Features**
- Multi-project comparison dashboards
- Team collaboration features
- Advanced reporting and analytics

## 🤝 **Contributing**

We welcome contributions! See our [Contributing Guide](CONTRIBUTING.md) for details.

### **Add New Language Support**
1. Create analyzer in `src/analyzers/your_language.py`
2. Add configuration in `configs/languages.json`
3. Update documentation and examples
4. Submit pull request with tests

### **Improve Analysis Accuracy**
1. Refine carbon calculation models
2. Add real-world benchmark data
3. Enhance complexity metrics
4. Validate against actual measurements

## 📄 **License**

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 **Acknowledgments**

- Inspired by [codecarbon](https://codecarbon.io/) project
- Chart.js for visualization components
- Open source carbon footprint research community

---

**🌱 Help reduce software's environmental impact, one codebase at a time!**