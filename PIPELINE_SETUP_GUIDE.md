# 🚀 Complete Pipeline Setup Guide - Carbon Footprint Analysis with Runtime Reports

## 📋 **Overview**

This guide shows you how to set up a complete Azure DevOps pipeline that:
- ✅ **Runs carbon footprint analysis** on every commit
- ✅ **Shows real-time results** during pipeline execution  
- ✅ **Displays interactive reports** in the pipeline interface
- ✅ **Enforces carbon thresholds** and fails builds if exceeded
- ✅ **Archives reports** for historical tracking
- ✅ **Provides live dashboard** for stakeholder viewing

## 🎯 **What You Get**

### **Real-Time Pipeline Output**
```bash
🌱 STARTING REAL-TIME CARBON FOOTPRINT ANALYSIS
============================================================
📅 Started: 2025-11-08 17:52:19
📂 Project: /path/to/your/project
📊 Reports: carbon-reports/

[17:52:19] 🔧 Setting up analysis environment...
   ✅ Carbon analyzer found
   ✅ Python 3.9 detected

[17:52:19] 📁 Scanning project structure...
   📁 Total files: 94,136
   💻 Source files: 77,894
   🗣️ Languages: JavaScript, Python, TypeScript, Java

[17:52:20] ⚡ Running carbon footprint analysis...
   ✅ Analysis completed successfully!

[17:52:20] 📊 Analysis complete! Displaying results...

============================================================
🌱 CARBON FOOTPRINT ANALYSIS - LIVE RESULTS
============================================================
📊 Primary Language: JavaScript
📁 Files Analyzed: 45
🌱 Carbon Footprint: 0.008234 kg CO2
⚡ Energy Usage: 0.017345 kWh
🌍 Impact Level: LOW

🎯 THRESHOLD CHECK:
   Current: 0.008234 kg CO2
   Limit:   0.100000 kg CO2
   Status:  ✅ WITHIN THRESHOLD

📊 BREAKDOWN:
   Code Execution: 40.6%
   Dependencies: 29.8%
   Frameworks: 23.5%
   Build System: 6.1%

💡 TOP RECOMMENDATIONS:
   1. Consider reducing bundle size by removing unused dependencies
   2. Implement code splitting for better performance
   3. Use React.memo for component optimization
============================================================
```

## 🔧 **Setup Steps**

### **1. Pipeline Configuration Files**

Your repository now contains these pipeline files:

#### **📄 `azure-pipelines.yml`** 
- Complete Azure DevOps pipeline configuration
- Multi-stage analysis with real-time reporting
- Threshold enforcement and artifact publishing
- HTML report generation and publishing

#### **📊 `carbon-footprint-analyzer/pipeline_reporter.py`**
- Real-time analysis reporter for live pipeline output
- Interactive dashboard server for stakeholder viewing  
- Comprehensive runtime display with metrics and recommendations

### **2. Azure DevOps Pipeline Setup**

1. **Create Pipeline in Azure DevOps**:
   ```
   Project Settings → Pipelines → Create Pipeline
   → Azure Repos Git → Select your Alpha repository
   → Existing Azure Pipelines YAML file
   → Select: /azure-pipelines.yml
   ```

2. **Configure Pipeline Variables**:
   ```yaml
   # In Azure DevOps Pipeline Variables:
   CARBON_THRESHOLD: '0.1'        # Maximum allowed kg CO2
   PYTHON_VERSION: '3.9'         # Python version to use
   ```

3. **Set Pipeline Triggers**:
   ```yaml
   # Already configured in azure-pipelines.yml:
   trigger:
   - main
   - develop  
   - feature/*
   ```

### **3. Pipeline Stages Breakdown**

#### **Stage 1: Carbon Footprint Analysis**
- ✅ **Environment Setup**: Install Python, dependencies
- ✅ **Project Scanning**: Detect languages and files
- ✅ **Analysis Execution**: Run carbon footprint calculation
- ✅ **Real-time Display**: Show live results in pipeline logs
- ✅ **Report Generation**: Create JSON and HTML reports
- ✅ **Threshold Check**: Validate against carbon limits

#### **Stage 2: Report Publishing**
- ✅ **HTML Report Tab**: Interactive dashboard in Azure DevOps
- ✅ **Artifact Archive**: Downloadable reports for offline analysis
- ✅ **Pipeline Variables**: Export metrics for downstream jobs
- ✅ **Notifications**: Email alerts if thresholds exceeded

#### **Stage 3: Summary Display**
- ✅ **Final Metrics**: Complete analysis summary
- ✅ **Trend Information**: Historical comparison
- ✅ **Action Items**: Next steps and recommendations

## 📊 **Runtime Report Features**

### **1. Live Pipeline Console Output**

During pipeline execution, you'll see:
- 🔄 **Real-time progress** with timestamps
- 📊 **Key metrics** displayed immediately
- 🎯 **Threshold validation** with pass/fail status
- 💡 **Optimization recommendations** 
- 🌍 **Environmental context** (smartphone charges, car distance)

### **2. Interactive HTML Reports**

Generated reports include:
- 📈 **Visual Dashboard**: Charts and graphs
- 📋 **Detailed Metrics**: File-by-file analysis
- 🎯 **Threshold Tracking**: Historical trend analysis
- 💡 **Action Items**: Prioritized optimization recommendations

### **3. Live Dashboard Server** (Optional)

