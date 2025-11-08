# 🏗️ Jenkins CI/CD Integration for Carbon Footprint Analysis

## 🎯 Why Jenkins Integration is Essential

### **Continuous Environmental Monitoring**
- **Automatic Analysis**: Every code commit triggers carbon footprint analysis
- **Trend Tracking**: Monitor environmental impact over time across builds
- **Early Detection**: Catch carbon-intensive code before production deployment
- **Team Awareness**: Keep the entire team informed about environmental impact

### **Quality Gates & Governance**  
- **Threshold Enforcement**: Fail/unstable builds that exceed carbon limits
- **Compliance Reporting**: Generate reports for environmental compliance
- **Automated Alerts**: Notify teams when footprint exceeds acceptable levels
- **Historical Data**: Build comprehensive environmental impact history

### **DevOps Integration Benefits**
- **Shift-Left Testing**: Include sustainability as part of quality assurance
- **Automated Optimization**: Identify performance improvements with environmental benefits
- **Stakeholder Visibility**: Provide management with environmental metrics
- **Cost Correlation**: Link energy consumption to operational costs

## 🚀 Quick Setup Guide

### **1. Install the Integration**

```bash
# In your Jenkins workspace, add carbon analyzer
git submodule add https://github.com/your-org/carbon-footprint-analyzer.git
cd carbon-footprint-analyzer

# Generate sample Jenkinsfile
python3 examples/integrations/jenkins_integration.py --create-jenkinsfile
cp Jenkinsfile ../  # Copy to repository root
```

### **2. Configure Jenkins Pipeline**

Copy the generated `Jenkinsfile` to your repository root. The pipeline includes:

- **Checkout**: Get latest code  
- **Analysis**: Run carbon footprint analysis
- **Reporting**: Generate HTML and JSON reports
- **Thresholds**: Check against carbon limits
- **Artifacts**: Archive reports and trends
- **Notifications**: Alert team of threshold violations

### **3. Environment Variables**

Configure these Jenkins environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `CARBON_THRESHOLD` | `0.1` | Maximum allowed kg CO2 before build marked unstable |
| `CARBON_CONFIG` | `web_app_config.json` | Configuration file for analysis |

### **4. Jenkins Plugins Required**

Install these Jenkins plugins for full functionality:

- **Pipeline Plugin**: For pipeline execution
- **HTML Publisher**: For HTML report publishing  
- **Plot Plugin**: For carbon footprint trend charts
- **Email Extension**: For threshold violation notifications
- **Workspace Cleanup**: For build hygiene

## 📊 What You Get

### **Build Integration**
```bash
# Every build runs:
🔍 Starting carbon footprint analysis...
📊 Detecting languages and analyzing project structure...
🌱 Calculating carbon footprint...
📄 Generating reports...

✅ Analysis completed successfully!
📊 Primary Language: javascript
📁 Files Analyzed: 45
🌱 Carbon Footprint: 0.008234 kg CO2
⚡ Energy Usage: 0.017345 kWh
```

### **Threshold Management**
```bash
# If threshold exceeded:
❌ THRESHOLD EXCEEDED: 0.150000 kg CO2 > 0.100000 kg CO2
⚠️ Build marked as UNSTABLE
📧 Email notification sent to team
```

### **Trend Tracking**
- **CSV Reports**: `carbon_trend.csv` with build-by-build data
- **Jenkins Plots**: Visual charts showing carbon footprint over time
- **Historical Analysis**: Compare current vs. previous builds

### **Report Artifacts**
- **HTML Dashboard**: Interactive reports viewable in Jenkins
- **JSON Data**: Machine-readable results for downstream processing
- **Properties Files**: Key metrics accessible to other pipeline steps

## 🔧 Advanced Configuration

### **Custom Thresholds by Project Type**

```groovy
// In Jenkinsfile, customize by branch or project
environment {
    CARBON_THRESHOLD = "${env.BRANCH_NAME == 'main' ? '0.05' : '0.1'}"
    CARBON_CONFIG = "${detectProjectType()}"
}

def detectProjectType() {
    if (fileExists('package.json')) return 'web_app_config.json'
    if (fileExists('requirements.txt')) return 'python_project_config.json'  
    if (fileExists('pom.xml')) return 'java_project_config.json'
    return 'basic_config.json'
}
```

### **Multi-Environment Analysis**

