#!/usr/bin/env python3
"""
HTML Dashboard Generator for Sustainability Analysis
Generates interactive HTML reports with charts and recommendations
"""

import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

class SustainabilityDashboardGenerator:
 """Generate interactive HTML dashboard for sustainability analysis"""
 
 def __init__(self):
 self.timestamp = datetime.now().isoformat()
 
 def generate_dashboard(self, analysis_data: Dict[str, Any], 
 output_path: str, template: str = 'comprehensive') -> str:
 """Generate complete HTML dashboard"""
 
 if template == 'comprehensive':
 html_content = self._generate_comprehensive_dashboard(analysis_data)
 elif template == 'executive':
 html_content = self._generate_executive_dashboard(analysis_data)
 else:
 html_content = self._generate_basic_dashboard(analysis_data)
 
 # Write to file
 with open(output_path, 'w', encoding='utf-8') as f:
 f.write(html_content)
 
 print(f"Dashboard generated: {output_path}")
 return output_path
 
 def _generate_comprehensive_dashboard(self, data: Dict[str, Any]) -> str:
 """Generate comprehensive dashboard with all features"""
 
 metrics = data.get('sustainability_metrics', {})
 summary = data.get('analysis_summary', {})
 issues = data.get('issues', [])
 recommendations = data.get('recommendations', [])
 
 # Generate chart data
 metrics_chart_data = self._generate_metrics_chart_data(metrics)
 language_chart_data = self._generate_language_chart_data(summary.get('language_breakdown', {}))
 trend_chart_data = self._generate_trend_chart_data(data)
 
 html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
 <meta charset="UTF-8">
 <meta name="viewport" content="width=device-width, initial-scale=1.0">
 <title>Sustainability Analysis Dashboard</title>
 <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
 <script src="https://cdn.jsdelivr.net/npm/date-fns@2.28.0/index.min.js"></script>
 <style>
 {self._get_dashboard_css()}
 </style>
</head>
<body>
 <div class="container">
 {self._generate_header(metrics, summary)}
 
 <div class="dashboard-grid">
 {self._generate_metrics_cards(metrics)}
 </div>
 
 <div class="charts-section">
 <div class="chart-container">
 <h3>Sustainability Metrics Overview</h3>
 <canvas id="metricsChart" width="400" height="200"></canvas>
 </div>
 
 <div class="chart-container">
 <h3>💻 Language Breakdown</h3>
 <canvas id="languageChart" width="400" height="200"></canvas>
 </div>
 </div>
 
 {self._generate_recommendations_section(recommendations)}
 {self._generate_issues_section(issues)}
 {self._generate_footer()}
 </div>

 <script>
 {self._generate_chart_scripts(metrics_chart_data, language_chart_data)}
 </script>
