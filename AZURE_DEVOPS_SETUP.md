# 🚀 Azure DevOps Pipeline Setup - Step by Step

## 📋 Prerequisites Checklist

Before starting, ensure you have:
- ✅ Azure DevOps account with project access
- ✅ Repository connected to Azure DevOps (GitHub, Azure Repos, etc.)
- ✅ Pipeline creation permissions
- ✅ Your code pushed to the repository with `azure-pipelines.yml` file

## 🎯 Method 1: Azure DevOps Web Portal (Recommended)

### Step 1: Navigate to Pipelines
1. Open your **Azure DevOps project**
2. Click **Pipelines** in the left sidebar
3. Click **"New pipeline"** button

### Step 2: Select Repository Source
Choose your repository source:
- **Azure Repos Git** (if using Azure Repos)
- **GitHub** (if using GitHub)
- **Bitbucket Cloud**
- **Other Git repositories**

### Step 3: Configure Pipeline
1. Select **"Existing Azure Pipelines YAML file"**
2. Choose your repository branch (usually `main` or `master`)
3. Select the YAML file path: **`azure-pipelines.yml`**
4. Click **"Continue"**

### Step 4: Review and Run
1. Review the pipeline configuration
2. Click **"Run"** to create and execute the pipeline
3. The pipeline will start immediately

### Step 5: Configure Variables (Optional but Recommended)
1. After pipeline creation, click **"Edit"**
2. Click **"Variables"** tab
3. Add these variables:

| Variable Name | Value | Description |
|---------------|-------|-------------|
| `sustainabilityThreshold` | `75` | Minimum score for quality gate |
| `reportFormat` | `all` | Generate all report formats |
| `TeamsWebhookUrl` | `https://outlook.office.com/webhook/...` | Teams notifications (optional) |

### Step 6: Save and Run Again
1. Click **"Save"** after adding variables
2. Click **"Run pipeline"** to test with new settings

## 🎯 Method 2: Azure CLI (Command Line)

### Prerequisites
```bash
# Install Azure CLI (if not already installed)
brew install azure-cli  # macOS
# or
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash  # Linux

# Login to Azure
az login

# Install DevOps extension
az extension add --name azure-devops

# Configure defaults
az devops configure --defaults organization=https://dev.azure.com/YourOrg project=YourProject
```

### Create Pipeline via CLI
```bash
# Create the pipeline
az pipelines create \
  --name "Sustainability-Analysis" \
  --description "Automated code sustainability evaluation and reporting" \
  --repository "Tracker" \
  --repository-type "tfsgit" \
  --branch "main" \
  --yaml-path "azure-pipelines.yml"

# Set pipeline variables
az pipelines variable create \
  --pipeline-name "Sustainability-Analysis" \
  --name "sustainabilityThreshold" \
  --value "75"

az pipelines variable create \
  --pipeline-name "Sustainability-Analysis" \
  --name "reportFormat" \
  --value "all"

# Run the pipeline
az pipelines run --name "Sustainability-Analysis"
```

### Check Pipeline Status
```bash
# List recent runs
az pipelines runs list --pipeline-name "Sustainability-Analysis" --top 5

# Get specific run details
az pipelines runs show --id <run-id>

# Download artifacts
az pipelines runs artifact download \
  --artifact-name "SustainabilityReports" \
  --run-id <run-id> \
  --path ./downloaded-reports
```

## 📊 What Happens When Pipeline Runs

### Stage 1: Sustainability Analysis (5-10 minutes)
```yaml
🔄 Checkout source code
🐍 Setup Python 3.9 environment
📦 Install dependencies (pandas, plotly, etc.)
🔍 Run sustainability analyzer on codebase
📊 Generate analysis metrics and data
✅ Extract scores for quality gates
```

### Stage 2: Report Generation (2-3 minutes)
```yaml
🎨 Generate interactive HTML dashboard
📋 Create advanced data tables
📄 Build executive summary PDF
🔗 Prepare Azure DevOps integration
📦 Package all reports as artifacts
```

### Stage 3: Quality Gate Evaluation (1 minute)
```yaml
🎯 Check overall sustainability score vs threshold
⚠️  Generate warnings for low scores
✅ Pass/fail quality gate based on criteria
📢 Prepare notifications if needed
```

### Stage 4: Publish Results (1 minute)
```yaml
📊 Publish test results to Azure DevOps
📦 Store artifacts (reports, dashboards)
📝 Create build summary with key metrics
🔔 Send Teams/email notifications (if configured)
```

## 🎊 Pipeline Output & Results

### Build Summary Display
After pipeline runs, you'll see in Azure DevOps:

```markdown
🌱 Sustainability Analysis Results

📊 Overall Score: 78.5/100

### Detailed Metrics:
- ⚡ Energy Efficiency: 82.3/100
- 💾 Resource Utilization: 76.8/100  
- 🌍 Carbon Footprint: 45.2/100 (lower is better)

### Quality Gate: ✅ PASSED

📈 View Detailed Dashboard
```

### Available Artifacts
1. **SustainabilityReports** artifact containing:
   - `dashboard.html` - Interactive visual dashboard
   - `azure-report.html` - Azure DevOps formatted report  
   - `executive-summary.pdf` - Stakeholder summary
   - `analysis.json` - Raw analysis data
   - `junit-results.xml` - Test results format

