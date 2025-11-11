# 🔄 Cross-Project Reusability Guide

## Overview

The Enhanced Sustainability Pipeline is designed with **maximum reusability** in mind. Here are multiple approaches to deploy this solution across different projects and organizations.

## 🎯 Reusability Approaches

### 1. **Template Repository** (Recommended)
Create a template repository that other projects can use as a starting point.

### 2. **Reusable Workflow** 
GitHub Actions reusable workflows for centralized maintenance.

### 3. **Copy & Customize**
Direct file copying with project-specific customizations.

### 4. **Organizational Standards**
Enterprise-wide deployment with centralized configuration.

### 5. **Marketplace Action**
Publish as a GitHub Action for community use.

---

## 🚀 Implementation Methods

### Method 1: GitHub Template Repository

**Setup:**
```bash
# Create template repository
gh repo create sustainability-pipeline-template --template --public
git clone https://github.com/your-org/sustainability-pipeline-template.git
```

**Structure:**
```
sustainability-pipeline-template/
├── .github/
│   └── workflows/
│       └── sustainability-pipeline.yml
├── sustainability_evaluator.py
├── setup/
│   ├── install.sh
│   └── configure.py
├── docs/
│   ├── README.md
│   └── configuration-guide.md
└── examples/
    ├── python-project/
    ├── javascript-project/
    └── mixed-project/
```

**Benefits:**
- ✅ One-click project setup
- ✅ Maintains template relationship
- ✅ Easy updates via template sync
- ✅ Customizable per project type

### Method 2: Reusable Workflow

**Create Reusable Workflow:**
```yaml
# .github/workflows/reusable-sustainability.yml
name: Reusable Sustainability Analysis

on:
  workflow_call:
    inputs:
      project_type:
        description: 'Project type (python, javascript, mixed)'
        required: false
        default: 'mixed'
        type: string
      min_score_threshold:
        description: 'Minimum sustainability score'
        required: false
        default: 60
        type: number
      analysis_depth:
        description: 'Analysis depth'
        required: false
        default: 'standard'
        type: string
    secrets:
      SLACK_WEBHOOK:
        required: false
    outputs:
      sustainability_score:
        description: "Overall sustainability score"
        value: ${{ jobs.analysis.outputs.score }}
```

**Usage in Projects:**
```yaml
# Any project's .github/workflows/sustainability.yml
name: Project Sustainability Check
on: [push, pull_request]

jobs:
  sustainability:
    uses: your-org/sustainability-pipeline-template/.github/workflows/reusable-sustainability.yml@main
    with:
      project_type: 'python'
      min_score_threshold: 70
      analysis_depth: 'comprehensive'
    secrets:
      SLACK_WEBHOOK: ${{ secrets.SLACK_WEBHOOK_URL }}
```

### Method 3: Custom GitHub Action

**Create Action Structure:**
```
sustainability-action/
├── action.yml
├── src/
│   ├── main.py
│   └── sustainability_evaluator.py
├── Dockerfile
└── README.md
```

**action.yml:**
```yaml
name: 'Sustainability Analysis Action'
description: 'Comprehensive code sustainability and environmental impact analysis'
inputs:
  project-path:
    description: 'Path to analyze'
    required: false
    default: '.'
  output-format:
    description: 'Report format (html, json, both)'
    required: false
    default: 'both'
  min-score:
    description: 'Minimum sustainability score threshold'
    required: false
    default: '60'
outputs:
  sustainability-score:
    description: 'Overall sustainability score'
  report-path:
    description: 'Path to generated report'
runs:
  using: 'docker'
  image: 'Dockerfile'
```

**Usage:**
```yaml
- name: Run Sustainability Analysis
  uses: your-org/sustainability-action@v1
  with:
    project-path: './src'
    output-format: 'both'
    min-score: '70'
```

---

## 🔧 Project Adaptation Strategies

### Language-Specific Configurations

