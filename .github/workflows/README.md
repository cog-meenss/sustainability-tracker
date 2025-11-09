# 🌱 Consolidated Sustainability Workflows

## Overview
This directory contains the consolidated GitHub Actions workflow that replaces the previous separate sustainability analysis workflows.

## What Changed
- ✅ **Consolidated** `sustainability-analysis.yml` + `sustainability-auto-report.yml` → `consolidated-sustainability.yml`
- ✅ **Smart Quality Gates** with automatic mode detection (strict for main, lenient for others)
- ✅ **Enhanced GitHub Pages** deployment with professional landing page
- ✅ **Comprehensive Reporting** with interactive dashboards and environmental impact

## Workflow Features

### 🎯 **Intelligent Quality Gates**
| Mode | Threshold | When Applied |
|------|-----------|--------------|
| **Strict** | 75/100 | Main branch, production releases |
| **Lenient** | 50/100 | Feature branches, development |
| **Manual** | Custom | Workflow dispatch with user input |

### 📊 **Comprehensive Analysis**
- Multi-language support (Python, JavaScript, TypeScript, etc.)
- Code pattern detection (async, loops, memory leaks)
- Environmental impact assessment
- Carbon footprint calculations
- Performance issue identification

### 🌐 **Professional Web Deployment**
- Auto-deployed to GitHub Pages
- Interactive dashboards with tooltips
- Real-time metrics and recommendations
- Professional single-tone design

### 🚀 **Advanced Features**
- **PR Comments** with detailed metrics
- **Artifact Upload** for report downloads
- **Auto-commit** reports to repository
- **Job Summaries** with comprehensive insights
- **Quality Gate Enforcement** with build failures

## Triggers
- **Push** to main/develop (code files only)
- **Pull Requests** to main
- **Weekly Schedule** (Mondays at 2 AM UTC)
- **Manual Dispatch** with custom options

## Backup
Original workflows are backed up in `backup/` directory:
- `backup/sustainability-analysis.yml` - Original comprehensive analysis
- `backup/sustainability-auto-report.yml` - Original report generation

## Benefits
✅ **Reduced Complexity** - Single workflow instead of 3  
✅ **Smart Logic** - Automatic quality gate selection  
✅ **Better Performance** - Optimized execution flow  
✅ **Enhanced UI** - Professional dashboard design  
✅ **Comprehensive Coverage** - All features in one place  

## Usage
The workflow runs automatically on code changes. For manual execution:

```bash
# Trigger with default settings
gh workflow run consolidated-sustainability.yml

# Trigger with custom options
gh workflow run consolidated-sustainability.yml \
  -f analysis_path="src/" \
  -f quality_gate_mode="strict" \
  -f output_name="custom-report"
```

## Quality Gate Strategy
- **Main Branch**: Strict mode (75% threshold) ensures production quality
- **Feature Branches**: Lenient mode (50% threshold) allows development flexibility
- **Manual Override**: Custom thresholds for special cases

---
*Consolidated sustainability workflow provides comprehensive green coding analysis with professional web deployment and intelligent quality gates.*