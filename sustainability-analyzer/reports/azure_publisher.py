#!/usr/bin/env python3
"""
Azure DevOps Report Publisher
Generates Azure DevOps compatible reports and publishes to pipeline
"""

import json
import argparse
import os
from datetime import datetime
from typing import Dict, List, Any
from pathlib import Path

class AzureDevOpsReportPublisher:
    """Publisher for Azure DevOps pipeline integration"""
    
    def __init__(self):
        self.build_id = os.environ.get('BUILD_BUILDID', 'local')
        self.build_number = os.environ.get('BUILD_BUILDNUMBER', 'local')
        self.repo_name = os.environ.get('BUILD_REPOSITORY_NAME', 'unknown')
        self.branch = os.environ.get('BUILD_SOURCEBRANCH', 'unknown')
        
    def publish_report(self, analysis_data: Dict[str, Any], output_dir: str) -> Dict[str, str]:
        """Publish complete Azure DevOps compatible report"""
        
        outputs = {}
        
        # Generate Azure DevOps HTML report
        html_report = self._generate_azure_html_report(analysis_data)
        html_path = os.path.join(output_dir, 'azure-sustainability-report.html')
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_report)
        outputs['html_report'] = html_path
        
        # Generate JUnit XML for test results integration
        junit_xml = self._generate_junit_xml(analysis_data)
        junit_path = os.path.join(output_dir, 'junit-results.xml')
        with open(junit_path, 'w', encoding='utf-8') as f:
            f.write(junit_xml)
        outputs['junit_xml'] = junit_path
        
        # Generate Azure DevOps pipeline summary
        summary_md = self._generate_pipeline_summary(analysis_data)
        summary_path = os.path.join(output_dir, 'pipeline-summary.md')
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(summary_md)
        outputs['summary'] = summary_path
        
        # Generate quality gate results
        quality_gate = self._generate_quality_gate_results(analysis_data)
        quality_path = os.path.join(output_dir, 'quality-gate.json')
        with open(quality_path, 'w', encoding='utf-8') as f:
            json.dump(quality_gate, f, indent=2)
        outputs['quality_gate'] = quality_path
        
        print(f"Azure DevOps reports published to: {output_dir}")
        return outputs
    
    def _generate_azure_html_report(self, data: Dict[str, Any]) -> str:
        """Generate Azure DevOps compatible HTML report"""
        
        metrics = data.get('sustainability_metrics', {})
        summary = data.get('analysis_summary', {})
        issues = data.get('issues', [])
        recommendations = data.get('recommendations', [])
        
        return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sustainability Analysis Report - Build {self.build_number}</title>
    <style>
        {self._get_azure_css()}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Sustainability Analysis Report</h1>
            <div class="build-info">
                <span class="build-number">Build {self.build_number}</span>
                <span class="repo-name">{self.repo_name}</span>
                <span class="branch">{self.branch}</span>
            </div>
        </div>
        
        {self._generate_executive_summary_section(metrics, summary)}
        {self._generate_metrics_section(metrics)}
        {self._generate_quality_gates_section(data)}
        {self._generate_detailed_findings_section(issues, recommendations)}
        {self._generate_actions_section(recommendations)}
        
        <div class="footer">
            <p>Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")} by Sustainability Code Analyzer</p>
        </div>
    </div>