**Python Projects:**
```yaml
env:
  PYTHON_VERSION: '3.11'
  ANALYSIS_TOOLS: 'bandit,safety,radon,pylint'
  PACKAGE_MANAGER: 'pip'
```

**JavaScript/Node.js Projects:**
```yaml
env:
  NODE_VERSION: '20'
  ANALYSIS_TOOLS: 'eslint,audit,jshint'
  PACKAGE_MANAGER: 'npm'
```

**Multi-Language Projects:**
```yaml
env:
  LANGUAGES: 'python,javascript'
  ANALYSIS_MODE: 'comprehensive'
```

### Framework-Specific Adaptations

**React Projects:**
```yaml
- name: React Bundle Analysis
  run: |
    npm run build
    npx webpack-bundle-analyzer build/static/js/*.js --report
```

**Django Projects:**
```yaml
- name: Django Security Check
  run: |
    python manage.py check --deploy
    bandit -r . -f json -o security-report.json
```

**FastAPI Projects:**
```yaml
- name: API Performance Analysis
  run: |
    pip install locust
    locust --headless -f performance/locustfile.py
```

---

## 📋 Configuration Templates

### Universal Configuration Template

```yaml
# sustainability-config.yml
analysis:
  depth: standard  # quick, standard, comprehensive
  languages: auto  # auto, python, javascript, mixed
  
thresholds:
  sustainability_score: 60
  energy_efficiency: 50
  security_score: 70
  
reporting:
  format: both  # html, json, both
  dashboard: true
  trends: true
  
notifications:
  pr_comments: true
  slack: false
  email: false
  
quality_gates:
  block_on_fail: false
  require_improvement: true
```

### Project Type Templates

**Microservice Template:**
```yaml
# microservice-sustainability.yml
analysis:
  focus: [performance, security, dependencies]
  containerized: true
  
thresholds:
  sustainability_score: 75  # Higher for production services
  memory_efficiency: 80
  
deployment:
  auto_deploy: true
  environment: production
```

**Library/Package Template:**
```yaml
# library-sustainability.yml
analysis:
  focus: [maintainability, documentation, dependencies]
  public_api: true
  
thresholds:
  code_quality: 85  # Higher for shared libraries
  documentation: 90
  
distribution:
  package_registry: true
  compatibility_check: true
```

---

## 🏢 Enterprise Deployment

### Organization-Wide Standards

**Centralized Configuration:**
```yaml
# .github/sustainability-standards.yml (Organization level)
organization:
  default_thresholds:
    sustainability_score: 70
    security_score: 80
  
  required_analysis: [sustainability, security, performance]
  
  notification_channels:
    slack_workspace: "dev-sustainability"
    email_list: "sustainability-team@company.com"
  
  compliance:
    reporting_frequency: weekly
    audit_requirements: true
```

**Repository Settings Template:**
```bash
#!/bin/bash
# setup-sustainability.sh - Organization deployment script

REPO_NAME=$1
PROJECT_TYPE=${2:-"mixed"}

# Clone template
gh repo create "$REPO_NAME" --template org/sustainability-template

# Configure repository settings  
gh api repos/org/$REPO_NAME -X PATCH -f has_pages=true
gh api repos/org/$REPO_NAME/actions/permissions -X PUT -f enabled=true

# Set required status checks
gh api repos/org/$REPO_NAME/branches/main/protection -X PUT \
  --field required_status_checks='{"strict":true,"contexts":["Sustainability Quality Gate"]}'

echo "✅ Sustainability pipeline configured for $REPO_NAME"
```

### Multi-Repository Management