```groovy
stage('Multi-Environment Carbon Analysis') {
    parallel {
        stage('Development Build') {
            environment { CARBON_THRESHOLD = '0.2' }
            steps { runCarbonAnalysis() }
        }
        stage('Production Simulation') {
            environment { CARBON_THRESHOLD = '0.05' }
            steps { runCarbonAnalysis() }
        }
    }
}
```

### **Integration with Other Tools**

```groovy
post {
    always {
        // Send to monitoring systems
        script {
            def props = readProperties file: 'carbon_analysis.properties'
            
            // Send to Grafana/Prometheus
            httpRequest(
                httpMode: 'POST',
                url: 'http://monitoring.company.com/metrics',
                requestBody: """
                {
                    "carbon_kg": ${props.CARBON_KG},
                    "energy_kwh": ${props.ENERGY_KWH},
                    "build_number": ${env.BUILD_NUMBER},
                    "project": "${env.JOB_NAME}"
                }
                """
            )
            
            // Update JIRA tickets with carbon impact
            jiraComment(
                issueKey: env.JIRA_ISSUE,
                body: "🌱 Carbon Impact: ${props.CARBON_KG} kg CO2 (${props.CARBON_IMPACT_LEVEL})"
            )
        }
    }
}
```

## 🎯 Integration Patterns

### **Pull Request Validation**
```groovy
// Only run carbon analysis on PRs
when { 
    changeRequest() 
}
steps {
    script {
        def result = runCarbonAnalysis()
        if (result > 0) {
            pullRequest.comment("⚠️ This PR increases carbon footprint by ${result}%")
        }
    }
}
```

### **Release Gates**
```groovy
// Block releases with high carbon footprint
stage('Release Gate') {
    when { tag "release-*" }
    steps {
        script {
            def analysis = runCarbonAnalysis()
            if (analysis.carbon_kg > 0.02) {
                error("❌ Release blocked: Carbon footprint too high for production")
            }
        }
    }
}
```

### **Performance Correlation**
```groovy
// Correlate with performance tests
stage('Performance + Carbon Analysis') {
    parallel {
        stage('JMeter Performance') { 
            steps { runJMeterTests() }
        }
        stage('Carbon Analysis') { 
            steps { runCarbonAnalysis() }
        }
    }
    post {
        always {
            script {
                correlatePerformanceWithCarbon()
            }
        }
    }
}
```

## 📈 Metrics & KPIs

Track these key metrics in your Jenkins dashboard:

- **Carbon Intensity**: kg CO2 per line of code
- **Energy Efficiency**: kWh per feature delivered  
- **Trend Analysis**: Week-over-week carbon footprint changes
- **Language Impact**: Carbon footprint by programming language
- **Threshold Violations**: Frequency and severity of exceedances
- **Optimization Success**: Impact of green coding practices

## 🔍 Troubleshooting

### **Common Issues**

| Issue | Solution |
|-------|----------|
| Import errors | Ensure carbon-footprint-analyzer is in workspace |
| Permission denied | Check Jenkins workspace permissions |
| Reports not generated | Verify HTML Publisher plugin configuration |
| Threshold always failing | Check CARBON_THRESHOLD environment variable |
| Trend charts not showing | Install Plot Plugin and verify CSV format |

### **Debug Mode**

```bash
# Run analysis with debug output
CARBON_DEBUG=true python3 jenkins_integration.py
```

## 🌱 Best Practices

1. **Start with Higher Thresholds**: Begin with 0.1 kg CO2, then gradually reduce
2. **Use Different Configs**: Customize analysis per project type
3. **Monitor Trends**: Focus on relative changes, not absolute values
4. **Team Education**: Share reports and educate on green coding practices
5. **Correlate with Performance**: Link carbon footprint to application performance
6. **Regular Reviews**: Review and adjust thresholds quarterly

## 🚀 Next Steps

After successful integration:

1. **Set Up Monitoring**: Connect to Grafana/Prometheus for long-term tracking
2. **Create Baselines**: Establish acceptable carbon footprint ranges
3. **Team Training**: Educate developers on sustainable coding practices
4. **Policy Development**: Create environmental coding standards
5. **Optimization Campaigns**: Regular code optimization sprints focused on efficiency

---

*This integration transforms carbon footprint analysis from a manual check into an automated, continuous process that keeps your software environmentally sustainable.* 🌱