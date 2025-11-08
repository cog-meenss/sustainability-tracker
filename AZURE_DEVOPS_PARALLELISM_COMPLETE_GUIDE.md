# 🚀 Complete Guide: Getting Azure DevOps Parallelism for Cloud Pipeline Execution

## 🎯 **QUICK START - 5 MINUTE SETUP**

### **Step 1: Request Free Parallelism Grant**
1. **Go to**: https://aka.ms/azpipelines-parallelism-request
2. **Fill out the form with these exact details**:

```
Organization Name: 159645
Project Name: Alpha
Project Description: Universal Carbon Footprint Analyzer - Open source tool for measuring environmental impact of software projects
Project URL: https://dev.azure.com/159645/Alpha/_git/Alpha
Use Case: Educational and research project for environmental sustainability analysis
Expected Usage: <30 minutes per month for development and testing
Open Source: Yes (if applicable)
```

### **Step 2: Submit Supporting Information**
In the "Additional Information" field, include:
```
This project is a carbon footprint analyzer that helps developers understand 
the environmental impact of their code. It's an educational tool focused on 
sustainability in software development. The pipeline will run carbon analysis 
on code repositories to generate environmental impact reports.

Monthly usage will be minimal (estimated <30 minutes) as this is primarily 
for development, testing, and demonstration purposes of the carbon analysis 
capabilities.
```

---

## ⏰ **TIMELINE & EXPECTATIONS**

| Step | Timeline | What Happens |
|------|----------|--------------|
| **Submit Request** | 5 minutes | Form submitted to Microsoft |
| **Review Process** | 2-3 business days | Microsoft reviews your request |
| **Approval Email** | Day 3-5 | You receive approval notification |
| **Pipeline Ready** | Immediate | Run your carbon analysis pipeline! |

---

## 📧 **WHAT TO EXPECT**

### **Approval Email Will Contain**:
- ✅ Confirmation of free parallelism grant
- ✅ Details: 1 hosted pipeline job
- ✅ Allocation: 1800 minutes per month (FREE)
- ✅ Instructions to start using hosted agents

### **Your Grant Will Include**:
- **1 Microsoft-hosted pipeline job**
- **1800 minutes/month** (more than enough for your needs)
- **All Azure DevOps regions** supported
- **Ubuntu, Windows, macOS** agents available

---

## 🎛️ **ALTERNATIVE: IMMEDIATE SOLUTION (Self-Hosted Agent)**

If you want to run the pipeline **TODAY** while waiting for the grant:

### **Option A: Quick Self-Hosted Setup (10 minutes)**

1. **Download Agent**:
   - Go to: Azure DevOps → Project Settings → Agent pools
   - Click "New agent" → Download for macOS
   - Extract to `/Users/159645/myagent`

2. **Configure Agent**:
   ```bash
   cd /Users/159645/myagent
   ./config.sh
   ```
   
3. **Enter Configuration**:
   ```
   Server URL: https://dev.azure.com/159645
   Authentication: Personal Access Token (create one in Azure DevOps)
   Agent pool: Default
   Agent name: MyMacAgent
   ```

4. **Start Agent**:
   ```bash
   ./run.sh
   ```

5. **Update Pipeline**: Change `azure-pipelines.yml`:
   ```yaml
   pool:
     name: 'Default'  # Your self-hosted pool
     # vmImage: 'ubuntu-latest'  # Comment this out
   ```

---

## 🔍 **TROUBLESHOOTING THE REQUEST**

### **Common Reasons for Delay**:
- **Incomplete form**: Make sure all fields are filled
- **Unclear use case**: Be specific about carbon analysis purpose
- **No project URL**: Include your Azure DevOps project link

### **If Request is Denied**:
1. **Resubmit** with more detailed description
2. **Emphasize educational/research** nature
3. **Mention environmental sustainability** focus
4. **Provide specific use case** for carbon analysis

### **Speed Up Approval**:
- ✅ **Be specific** about carbon footprint analysis purpose
- ✅ **Mention sustainability** and environmental focus
- ✅ **Provide accurate project URL**
- ✅ **Estimate realistic usage** (<30 min/month)

---

## 💰 **COST BREAKDOWN**

| Option | Setup Time | Monthly Cost | Minutes Included |
|--------|------------|--------------|------------------|
| **Free Grant** | 2-3 days wait | $0 | 1800 |
| **Self-Hosted** | 10 minutes | $0 | Unlimited |
| **Paid Hosted** | Immediate | $40 | 1800 |

**💡 Recommendation**: Request the free grant - it's the best long-term solution!

---

## 🚀 **ONCE YOU HAVE PARALLELISM**

### **Your Pipeline Will Automatically**:
1. 🔍 **Analyze your code** for carbon footprint
2. 📊 **Generate beautiful reports** with charts and metrics
3. ⚡ **Calculate energy consumption** and CO2 emissions
4. 🎯 **Check thresholds** and provide warnings
5. 💡 **Suggest optimizations** for better efficiency
6. 📦 **Archive results** as downloadable artifacts

### **Access Your Results**:
- **Pipeline Logs**: Real-time analysis output
- **Artifacts**: Download `carbon-footprint-html-reports`
- **HTML Dashboard**: Interactive charts and recommendations
- **JSON Data**: Raw data for further processing

---

## 📋 **VERIFICATION CHECKLIST**

Before submitting your parallelism request:

- [ ] **Organization**: 159645 ✓
- [ ] **Project**: Alpha ✓
- [ ] **Description**: Carbon footprint analysis tool ✓
- [ ] **Use Case**: Educational/research sustainability ✓
- [ ] **URL**: https://dev.azure.com/159645/Alpha/_git/Alpha ✓
- [ ] **Estimated Usage**: <30 minutes/month ✓

---

## 🎉 **SUCCESS INDICATORS**

### **You'll Know It Worked When**:
1. ✅ **Pipeline queue status**: Shows "Running" instead of "No hosted parallelism"
2. ✅ **Agent selection**: Automatically picks Microsoft-hosted agent
3. ✅ **Build logs**: Shows Ubuntu/Windows/macOS agent startup
4. ✅ **Carbon analysis**: Your analyzer runs and generates reports

### **First Successful Run Will Show**:
```
🌍 CARBON FOOTPRINT ANALYSIS PIPELINE
=====================================
Repository: Alpha
Branch: main
Threshold: 0.1 kg CO2
Agent: Microsoft-hosted (ubuntu-latest)

🔍 Starting Carbon Footprint Analysis...
📊 Analyzing 101 files...
⚡ Calculating carbon footprint...
✅ Analysis completed successfully!
```

---

## 🆘 **NEED HELP?**

### **If Your Request is Taking Too Long**:
- Check your email (including spam folder)
- Resubmit with more detailed justification
- Try alternative email address
- Contact Azure DevOps support

### **Pipeline Still Not Running?**:
- Verify your organization has the grant
- Check pipeline YAML syntax
- Ensure agent pool configuration is correct
- Try triggering pipeline manually

---

## 🌟 **FINAL RECOMMENDATION**

**Submit the free parallelism grant request NOW** - it takes 5 minutes to submit and will give you a permanent, hassle-free solution for running your carbon analysis pipeline in the cloud!

**Form Link**: https://aka.ms/azpipelines-parallelism-request

Once approved, your pipeline will run automatically on every commit, providing real-time carbon footprint analysis of your code changes! 🌱✨