**Bulk Deployment Script:**
```python
#!/usr/bin/env python3
# deploy-sustainability.py

import os
import subprocess
from pathlib import Path

class SustainabilityDeployer:
    def __init__(self, organization):
        self.org = organization
        self.template_repo = f"{organization}/sustainability-template"
    
    def get_repositories(self):
        """Get all repositories in organization"""
        cmd = f"gh repo list {self.org} --json name,isPrivate,primaryLanguage"
        result = subprocess.run(cmd.split(), capture_output=True, text=True)
        return json.loads(result.stdout)
    
    def deploy_to_repo(self, repo_name, project_type="mixed"):
        """Deploy sustainability pipeline to specific repository"""
        print(f"🚀 Deploying to {repo_name}...")
        
        # Clone repository
        subprocess.run(f"gh repo clone {self.org}/{repo_name}".split())
        
        # Copy workflow files
        workflow_source = f"{self.template_repo}/.github/workflows/"
        workflow_dest = f"{repo_name}/.github/workflows/"
        subprocess.run(f"cp -r {workflow_source} {workflow_dest}".split())
        
        # Copy sustainability evaluator
        subprocess.run(f"cp {self.template_repo}/sustainability_evaluator.py {repo_name}/".split())
        
        # Configure for project type
        self.configure_for_project_type(repo_name, project_type)
        
        # Commit and push
        os.chdir(repo_name)
        subprocess.run("git add .".split())
        subprocess.run("git commit -m '🌱 Add sustainability pipeline'".split())
        subprocess.run("git push".split())
        os.chdir("..")
        
        print(f"✅ Successfully deployed to {repo_name}")
    
    def bulk_deploy(self):
        """Deploy to all repositories in organization"""
        repos = self.get_repositories()
        
        for repo in repos:
            project_type = self.detect_project_type(repo['primaryLanguage'])
            self.deploy_to_repo(repo['name'], project_type)
    
    def detect_project_type(self, language):
        """Detect project type from primary language"""
        mapping = {
            'Python': 'python',
            'JavaScript': 'javascript', 
            'TypeScript': 'javascript',
            'Go': 'go',
            'Java': 'java'
        }
        return mapping.get(language, 'mixed')

# Usage
if __name__ == "__main__":
    deployer = SustainabilityDeployer("your-org")
    deployer.bulk_deploy()
```

---

## 🎛️ Customization Framework

### Configuration Override System

**Project-Specific Overrides:**
```yaml
# .sustainability/config.yml (Project level)
extends: organization-defaults

overrides:
  thresholds:
    sustainability_score: 80  # Stricter than org default
  
  analysis:
    exclude_patterns:
      - "legacy/**"
      - "vendor/**"
  
  custom_rules:
    - name: "database-efficiency"
      pattern: "SELECT \\* FROM"
      severity: "warning"
      message: "Avoid SELECT * for better performance"
```

### Plugin Architecture

**Custom Analysis Plugins:**
```python
# plugins/custom_sustainability_plugin.py
class CustomSustainabilityPlugin:
    def __init__(self, config):
        self.config = config
    
    def analyze_code(self, file_path):
        """Custom analysis logic"""
        return {
            'score': 75,
            'issues': [],
            'recommendations': []
        }
    
    def generate_report(self, analysis_results):
        """Custom reporting logic"""
        pass

# Register plugin
SUSTAINABILITY_PLUGINS = [
    'plugins.custom_sustainability_plugin.CustomSustainabilityPlugin',
    'plugins.industry_specific.FinanceCompliancePlugin',
    'plugins.framework_specific.ReactSustainabilityPlugin'
]
```

---

## 📦 Distribution Methods

### 1. GitHub Marketplace Action
```bash
# Publish to GitHub Marketplace
gh auth login
cd sustainability-action
git tag v1.0.0
git push origin v1.0.0
# Submit to marketplace via GitHub UI
```

### 2. Docker Image Distribution
```dockerfile
# Dockerfile for containerized deployment
FROM python:3.11-slim

RUN pip install sustainability-analyzer

COPY sustainability_evaluator.py /app/
COPY entrypoint.sh /app/

WORKDIR /app
ENTRYPOINT ["/app/entrypoint.sh"]
```