### Test Results Integration
- Sustainability metrics appear in **Tests** tab
- Pass/fail status based on quality thresholds
- Detailed breakdown by metric categories

## ⚡ Pipeline Triggers

Your pipeline will automatically run on:

### Push Triggers
```yaml
✅ Push to main branch
✅ Push to develop branch  
✅ Excludes: README.md, docs/* changes
```

### Pull Request Triggers
```yaml
✅ PR targeting main branch
✅ PR targeting develop branch
✅ Shows sustainability impact of changes
```

### Scheduled Triggers
```yaml
🕐 Weekly analysis: Monday 2 AM UTC
📅 Ensures regular sustainability monitoring
🔄 Always runs even without code changes
```

### Manual Triggers
```yaml
▶️  Run pipeline button in Azure DevOps
🎯 On-demand analysis anytime
🔧 Test configuration changes
```

## 🛠️ Customization Options

### Adjust Quality Thresholds
```yaml
# In Pipeline Variables or azure-pipelines.yml
sustainabilityThreshold: 75      # Overall minimum score
energyThreshold: 80             # Energy efficiency minimum
carbonMaximum: 40               # Carbon footprint maximum
performanceThreshold: 85        # Performance minimum
```

### Configure Report Types
```yaml
reportFormat: "all"             # Generate all formats
# OR
reportFormat: "html"            # Only HTML dashboard
# OR  
reportFormat: "json,azure"      # JSON + Azure DevOps format
```

### Teams Notifications Setup
1. Create Teams webhook in your channel:
   - Teams → Channel → Connectors → Incoming Webhook
2. Copy webhook URL
3. Add as pipeline variable: `TeamsWebhookUrl`

### Email Notifications
```yaml
# Add to azure-pipelines.yml
- task: EmailReport@1
  condition: or(failed(), eq(variables['SustainabilityCheckPassed'], 'false'))
  inputs:
    to: 'team@company.com'
    subject: 'Sustainability Alert: $(Build.BuildNumber)'
    body: |
      Sustainability score below threshold
      Score: $(OverallSustainabilityScore)/100
      View report: $(System.TeamFoundationCollectionUri)$(System.TeamProject)/_build/results?buildId=$(Build.BuildId)
```

## 📈 Monitoring & Analytics

### Pipeline Analytics
- **Success/failure rates** - Track pipeline reliability
- **Duration trends** - Monitor analysis performance  
- **Quality gate statistics** - Success rates over time

### Build Retention
Configure in **Project Settings** → **Pipelines** → **Retention**:
- Keep sustainability reports for compliance
- Archive historical analysis data
- Maintain trend analysis capability

### Dashboard Integration
Create Azure DevOps dashboard widgets for:
- Latest sustainability scores
- Quality gate pass/fail trends
- Pipeline run frequency
- Alert notifications

## 🐛 Troubleshooting Common Issues

### ❌ "YAML file not found"
**Solution:** Ensure `azure-pipelines.yml` is in repository root
```bash
# Check file exists
ls -la azure-pipelines.yml

# If missing, create symlink
ln -sf sustainability-analyzer/pipeline/azure-pipelines.yml azure-pipelines.yml
git add azure-pipelines.yml
git commit -m "Add pipeline configuration"
git push
```

### ❌ "Python dependencies failed"
**Solution:** Update requirements.txt or use different Python version
```yaml
# In azure-pipelines.yml, try different Python version
variables:
  pythonVersion: '3.10'  # Instead of '3.9'
```

### ❌ "Analysis files not found"
**Solution:** Check file paths and repository structure
```yaml
# Add debugging step to azure-pipelines.yml
- script: |
    echo "Repository contents:"
    find . -name "*.py" -type f | head -20
    echo "Sustainability analyzer files:"
    ls -la sustainability-analyzer/
  displayName: 'Debug Repository Structure'
```

### ❌ "Quality gate always fails"
**Solution:** Adjust threshold or check score calculation
```bash
# Check actual scores in pipeline logs
# Lower threshold temporarily for testing
sustainabilityThreshold: 50  # Temporary lower threshold
```

## ✅ Verification Checklist

After pipeline setup, verify:

- [ ] Pipeline created successfully in Azure DevOps
- [ ] Pipeline runs without errors  
- [ ] All stages complete (Analysis → Quality Gate → Notification)
- [ ] Artifacts published (SustainabilityReports)
- [ ] Build summary shows sustainability metrics
- [ ] Test results appear in Tests tab
- [ ] Quality gate evaluates correctly
- [ ] Notifications work (if configured)
- [ ] Reports downloadable and readable

## 🚀 Next Steps

1. **Establish Baseline** - Run initial analysis to get baseline scores
2. **Set Team Goals** - Define target sustainability scores
3. **Enable Branch Policies** - Require sustainability checks for PRs
4. **Create Dashboards** - Set up monitoring dashboards
5. **Train Team** - Share sustainability metrics and improvement strategies

## 📞 Getting Help

- **Pipeline Issues**: Check Azure DevOps pipeline logs
- **Analysis Issues**: Review `analysis.json` in artifacts
- **Report Issues**: Verify report generation in pipeline steps
- **Configuration**: Check pipeline variables and YAML syntax

---

**🎉 Your sustainability analysis pipeline is ready to run in Azure DevOps!**

The pipeline will automatically analyze your code sustainability, generate comprehensive reports, and provide actionable insights for improvement.