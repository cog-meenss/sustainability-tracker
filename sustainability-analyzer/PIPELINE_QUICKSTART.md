# 🚀 How to Run Sustainability Analysis in Azure DevOps Pipeline

## 🎯 Quick Start (3 Steps)

### 1. **Your Code is Ready!** ✅
All sustainability analysis files have been committed to your repository:
```bash
git log --oneline -1  # Shows: "🌱 Add sustainability analysis pipeline"
```

### 2. **Create Pipeline in Azure DevOps**
**Option A: Azure DevOps Portal**
1. Go to **Pipelines** → **New Pipeline**
2. Select your repository source
3. Choose **"Existing Azure Pipelines YAML file"**
4. Select: `azure-pipelines.yml`
5. Click **Run**

**Option B: Azure CLI**
```bash
az pipelines create \
  --name "Sustainability-Analysis" \
  --description "Code sustainability evaluation" \
  --repository-name "Tracker" \
  --branch main \
  --yaml-path azure-pipelines.yml
```

### 3. **Configure Pipeline Variables**
Add these variables in **Pipeline** → **Edit** → **Variables**:
| Variable | Value | Description |
|----------|-------|-------------|
| `sustainabilityThreshold` | `75` | Minimum score for quality gate |
| `reportFormat` | `all` | Generate all report types |
| `TeamsWebhookUrl` | `https://...` | Teams notifications (optional) |

## 🎊 What You Get

### **Automated Pipeline Stages:**
1. 🔍 **Sustainability Analysis** - Analyzes your code for sustainability metrics
2. 🎯 **Quality Gate** - Pass/fail based on sustainability threshold
3. 📢 **Notifications** - Teams/email alerts for failed quality gates

### **Generated Reports:**
- 📊 **Interactive Dashboard** - Visual charts and metrics
- 📋 **Data Tables** - Sortable/filterable data with export
- 📄 **Executive Summary** - Stakeholder-friendly PDF report
- 🔍 **Raw JSON Data** - For integration with other tools

### **Pipeline Integration:**
- ✅ **Build Artifacts** - All reports stored as build artifacts
- 📈 **Build Summary** - Key metrics displayed in pipeline overview
- 🧪 **Test Results** - Sustainability analysis as test results
- 🎯 **Quality Gates** - Automated pass/fail based on scores

## 📊 Sample Pipeline Output

```
🌱 Sustainability Analysis Results

📊 Overall Score: 78.5/100

### Detailed Metrics:
- ⚡ Energy Efficiency: 82.3/100
- 💾 Resource Utilization: 76.8/100  
- 🌍 Carbon Footprint: 45.2/100 (lower is better)
- 🚀 Performance: 85.1/100
- ♻️ Best Practices: 72.9/100

### Quality Gate: ✅ PASSED

📈 View Detailed Dashboard
```

## 🔧 Pipeline Triggers

**Automatic Triggers:**
- ✅ Push to `main` or `develop` branches
- ✅ Pull requests to `main` or `develop`  
- ✅ Weekly scheduled analysis (Monday 2 AM UTC)

**Manual Triggers:**
- ✅ Run from Azure DevOps portal
- ✅ Azure CLI: `az pipelines run --name "Sustainability-Analysis"`

## 🎯 Quality Gates & Thresholds

**Default Configuration:**
- Overall sustainability score ≥ **75/100** = ✅ PASS
- Below threshold = ⚠️ WARNING (not failure)
- Configurable per project needs

**Customizable Thresholds:**
```yaml
variables:
  sustainabilityThreshold: 75    # Overall score
  energyThreshold: 80           # Energy efficiency
  carbonMaximum: 40             # Carbon footprint (max)
  performanceThreshold: 85      # Performance minimum
```

## 📈 Monitoring & Analytics

### **Build Trends:**
- Track sustainability scores over time
- Identify improvement/regression patterns
- Set team goals and targets

### **Quality Metrics:**
- Pass/fail rates for quality gates
- Average sustainability scores
- Most common issues and fixes

### **Team Notifications:**
- Teams webhook integration
- Email alerts for threshold violations
- Custom notification rules

## 🛠️ Local Testing

Test your pipeline configuration locally:
```bash
# Run complete pipeline test
./sustainability-analyzer/test-pipeline.sh

# View results
open sustainability-analyzer/pipeline-test-output/dashboard.html
```

## 🔧 Customization Options

### **Analysis Scope:**
```yaml
# Modify file inclusion/exclusion
paths:
  include: [src/*, backend/*, frontend/*]
  exclude: [docs/*, test/*, *.md]
```

### **Report Types:**
```yaml
# Choose specific report formats
variables:
  reportFormat: "html"      # html, json, azure, all
  generatePDF: true         # Executive summary PDF
  includeCharts: true       # Interactive visualizations
```

### **Notification Settings:**
```yaml
# Teams integration
variables:
  TeamsWebhookUrl: "https://outlook.office.com/webhook/..."
  notifyOnSuccess: false    # Only notify on failures
  notifyOnThreshold: true   # Notify when below threshold
```

## 📚 Documentation

### **Complete Guides:**
- 📖 **Setup Guide:** `sustainability-analyzer/PIPELINE_SETUP.md`
- 🔧 **Configuration:** `sustainability-analyzer/config/analyzer_config.json`
- 🧪 **Testing:** `sustainability-analyzer/test-pipeline.sh`

### **Generated Reports:**
- 📊 **Visual Dashboard:** Interactive charts and graphs
- 📋 **Data Tables:** Advanced filtering and export
- 📄 **Executive Summary:** Stakeholder-ready PDF

## ✅ Success Verification

After pipeline setup, check:

1. **Pipeline Runs Successfully** ✅
   ```bash
   # Check latest build status
   az pipelines runs list --top 1
   ```

2. **Reports Generated** ✅
   - Check **Artifacts** tab in build results
   - Download and review sustainability reports

3. **Quality Gate Works** ✅
   - Verify threshold evaluation in pipeline logs
   - Check build summary for sustainability metrics

4. **Metrics Extracted** ✅
   - Build variables contain sustainability scores
   - Pipeline summary displays key metrics

## 🚀 Ready to Go!

Your sustainability analysis pipeline is **ready to run**! 

### **Next Steps:**
1. **Create pipeline** in Azure DevOps (using `azure-pipelines.yml`)
2. **Set variables** (threshold, webhook URL)
3. **Run pipeline** and review results
4. **Share reports** with your team
5. **Set improvement goals** based on baseline scores

### **Need Help?**
- 📖 Review: `sustainability-analyzer/PIPELINE_SETUP.md`
- 🧪 Test: `./sustainability-analyzer/test-pipeline.sh`
- 📊 Demo: `sustainability-analyzer/dashboard/demo_output/`

**Happy sustainable coding!** 🌱✨