### 3. Package Manager Distribution
```bash
# PyPI Package
pip install sustainability-pipeline-tool

# NPM Package  
npm install -g @your-org/sustainability-pipeline
```

---

## 🔄 Maintenance & Updates

### Centralized Update System

**Template Sync Automation:**
```yaml
# .github/workflows/template-sync.yml
name: Sync Template Updates
on:
  schedule:
    - cron: '0 2 * * 1'  # Weekly Monday 2 AM
  
jobs:
  sync-template:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - name: Sync from template
      run: |
        git remote add template https://github.com/org/sustainability-template.git
        git fetch template
        git merge template/main --allow-unrelated-histories
        git push origin main
```

**Automated Dependency Updates:**
```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
  
  - package-ecosystem: "pip"
    directory: "/sustainability-tools"
    schedule:
      interval: "weekly"
```

---

## 📊 Adoption Tracking

### Usage Analytics

```python
# analytics/track_adoption.py
class AdoptionTracker:
    def track_usage(self, repo_name, analysis_results):
        """Track sustainability pipeline usage across organization"""
        metrics = {
            'repo': repo_name,
            'timestamp': datetime.now(),
            'score': analysis_results['sustainability_score'],
            'analysis_duration': analysis_results['duration'],
            'recommendations_count': len(analysis_results['recommendations'])
        }
        
        # Send to analytics platform
        self.send_to_analytics(metrics)
    
    def generate_adoption_report(self):
        """Generate organization-wide adoption and improvement report"""
        return {
            'repos_using_pipeline': 45,
            'average_sustainability_score': 72.3,
            'total_improvements': 156,
            'co2_reduction_estimate': '2.3 tons/year'
        }
```

### Success Metrics Dashboard

**Organization Dashboard:**
- 📊 Adoption rate across repositories
- 📈 Average sustainability score trends
- 🎯 Quality gate pass/fail rates
- 💡 Most common recommendation types
- 🌱 Environmental impact estimates

---

## 🎯 Best Practices for Reusability

### 1. **Modular Design**
- Separate core logic from configuration
- Plugin-based architecture for extensibility
- Clear interfaces between components

### 2. **Configuration Management**
- Use inheritance for configuration files
- Provide sensible defaults
- Allow project-specific overrides

### 3. **Documentation**
- Comprehensive setup guides per project type
- Migration documentation for existing projects
- Troubleshooting guides and FAQ

### 4. **Version Management**
- Semantic versioning for releases
- Backward compatibility guarantees
- Migration guides between versions

### 5. **Community Support**
- Open source with clear contribution guidelines
- Issue templates and support channels
- Regular maintenance and updates

---

## 🚀 Quick Start for New Projects

```bash
#!/bin/bash
# quick-setup.sh - One-command setup

PROJECT_TYPE=${1:-"mixed"}
REPO_NAME=${2:-$(basename $(pwd))}

echo "🌱 Setting up sustainability pipeline for $REPO_NAME ($PROJECT_TYPE)"

# Download template files
curl -sSL https://github.com/your-org/sustainability-template/archive/main.zip > template.zip
unzip template.zip

# Copy relevant files
cp -r sustainability-template-main/.github .
cp sustainability-template-main/sustainability_evaluator.py .

# Configure for project type
if [ "$PROJECT_TYPE" = "python" ]; then
    cp sustainability-template-main/configs/python-config.yml .sustainability/config.yml
elif [ "$PROJECT_TYPE" = "javascript" ]; then
    cp sustainability-template-main/configs/javascript-config.yml .sustainability/config.yml
fi

# Cleanup
rm -rf template.zip sustainability-template-main

# Initialize git workflow
git add .
git commit -m "🌱 Initialize sustainability pipeline"

echo "✅ Sustainability pipeline configured!"
echo "📊 Visit https://your-org.github.io/$REPO_NAME after first push"
```

This comprehensive reusability framework makes the sustainability pipeline easily deployable across any number of projects while maintaining consistency and allowing for project-specific customizations!