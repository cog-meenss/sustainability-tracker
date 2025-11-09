# 🚀 Azure DevOps Pipeline Setup Guide
## Running Sustainability Analysis in CI/CD Pipeline

### 📋 Prerequisites

1. **Azure DevOps Project** with repository access
2. **Python 3.9+** available in pipeline agents
3. **Build permissions** to create and modify pipelines
4. **Artifact storage** permissions for reports

### 🛠️ Step-by-Step Setup

#### 1. **Commit Code to Repository**

```bash
# Add all sustainability analyzer files to your repository
git add sustainability-analyzer/
git commit -m "Add sustainability analysis pipeline integration"
git push origin main
```

#### 2. **Create Azure Pipeline**

1. Go to **Azure DevOps** → **Pipelines** → **New Pipeline**
2. Select your repository source
3. Choose **Existing Azure Pipelines YAML file**
4. Select: `sustainability-analyzer/pipeline/azure-pipelines.yml`
5. Click **Continue** → **Run**

#### 3. **Configure Pipeline Variables**

Navigate to **Pipelines** → **Edit** → **Variables** and add:

| Variable Name | Value | Description |
|---------------|-------|-------------|
| `sustainabilityThreshold` | `75` | Minimum score for quality gate |
| `TeamsWebhookUrl` | `https://...` | Teams notification webhook (optional) |
| `reportFormat` | `all` | Report format: html, json, azure, all |

#### 4. **Set Variable Groups** (Optional)

Create variable group `sustainability-analysis-config`:
- **Library** → **Variable groups** → **+ Variable group**
- Name: `sustainability-analysis-config`
- Add variables as needed

### 🎯 Pipeline Execution Flow

#### **Stage 1: Sustainability Analysis**
```yaml
- ✅ Checkout source code
- ✅ Setup Python 3.9
- ✅ Install dependencies
- ✅ Run sustainability analyzer
- ✅ Generate comprehensive reports
- ✅ Extract metrics for quality gate
- ✅ Publish test results
- ✅ Publish artifacts
```

#### **Stage 2: Quality Gate**
```yaml
- 🎯 Evaluate sustainability thresholds
- ⚠️  Warning if below threshold
- ✅ Pass/fail based on configured limits
```

#### **Stage 3: Notifications**
```yaml
- 📢 Teams notifications (if configured)
- 📊 Build summary with scores
- 📈 Link to detailed reports
```

### 📊 What You Get

#### **Automated Reports:**
- 🎨 **Interactive HTML Dashboard** - Visual charts and metrics
- 📋 **Azure DevOps Integration** - Native pipeline reporting
- 📄 **Executive Summary PDF** - Stakeholder-friendly overview
- 🔍 **Raw JSON Data** - For integration with other tools

#### **Pipeline Integration:**
- 🎯 **Quality Gates** - Automated pass/fail based on scores
- 📈 **Build Summaries** - Key metrics in pipeline overview
- 🧪 **Test Results** - Sustainability analysis as test results
- 📦 **Artifacts** - All reports stored as build artifacts

### 🚀 Quick Start Commands

#### **Run Pipeline Manually:**
```bash
# Trigger pipeline run
az pipelines run --name "Sustainability-Analysis" --branch main
```

#### **View Results:**
```bash
# Get latest build
az pipelines build list --top 1 --query "[0].{BuildNumber:buildNumber,Status:status,Result:result}"

# Download artifacts
az pipelines runs artifact download --artifact-name "SustainabilityReports" --path ./reports
```

### 🔧 Customization Options

#### **Pipeline Triggers:**
```yaml
# Modify triggers in azure-pipelines.yml
trigger:
  branches:
    include: [main, develop, release/*]
  paths:
    include: [src/*, backend/*, frontend/*]
    exclude: [docs/*, *.md]

# Schedule options
schedules:
- cron: "0 2 * * 1"      # Weekly Monday 2 AM
- cron: "0 6 * * 1-5"    # Daily weekdays 6 AM
- cron: "0 0 1 * *"      # Monthly 1st day
```

#### **Quality Gate Thresholds:**
```yaml
variables:
  sustainabilityThreshold: 75    # Overall score minimum
  energyThreshold: 80           # Energy efficiency minimum  
  carbonThreshold: 40           # Carbon footprint maximum
  performanceThreshold: 85      # Performance minimum
```

#### **Report Formats:**
```yaml
# Configure report generation
- script: |
    # HTML Dashboard
    python sustainability-analyzer/reports/html_generator.py \
      --input analysis.json --output dashboard.html
    
    # Executive PDF
    python sustainability-analyzer/reports/executive_summary.py \
      --input analysis.json --output summary.pdf
    
    # Azure DevOps format
    python sustainability-analyzer/reports/azure_publisher.py \
      --input analysis.json --output azure-report.html
```

### 📈 Monitoring & Alerts

#### **Teams Integration:**
1. Create Teams webhook in your channel
2. Add webhook URL to pipeline variables
3. Automatic notifications on failures or threshold violations

#### **Email Notifications:**
```yaml
# Add to pipeline
- task: EmailReport@1
  inputs:
    sendMailConditionConfig: 'Always'
    subject: 'Sustainability Analysis: $(Build.BuildNumber)'
    to: 'team@company.com'
    body: |
      Sustainability Score: $(OverallSustainabilityScore)/100
      Status: $(SustainabilityCheckPassed)
      
      View detailed report: $(System.TeamFoundationCollectionUri)$(System.TeamProject)/_build/results?buildId=$(Build.BuildId)
```

### 🐛 Troubleshooting

#### **Common Issues:**

**❌ Python Dependencies Failed**
```bash
# Solution: Update requirements.txt
pip install --upgrade pip setuptools wheel
pip install -r sustainability-analyzer/requirements.txt
```

**❌ Analysis Files Not Found**
```bash
# Solution: Check file paths
- script: |
    echo "Current directory: $(pwd)"
    echo "Files available:"
    find . -name "*.py" -type f | head -10
```

**❌ Quality Gate Always Fails**
```bash
# Solution: Check threshold values
echo "Threshold: $(sustainabilityThreshold)"
echo "Actual Score: $(OverallSustainabilityScore)"
```

### ✅ Success Verification

After pipeline setup, verify:

1. **Pipeline Runs Successfully** ✅
2. **Reports Generated** → Check artifacts
3. **Quality Gate Works** → Check stage results  
4. **Metrics Extracted** → Check build summary
5. **Notifications Sent** → Check Teams/email

### 🎯 Next Steps

1. **Integrate with Pull Requests** - Add PR triggers
2. **Set Up Dashboards** - Azure DevOps analytics
3. **Create Baselines** - Track improvement over time
4. **Add Custom Rules** - Project-specific sustainability rules
5. **Automate Actions** - Auto-fix common issues

**Ready to run sustainability analysis in your Azure DevOps pipeline!** 🚀