</body>
</html>
"""
 return html_template
 
 def _get_dashboard_css(self) -> str:
 """Generate CSS for dashboard styling"""
 return """
 * {
 margin: 0;
 padding: 0;
 box-sizing: border-box;
 }
 
 body {
 font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
 background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
 min-height: 100vh;
 padding: 20px;
 }
 
 .container {
 max-width: 1200px;
 margin: 0 auto;
 background: white;
 border-radius: 15px;
 box-shadow: 0 10px 30px rgba(0,0,0,0.1);
 overflow: hidden;
 }
 
 .header {
 background: linear-gradient(135deg, #2d5016 0%, #3e7b00 100%);
 color: white;
 padding: 30px;
 text-align: center;
 }
 
 .header h1 {
 font-size: 2.5em;
 margin-bottom: 10px;
 font-weight: 300;
 }
 
 .header .subtitle {
 font-size: 1.2em;
 opacity: 0.9;
 }
 
 .overall-score {
 font-size: 3em;
 font-weight: bold;
 margin: 20px 0;
 text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
 }
 
 .dashboard-grid {
 display: grid;
 grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
 gap: 20px;
 padding: 30px;
 }
 
 .metric-card {
 background: white;
 border-radius: 10px;
 padding: 25px;
 box-shadow: 0 5px 15px rgba(0,0,0,0.08);
 border-left: 5px solid;
 transition: transform 0.3s ease;
 }
 
 .metric-card:hover {
 transform: translateY(-5px);
 }
 
 .metric-card.energy { border-left-color: #f39c12; }
 .metric-card.resource { border-left-color: #3498db; }
 .metric-card.carbon { border-left-color: #e74c3c; }
 .metric-card.performance { border-left-color: #2ecc71; }
 .metric-card.practices { border-left-color: #9b59b6; }
 
 .metric-title {
 font-size: 1.1em;
 color: #666;
 margin-bottom: 10px;
 }
 
 .metric-value {
 font-size: 2.5em;
 font-weight: bold;
 color: #333;
 }
 
 .metric-unit {
 font-size: 0.8em;
 color: #999;
 }
 
 .charts-section {
 display: grid;
 grid-template-columns: 1fr 1fr;
 gap: 30px;
 padding: 30px;
 background: #f8f9fa;
 }
 
 .chart-container {
 background: white;
 border-radius: 10px;
 padding: 25px;
 box-shadow: 0 5px 15px rgba(0,0,0,0.08);
 }
 
 .chart-container h3 {
 margin-bottom: 20px;
 color: #333;
 font-weight: 500;
 }
 
 .recommendations-section {
 padding: 30px;
 }
 
 .recommendations-grid {
 display: grid;
 grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
 gap: 20px;
 margin-top: 20px;
 }
 
 .recommendation-card {
 background: #fff3cd;
 border: 1px solid #ffeaa7;
 border-radius: 8px;
 padding: 20px;
 }
 
 .recommendation-card.high { 
 background: #f8d7da; 
 border-color: #f5c6cb; 
 }
 
 .recommendation-card.medium { 
 background: #fff3cd; 
 border-color: #ffeaa7; 
 }
 
 .recommendation-card.low { 
 background: #d1ecf1; 
 border-color: #bee5eb; 
 }
 
 .recommendation-title {
 font-weight: bold;
 margin-bottom: 10px;
 color: #333;
 }
 
 .priority-badge {
 display: inline-block;
 padding: 4px 8px;
 border-radius: 4px;
 font-size: 0.8em;
 font-weight: bold;
 text-transform: uppercase;
 }
 
 .priority-high { background: #dc3545; color: white; }
 .priority-medium { background: #ffc107; color: #333; }
 .priority-low { background: #17a2b8; color: white; }
 
 .issues-section {
 padding: 30px;
 background: #f8f9fa;
 }
 
 .issue-item {
 background: white;
 border-left: 4px solid #dc3545;
 padding: 15px;
 margin-bottom: 10px;
 border-radius: 5px;
 }
 
 .footer {
 background: #333;
 color: white;
 text-align: center;
 padding: 20px;
 font-size: 0.9em;
 }
 
 @media (max-width: 768px) {
 .charts-section {
 grid-template-columns: 1fr;
 }
 
 .dashboard-grid {
 grid-template-columns: 1fr;
 }
 }
 """
 
 def _generate_header(self, metrics: Dict, summary: Dict) -> str:
 """Generate dashboard header with overall score"""
 overall_score = metrics.get('overall_score', 0)
 file_count = summary.get('file_count', 0)
 execution_time = summary.get('execution_time', 0)
 
 score_color = self._get_score_color(overall_score)
 
 return f"""
 <div class="header">
 <h1>Sustainability Analysis Dashboard</h1>
 <div class="subtitle">Code Sustainability & Environmental Impact Assessment</div>
 <div class="overall-score" style="color: {score_color}">
 {overall_score:.1f}/100
 </div>
 <div class="subtitle">
 {file_count} files analyzed in {execution_time:.2f}s
 </div>
 </div>
 """
 
 def _generate_metrics_cards(self, metrics: Dict) -> str:
 """Generate metric cards for dashboard"""
 cards = []
 
 metric_configs = [
 ('energy_efficiency', 'Energy Efficiency', 'energy'),
 ('resource_utilization', 'Resource Utilization', 'resource'), 
 ('carbon_footprint', 'Carbon Footprint', 'carbon'),
 ('performance_optimization', 'Performance', 'performance'),
 ('sustainable_practices', 'Practices', 'practices')
 ]
 
 for metric_key, title, css_class in metric_configs:
 value = metrics.get(metric_key, 0)
 color = self._get_score_color(value, invert=(metric_key == 'carbon_footprint'))
 
 cards.append(f"""
 <div class="metric-card {css_class}">
 <div class="metric-title">{title}</div>
 <div class="metric-value" style="color: {color}">
 {value:.1f}
 <span class="metric-unit">/100</span>
 </div>
 </div>
 """)
 
 return ''.join(cards)
 
 def _generate_recommendations_section(self, recommendations: List[Dict]) -> str:
 """Generate recommendations section"""
 if not recommendations:
 return ""
 
 cards = []
 for rec in recommendations[:6]: # Limit to top 6
 priority = rec.get('priority', 'medium')
 
 cards.append(f"""
 <div class="recommendation-card {priority}">
 <div class="recommendation-title">
 {rec.get('title', 'Recommendation')}
 <span class="priority-badge priority-{priority}">{priority}</span>
 </div>
 <div class="recommendation-description">
 {rec.get('description', '')}
 </div>
 <div style="margin-top: 10px; font-size: 0.9em; color: #666;">
 Impact: {rec.get('impact', 'N/A')} | Effort: {rec.get('effort', 'N/A')}
 </div>
 </div>
 """)
 
 return f"""
 <div class="recommendations-section">
 <h2>Sustainability Recommendations</h2>
 <div class="recommendations-grid">
 {''.join(cards)}
 </div>
 </div>
 """
 
 def _generate_issues_section(self, issues: List[Dict]) -> str:
 """Generate issues section"""
 if not issues:
 return ""
 
 issue_items = []
 for issue in issues[:10]: # Limit to top 10
 issue_items.append(f"""
 <div class="issue-item">
 <strong>{issue.get('type', 'Issue')}</strong> in {issue.get('file', 'Unknown file')}
 <br>
 <span style="color: #666;">{issue.get('message', 'No message')}</span>
 </div>
 """)
 
 return f"""
 <div class="issues-section">
 <h2>Sustainability Issues ({len(issues)} found)</h2>
 {''.join(issue_items)}
 </div>
 """
 
 def _generate_footer(self) -> str:
 """Generate dashboard footer"""
 return f"""
 <div class="footer">
 Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")} | 
 Sustainability Code Evaluation Analyzer
 </div>
 """
 
 def _generate_metrics_chart_data(self, metrics: Dict) -> Dict:
 """Generate data for metrics radar chart"""
 return {
 'labels': ['Energy Efficiency', 'Resource Utilization', 'Carbon Footprint', 'Performance', 'Practices'],
 'datasets': [{
 'label': 'Sustainability Metrics',
 'data': [
 metrics.get('energy_efficiency', 0),
 metrics.get('resource_utilization', 0),
 100 - metrics.get('carbon_footprint', 0), # Invert carbon footprint
 metrics.get('performance_optimization', 0),
 metrics.get('sustainable_practices', 0)
 ],
 'backgroundColor': 'rgba(46, 204, 113, 0.2)',
 'borderColor': 'rgba(46, 204, 113, 1)',
 'pointBackgroundColor': 'rgba(46, 204, 113, 1)',
 'pointBorderColor': '#fff',
 'pointHoverBackgroundColor': '#fff',
 'pointHoverBorderColor': 'rgba(46, 204, 113, 1)'
 }]
 }
 
 def _generate_language_chart_data(self, language_breakdown: Dict) -> Dict:
 """Generate data for language distribution chart"""
 if not language_breakdown:
 return {'labels': [], 'datasets': []}
 
 colors = [
 '#FF6B35', '#F7931E', '#FFD23F', '#06FFA5', 
 '#118AB2', '#073B4C', '#9B5DE5', '#F15BB5'
 ]
 
 return {
 'labels': list(language_breakdown.keys()),
 'datasets': [{
 'data': list(language_breakdown.values()),
 'backgroundColor': colors[:len(language_breakdown)]
 }]
 }
 
 def _generate_chart_scripts(self, metrics_data: Dict, language_data: Dict) -> str:
 """Generate JavaScript for charts"""
 return f"""
 // Metrics Radar Chart
 const metricsCtx = document.getElementById('metricsChart').getContext('2d');
 new Chart(metricsCtx, {{
 type: 'radar',
 data: {json.dumps(metrics_data)},
 options: {{
 responsive: true,
 maintainAspectRatio: false,
 scales: {{
 r: {{
 beginAtZero: true,
 max: 100,
 ticks: {{
 stepSize: 20
 }}
 }}
 }},
 plugins: {{
 legend: {{
 display: false
 }}
 }}
 }}
 }});
 
 // Language Distribution Pie Chart 
 const languageCtx = document.getElementById('languageChart').getContext('2d');
 new Chart(languageCtx, {{
 type: 'doughnut',
 data: {json.dumps(language_data)},
 options: {{
 responsive: true,
 maintainAspectRatio: false,
 plugins: {{
 legend: {{
 position: 'bottom'
 }}
 }}
 }}
 }});
 """
 
 def _get_score_color(self, score: float, invert: bool = False) -> str:
 """Get color based on score (green=good, red=bad)"""
 if invert:
 score = 100 - score # For metrics where lower is better
 
 if score >= 80:
 return '#2ecc71' # Green
 elif score >= 60:
 return '#f39c12' # Orange 
 else:
 return '#e74c3c' # Red
 
 def _generate_trend_chart_data(self, data: Dict) -> Dict:
 """Generate trend data (placeholder for future historical analysis)"""
 return {
 'labels': ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
 'datasets': [{
 'label': 'Overall Score Trend',
 'data': [65, 72, 78, data.get('sustainability_metrics', {}).get('overall_score', 75)],
 'borderColor': 'rgba(46, 204, 113, 1)',
 'tension': 0.1
 }]
 }

def main():
 """Command line interface for dashboard generator"""
 parser = argparse.ArgumentParser(description='Generate Sustainability Dashboard')
 parser.add_argument('--input', required=True, help='Input analysis JSON file')
 parser.add_argument('--output', default='sustainability_dashboard.html', 
 help='Output HTML file')
 parser.add_argument('--template', choices=['basic', 'comprehensive', 'executive'],
 default='comprehensive', help='Dashboard template')
 
 args = parser.parse_args()
 
 # Load analysis data
 try:
 with open(args.input, 'r') as f:
 analysis_data = json.load(f)
 except Exception as e:
 print(f"Error loading analysis data: {e}")
 return 1
 
 # Generate dashboard
 generator = SustainabilityDashboardGenerator()
 output_path = generator.generate_dashboard(
 analysis_data, args.output, args.template
 )
 
 print(f"Dashboard generated successfully: {output_path}")
 return 0

if __name__ == "__main__":
 exit(main())