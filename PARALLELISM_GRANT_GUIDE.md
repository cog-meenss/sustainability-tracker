# Azure DevOps Parallelism Grant Request Guide

## 🎯 **IMMEDIATE ACTION REQUIRED**

Your Azure DevOps pipeline cannot run because Microsoft requires a parallelism grant for hosted agents.

### **Quick Solution: Request Free Grant**

1. **Fill out the form**: https://aka.ms/azpipelines-parallelism-request
2. **Required Information**:
   - **Organization**: 159645
   - **Project**: Alpha
   - **Use Case**: Open source carbon footprint analysis tool development
   - **Justification**: Educational/research project for environmental sustainability

### **Form Details to Include**:
```
Organization Name: 159645
Project Name: Alpha
Project Description: Universal Carbon Footprint Analyzer - Environmental sustainability tool for code analysis
Use Case: Open source development and research
Estimated Monthly Usage: <30 minutes/month
Project URL: https://dev.azure.com/159645/Alpha/_git/Alpha
```

### **Expected Timeline**:
- **Response Time**: Usually 2-3 business days
- **Grant Type**: 1 free hosted pipeline with 1800 minutes/month
- **Cost**: Completely FREE

---

## 🏃‍♂️ **ALTERNATIVE: Self-Hosted Agent (Immediate)**

If you want to run the pipeline immediately, set up a self-hosted agent:

### **Steps**:
1. Go to Azure DevOps → Project Settings → Agent pools
2. Create new pool: "Default" (self-hosted)
3. Download agent for macOS
4. Install and configure on your machine
5. Update pipeline to use self-hosted pool

### **Pipeline Update Needed**:
```yaml
pool:
  name: 'Default'  # Your self-hosted pool name
  # vmImage: 'ubuntu-latest'  # Comment out hosted agent
```

---

## 🎯 **RECOMMENDATION**

**Request the free grant** - it's the easiest long-term solution and gives you:
- ✅ No setup required
- ✅ No maintenance
- ✅ Secure hosted environment
- ✅ 1800 minutes/month (plenty for your needs)
- ✅ Automatic updates and patching

The carbon footprint analysis pipeline will work perfectly once you have parallelism!

---

## 📋 **WHAT TO EXPECT**

Once approved, your pipeline will:
1. 🔍 Automatically analyze your code for carbon footprint
2. 📊 Generate beautiful HTML reports with charts
3. ⚡ Calculate energy usage and CO2 emissions
4. 🎯 Check against thresholds and provide recommendations
5. 📦 Archive all results as downloadable artifacts

**The pipeline is ready - it just needs the parallelism grant to run!**