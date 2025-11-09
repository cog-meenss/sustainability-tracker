#!/usr/bin/env python3
"""
🎯 Comprehensive Dashboard Runner
Executes sustainability analysis and generates all visual reports
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
import subprocess
import webbrowser
from typing import Dict

# Add analyzer to path
sys.path.append(str(Path(__file__).parent.parent / 'analyzer'))
sys.path.append(str(Path(__file__).parent.parent / 'reports'))

try:
    from sustainability_analyzer import SustainabilityAnalyzer
    from visual_dashboard_generator import VisualDashboardGenerator
    from data_tables_generator import DataTablesGenerator
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure all analyzer modules are in the correct directories")
    sys.exit(1)

class DashboardRunner:
    """Main dashboard runner for complete analysis and visualization"""
    
    def __init__(self, project_path: str, output_dir: str = "dashboard_output"):
        self.project_path = Path(project_path)
        self.output_dir = Path(output_dir)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create output directory
        self.output_dir.mkdir(exist_ok=True)
        
        # Initialize generators
        self.analyzer = SustainabilityAnalyzer()
        self.visual_generator = VisualDashboardGenerator()
        self.tables_generator = DataTablesGenerator()
    
    def run_complete_analysis(self) -> Dict[str, str]:
        """Run complete sustainability analysis and generate all reports"""
        
        print(f"🚀 Starting complete sustainability analysis...")
        print(f"📁 Project: {self.project_path}")
        print(f"📊 Output: {self.output_dir}")
        
        # Step 1: Run sustainability analysis
        print("\n🔍 Step 1: Running sustainability analysis...")
        analysis_data = self.analyzer.analyze_project(str(self.project_path))
        
        # Save raw analysis data
        analysis_file = self.output_dir / f"analysis_{self.timestamp}.json"
        with open(analysis_file, 'w') as f:
            json.dump(analysis_data, f, indent=2)
        print(f"💾 Analysis data saved: {analysis_file}")
        
        # Step 2: Generate visual dashboard
        print("\n🎨 Step 2: Generating visual dashboard...")
        visual_dashboard = self.output_dir / f"visual_dashboard_{self.timestamp}.html"
        self.visual_generator.generate_visual_dashboard(analysis_data, str(visual_dashboard))
        
        # Step 3: Generate data tables
        print("\n📊 Step 3: Generating interactive data tables...")
        data_tables = self.output_dir / f"data_tables_{self.timestamp}.html"
        self.tables_generator.generate_data_tables(analysis_data, str(data_tables))
        
        # Step 4: Generate summary report
        print("\n📄 Step 4: Generating summary report...")
        summary_report = self.generate_summary_report(analysis_data)
        
        # Step 5: Create index page
        print("\n🏠 Step 5: Creating navigation index...")
        index_file = self.create_index_page({
            'visual_dashboard': visual_dashboard.name,
            'data_tables': data_tables.name,
            'analysis_json': analysis_file.name,
            'summary_report': 'summary_report.html'
        }, analysis_data)
        
        results = {
            'index': str(index_file),
            'visual_dashboard': str(visual_dashboard),
            'data_tables': str(data_tables),
            'analysis_data': str(analysis_file),
            'summary_report': str(summary_report)
        }
        
        print("\n✅ Complete analysis finished!")
        print(f"🌐 Main dashboard: file://{index_file.absolute()}")
        
        return results
    
    def generate_summary_report(self, analysis_data: Dict) -> Path:
        """Generate executive summary report"""
        
        metrics = analysis_data.get('sustainability_metrics', {})
        summary = analysis_data.get('analysis_summary', {})
        issues = analysis_data.get('issues', [])
        recommendations = analysis_data.get('recommendations', [])
        
        overall_score = metrics.get('overall_score', 0)
        score_color = self._get_score_color(overall_score)
        score_status = self._get_score_status(overall_score)
        
        # Count issues by severity
        high_issues = len([i for i in issues if i.get('severity') == 'high'])
        medium_issues = len([i for i in issues if i.get('severity') == 'medium'])
        low_issues = len([i for i in issues if i.get('severity') == 'low'])
        
        # Count recommendations by priority
        high_recs = len([r for r in recommendations if r.get('priority') == 'high'])
        medium_recs = len([r for r in recommendations if r.get('priority') == 'medium'])
        low_recs = len([r for r in recommendations if r.get('priority') == 'low'])
        
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📄 Sustainability Summary Report</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        body {{
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }}
        .report-container {{
            max-width: 1200px;
            margin: 2rem auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .report-header {{
            background: linear-gradient(135deg, #2d5016 0%, #3e7b00 100%);
            color: white;
            padding: 3rem 2rem;
            text-align: center;
        }}
        .report-header h1 {{
            font-size: 3rem;
            font-weight: 300;
            margin-bottom: 1rem;
        }}
        .overall-score {{
            font-size: 4rem;
            font-weight: bold;
            color: {score_color};
            margin: 1rem 0;
        }}
        .report-content {{
            padding: 3rem 2rem;
        }}
        .metric-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem;
            margin-bottom: 1rem;
            background: #f8f9fa;
            border-radius: 10px;
            border-left: 4px solid;
        }}
        .metric-row.energy {{ border-left-color: #f39c12; }}
        .metric-row.resource {{ border-left-color: #3498db; }}
        .metric-row.carbon {{ border-left-color: #e74c3c; }}
        .metric-row.performance {{ border-left-color: #2ecc71; }}
        .metric-row.practices {{ border-left-color: #9b59b6; }}
        .summary-section {{
            background: white;
            border-radius: 10px;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        }}
        .issue-indicator {{
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-weight: bold;
            text-align: center;
        }}
        .issue-high {{ background: #e74c3c; color: white; }}
        .issue-medium {{ background: #f39c12; color: white; }}
        .issue-low {{ background: #3498db; color: white; }}
        .print-section {{
            background: #f8f9fa;
            padding: 2rem;
            text-align: center;
        }}
        @media print {{
            .print-section {{ display: none; }}
            body {{ background: white; }}
        }}
    </style>
</head>
<body>
    <div class="report-container">
        <div class="report-header">
            <h1><i class="fas fa-file-alt"></i> Executive Summary Report</h1>
            <p class="lead">Sustainability Analysis Results</p>
            <div class="overall-score">{overall_score:.1f}/100</div>
            <p class="fs-4">Status: {score_status}</p>
            <p>Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")}</p>
        </div>
        
        <div class="report-content">
            <!-- Key Metrics -->
            <div class="summary-section">
                <h2><i class="fas fa-chart-bar"></i> Key Sustainability Metrics</h2>
                
                <div class="metric-row energy">
                    <div>
                        <strong>Energy Efficiency</strong>
                        <p class="mb-0 text-muted">Power consumption optimization</p>
                    </div>
                    <div class="text-end">
                        <span class="fs-3 fw-bold">{metrics.get('energy_efficiency', 0):.1f}/100</span>
                    </div>
                </div>
                
                <div class="metric-row resource">
                    <div>
                        <strong>Resource Utilization</strong>
                        <p class="mb-0 text-muted">Memory and CPU efficiency</p>
                    </div>
                    <div class="text-end">
                        <span class="fs-3 fw-bold">{metrics.get('resource_utilization', 0):.1f}/100</span>
                    </div>
                </div>
                
                <div class="metric-row carbon">
                    <div>
                        <strong>Carbon Footprint</strong>
                        <p class="mb-0 text-muted">Environmental impact score</p>
                    </div>
                    <div class="text-end">
                        <span class="fs-3 fw-bold">{metrics.get('carbon_footprint', 0):.1f}/100</span>
                    </div>
                </div>
                
                <div class="metric-row performance">
                    <div>
                        <strong>Performance Optimization</strong>
                        <p class="mb-0 text-muted">Speed and efficiency measures</p>
                    </div>
                    <div class="text-end">
                        <span class="fs-3 fw-bold">{metrics.get('performance_optimization', 0):.1f}/100</span>
                    </div>
                </div>
                
                <div class="metric-row practices">
                    <div>
                        <strong>Sustainable Practices</strong>
                        <p class="mb-0 text-muted">Code quality and maintainability</p>
                    </div>
                    <div class="text-end">
                        <span class="fs-3 fw-bold">{metrics.get('sustainable_practices', 0):.1f}/100</span>
                    </div>
                </div>
            </div>
            
            <!-- Project Overview -->
            <div class="row">
                <div class="col-md-6">
                    <div class="summary-section">
                        <h3><i class="fas fa-info-circle"></i> Project Overview</h3>
                        <table class="table">
                            <tr><td><strong>Total Files</strong></td><td>{summary.get('file_count', 0)}</td></tr>
                            <tr><td><strong>Languages</strong></td><td>{len(summary.get('language_breakdown', {}))}</td></tr>
                            <tr><td><strong>Analysis Time</strong></td><td>{summary.get('execution_time', 0):.3f}s</td></tr>
                            <tr><td><strong>Primary Language</strong></td><td>{max(summary.get('language_breakdown', {}).items(), key=lambda x: x[1])[0] if summary.get('language_breakdown') else 'None'}</td></tr>
                        </table>
                    </div>
                </div>
                
                <div class="col-md-6">
                    <div class="summary-section">
                        <h3><i class="fas fa-exclamation-triangle"></i> Issues Summary</h3>
                        <div class="d-flex justify-content-around">
                            <div class="text-center">
                                <div class="issue-indicator issue-high">{high_issues}</div>
                                <p class="mt-2 mb-0"><small>High Priority</small></p>
                            </div>
                            <div class="text-center">
                                <div class="issue-indicator issue-medium">{medium_issues}</div>
                                <p class="mt-2 mb-0"><small>Medium Priority</small></p>
                            </div>
                            <div class="text-center">
                                <div class="issue-indicator issue-low">{low_issues}</div>
                                <p class="mt-2 mb-0"><small>Low Priority</small></p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Recommendations -->
            <div class="summary-section">
                <h3><i class="fas fa-lightbulb"></i> Key Recommendations</h3>
                <div class="row">
                    <div class="col-md-4 text-center">
                        <div class="issue-indicator issue-high">{high_recs}</div>
                        <p class="mt-2">High Priority Actions</p>
                    </div>
                    <div class="col-md-4 text-center">
                        <div class="issue-indicator issue-medium">{medium_recs}</div>
                        <p class="mt-2">Medium Priority Actions</p>
                    </div>
                    <div class="col-md-4 text-center">
                        <div class="issue-indicator issue-low">{low_recs}</div>
                        <p class="mt-2">Low Priority Actions</p>
                    </div>
                </div>
                
                <div class="mt-4">
                    <h4>Top Priority Actions:</h4>
                    <ul class="list-group">
                        {''.join([f'<li class="list-group-item"><strong>{r.get("title", "Action")}</strong><br><small class="text-muted">{r.get("description", "")}</small></li>' for r in recommendations[:5]])}
                    </ul>
                </div>
            </div>
            
            <!-- Next Steps -->
            <div class="summary-section">
                <h3><i class="fas fa-arrow-right"></i> Next Steps</h3>
                <ol class="fs-5">
                    <li>Address <strong>{high_issues} high-priority issues</strong> immediately</li>
                    <li>Implement <strong>{high_recs} critical recommendations</strong></li>
                    <li>Monitor energy efficiency improvements</li>
                    <li>Schedule regular sustainability reviews</li>
                    <li>Set targets for {overall_score + 10:.0f}% overall score improvement</li>
                </ol>
            </div>
        </div>
        
        <div class="print-section">
            <button class="btn btn-primary btn-lg" onclick="window.print()">
                <i class="fas fa-print"></i> Print Report
            </button>
            <a href="index.html" class="btn btn-secondary btn-lg ms-3">
                <i class="fas fa-arrow-left"></i> Back to Dashboard
            </a>
        </div>
    </div>
</body>
</html>
"""
        
        summary_file = self.output_dir / "summary_report.html"
        with open(summary_file, 'w') as f:
            f.write(html_content)
        
        return summary_file
    
    def create_index_page(self, files: Dict[str, str], analysis_data: Dict) -> Path:
        """Create main navigation index page"""
        
        metrics = analysis_data.get('sustainability_metrics', {})
        overall_score = metrics.get('overall_score', 0)
        
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🌱 Sustainability Analysis Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        body {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }}
        .dashboard-container {{
            max-width: 1200px;
            margin: 2rem auto;
            padding: 2rem;
        }}
        .hero-section {{
            background: linear-gradient(135deg, #2d5016 0%, #3e7b00 100%);
            color: white;
            text-align: center;
            padding: 4rem 2rem;
            border-radius: 20px;
            margin-bottom: 3rem;
            position: relative;
            overflow: hidden;
        }}
        .hero-section::before {{
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse"><path d="M 10 0 L 0 0 0 10" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="0.5"/></pattern></defs><rect width="100" height="100" fill="url(%23grid)"/></svg>');
            animation: drift 20s infinite linear;
        }}
        @keyframes drift {{
            0% {{ transform: translate(0, 0); }}
            100% {{ transform: translate(-10px, -10px); }}
        }}
        .hero-content {{
            position: relative;
            z-index: 1;
        }}
        .hero-score {{
            font-size: 5rem;
            font-weight: bold;
            margin: 1rem 0;
            color: {self._get_score_color(overall_score)};
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        .dashboard-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 2rem;
            margin-bottom: 3rem;
        }}
        .dashboard-card {{
            background: white;
            border-radius: 20px;
            padding: 2.5rem;
            text-align: center;
            box-shadow: 0 15px 35px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }}
        .dashboard-card::before {{
            content: '';
            position: absolute;
            top: -50%;
            right: -50%;
            width: 100px;
            height: 100px;
            background: rgba(62, 123, 0, 0.05);
            border-radius: 50%;
            transition: all 0.3s ease;
        }}
        .dashboard-card:hover {{
            transform: translateY(-10px) scale(1.02);
            box-shadow: 0 25px 50px rgba(0,0,0,0.15);
        }}
        .dashboard-card:hover::before {{
            top: -25%;
            right: -25%;
            width: 150px;
            height: 150px;
        }}
        .card-icon {{
            font-size: 4rem;
            margin-bottom: 1.5rem;
            color: #3e7b00;
        }}
        .card-title {{
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 1rem;
            color: #2d5016;
        }}
        .card-description {{
            color: #666;
            margin-bottom: 2rem;
            line-height: 1.6;
        }}
        .dashboard-btn {{
            background: linear-gradient(135deg, #3e7b00, #2d5016);
            color: white;
            border: none;
            padding: 1rem 2rem;
            border-radius: 25px;
            font-size: 1.1rem;
            font-weight: 600;
            text-decoration: none;
            display: inline-block;
            transition: all 0.3s ease;
            position: relative;
            z-index: 1;
        }}
        .dashboard-btn:hover {{
            color: white;
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(62, 123, 0, 0.4);
        }}
        .metrics-overview {{
            background: white;
            border-radius: 20px;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }}
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
        }}
        .metric-item {{
            text-align: center;
            padding: 1.5rem;
            background: #f8f9fa;
            border-radius: 15px;
            border-left: 4px solid;
        }}
        .metric-item.energy {{ border-left-color: #f39c12; }}
        .metric-item.resource {{ border-left-color: #3498db; }}
        .metric-item.carbon {{ border-left-color: #e74c3c; }}
        .metric-item.performance {{ border-left-color: #2ecc71; }}
        .metric-item.practices {{ border-left-color: #9b59b6; }}
        .metric-value {{
            font-size: 2rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }}
        .metric-label {{
            font-size: 0.9rem;
            color: #666;
            font-weight: 500;
        }}
        .footer {{
            text-align: center;
            color: white;
            margin-top: 3rem;
            padding: 2rem;
            background: rgba(0,0,0,0.1);
            border-radius: 15px;
        }}
        @media (max-width: 768px) {{
            .dashboard-grid {{
                grid-template-columns: 1fr;
            }}
            .hero-score {{
                font-size: 4rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="dashboard-container">
        <!-- Hero Section -->
        <div class="hero-section">
            <div class="hero-content">
                <h1><i class="fas fa-leaf"></i> Sustainability Analysis Dashboard</h1>
                <p class="lead">Comprehensive Code Sustainability Assessment & Environmental Impact Analysis</p>
                <div class="hero-score">{overall_score:.1f}/100</div>
                <p class="fs-4">Overall Sustainability Score</p>
                <p><i class="fas fa-calendar"></i> Generated on {datetime.now().strftime("%B %d, %Y at %H:%M UTC")}</p>
            </div>
        </div>
        
        <!-- Metrics Overview -->
        <div class="metrics-overview">
            <h2 class="text-center mb-4"><i class="fas fa-chart-bar"></i> Key Metrics Overview</h2>
            <div class="metrics-grid">
                <div class="metric-item energy">
                    <div class="metric-value" style="color: #f39c12;">{metrics.get('energy_efficiency', 0):.1f}</div>
                    <div class="metric-label">Energy Efficiency</div>
                </div>
                <div class="metric-item resource">
                    <div class="metric-value" style="color: #3498db;">{metrics.get('resource_utilization', 0):.1f}</div>
                    <div class="metric-label">Resource Usage</div>
                </div>
                <div class="metric-item carbon">
                    <div class="metric-value" style="color: #e74c3c;">{metrics.get('carbon_footprint', 0):.1f}</div>
                    <div class="metric-label">Carbon Impact</div>
                </div>
                <div class="metric-item performance">
                    <div class="metric-value" style="color: #2ecc71;">{metrics.get('performance_optimization', 0):.1f}</div>
                    <div class="metric-label">Performance</div>
                </div>
                <div class="metric-item practices">
                    <div class="metric-value" style="color: #9b59b6;">{metrics.get('sustainable_practices', 0):.1f}</div>
                    <div class="metric-label">Best Practices</div>
                </div>
            </div>
        </div>
        
        <!-- Dashboard Navigation -->
        <div class="dashboard-grid">
            <div class="dashboard-card">
                <div class="card-icon">
                    <i class="fas fa-chart-pie"></i>
                </div>
                <h3 class="card-title">Visual Dashboard</h3>
                <p class="card-description">
                    Interactive charts, graphs, and visual analytics with radar plots, 
                    gauge meters, and 3D visualizations for comprehensive data exploration.
                </p>
                <a href="{files['visual_dashboard']}" class="dashboard-btn">
                    <i class="fas fa-chart-line"></i> Open Visual Dashboard
                </a>
            </div>
            
            <div class="dashboard-card">
                <div class="card-icon">
                    <i class="fas fa-table"></i>
                </div>
                <h3 class="card-title">Data Tables</h3>
                <p class="card-description">
                    Advanced interactive tables with sorting, filtering, search, and export 
                    capabilities for detailed data analysis and manipulation.
                </p>
                <a href="{files['data_tables']}" class="dashboard-btn">
                    <i class="fas fa-list"></i> Open Data Tables
                </a>
            </div>
            
            <div class="dashboard-card">
                <div class="card-icon">
                    <i class="fas fa-file-alt"></i>
                </div>
                <h3 class="card-title">Executive Summary</h3>
                <p class="card-description">
                    Comprehensive executive summary report with key findings, 
                    recommendations, and actionable insights for stakeholders.
                </p>
                <a href="{files['summary_report']}" class="dashboard-btn">
                    <i class="fas fa-file-pdf"></i> View Summary Report
                </a>
            </div>
            
            <div class="dashboard-card">
                <div class="card-icon">
                    <i class="fas fa-code"></i>
                </div>
                <h3 class="card-title">Raw Data</h3>
                <p class="card-description">
                    Complete analysis results in JSON format for integration 
                    with other tools, APIs, or custom analysis workflows.
                </p>
                <a href="{files['analysis_json']}" class="dashboard-btn" download>
                    <i class="fas fa-download"></i> Download JSON Data
                </a>
            </div>
        </div>
        
        <!-- Footer -->
        <div class="footer">
            <h4><i class="fas fa-leaf"></i> Sustainability Code Evaluation Analyzer</h4>
            <p>
                Building sustainable software for a better tomorrow | 
                Analysis powered by advanced sustainability metrics | 
                Dashboard generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")}
            </p>
            <p>
                <small>
                    <i class="fas fa-info-circle"></i> 
                    This dashboard provides comprehensive insights into your code's environmental impact and sustainability practices.
                </small>
            </p>
        </div>
    </div>
    
    <!-- Auto-refresh functionality -->
    <script>
        // Add smooth scrolling and animations
        document.addEventListener('DOMContentLoaded', function() {{
            // Animate metric values on load
            const metricValues = document.querySelectorAll('.metric-value');
            metricValues.forEach(value => {{
                const finalValue = parseFloat(value.textContent);
                let currentValue = 0;
                const increment = finalValue / 50;
                const timer = setInterval(() => {{
                    currentValue += increment;
                    if (currentValue >= finalValue) {{
                        currentValue = finalValue;
                        clearInterval(timer);
                    }}
                    value.textContent = currentValue.toFixed(1);
                }}, 30);
            }});
            
            // Add click tracking
            document.querySelectorAll('.dashboard-btn').forEach(btn => {{
                btn.addEventListener('click', function(e) {{
                    console.log('Dashboard navigation:', this.textContent.trim());
                }});
            }});
        }});
    </script>
</body>
</html>
"""
        
        index_file = self.output_dir / "index.html"
        with open(index_file, 'w') as f:
            f.write(html_content)
        
        return index_file
    
    def _get_score_color(self, score: float) -> str:
        """Get color based on score"""
        if score >= 80:
            return '#2ecc71'
        elif score >= 60:
            return '#f39c12'
        else:
            return '#e74c3c'
    
    def _get_score_status(self, score: float) -> str:
        """Get status based on score"""
        if score >= 90:
            return 'EXCELLENT'
        elif score >= 80:
            return 'VERY GOOD'
        elif score >= 70:
            return 'GOOD'
        elif score >= 60:
            return 'FAIR'
        else:
            return 'NEEDS IMPROVEMENT'

def main():
    """Command line interface for dashboard runner"""
    parser = argparse.ArgumentParser(description='🎯 Comprehensive Sustainability Dashboard Runner')
    parser.add_argument('project_path', help='Path to the project to analyze')
    parser.add_argument('--output', '-o', default='dashboard_output', help='Output directory for reports')
    parser.add_argument('--open', '-b', action='store_true', help='Open dashboard in browser after generation')
    
    args = parser.parse_args()
    
    # Validate project path
    if not os.path.exists(args.project_path):
        print(f"❌ Error: Project path '{args.project_path}' does not exist")
        return 1
    
    # Run complete analysis
    try:
        runner = DashboardRunner(args.project_path, args.output)
        results = runner.run_complete_analysis()
        
        print(f"\n🎉 Dashboard generation complete!")
        print(f"📊 Dashboard files generated:")
        for name, path in results.items():
            print(f"   {name}: {path}")
        
        # Open in browser if requested
        if args.open:
            index_file = results['index']
            webbrowser.open(f"file://{os.path.abspath(index_file)}")
            print(f"\n🌐 Opening dashboard in browser...")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error during dashboard generation: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit(main())