</body>
</html>
"""
    
    def _get_azure_css(self) -> str:
        """Azure DevOps compatible CSS styling"""
        return """
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f6f8fa;
            color: #24292e;
            line-height: 1.5;
        }
        
        .container {
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            border-radius: 6px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.12);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(90deg, #0078d4, #106ebe);
            color: white;
            padding: 25px 30px;
            border-bottom: 3px solid #005a9e;
        }
        
        .header h1 {
            margin: 0 0 10px 0;
            font-size: 24px;
            font-weight: 600;
        }
        
        .build-info {
            display: flex;
            gap: 20px;
            font-size: 14px;
            opacity: 0.9;
        }
        
        .build-info span {
            background: rgba(255,255,255,0.2);
            padding: 4px 12px;
            border-radius: 12px;
        }
        
        .section {
            padding: 25px 30px;
            border-bottom: 1px solid #e1e4e8;
        }
        
        .section h2 {
            margin: 0 0 20px 0;
            font-size: 18px;
            font-weight: 600;
            color: #0366d6;
        }
        
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        
        .metric-card {
            background: #f8f9fa;
            border: 1px solid #e1e4e8;
            border-radius: 6px;
            padding: 15px;
            text-align: center;
        }
        
        .metric-value {
            font-size: 28px;
            font-weight: bold;
            margin-bottom: 5px;
        }
        
        .metric-label {
            font-size: 12px;
            color: #586069;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .score-excellent { color: #28a745; }
        .score-good { color: #ffc107; }
        .score-poor { color: #dc3545; }
        
        .quality-gate {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 15px;
            border-radius: 6px;
            margin: 15px 0;
        }
        
        .quality-gate.passed {
            background: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
        }
        
        .quality-gate.failed {
            background: #f8d7da;
            border: 1px solid #f5c6cb;
            color: #721c24;
        }
        
        .quality-gate.warning {
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            color: #856404;
        }
        
        .findings-list {
            list-style: none;
            padding: 0;
        }
        
        .finding-item {
            background: #fff5f5;
            border: 1px solid #fed7d7;
            border-left: 4px solid #e53e3e;
            padding: 12px 15px;
            margin-bottom: 10px;
            border-radius: 4px;
        }
        
        .finding-item.warning {
            background: #fffbf0;
            border-color: #fbb6ce;
            border-left-color: #ed8936;
        }
        
        .recommendation-list {
            list-style: none;
            padding: 0;
        }
        
        .recommendation-item {
            background: #edf2f7;
            border: 1px solid #cbd5e0;
            border-left: 4px solid #4299e1;
            padding: 15px;
            margin-bottom: 15px;
            border-radius: 4px;
        }
        
        .recommendation-title {
            font-weight: 600;
            margin-bottom: 8px;
            color: #2d3748;
        }
        
        .priority-badge {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 10px;
            font-weight: 600;
            text-transform: uppercase;
            margin-left: 8px;
        }
        
        .priority-high { background: #fed7d7; color: #c53030; }
        .priority-medium { background: #feebc8; color: #dd6b20; }
        .priority-low { background: #c6f6d5; color: #2f855a; }
        
        .footer {
            padding: 15px 30px;
            background: #f6f8fa;
            font-size: 12px;
            color: #586069;
            text-align: center;
        }
        
        .summary-stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        
        .stat-item {
            text-align: center;
        }
        
        .stat-number {
            font-size: 24px;
            font-weight: bold;
            color: #0366d6;
        }
        
        .stat-label {
            font-size: 11px;
            color: #586069;
            text-transform: uppercase;
        }
        """
    
    def _generate_executive_summary_section(self, metrics: Dict, summary: Dict) -> str:
        """Generate executive summary section"""
        overall_score = metrics.get('overall_score', 0)
        file_count = summary.get('file_count', 0)
        execution_time = summary.get('execution_time', 0)
        
        score_class = self._get_score_class(overall_score)
        status = "PASSED" if overall_score >= 75 else "ATTENTION REQUIRED"
        
        return f"""
        <div class="section">
            <h2>📋 Executive Summary</h2>
            <div class="quality-gate {'passed' if overall_score >= 75 else 'warning'}">
                <strong>Overall Sustainability Score: {overall_score:.1f}/100 - {status}</strong>
            </div>
            
            <div class="summary-stats">
                <div class="stat-item">
                    <div class="stat-number">{file_count}</div>
                    <div class="stat-label">Files Analyzed</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{execution_time:.1f}s</div>
                    <div class="stat-label">Analysis Time</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number {score_class}">{overall_score:.1f}</div>
                    <div class="stat-label">Overall Score</div>
                </div>
            </div>
        </div>
        """
    
    def _generate_metrics_section(self, metrics: Dict) -> str:
        """Generate detailed metrics section"""
        return f"""
        <div class="section">
            <h2>Sustainability Metrics</h2>
            <div class="metrics-grid">
                <div class="metric-card">
                    <div class="metric-value {self._get_score_class(metrics.get('energy_efficiency', 0))}">
                        {metrics.get('energy_efficiency', 0):.1f}
                    </div>
                    <div class="metric-label">Energy Efficiency</div>
                </div>
                
                <div class="metric-card">
                    <div class="metric-value {self._get_score_class(metrics.get('resource_utilization', 0))}">
                        {metrics.get('resource_utilization', 0):.1f}
                    </div>
                    <div class="metric-label">Resource Utilization</div>
                </div>
                
                <div class="metric-card">
                    <div class="metric-value {self._get_score_class(100 - metrics.get('carbon_footprint', 0))}">
                        {metrics.get('carbon_footprint', 0):.1f}
                    </div>
                    <div class="metric-label">🌍 Carbon Footprint</div>
                </div>
                
                <div class="metric-card">
                    <div class="metric-value {self._get_score_class(metrics.get('performance_optimization', 0))}">
                        {metrics.get('performance_optimization', 0):.1f}
                    </div>
                    <div class="metric-label">Performance</div>
                </div>
                
                <div class="metric-card">
                    <div class="metric-value {self._get_score_class(metrics.get('sustainable_practices', 0))}">
                        {metrics.get('sustainable_practices', 0):.1f}
                    </div>
                    <div class="metric-label">♻️ Practices</div>
                </div>
            </div>
        </div>
        """
    
    def _generate_quality_gates_section(self, data: Dict) -> str:
        """Generate quality gates section"""
        metrics = data.get('sustainability_metrics', {})
        overall_score = metrics.get('overall_score', 0)
        
        gates = [
            ('Overall Score', overall_score, 75, '≥'),
            ('Energy Efficiency', metrics.get('energy_efficiency', 0), 70, '≥'),
            ('Carbon Footprint', metrics.get('carbon_footprint', 0), 40, '≤'),
        ]
        
        gate_html = []
        for name, value, threshold, operator in gates:
            if operator == '≥':
                passed = value >= threshold
            else:
                passed = value <= threshold
            
            gate_class = 'passed' if passed else 'failed'
            status_icon = '' if passed else ''
            
            gate_html.append(f"""
            <div class="quality-gate {gate_class}">
                {status_icon} <strong>{name}:</strong> {value:.1f} {operator} {threshold} (threshold)
            </div>
            """)
        
        return f"""
        <div class="section">
            <h2>Quality Gates</h2>
            {''.join(gate_html)}
        </div>
        """
    
    def _generate_detailed_findings_section(self, issues: List[Dict], recommendations: List[Dict]) -> str:
        """Generate detailed findings section"""
        issue_items = []
        for issue in issues[:5]:  # Top 5 issues
            severity_class = 'warning' if issue.get('severity') == 'medium' else 'error'
            issue_items.append(f"""
            <li class="finding-item {severity_class}">
                <strong>{issue.get('type', 'Issue')}</strong> in {issue.get('file', 'unknown')}
                <br>{issue.get('message', 'No details available')}
            </li>
            """)
        
        return f"""
        <div class="section">
            <h2>Key Findings</h2>
            <h3>Issues Identified ({len(issues)} total)</h3>
            <ul class="findings-list">
                {''.join(issue_items) if issue_items else '<li class="finding-item">No critical issues found</li>'}
            </ul>
        </div>
        """
    
    def _generate_actions_section(self, recommendations: List[Dict]) -> str:
        """Generate recommended actions section"""
        rec_items = []
        for rec in recommendations[:5]:  # Top 5 recommendations
            priority = rec.get('priority', 'medium')
            rec_items.append(f"""
            <li class="recommendation-item">
                <div class="recommendation-title">
                    {rec.get('title', 'Recommendation')}
                    <span class="priority-badge priority-{priority}">{priority}</span>
                </div>
                <p>{rec.get('description', 'No description available')}</p>
                <small>Impact: {rec.get('impact', 'Unknown')} | Effort: {rec.get('effort', 'Unknown')}</small>
            </li>
            """)
        
        return f"""
        <div class="section">
            <h2>Recommended Actions</h2>
            <ul class="recommendation-list">
                {''.join(rec_items) if rec_items else '<li class="recommendation-item">No specific recommendations at this time</li>'}
            </ul>
        </div>
        """
    
    def _generate_junit_xml(self, data: Dict) -> str:
        """Generate JUnit XML for Azure DevOps test integration"""
        metrics = data.get('sustainability_metrics', {})
        issues = data.get('issues', [])
        
        # Create test cases for each metric
        test_cases = []
        
        # Overall score test
        overall_score = metrics.get('overall_score', 0)
        if overall_score >= 75:
            test_cases.append('<testcase name="Overall Sustainability Score" classname="SustainabilityTests" time="0.1"/>')
        else:
            test_cases.append(f'''
            <testcase name="Overall Sustainability Score" classname="SustainabilityTests" time="0.1">
                <failure message="Sustainability score below threshold" type="QualityGate">
                    Overall score {overall_score:.1f} is below required threshold of 75
                </failure>
            </testcase>
            ''')
        
        # Energy efficiency test
        energy_score = metrics.get('energy_efficiency', 0)
        if energy_score >= 70:
            test_cases.append('<testcase name="Energy Efficiency" classname="SustainabilityTests" time="0.1"/>')
        else:
            test_cases.append(f'''
            <testcase name="Energy Efficiency" classname="SustainabilityTests" time="0.1">
                <failure message="Energy efficiency below threshold" type="QualityGate">
                    Energy efficiency score {energy_score:.1f} is below required threshold of 70
                </failure>
            </testcase>
            ''')
        
        return f'''<?xml version="1.0" encoding="UTF-8"?>
<testsuite name="SustainabilityTests" tests="{len(test_cases)}" failures="{len([tc for tc in test_cases if 'failure' in tc])}" time="0.5">
    {''.join(test_cases)}
</testsuite>'''
    
    def _generate_pipeline_summary(self, data: Dict) -> str:
        """Generate markdown summary for Azure DevOps pipeline"""
        metrics = data.get('sustainability_metrics', {})
        summary = data.get('analysis_summary', {})
        
        overall_score = metrics.get('overall_score', 0)
        status_emoji = "" if overall_score >= 75 else ""
        
        return f'''# 🌱 Sustainability Analysis Summary

## {status_emoji} Overall Score: {overall_score:.1f}/100

### 📊 Key Metrics:
- ⚡ **Energy Efficiency**: {metrics.get('energy_efficiency', 0):.1f}/100
- 💾 **Resource Utilization**: {metrics.get('resource_utilization', 0):.1f}/100
- 🌍 **Carbon Footprint**: {metrics.get('carbon_footprint', 0):.1f}/100 _(lower is better)_
- 🚀 **Performance**: {metrics.get('performance_optimization', 0):.1f}/100
- ♻️ **Practices**: {metrics.get('sustainable_practices', 0):.1f}/100

### 📁 Analysis Details:
- **Files Analyzed**: {summary.get('file_count', 0)}
- **Languages**: {', '.join(summary.get('language_breakdown', {}).keys())}
- **Analysis Time**: {summary.get('execution_time', 0):.2f}s

### 🎯 Quality Gate: {' PASSED' if overall_score >= 75 else ' FAILED'}

> 📈 [View Detailed Report]({{{{System.TeamFoundationCollectionUri}}}}{{{{System.TeamProject}}}}/_build/results?buildId={{{{Build.BuildId}}}}&view=artifacts)
'''
    
    def _generate_quality_gate_results(self, data: Dict) -> Dict[str, Any]:
        """Generate quality gate results for pipeline integration"""
        metrics = data.get('sustainability_metrics', {})
        
        return {
            'overall_passed': metrics.get('overall_score', 0) >= 75,
            'thresholds': {
                'overall_score': {
                    'value': metrics.get('overall_score', 0),
                    'threshold': 75,
                    'passed': metrics.get('overall_score', 0) >= 75
                },
                'energy_efficiency': {
                    'value': metrics.get('energy_efficiency', 0),
                    'threshold': 70,
                    'passed': metrics.get('energy_efficiency', 0) >= 70
                },
                'carbon_footprint': {
                    'value': metrics.get('carbon_footprint', 0),
                    'threshold': 40,
                    'passed': metrics.get('carbon_footprint', 0) <= 40
                }
            },
            'recommendations_count': len(data.get('recommendations', [])),
            'issues_count': len(data.get('issues', [])),
            'timestamp': datetime.now().isoformat()
        }
    
    def _get_score_class(self, score: float) -> str:
        """Get CSS class based on score"""
        if score >= 80:
            return 'score-excellent'
        elif score >= 60:
            return 'score-good'
        else:
            return 'score-poor'

def main():
    """Command line interface for Azure DevOps publisher"""
    parser = argparse.ArgumentParser(description='Azure DevOps Report Publisher')
    parser.add_argument('--input', required=True, help='Input analysis JSON file')
    parser.add_argument('--output', default='azure-reports', help='Output directory')
    
    args = parser.parse_args()
    
    # Load analysis data
    try:
        with open(args.input, 'r') as f:
            analysis_data = json.load(f)
    except Exception as e:
        print(f"Error loading analysis data: {e}")
        return 1
    
    # Create output directory
    os.makedirs(args.output, exist_ok=True)
    
    # Publish reports
    publisher = AzureDevOpsReportPublisher()
    outputs = publisher.publish_report(analysis_data, args.output)
    
    print(f" Azure DevOps reports published:")
    for report_type, path in outputs.items():
        print(f"  📄 {report_type}: {path}")
    
    return 0

if __name__ == "__main__":
    exit(main())