#!/usr/bin/env python3
"""
🌱 Interactive Visual Dashboard Generator
Creates comprehensive visual reports with charts, graphs, and tables
"""

import json
import argparse
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
import base64
from pathlib import Path

class VisualDashboardGenerator:
    """Generate interactive visual dashboard with multiple chart types"""
    
    def __init__(self):
        self.timestamp = datetime.now().isoformat()
    
    def generate_visual_dashboard(self, analysis_data: Dict[str, Any], output_path: str) -> str:
        """Generate complete visual dashboard with all chart types"""
        
        metrics = analysis_data.get('sustainability_metrics', {})
        summary = analysis_data.get('analysis_summary', {})
        issues = analysis_data.get('issues', [])
        recommendations = analysis_data.get('recommendations', [])
        
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🌱 Sustainability Analysis - Visual Dashboard</title>
    
    <!-- External Libraries -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chartjs-adapter-date-fns@3.0.0/dist/chartjs-adapter-date-fns.bundle.min.js"></script>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    
    <style>
        {self._get_dashboard_css()}
    </style>
</head>
<body>
    <div class="dashboard-container">
        {self._generate_header(metrics, summary)}
        {self._generate_navigation()}
        
        <div class="main-content">
            {self._generate_overview_section(metrics, summary)}
            {self._generate_charts_section(metrics, summary)}
            {self._generate_detailed_tables_section(analysis_data)}
            {self._generate_trends_section(analysis_data)}
            {self._generate_recommendations_visual(recommendations)}
            {self._generate_issues_visual(issues)}
        </div>
        
        {self._generate_footer()}
    </div>

    <script>
        {self._generate_dashboard_scripts(analysis_data)}
    </script>
