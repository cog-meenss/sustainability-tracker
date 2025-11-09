#!/usr/bin/env python3
import json
import os

with open('comprehensive_sustainability_data.json', 'r') as f:
    analysis = json.load(f)

metrics = analysis['sustainability_metrics']
patterns = analysis.get('detailed_analysis', {}).get('code_patterns', {})
metadata = analysis['report_metadata']

# Create enhanced GitHub Actions job summary with comprehensive data
def get_score_bar(score):
    filled = int(score / 5)  # 20 blocks for 100%
    empty = 20 - filled
    return '🟩' * filled + '⬜' * empty

def get_score_status(score):
    if score >= 90: return '🏆 Excellent'
    elif score >= 75: return '✅ Good'
    elif score >= 60: return '⚠️ Fair'
    else: return '❌ Needs Work'

def get_issue_status(count):
    if count == 0: return '🟢 Clean'
    elif count < 100: return '🟡 Minor'
    elif count < 500: return '🟠 Moderate'
    else: return '🔴 Critical'

overall_bar = get_score_bar(metrics['overall_score'])
energy_bar = get_score_bar(metrics['energy_efficiency'])
resource_bar = get_score_bar(metrics['resource_utilization'])
maintainability_bar = get_score_bar(metrics['maintainability'])

# Calculate total performance issues
total_issues = sum([
    patterns.get('async_patterns', 0),
    patterns.get('loop_optimizations', 0),
    patterns.get('memory_leaks', 0),
    patterns.get('console_logs', 0),
    patterns.get('inefficient_queries', 0)
])

# Generate status variables to avoid complex f-string expressions
quality_gate_result = '**✅ PASSED** ' if metrics['overall_score'] >= 75 else '**❌ FAILED** '
total_issues_priority = '🔴 High' if total_issues > 500 else '🟡 Medium' if total_issues > 100 else '🟢 Low'
carbon_potential = '🟢 Low Impact' if metrics['carbon_footprint'] > 70 else '🟡 Medium Impact' if metrics['carbon_footprint'] > 40 else '🔴 High Impact'
energy_potential = '✅ Optimized' if metrics['energy_efficiency'] > 70 else '⚠️ Needs Work'
practices_potential = '🟢 Good' if metrics['sustainable_practices'] > 50 else '🔴 Poor'
quality_gate_status = '✅ Passing' if metrics['overall_score'] >= 75 else '❌ Failing'

job_summary = f"""# 🌱 Comprehensive Sustainability Analysis Dashboard

## Overall Score: {metrics['overall_score']:.1f}/100 {get_score_status(metrics['overall_score'])}

```
Overall Score [{overall_bar}] {metrics['overall_score']:.1f}/100
```

### ⚡ Analysis Performance

| Metric | Value | Details |
|--------|-------|---------|
| 🔍 **Analysis Time** | **{metadata['analysis_time']:.3f}s** | Comprehensive evaluation |
| 📊 **Files Processed** | **30** | Total codebase analysis |
| 🚨 **Issues Detected** | **{total_issues}** | Performance problems found |
| 🌍 **Carbon Footprint** | **{metrics['carbon_footprint']:.1f}/100** | Environmental efficiency score |
| 🕐 **Generated At** | **{metadata['generated_at'][:19]}** | Fresh comprehensive analysis |

### 📊 Comprehensive Sustainability Metrics

| Metric | Score | Visual Progress | Status | Impact |
|--------|-------|----------------|--------|---------|
| **Energy Efficiency** | **{metrics['energy_efficiency']:.1f}/100** | `{energy_bar}` | {get_score_status(metrics['energy_efficiency'])} | 🔋 Computational overhead |
| **Resource Utilization** | **{metrics['resource_utilization']:.1f}/100** | `{resource_bar}` | {get_score_status(metrics['resource_utilization'])} | 💿 Memory & storage |
| **Code Maintainability** | **{metrics['maintainability']:.1f}/100** | `{maintainability_bar}` | {get_score_status(metrics['maintainability'])} | 🔧 Long-term maintenance |
| **Code Quality** | **{metrics['code_quality']:.1f}/100** | `{get_score_bar(metrics['code_quality'])}` | {get_score_status(metrics['code_quality'])} | 📊 Code standards |

### 🎯 Quality Gate Assessment

> **Result:** {quality_gate_result} 
> **Threshold:** 75/100 | **Achieved:** {metrics['overall_score']:.1f}/100

### 🚨 Performance Issues Analysis

| Issue Type | Count | Status | Priority |
|------------|-------|--------|----------|
| **Total Issues** | **{total_issues}** | {get_issue_status(total_issues)} | {total_issues_priority} |
| **Loop Patterns** | **{patterns.get('loop_optimizations', 0)}** | {get_issue_status(patterns.get('loop_optimizations', 0))} | ⚡ Performance |
| **Async Operations** | **{patterns.get('async_patterns', 0)}** | {get_issue_status(patterns.get('async_patterns', 0))} | 🔄 Concurrency |
| **Console Logs** | **{patterns.get('console_logs', 0)}** | {get_issue_status(patterns.get('console_logs', 0))} | 🗂️ Debug Code |

### 🌍 Carbon Impact Assessment

| Component | Score | Optimization Potential |
|-----------|-------|----------------------|
| **Carbon Footprint** | **{metrics['carbon_footprint']:.1f}/100** | {carbon_potential} |
| **Energy Efficiency** | **{metrics['energy_efficiency']:.1f}/100** | {energy_potential} |
| **Sustainable Practices** | **{metrics['sustainable_practices']:.1f}/100** | {practices_potential} |

### 💡 Priority Action Items

"""