For stakeholder viewing during development:

```bash
# Start live dashboard (local development)
cd carbon-footprint-analyzer
python3 pipeline_reporter.py --server --port 8080

# View at: http://localhost:8080
# Shows real-time analysis results
# Updates automatically as analysis runs
```

## 🎯 **Pipeline Behavior**

### **✅ Success Scenarios**
```
Carbon footprint ≤ threshold:
  ✅ Pipeline Status: SUCCESS
  📊 Reports: Generated and published
  📧 Notifications: Success summary
```

### **⚠️ Warning Scenarios**  
```
Carbon footprint > threshold:
  ⚠️ Pipeline Status: SUCCESS WITH ISSUES
  📊 Reports: Generated with warnings
  📧 Notifications: Threshold exceeded alert
  🔍 Action: Review optimization recommendations
```

### **❌ Failure Scenarios**
```
Analysis fails or critical errors:
  ❌ Pipeline Status: FAILED
  📊 Reports: Error logs available
  📧 Notifications: Failure alert
  🔧 Action: Check environment and dependencies
```

## 📈 **Accessing Reports During Runtime**

### **1. Azure DevOps Interface**

While pipeline is running:
- 📊 **Console Logs**: Real-time analysis output
- 🔍 **Live Progress**: Step-by-step execution status
- ⏱️ **Timing**: Duration of each analysis phase

After pipeline completes:
- 📋 **"Carbon Footprint Report" Tab**: Interactive HTML dashboard
- 📦 **"Artifacts"**: Downloadable JSON and HTML reports
- 📊 **Pipeline Summary**: Key metrics in overview

### **2. Direct Report Access**

```bash
# Download and view reports locally:
# 1. Go to Pipeline → Artifacts
# 2. Download "carbon-footprint-reports.zip"
# 3. Extract and open complete_analysis.html
# 4. View interactive dashboard with full details
```

### **3. Integration with Tools**

```bash
# Use JSON reports with other tools:
# - Grafana dashboards for long-term monitoring
# - JIRA integration for tracking optimization tasks
# - Slack notifications with key metrics
# - Email reports to stakeholders
```

## 🌍 **Real-World Usage Examples**

### **Example 1: Feature Development**
```
Developer creates feature branch:
  → Push triggers pipeline
  → Real-time analysis shows: 0.045 kg CO2 (under 0.1 threshold)
  → Pipeline succeeds ✅
  → Developer sees optimization tips in report
  → Merge to main approved
```

### **Example 2: Dependency Addition**
```
Developer adds heavy npm packages:
  → Push triggers pipeline  
  → Real-time analysis shows: 0.125 kg CO2 (over 0.1 threshold)
  → Pipeline succeeds with warnings ⚠️
  → Team receives threshold alert
  → Review meeting scheduled to discuss alternatives
```

### **Example 3: Performance Optimization**
```
Team implements code splitting:
  → Push triggers pipeline
  → Real-time analysis shows: 0.032 kg CO2 (significant improvement)
  → Pipeline reports 60% reduction from previous build
  → Success celebrated in team chat 🎉
```

## 🔧 **Customization Options**

### **Adjust Thresholds by Environment**
```yaml
# In azure-pipelines.yml:
variables:
  ${{ if eq(variables['Build.SourceBranch'], 'refs/heads/main') }}:
    CARBON_THRESHOLD: '0.05'  # Stricter for production
  ${{ else }}:
    CARBON_THRESHOLD: '0.1'   # More lenient for development
```

### **Different Configs by Project Type**
```yaml
# Auto-detect project type and use appropriate config:
- script: |
    if [ -f "package.json" ]; then
      echo "##vso[task.setvariable variable=CARBON_CONFIG]web_app_config.json"
    elif [ -f "requirements.txt" ]; then
      echo "##vso[task.setvariable variable=CARBON_CONFIG]python_project_config.json"
    fi
```

### **Integration with Existing Workflows**
```yaml
# Add carbon analysis to existing pipelines:
- template: existing-build-template.yml
- template: carbon-analysis-template.yml    # Add this line
- template: existing-deploy-template.yml
```

## 📧 **Notification Setup**

```yaml
# Add to azure-pipelines.yml for email alerts:
- task: EmailReport@1
  condition: gt(variables['CarbonFootprint'], variables['CARBON_THRESHOLD'])
  inputs:
    sendMailConditionConfig: 'Always'
    subject: '⚠️ Carbon Threshold Exceeded - $(Build.Repository.Name)'
    to: 'team@yourcompany.com'
    body: |
      Carbon footprint analysis shows emissions above threshold:
      
      Current: $(CarbonFootprint) kg CO2
      Threshold: $(CARBON_THRESHOLD) kg CO2
      
      View Report: $(System.TeamFoundationCollectionUri)$(System.TeamProject)/_build/results?buildId=$(Build.BuildId)&view=artifacts
```

## 🎉 **Summary**

Your carbon footprint analysis pipeline now provides:

✅ **Real-time visibility** into environmental impact  
✅ **Automated quality gates** with configurable thresholds  
✅ **Interactive reports** for detailed analysis  
✅ **Historical tracking** through archived artifacts  
✅ **Team notifications** when action is needed  
✅ **Optimization guidance** with actionable recommendations  

**Result**: A production-ready, automated carbon footprint monitoring system integrated into your development workflow! 🌱🚀