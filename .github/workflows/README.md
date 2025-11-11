# 🌱 Consolidated Sustainability Workflows

## Overview
# 🌱 Sustainability Tracker Workflows

This directory contains the active GitHub Actions workflows for automated sustainability analysis and reporting.

## 📋 Active Workflow

### 🚀 **Single Production Workflow**
- **`consolidated-sustainability.yml`** ⭐ **MAIN & ONLY WORKFLOW**
  - **Purpose:** Complete sustainability analysis with GitHub Pages deployment
  - **Triggers:** Push to main/develop, PRs, manual dispatch
  - **Output:** Publishes to https://cog-meenss.github.io/sustainability-tracker/sustainability-reports/latest-report.html
  - **Status:** ✅ Production ready, no errors, no conflicts
  - **Features:** 
    - ✨ Enhanced URL display in deployment view
    - 📊 GitHub Job Summary with clickable links
    - 🌐 Prominent GitHub Pages URL logging
    - � Single concurrency group prevents conflicts

## 🗂️ Removed Workflows (Cleaned Up)
- ❌ `sustainability.yml` - Had SLACK_WEBHOOK_URL context access errors
- ❌ `enhanced-sustainability-pipeline.yml` - Had multiple context access warnings  
- ❌ `github-pages.yml` - Disabled and consolidated into main workflow
- ❌ `clean-sustainability-pipeline.yml` - Removed to avoid duplicate/conflicting workflows

## 🎯 Quick Start
1. **For this project:** The `consolidated-sustainability.yml` runs automatically - single workflow, no conflicts
2. **For new projects:** Copy `consolidated-sustainability.yml` as your template (it's clean and comprehensive)
3. **For organizations:** Create a reusable workflow based on the consolidated template

## 📊 GitHub Pages Deployment
Reports are automatically published to:
- **Main Dashboard:** https://cog-meenss.github.io/sustainability-tracker/
- **Latest Report:** https://cog-meenss.github.io/sustainability-tracker/sustainability-reports/latest-report.html

## 📁 Backup Directory
The `backup/` folder contains archived workflows for reference only.

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