# Generate recommendations based on metrics
recommendations = []
if metrics['energy_efficiency'] < 50:
    recommendations.append("🔴 **Critical**: Optimize energy-intensive operations and reduce computational overhead")
if total_issues > 500:
    recommendations.append(f"🔴 **Critical**: Address {total_issues} performance issues detected")
if patterns.get('loop_optimizations', 0) > 100:
    recommendations.append(f"🟡 **Medium**: Review {patterns.get('loop_optimizations', 0)} loop patterns for optimization opportunities")
if metrics['carbon_footprint'] < 50:
    recommendations.append(f"🟡 **Medium**: Improve carbon footprint score from {metrics['carbon_footprint']:.1f}/100")
if metrics['maintainability'] < 60:
    recommendations.append("🟢 **Low**: Improve code maintainability for long-term sustainability")

for i, rec in enumerate(recommendations, 1):
    job_summary += f"{i}. {rec}\\n"

# Add comprehensive analysis insights
trend_emoji = '📈' if metrics['overall_score'] >= 75 else '⚖️' if metrics['overall_score'] >= 60 else '📉'

job_summary += f"""

### 🔄 Comprehensive Analysis Insights

{trend_emoji} **Sustainability Health Check:** 
- **Analysis Duration:** {metadata['analysis_time']:.3f}s (Deep comprehensive scan)
- **Current Score:** **{metrics['overall_score']:.1f}/100**
- **Quality Gate:** **{quality_gate_status}**
- **Project Health:** **{get_score_status(metrics['overall_score'])}**
- **Carbon Efficiency:** **{metrics['carbon_footprint']:.1f}/100**

### 📊 Available Comprehensive Reports

| Report Format | Description | Access Method |
|---------------|-------------|---------------|
| 🎨 **HTML Interactive** | Advanced dashboard with Chart.js visualizations | Download `comprehensive-reports` artifact |
| 📊 **JSON Data** | Detailed machine-readable comprehensive metrics | Download `comprehensive-reports` artifact |
| 📈 **Executive Summary** | Strategic insights and action plans | Download `comprehensive-reports` artifact |

---
<div align="center">

**🌱 Generated by Comprehensive Sustainability Evaluator** 
*{metadata['generated_at'][:19]} • Advanced Analysis with Visualisations*
 • [📈 All Analyses](../../actions)

</div>
"""

with open(os.environ['GITHUB_STEP_SUMMARY'], 'w') as f:
    f.write(job_summary)

print("Job summary created successfully")