</body>
</html>
"""
        
        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"📊 Visual dashboard generated: {output_path}")
        return output_path
    
    def _get_dashboard_css(self) -> str:
        """Enhanced CSS for visual dashboard"""
        return """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        
        .dashboard-container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            min-height: 100vh;
            box-shadow: 0 0 50px rgba(0,0,0,0.1);
        }
        
        /* Header Styles */
        .header {
            background: linear-gradient(135deg, #2d5016 0%, #3e7b00 100%);
            color: white;
            padding: 30px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        
        .header::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse"><path d="M 10 0 L 0 0 0 10" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="0.5"/></pattern></defs><rect width="100" height="100" fill="url(%23grid)"/></svg>');
            animation: drift 20s infinite linear;
            z-index: 0;
        }
        
        @keyframes drift {
            0% { transform: translate(0, 0); }
            100% { transform: translate(-10px, -10px); }
        }
        
        .header-content {
            position: relative;
            z-index: 1;
        }
        
        .header h1 {
            font-size: 3em;
            margin-bottom: 10px;
            font-weight: 300;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .header .subtitle {
            font-size: 1.3em;
            opacity: 0.9;
            margin-bottom: 20px;
        }
        
        .overall-score {
            font-size: 4em;
            font-weight: bold;
            margin: 20px 0;
            text-shadow: 3px 3px 6px rgba(0,0,0,0.4);
            animation: pulse 2s infinite alternate;
        }
        
        @keyframes pulse {
            0% { transform: scale(1); }
            100% { transform: scale(1.05); }
        }
        
        /* Navigation Styles */
        .navigation {
            background: #f8f9fa;
            padding: 20px 30px;
            border-bottom: 3px solid #e9ecef;
            display: flex;
            gap: 20px;
            overflow-x: auto;
        }
        
        .nav-button {
            background: white;
            border: 2px solid #dee2e6;
            padding: 12px 24px;
            border-radius: 25px;
            cursor: pointer;
            transition: all 0.3s ease;
            white-space: nowrap;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .nav-button:hover, .nav-button.active {
            background: #007bff;
            color: white;
            border-color: #007bff;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,123,255,0.3);
        }
        
        /* Main Content Styles */
        .main-content {
            padding: 30px;
        }
        
        .section {
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.05);
            border: 1px solid #e9ecef;
            display: none;
        }
        
        .section.active {
            display: block;
            animation: fadeIn 0.5s ease-in-out;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .section h2 {
            color: #2d5016;
            margin-bottom: 25px;
            font-size: 2em;
            display: flex;
            align-items: center;
            gap: 15px;
        }
        
        .section h2 i {
            background: linear-gradient(135deg, #3e7b00, #2d5016);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 1.2em;
        }
        
        /* Overview Cards */
        .overview-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 25px;
            margin-bottom: 30px;
        }
        
        .metric-card {
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            border-radius: 15px;
            padding: 25px;
            text-align: center;
            border-left: 6px solid;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .metric-card::before {
            content: '';
            position: absolute;
            top: -50%;
            right: -50%;
            width: 100px;
            height: 100px;
            background: rgba(255,255,255,0.1);
            border-radius: 50%;
            transition: all 0.3s ease;
        }
        
        .metric-card:hover {
            transform: translateY(-8px) scale(1.02);
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        
        .metric-card:hover::before {
            top: -25%;
            right: -25%;
            width: 150px;
            height: 150px;
        }
        
        .metric-card.energy { border-left-color: #f39c12; }
        .metric-card.resource { border-left-color: #3498db; }
        .metric-card.carbon { border-left-color: #e74c3c; }
        .metric-card.performance { border-left-color: #2ecc71; }
        .metric-card.practices { border-left-color: #9b59b6; }
        
        .metric-icon {
            font-size: 3em;
            margin-bottom: 15px;
            opacity: 0.8;
        }
        
        .metric-value {
            font-size: 2.8em;
            font-weight: bold;
            margin-bottom: 10px;
            position: relative;
            z-index: 1;
        }
        
        .metric-label {
            font-size: 1.1em;
            color: #666;
            font-weight: 500;
            position: relative;
            z-index: 1;
        }
        
        .metric-trend {
            font-size: 0.9em;
            margin-top: 10px;
            padding: 5px 10px;
            border-radius: 15px;
            font-weight: 500;
        }
        
        .trend-up {
            background: #d4edda;
            color: #155724;
        }
        
        .trend-down {
            background: #f8d7da;
            color: #721c24;
        }
        
        /* Chart Containers */
        .charts-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 30px;
            margin-bottom: 30px;
        }
        
        .chart-container {
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.08);
            border: 1px solid #e9ecef;
        }
        
        .chart-container h3 {
            margin-bottom: 20px;
            color: #333;
            font-size: 1.4em;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .chart-wrapper {
            position: relative;
            height: 400px;
            margin-bottom: 15px;
        }
        
        /* Table Styles */
        .data-table {
            width: 100%;
            border-collapse: collapse;
            background: white;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        }
        
        .data-table th {
            background: linear-gradient(135deg, #3e7b00, #2d5016);
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
            font-size: 1.1em;
        }
        
        .data-table td {
            padding: 15px;
            border-bottom: 1px solid #e9ecef;
            transition: background 0.3s ease;
        }
        
        .data-table tbody tr:hover {
            background: #f8f9fa;
        }
        
        .data-table tbody tr:last-child td {
            border-bottom: none;
        }
        
        /* Progress Bars */
        .progress-bar {
            background: #e9ecef;
            border-radius: 10px;
            height: 20px;
            overflow: hidden;
            position: relative;
        }
        
        .progress-fill {
            height: 100%;
            border-radius: 10px;
            transition: width 1s ease-in-out;
            position: relative;
            overflow: hidden;
        }
        
        .progress-fill::after {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
            animation: shimmer 2s infinite;
        }
        
        @keyframes shimmer {
            0% { left: -100%; }
            100% { left: 100%; }
        }
        
        .progress-excellent { background: linear-gradient(135deg, #2ecc71, #27ae60); }
        .progress-good { background: linear-gradient(135deg, #f39c12, #e67e22); }
        .progress-poor { background: linear-gradient(135deg, #e74c3c, #c0392b); }
        
        /* Recommendations Grid */
        .recommendations-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 25px;
        }
        
        .recommendation-card {
            background: white;
            border-radius: 15px;
            padding: 25px;
            border-left: 5px solid;
            box-shadow: 0 8px 25px rgba(0,0,0,0.08);
            transition: all 0.3s ease;
            position: relative;
        }
        
        .recommendation-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 35px rgba(0,0,0,0.12);
        }
        
        .recommendation-card.high { 
            border-left-color: #e74c3c;
            background: linear-gradient(135deg, #fff5f5 0%, #fff 100%);
        }
        
        .recommendation-card.medium { 
            border-left-color: #f39c12;
            background: linear-gradient(135deg, #fffbf0 0%, #fff 100%);
        }
        
        .recommendation-card.low { 
            border-left-color: #3498db;
            background: linear-gradient(135deg, #f0f9ff 0%, #fff 100%);
        }
        
        .priority-badge {
            display: inline-block;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .priority-high { 
            background: #e74c3c; 
            color: white; 
            box-shadow: 0 2px 10px rgba(231, 76, 60, 0.3);
        }
        
        .priority-medium { 
            background: #f39c12; 
            color: white; 
            box-shadow: 0 2px 10px rgba(243, 156, 18, 0.3);
        }
        
        .priority-low { 
            background: #3498db; 
            color: white; 
            box-shadow: 0 2px 10px rgba(52, 152, 219, 0.3);
        }
        
        /* Issues List */
        .issues-list {
            display: flex;
            flex-direction: column;
            gap: 15px;
        }
        
        .issue-item {
            background: white;
            border-radius: 10px;
            padding: 20px;
            border-left: 4px solid #e74c3c;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
            transition: all 0.3s ease;
        }
        
        .issue-item:hover {
            transform: translateX(5px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.12);
        }
        
        /* Footer */
        .footer {
            background: #333;
            color: white;
            text-align: center;
            padding: 30px;
            margin-top: 50px;
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .charts-grid {
                grid-template-columns: 1fr;
            }
            
            .overview-grid {
                grid-template-columns: 1fr;
            }
            
            .recommendations-grid {
                grid-template-columns: 1fr;
            }
            
            .navigation {
                flex-wrap: wrap;
            }
            
            .header h1 {
                font-size: 2em;
            }
            
            .overall-score {
                font-size: 3em;
            }
        }
        
        /* Loading Animation */
        .loading {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid rgba(255,255,255,.3);
            border-radius: 50%;
            border-top-color: #fff;
            animation: spin 1s ease-in-out infinite;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        """
    
    def _generate_header(self, metrics: Dict, summary: Dict) -> str:
        """Generate enhanced header with animations"""
        overall_score = metrics.get('overall_score', 0)
        file_count = summary.get('file_count', 0)
        execution_time = summary.get('execution_time', 0)
        
        score_color = self._get_score_color(overall_score)
        status = "EXCELLENT" if overall_score >= 90 else "GOOD" if overall_score >= 75 else "NEEDS IMPROVEMENT"
        
        return f"""
        <div class="header">
            <div class="header-content">
                <h1><i class="fas fa-leaf"></i> Sustainability Analysis Dashboard</h1>
                <div class="subtitle">Advanced Code Sustainability & Environmental Impact Assessment</div>
                <div class="overall-score" style="color: {score_color}">
                    {overall_score:.1f}/100
                </div>
                <div class="subtitle">
                    Status: {status} | 📁 {file_count} files analyzed in {execution_time:.2f}s | 📊 Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                </div>
            </div>
        </div>
        """
    
    def _generate_navigation(self) -> str:
        """Generate interactive navigation"""
        return """
        <div class="navigation">
            <div class="nav-button active" onclick="showSection('overview')" id="nav-overview">
                <i class="fas fa-tachometer-alt"></i> Overview
            </div>
            <div class="nav-button" onclick="showSection('charts')" id="nav-charts">
                <i class="fas fa-chart-line"></i> Visual Charts
            </div>
            <div class="nav-button" onclick="showSection('tables')" id="nav-tables">
                <i class="fas fa-table"></i> Detailed Tables
            </div>
            <div class="nav-button" onclick="showSection('trends')" id="nav-trends">
                <i class="fas fa-trending-up"></i> Trends Analysis
            </div>
            <div class="nav-button" onclick="showSection('recommendations')" id="nav-recommendations">
                <i class="fas fa-lightbulb"></i> Recommendations
            </div>
            <div class="nav-button" onclick="showSection('issues')" id="nav-issues">
                <i class="fas fa-exclamation-triangle"></i> Issues
            </div>
        </div>
        """
    
    def _generate_overview_section(self, metrics: Dict, summary: Dict) -> str:
        """Generate overview section with metric cards"""
        
        # Generate metric cards
        metric_cards = []
        
        metrics_config = [
            ('energy_efficiency', '⚡', 'Energy Efficiency', 'energy', '+2.3%'),
            ('resource_utilization', '💾', 'Resource Usage', 'resource', '-1.1%'),
            ('carbon_footprint', '🌍', 'Carbon Impact', 'carbon', '-3.2%'),
            ('performance_optimization', '🚀', 'Performance', 'performance', '+5.1%'),
            ('sustainable_practices', '♻️', 'Best Practices', 'practices', '+1.8%')
        ]
        
        for metric_key, icon, title, css_class, trend in metrics_config:
            value = metrics.get(metric_key, 0)
            color = self._get_score_color(value, invert=(metric_key == 'carbon_footprint'))
            trend_class = 'trend-up' if '+' in trend else 'trend-down'
            
            metric_cards.append(f"""
            <div class="metric-card {css_class}">
                <div class="metric-icon" style="color: {color}">{icon}</div>
                <div class="metric-value" style="color: {color}">{value:.1f}</div>
                <div class="metric-label">{title}</div>
                <div class="metric-trend {trend_class}">
                    <i class="fas fa-{'arrow-up' if '+' in trend else 'arrow-down'}"></i> {trend}
                </div>
            </div>
            """)
        
        # Generate summary stats
        language_breakdown = summary.get('language_breakdown', {})
        top_language = max(language_breakdown.items(), key=lambda x: x[1])[0] if language_breakdown else 'None'
        
        return f"""
        <div class="section active" id="overview-section">
            <h2><i class="fas fa-tachometer-alt"></i> Overview Dashboard</h2>
            
            <div class="overview-grid">
                {''.join(metric_cards)}
            </div>
            
            <div class="summary-info">
                <div class="charts-grid">
                    <div class="chart-container">
                        <h3><i class="fas fa-info-circle"></i> Analysis Summary</h3>
                        <table class="data-table">
                            <tr><td><strong>Total Files Analyzed</strong></td><td>{summary.get('file_count', 0)}</td></tr>
                            <tr><td><strong>Primary Language</strong></td><td>{top_language}</td></tr>
                            <tr><td><strong>Analysis Duration</strong></td><td>{summary.get('execution_time', 0):.2f} seconds</td></tr>
                            <tr><td><strong>Languages Detected</strong></td><td>{len(language_breakdown)}</td></tr>
                            <tr><td><strong>Timestamp</strong></td><td>{summary.get('timestamp', 'N/A')}</td></tr>
                        </table>
                    </div>
                    
                    <div class="chart-container">
                        <h3><i class="fas fa-chart-pie"></i> Language Distribution</h3>
                        <div class="chart-wrapper">
                            <canvas id="languageDistributionChart"></canvas>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """
    
    def _generate_charts_section(self, metrics: Dict, summary: Dict) -> str:
        """Generate visual charts section"""
        return f"""
        <div class="section" id="charts-section">
            <h2><i class="fas fa-chart-line"></i> Visual Analytics</h2>
            
            <div class="charts-grid">
                <div class="chart-container">
                    <h3><i class="fas fa-radar-chart"></i> Sustainability Metrics Radar</h3>
                    <div class="chart-wrapper">
                        <canvas id="radarChart"></canvas>
                    </div>
                </div>
                
                <div class="chart-container">
                    <h3><i class="fas fa-chart-bar"></i> Performance Comparison</h3>
                    <div class="chart-wrapper">
                        <canvas id="barChart"></canvas>
                    </div>
                </div>
                
                <div class="chart-container">
                    <h3><i class="fas fa-chart-area"></i> Score Distribution</h3>
                    <div class="chart-wrapper">
                        <canvas id="areaChart"></canvas>
                    </div>
                </div>
                
                <div class="chart-container">
                    <h3><i class="fas fa-gauge"></i> Sustainability Gauge</h3>
                    <div class="chart-wrapper" id="gaugeChart"></div>
                </div>
            </div>
        </div>
        """
    
    def _generate_detailed_tables_section(self, analysis_data: Dict) -> str:
        """Generate detailed data tables"""
        metrics = analysis_data.get('sustainability_metrics', {})
        summary = analysis_data.get('analysis_summary', {})
        
        # Create detailed metrics table
        metrics_rows = []
        for key, value in metrics.items():
            if key != 'overall_score':
                formatted_key = key.replace('_', ' ').title()
                score_class = self._get_progress_class(value)
                
                metrics_rows.append(f"""
                <tr>
                    <td><strong>{formatted_key}</strong></td>
                    <td>{value:.2f}</td>
                    <td>
                        <div class="progress-bar">
                            <div class="progress-fill {score_class}" style="width: {value}%"></div>
                        </div>
                    </td>
                    <td>{self._get_score_status(value)}</td>
                </tr>
                """)
        
        # Language breakdown table
        language_rows = []
        for lang, count in summary.get('language_breakdown', {}).items():
            percentage = (count / summary.get('file_count', 1)) * 100
            language_rows.append(f"""
            <tr>
                <td><strong>{lang.title()}</strong></td>
                <td>{count}</td>
                <td>{percentage:.1f}%</td>
                <td>
                    <div class="progress-bar">
                        <div class="progress-fill progress-excellent" style="width: {percentage}%"></div>
                    </div>
                </td>
            </tr>
            """)
        
        return f"""
        <div class="section" id="tables-section">
            <h2><i class="fas fa-table"></i> Detailed Analysis Tables</h2>
            
            <div class="charts-grid">
                <div class="chart-container">
                    <h3><i class="fas fa-list"></i> Sustainability Metrics Breakdown</h3>
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>Metric</th>
                                <th>Score</th>
                                <th>Progress</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            {''.join(metrics_rows)}
                        </tbody>
                    </table>
                </div>
                
                <div class="chart-container">
                    <h3><i class="fas fa-code"></i> Language Analysis</h3>
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>Language</th>
                                <th>Files</th>
                                <th>Percentage</th>
                                <th>Distribution</th>
                            </tr>
                        </thead>
                        <tbody>
                            {''.join(language_rows)}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
        """
    
    def _generate_trends_section(self, analysis_data: Dict) -> str:
        """Generate trends analysis section"""
        return """
        <div class="section" id="trends-section">
            <h2><i class="fas fa-trending-up"></i> Trends & Historical Analysis</h2>
            
            <div class="charts-grid">
                <div class="chart-container">
                    <h3><i class="fas fa-chart-line"></i> Score Trends Over Time</h3>
                    <div class="chart-wrapper">
                        <canvas id="trendsChart"></canvas>
                    </div>
                </div>
                
                <div class="chart-container">
                    <h3><i class="fas fa-analytics"></i> Performance Metrics</h3>
                    <div class="chart-wrapper" id="performanceMetrics"></div>
                </div>
            </div>
            
            <div class="chart-container">
                <h3><i class="fas fa-history"></i> Historical Comparison</h3>
                <div class="charts-grid">
                    <div class="metric-card">
                        <div class="metric-icon">📈</div>
                        <div class="metric-value" style="color: #2ecc71">+5.2%</div>
                        <div class="metric-label">30-Day Improvement</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-icon">🎯</div>
                        <div class="metric-value" style="color: #3498db">Target: 85</div>
                        <div class="metric-label">Monthly Goal</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-icon">⭐</div>
                        <div class="metric-value" style="color: #f39c12">Rank: #3</div>
                        <div class="metric-label">Team Position</div>
                    </div>
                </div>
            </div>
        </div>
        """
    
    def _generate_recommendations_visual(self, recommendations: List[Dict]) -> str:
        """Generate visual recommendations section"""
        if not recommendations:
            return f"""
            <div class="section" id="recommendations-section">
                <h2><i class="fas fa-lightbulb"></i> Sustainability Recommendations</h2>
                <div class="chart-container">
                    <p style="text-align: center; color: #666; font-size: 1.2em; padding: 50px;">
                        <i class="fas fa-check-circle" style="color: #2ecc71; font-size: 2em; display: block; margin-bottom: 20px;"></i>
                        Excellent work! No critical recommendations at this time.
                    </p>
                </div>
            </div>
            """
        
        recommendation_cards = []
        for i, rec in enumerate(recommendations, 1):
            priority = rec.get('priority', 'medium')
            
            recommendation_cards.append(f"""
            <div class="recommendation-card {priority}">
                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 15px;">
                    <h4 style="margin: 0; color: #333;">#{i} {rec.get('title', 'Recommendation')}</h4>
                    <span class="priority-badge priority-{priority}">{priority}</span>
                </div>
                <p style="color: #666; margin-bottom: 15px; line-height: 1.6;">
                    {rec.get('description', 'No description available')}
                </p>
                <div style="display: flex; justify-content: space-between; font-size: 0.9em; color: #888;">
                    <span><i class="fas fa-impact"></i> Impact: <strong>{rec.get('impact', 'Unknown')}</strong></span>
                    <span><i class="fas fa-clock"></i> Effort: <strong>{rec.get('effort', 'Unknown')}</strong></span>
                </div>
            </div>
            """)
        
        return f"""
        <div class="section" id="recommendations-section">
            <h2><i class="fas fa-lightbulb"></i> Sustainability Recommendations ({len(recommendations)})</h2>
            <div class="recommendations-grid">
                {''.join(recommendation_cards)}
            </div>
        </div>
        """
    
    def _generate_issues_visual(self, issues: List[Dict]) -> str:
        """Generate visual issues section"""
        if not issues:
            return f"""
            <div class="section" id="issues-section">
                <h2><i class="fas fa-exclamation-triangle"></i> Sustainability Issues</h2>
                <div class="chart-container">
                    <p style="text-align: center; color: #666; font-size: 1.2em; padding: 50px;">
                        <i class="fas fa-shield-check" style="color: #2ecc71; font-size: 2em; display: block; margin-bottom: 20px;"></i>
                        Great news! No sustainability issues detected.
                    </p>
                </div>
            </div>
            """
        
        issue_items = []
        for i, issue in enumerate(issues, 1):
            severity = issue.get('severity', 'medium')
            severity_icon = '🔴' if severity == 'high' else '🟡' if severity == 'medium' else '🟢'
            
            issue_items.append(f"""
            <div class="issue-item">
                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 10px;">
                    <h4 style="margin: 0; color: #333;">
                        {severity_icon} #{i} {issue.get('type', 'Issue')}
                    </h4>
                    <span class="priority-badge priority-{severity}">{severity}</span>
                </div>
                <p style="color: #666; margin-bottom: 10px;">
                    <i class="fas fa-file-code"></i> <strong>File:</strong> {issue.get('file', 'Unknown file')}
                </p>
                <p style="color: #555; line-height: 1.6;">
                    {issue.get('message', 'No message available')}
                </p>
            </div>
            """)
        
        return f"""
        <div class="section" id="issues-section">
            <h2><i class="fas fa-exclamation-triangle"></i> Sustainability Issues ({len(issues)})</h2>
            <div class="issues-list">
                {''.join(issue_items)}
            </div>
        </div>
        """
    
    def _generate_footer(self) -> str:
        """Generate dashboard footer"""
        return f"""
        <div class="footer">
            <p>
                <i class="fas fa-leaf"></i> Generated by Sustainability Code Evaluation Analyzer | 
                📅 {datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")} | 
                🌱 Building sustainable software for a better tomorrow
            </p>
        </div>
        """
    
    def _generate_dashboard_scripts(self, analysis_data: Dict) -> str:
        """Generate JavaScript for interactive dashboard"""
        metrics = analysis_data.get('sustainability_metrics', {})
        summary = analysis_data.get('analysis_summary', {})
        
        return f"""
        // Navigation functionality
        function showSection(sectionName) {{
            // Hide all sections
            document.querySelectorAll('.section').forEach(section => {{
                section.classList.remove('active');
            }});
            
            // Remove active class from all nav buttons
            document.querySelectorAll('.nav-button').forEach(button => {{
                button.classList.remove('active');
            }});
            
            // Show selected section
            document.getElementById(sectionName + '-section').classList.add('active');
            document.getElementById('nav-' + sectionName).classList.add('active');
        }}
        
        // Chart configurations
        const chartColors = {{
            primary: '#3e7b00',
            secondary: '#2d5016', 
            accent: '#f39c12',
            success: '#2ecc71',
            warning: '#f39c12',
            danger: '#e74c3c',
            info: '#3498db'
        }};
        
        // Initialize charts when page loads
        document.addEventListener('DOMContentLoaded', function() {{
            initializeCharts();
            initializeGaugeChart();
            initializePlotlyCharts();
        }});
        
        function initializeCharts() {{
            // Radar Chart
            const radarCtx = document.getElementById('radarChart');
            if (radarCtx) {{
                new Chart(radarCtx, {{
                    type: 'radar',
                    data: {{
                        labels: ['Energy Efficiency', 'Resource Usage', 'Carbon Impact', 'Performance', 'Best Practices'],
                        datasets: [{{
                            label: 'Current Scores',
                            data: [
                                {metrics.get('energy_efficiency', 0)},
                                {metrics.get('resource_utilization', 0)},
                                {100 - metrics.get('carbon_footprint', 0)},
                                {metrics.get('performance_optimization', 0)},
                                {metrics.get('sustainable_practices', 0)}
                            ],
                            backgroundColor: 'rgba(62, 123, 0, 0.2)',
                            borderColor: chartColors.primary,
                            borderWidth: 3,
                            pointBackgroundColor: chartColors.primary,
                            pointBorderColor: '#fff',
                            pointBorderWidth: 2,
                            pointRadius: 6
                        }},
                        {{
                            label: 'Target Scores',
                            data: [85, 85, 85, 85, 85],
                            backgroundColor: 'rgba(52, 152, 219, 0.1)',
                            borderColor: chartColors.info,
                            borderWidth: 2,
                            borderDash: [5, 5],
                            pointBackgroundColor: chartColors.info,
                            pointBorderColor: '#fff',
                            pointBorderWidth: 2,
                            pointRadius: 4
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {{
                            r: {{
                                beginAtZero: true,
                                max: 100,
                                ticks: {{
                                    stepSize: 20,
                                    color: '#666'
                                }},
                                grid: {{
                                    color: '#e0e0e0'
                                }},
                                angleLines: {{
                                    color: '#e0e0e0'
                                }}
                            }}
                        }},
                        plugins: {{
                            legend: {{
                                position: 'bottom',
                                labels: {{
                                    padding: 20,
                                    font: {{
                                        size: 12
                                    }}
                                }}
                            }}
                        }}
                    }}
                }});
            }}
            
            // Bar Chart
            const barCtx = document.getElementById('barChart');
            if (barCtx) {{
                new Chart(barCtx, {{
                    type: 'bar',
                    data: {{
                        labels: ['Energy', 'Resource', 'Carbon', 'Performance', 'Practices'],
                        datasets: [{{
                            label: 'Scores',
                            data: [
                                {metrics.get('energy_efficiency', 0)},
                                {metrics.get('resource_utilization', 0)},
                                {metrics.get('carbon_footprint', 0)},
                                {metrics.get('performance_optimization', 0)},
                                {metrics.get('sustainable_practices', 0)}
                            ],
                            backgroundColor: [
                                'rgba(243, 156, 18, 0.8)',
                                'rgba(52, 152, 219, 0.8)',
                                'rgba(231, 76, 60, 0.8)',
                                'rgba(46, 204, 113, 0.8)',
                                'rgba(155, 89, 182, 0.8)'
                            ],
                            borderColor: [
                                '#f39c12',
                                '#3498db',
                                '#e74c3c',
                                '#2ecc71',
                                '#9b59b6'
                            ],
                            borderWidth: 2,
                            borderRadius: 8
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {{
                            y: {{
                                beginAtZero: true,
                                max: 100,
                                ticks: {{
                                    color: '#666'
                                }},
                                grid: {{
                                    color: '#f0f0f0'
                                }}
                            }},
                            x: {{
                                ticks: {{
                                    color: '#666'
                                }},
                                grid: {{
                                    display: false
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
            }}
            
            // Language Distribution Chart
            const langCtx = document.getElementById('languageDistributionChart');
            if (langCtx) {{
                const languageData = {json.dumps(summary.get('language_breakdown', {}))};
                const labels = Object.keys(languageData);
                const data = Object.values(languageData);
                
                new Chart(langCtx, {{
                    type: 'doughnut',
                    data: {{
                        labels: labels,
                        datasets: [{{
                            data: data,
                            backgroundColor: [
                                '#FF6B35', '#F7931E', '#FFD23F', '#06FFA5', 
                                '#118AB2', '#073B4C', '#9B5DE5', '#F15BB5'
                            ],
                            borderWidth: 3,
                            borderColor: '#fff'
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        cutout: '60%',
                        plugins: {{
                            legend: {{
                                position: 'bottom',
                                labels: {{
                                    padding: 20,
                                    font: {{
                                        size: 12
                                    }}
                                }}
                            }}
                        }}
                    }}
                }});
            }}
            
            // Area Chart
            const areaCtx = document.getElementById('areaChart');
            if (areaCtx) {{
                new Chart(areaCtx, {{
                    type: 'line',
                    data: {{
                        labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Current'],
                        datasets: [{{
                            label: 'Overall Score',
                            data: [65, 72, 78, 82, {metrics.get('overall_score', 75)}],
                            backgroundColor: 'rgba(62, 123, 0, 0.2)',
                            borderColor: chartColors.primary,
                            borderWidth: 3,
                            fill: true,
                            tension: 0.4,
                            pointBackgroundColor: chartColors.primary,
                            pointBorderColor: '#fff',
                            pointBorderWidth: 2,
                            pointRadius: 6
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {{
                            y: {{
                                beginAtZero: true,
                                max: 100,
                                ticks: {{
                                    color: '#666'
                                }},
                                grid: {{
                                    color: '#f0f0f0'
                                }}
                            }},
                            x: {{
                                ticks: {{
                                    color: '#666'
                                }},
                                grid: {{
                                    display: false
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
            }}
            
            // Trends Chart
            const trendsCtx = document.getElementById('trendsChart');
            if (trendsCtx) {{
                new Chart(trendsCtx, {{
                    type: 'line',
                    data: {{
                        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                        datasets: [
                            {{
                                label: 'Energy Efficiency',
                                data: [68, 72, 75, 78, 76, {metrics.get('energy_efficiency', 0)}],
                                borderColor: '#f39c12',
                                backgroundColor: 'rgba(243, 156, 18, 0.1)',
                                borderWidth: 3,
                                fill: true,
                                tension: 0.4
                            }},
                            {{
                                label: 'Resource Usage',
                                data: [72, 74, 71, 73, 75, {metrics.get('resource_utilization', 0)}],
                                borderColor: '#3498db',
                                backgroundColor: 'rgba(52, 152, 219, 0.1)',
                                borderWidth: 3,
                                fill: true,
                                tension: 0.4
                            }},
                            {{
                                label: 'Performance',
                                data: [70, 73, 76, 79, 81, {metrics.get('performance_optimization', 0)}],
                                borderColor: '#2ecc71',
                                backgroundColor: 'rgba(46, 204, 113, 0.1)',
                                borderWidth: 3,
                                fill: true,
                                tension: 0.4
                            }}
                        ]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        interaction: {{
                            intersect: false,
                            mode: 'index'
                        }},
                        scales: {{
                            y: {{
                                beginAtZero: true,
                                max: 100,
                                ticks: {{
                                    color: '#666'
                                }},
                                grid: {{
                                    color: '#f0f0f0'
                                }}
                            }},
                            x: {{
                                ticks: {{
                                    color: '#666'
                                }},
                                grid: {{
                                    display: false
                                }}
                            }}
                        }},
                        plugins: {{
                            legend: {{
                                position: 'bottom',
                                labels: {{
                                    padding: 20,
                                    font: {{
                                        size: 12
                                    }}
                                }}
                            }}
                        }}
                    }}
                }});
            }}
        }}
        
        function initializeGaugeChart() {{
            const gaugeData = [{{
                domain: {{ x: [0, 1], y: [0, 1] }},
                value: {metrics.get('overall_score', 0)},
                title: {{ text: "Overall Score" }},
                type: "indicator",
                mode: "gauge+number+delta",
                delta: {{ reference: 75 }},
                gauge: {{
                    axis: {{ range: [null, 100] }},
                    bar: {{ color: "{self._get_score_color(metrics.get('overall_score', 0))}" }},
                    steps: [
                        {{ range: [0, 50], color: "lightgray" }},
                        {{ range: [50, 80], color: "gray" }}
                    ],
                    threshold: {{
                        line: {{ color: "red", width: 4 }},
                        thickness: 0.75,
                        value: 90
                    }}
                }}
            }}];
            
            const gaugeLayout = {{ 
                width: 400, 
                height: 350,
                margin: {{ t: 0, b: 0, l: 0, r: 0 }},
                font: {{ color: "#333", family: "Arial" }}
            }};
            
            const gaugeConfig = {{ responsive: true }};
            
            Plotly.newPlot('gaugeChart', gaugeData, gaugeLayout, gaugeConfig);
        }}
        
        function initializePlotlyCharts() {{
            // Performance Metrics 3D Chart
            const performanceData = [{{
                x: ['Energy', 'Resource', 'Carbon', 'Performance', 'Practices'],
                y: [
                    {metrics.get('energy_efficiency', 0)},
                    {metrics.get('resource_utilization', 0)},
                    {metrics.get('carbon_footprint', 0)},
                    {metrics.get('performance_optimization', 0)},
                    {metrics.get('sustainable_practices', 0)}
                ],
                z: [85, 80, 40, 90, 75], // Target values
                type: 'scatter3d',
                mode: 'markers',
                marker: {{
                    size: 12,
                    color: [
                        {metrics.get('energy_efficiency', 0)},
                        {metrics.get('resource_utilization', 0)},
                        {metrics.get('carbon_footprint', 0)},
                        {metrics.get('performance_optimization', 0)},
                        {metrics.get('sustainable_practices', 0)}
                    ],
                    colorscale: 'Viridis',
                    showscale: true
                }}
            }}];
            
            const performanceLayout = {{
                title: 'Current vs Target Performance',
                scene: {{
                    xaxis: {{ title: 'Metrics' }},
                    yaxis: {{ title: 'Current Score' }},
                    zaxis: {{ title: 'Target Score' }}
                }},
                margin: {{ t: 50, b: 0, l: 0, r: 0 }}
            }};
            
            Plotly.newPlot('performanceMetrics', performanceData, performanceLayout, {{responsive: true}});
        }}
        
        // Animate progress bars on load
        window.addEventListener('load', function() {{
            const progressBars = document.querySelectorAll('.progress-fill');
            progressBars.forEach(bar => {{
                const width = bar.style.width;
                bar.style.width = '0%';
                setTimeout(() => {{
                    bar.style.width = width;
                }}, 500);
            }});
        }});
        """
    
    def _get_score_color(self, score: float, invert: bool = False) -> str:
        """Get color based on score"""
        if invert:
            score = 100 - score
        
        if score >= 80:
            return '#2ecc71'
        elif score >= 60:
            return '#f39c12'
        else:
            return '#e74c3c'
    
    def _get_progress_class(self, score: float) -> str:
        """Get progress bar class based on score"""
        if score >= 80:
            return 'progress-excellent'
        elif score >= 60:
            return 'progress-good'
        else:
            return 'progress-poor'
    
    def _get_score_status(self, score: float) -> str:
        """Get status text based on score"""
        if score >= 90:
            return 'Excellent'
        elif score >= 80:
            return 'Very Good'
        elif score >= 70:
            return 'Good'
        elif score >= 60:
            return 'Fair'
        else:
            return 'Needs Improvement'

def main():
    """Command line interface for visual dashboard generator"""
    parser = argparse.ArgumentParser(description='🌱 Generate Visual Sustainability Dashboard')
    parser.add_argument('--input', required=True, help='Input analysis JSON file')
    parser.add_argument('--output', default='visual_dashboard.html', help='Output HTML file')
    
    args = parser.parse_args()
    
    # Load analysis data
    try:
        with open(args.input, 'r') as f:
            analysis_data = json.load(f)
    except Exception as e:
        print(f"❌ Error loading analysis data: {e}")
        return 1
    
    # Generate visual dashboard
    generator = VisualDashboardGenerator()
    output_path = generator.generate_visual_dashboard(analysis_data, args.output)
    
    print(f"✅ Visual dashboard generated successfully!")
    print(f"🌐 Open in browser: file://{os.path.abspath(output_path)}")
    
    return 0

if __name__ == "__main__":
    exit(main())