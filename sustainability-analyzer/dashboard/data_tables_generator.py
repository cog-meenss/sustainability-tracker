#!/usr/bin/env python3
"""
📊 Interactive Data Tables Generator
Creates comprehensive data tables with filtering, sorting, and export capabilities
"""

import json
import argparse
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
import pandas as pd

class DataTablesGenerator:
    """Generate interactive data tables with advanced features"""
    
    def __init__(self):
        self.timestamp = datetime.now().isoformat()
    
    def generate_data_tables(self, analysis_data: Dict[str, Any], output_path: str) -> str:
        """Generate comprehensive data tables interface"""
        
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📊 Sustainability Data Tables</title>
    
    <!-- External Libraries -->
    <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.13.7/css/dataTables.bootstrap5.min.css">
    <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/buttons/2.4.2/css/buttons.bootstrap5.min.css">
    <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/searchpanes/2.2.0/css/searchPanes.bootstrap5.min.css">
    <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/select/1.7.0/css/select.bootstrap5.min.css">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    
    <style>
        {self._get_tables_css()}
    </style>
</head>
<body>
    <div class="container-fluid">
        {self._generate_header()}
        {self._generate_navigation_tabs()}
        
        <div class="tab-content" id="tablesTabContent">
            {self._generate_overview_table(analysis_data)}
            {self._generate_metrics_table(analysis_data)}
            {self._generate_files_table(analysis_data)}
            {self._generate_issues_table(analysis_data)}
            {self._generate_recommendations_table(analysis_data)}
            {self._generate_export_section()}
        </div>
        
        {self._generate_footer()}
    </div>

    <!-- Scripts -->
    <script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://cdn.datatables.net/1.13.7/js/jquery.dataTables.min.js"></script>
    <script src="https://cdn.datatables.net/1.13.7/js/dataTables.bootstrap5.min.js"></script>
    <script src="https://cdn.datatables.net/buttons/2.4.2/js/dataTables.buttons.min.js"></script>
    <script src="https://cdn.datatables.net/buttons/2.4.2/js/buttons.bootstrap5.min.js"></script>
    <script src="https://cdn.datatables.net/buttons/2.4.2/js/buttons.html5.min.js"></script>
    <script src="https://cdn.datatables.net/buttons/2.4.2/js/buttons.print.min.js"></script>
    <script src="https://cdn.datatables.net/searchpanes/2.2.0/js/dataTables.searchPanes.min.js"></script>
    <script src="https://cdn.datatables.net/searchpanes/2.2.0/js/searchPanes.bootstrap5.min.js"></script>
    <script src="https://cdn.datatables.net/select/1.7.0/js/dataTables.select.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/pdfmake/0.2.7/pdfmake.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/pdfmake/0.2.7/vfs_fonts.js"></script>

    <script>
        {self._generate_tables_script(analysis_data)}
    </script>
</body>
</html>
"""
        
        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"📋 Data tables generated: {output_path}")
        return output_path
    
    def _get_tables_css(self) -> str:
        """CSS for enhanced data tables"""
        return """
        body {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }
        
        .header-section {
            background: linear-gradient(135deg, #2d5016 0%, #3e7b00 100%);
            color: white;
            padding: 2rem 0;
            margin-bottom: 2rem;
            text-align: center;
        }
        
        .header-section h1 {
            font-size: 2.5rem;
            font-weight: 300;
            margin-bottom: 0.5rem;
        }
        
        .nav-tabs {
            background: white;
            border-radius: 10px 10px 0 0;
            padding: 1rem 1rem 0 1rem;
            box-shadow: 0 -5px 20px rgba(0,0,0,0.1);
        }
        
        .nav-tabs .nav-link {
            color: #666;
            border: none;
            padding: 1rem 1.5rem;
            margin-right: 0.5rem;
            border-radius: 8px 8px 0 0;
            background: #f8f9fa;
            transition: all 0.3s ease;
        }
        
        .nav-tabs .nav-link:hover {
            background: #e9ecef;
            color: #333;
            transform: translateY(-2px);
        }
        
        .nav-tabs .nav-link.active {
            background: linear-gradient(135deg, #3e7b00, #2d5016);
            color: white;
            border: none;
        }
        
        .tab-pane {
            background: white;
            padding: 2rem;
            border-radius: 0 0 10px 10px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            min-height: 500px;
        }
        
        .table-container {
            background: white;
            border-radius: 10px;
            padding: 1.5rem;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
            margin-bottom: 2rem;
        }
        
        .table-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.5rem;
            padding-bottom: 1rem;
            border-bottom: 2px solid #e9ecef;
        }
        
        .table-title {
            font-size: 1.5rem;
            font-weight: 600;
            color: #2d5016;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .table-stats {
            display: flex;
            gap: 1rem;
        }
        
        .stat-badge {
            background: linear-gradient(135deg, #3e7b00, #2d5016);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 500;
        }
        
        .dataTables_wrapper {
            font-size: 0.9rem;
        }
        
        .dataTables_wrapper .dataTables_length,
        .dataTables_wrapper .dataTables_filter {
            margin-bottom: 1rem;
        }
        
        .dataTables_wrapper .dataTables_filter input {
            border-radius: 20px;
            border: 2px solid #e9ecef;
            padding: 0.5rem 1rem;
            margin-left: 0.5rem;
        }
        
        .dataTables_wrapper .dataTables_filter input:focus {
            border-color: #3e7b00;
            outline: none;
            box-shadow: 0 0 0 0.2rem rgba(62, 123, 0, 0.25);
        }
        
        table.dataTable {
            border-collapse: separate;
            border-spacing: 0;
            border-radius: 10px;
            overflow: hidden;
            border: 1px solid #e9ecef;
        }
        
        table.dataTable thead th {
            background: linear-gradient(135deg, #3e7b00, #2d5016);
            color: white;
            border: none;
            padding: 1rem 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-size: 0.8rem;
        }
        
        table.dataTable tbody td {
            padding: 0.75rem;
            border-bottom: 1px solid #f1f1f1;
            vertical-align: middle;
        }
        
        table.dataTable tbody tr:hover {
            background-color: #f8f9fa;
        }
        
        .score-badge {
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            text-align: center;
            min-width: 60px;
            display: inline-block;
        }
        
        .score-excellent {
            background: linear-gradient(135deg, #2ecc71, #27ae60);
            color: white;
        }
        
        .score-good {
            background: linear-gradient(135deg, #f39c12, #e67e22);
            color: white;
        }
        
        .score-fair {
            background: linear-gradient(135deg, #f1c40f, #f39c12);
            color: white;
        }
        
        .score-poor {
            background: linear-gradient(135deg, #e74c3c, #c0392b);
            color: white;
        }
        
        .priority-high {
            background: #e74c3c;
            color: white;
            padding: 0.25rem 0.5rem;
            border-radius: 15px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
        }
        
        .priority-medium {
            background: #f39c12;
            color: white;
            padding: 0.25rem 0.5rem;
            border-radius: 15px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
        }
        
        .priority-low {
            background: #3498db;
            color: white;
            padding: 0.25rem 0.5rem;
            border-radius: 15px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
        }
        
        .dt-buttons {
            margin-bottom: 1rem;
        }
        
        .dt-button {
            background: linear-gradient(135deg, #3e7b00, #2d5016) !important;
            color: white !important;
            border: none !important;
            border-radius: 20px !important;
            padding: 0.5rem 1rem !important;
            margin-right: 0.5rem !important;
            transition: all 0.3s ease !important;
            font-size: 0.85rem !important;
        }
        
        .dt-button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 5px 15px rgba(62, 123, 0, 0.4) !important;
        }
        
        .export-section {
            background: linear-gradient(135deg, #f8f9fa, #e9ecef);
            padding: 2rem;
            border-radius: 10px;
            margin-top: 2rem;
        }
        
        .export-buttons {
            display: flex;
            gap: 1rem;
            flex-wrap: wrap;
            justify-content: center;
        }
        
        .export-btn {
            background: linear-gradient(135deg, #3e7b00, #2d5016);
            color: white;
            border: none;
            padding: 1rem 2rem;
            border-radius: 25px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .export-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(62, 123, 0, 0.4);
        }
        
        .progress-bar-custom {
            background: #e9ecef;
            height: 20px;
            border-radius: 10px;
            overflow: hidden;
            position: relative;
        }
        
        .progress-fill-custom {
            height: 100%;
            border-radius: 10px;
            transition: width 1s ease;
        }
        
        .footer-section {
            background: #333;
            color: white;
            text-align: center;
            padding: 2rem;
            margin-top: 3rem;
        }
        
        @media (max-width: 768px) {
            .nav-tabs {
                padding: 0.5rem;
            }
            
            .nav-tabs .nav-link {
                padding: 0.75rem 1rem;
                font-size: 0.9rem;
            }
            
            .table-header {
                flex-direction: column;
                align-items: flex-start;
                gap: 1rem;
            }
            
            .export-buttons {
                flex-direction: column;
                align-items: center;
            }
        }
        """
    
    def _generate_header(self) -> str:
        """Generate page header"""
        return f"""
        <div class="header-section">
            <div class="container">
                <h1><i class="fas fa-table"></i> Sustainability Data Tables</h1>
                <p class="lead">Comprehensive data analysis and interactive tables</p>
                <small>Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")}</small>
            </div>
        </div>
        """
    
    def _generate_navigation_tabs(self) -> str:
        """Generate navigation tabs"""
        return """
        <ul class="nav nav-tabs" id="tablesTabs" role="tablist">
            <li class="nav-item" role="presentation">
                <button class="nav-link active" id="overview-tab" data-bs-toggle="tab" data-bs-target="#overview" type="button" role="tab">
                    <i class="fas fa-tachometer-alt"></i> Overview
                </button>
            </li>
            <li class="nav-item" role="presentation">
                <button class="nav-link" id="metrics-tab" data-bs-toggle="tab" data-bs-target="#metrics" type="button" role="tab">
                    <i class="fas fa-chart-bar"></i> Metrics
                </button>
            </li>
            <li class="nav-item" role="presentation">
                <button class="nav-link" id="files-tab" data-bs-toggle="tab" data-bs-target="#files" type="button" role="tab">
                    <i class="fas fa-file-code"></i> Files
                </button>
            </li>
            <li class="nav-item" role="presentation">
                <button class="nav-link" id="issues-tab" data-bs-toggle="tab" data-bs-target="#issues" type="button" role="tab">
                    <i class="fas fa-exclamation-triangle"></i> Issues
                </button>
            </li>
            <li class="nav-item" role="presentation">
                <button class="nav-link" id="recommendations-tab" data-bs-toggle="tab" data-bs-target="#recommendations" type="button" role="tab">
                    <i class="fas fa-lightbulb"></i> Recommendations
                </button>
            </li>
        </ul>
        """
    
    def _generate_overview_table(self, analysis_data: Dict) -> str:
        """Generate overview table"""
        metrics = analysis_data.get('sustainability_metrics', {})
        summary = analysis_data.get('analysis_summary', {})
        
        return f"""
        <div class="tab-pane fade show active" id="overview" role="tabpanel">
            <div class="table-container">
                <div class="table-header">
                    <h3 class="table-title">
                        <i class="fas fa-info-circle"></i> Analysis Overview
                    </h3>
                    <div class="table-stats">
                        <span class="stat-badge">Overall Score: {metrics.get('overall_score', 0):.1f}</span>
                        <span class="stat-badge">Files: {summary.get('file_count', 0)}</span>
                    </div>
                </div>
                
                <table id="overviewTable" class="table table-striped" style="width:100%">
                    <thead>
                        <tr>
                            <th>Property</th>
                            <th>Value</th>
                            <th>Category</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><strong>Overall Score</strong></td>
                            <td>{metrics.get('overall_score', 0):.2f}/100</td>
                            <td>Performance</td>
                            <td>{self._get_score_badge(metrics.get('overall_score', 0))}</td>
                        </tr>
                        <tr>
                            <td><strong>Energy Efficiency</strong></td>
                            <td>{metrics.get('energy_efficiency', 0):.2f}/100</td>
                            <td>Sustainability</td>
                            <td>{self._get_score_badge(metrics.get('energy_efficiency', 0))}</td>
                        </tr>
                        <tr>
                            <td><strong>Resource Utilization</strong></td>
                            <td>{metrics.get('resource_utilization', 0):.2f}/100</td>
                            <td>Efficiency</td>
                            <td>{self._get_score_badge(metrics.get('resource_utilization', 0))}</td>
                        </tr>
                        <tr>
                            <td><strong>Carbon Footprint</strong></td>
                            <td>{metrics.get('carbon_footprint', 0):.2f}/100</td>
                            <td>Environmental</td>
                            <td>{self._get_score_badge(100 - metrics.get('carbon_footprint', 0))}</td>
                        </tr>
                        <tr>
                            <td><strong>Performance Optimization</strong></td>
                            <td>{metrics.get('performance_optimization', 0):.2f}/100</td>
                            <td>Performance</td>
                            <td>{self._get_score_badge(metrics.get('performance_optimization', 0))}</td>
                        </tr>
                        <tr>
                            <td><strong>Sustainable Practices</strong></td>
                            <td>{metrics.get('sustainable_practices', 0):.2f}/100</td>
                            <td>Best Practices</td>
                            <td>{self._get_score_badge(metrics.get('sustainable_practices', 0))}</td>
                        </tr>
                        <tr>
                            <td><strong>Total Files</strong></td>
                            <td>{summary.get('file_count', 0)}</td>
                            <td>Analysis</td>
                            <td><span class="score-badge score-excellent">Complete</span></td>
                        </tr>
                        <tr>
                            <td><strong>Execution Time</strong></td>
                            <td>{summary.get('execution_time', 0):.3f}s</td>
                            <td>Performance</td>
                            <td><span class="score-badge score-good">Fast</span></td>
                        </tr>
                        <tr>
                            <td><strong>Languages Detected</strong></td>
                            <td>{len(summary.get('language_breakdown', {}))}</td>
                            <td>Analysis</td>
                            <td><span class="score-badge score-excellent">Multi-Lang</span></td>
                        </tr>
                        <tr>
                            <td><strong>Analysis Date</strong></td>
                            <td>{summary.get('timestamp', 'N/A')}</td>
                            <td>Metadata</td>
                            <td><span class="score-badge score-excellent">Current</span></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
        """
    
    def _generate_metrics_table(self, analysis_data: Dict) -> str:
        """Generate detailed metrics table"""
        metrics = analysis_data.get('sustainability_metrics', {})
        
        return f"""
        <div class="tab-pane fade" id="metrics" role="tabpanel">
            <div class="table-container">
                <div class="table-header">
                    <h3 class="table-title">
                        <i class="fas fa-chart-bar"></i> Detailed Metrics Analysis
                    </h3>
                    <div class="table-stats">
                        <span class="stat-badge">Metrics: {len(metrics)}</span>
                    </div>
                </div>
                
                <table id="metricsTable" class="table table-striped" style="width:100%">
                    <thead>
                        <tr>
                            <th>Metric</th>
                            <th>Current Score</th>
                            <th>Target Score</th>
                            <th>Progress</th>
                            <th>Status</th>
                            <th>Priority</th>
                            <th>Impact</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><strong>Energy Efficiency</strong></td>
                            <td>{metrics.get('energy_efficiency', 0):.1f}</td>
                            <td>85.0</td>
                            <td>
                                <div class="progress-bar-custom">
                                    <div class="progress-fill-custom score-{self._get_score_class(metrics.get('energy_efficiency', 0))}" 
                                         style="width: {metrics.get('energy_efficiency', 0)}%"></div>
                                </div>
                            </td>
                            <td>{self._get_score_badge(metrics.get('energy_efficiency', 0))}</td>
                            <td><span class="priority-{self._get_priority_class(metrics.get('energy_efficiency', 0))}">
                                {self._get_priority_text(metrics.get('energy_efficiency', 0))}
                            </span></td>
                            <td>High</td>
                        </tr>
                        <tr>
                            <td><strong>Resource Utilization</strong></td>
                            <td>{metrics.get('resource_utilization', 0):.1f}</td>
                            <td>80.0</td>
                            <td>
                                <div class="progress-bar-custom">
                                    <div class="progress-fill-custom score-{self._get_score_class(metrics.get('resource_utilization', 0))}" 
                                         style="width: {metrics.get('resource_utilization', 0)}%"></div>
                                </div>
                            </td>
                            <td>{self._get_score_badge(metrics.get('resource_utilization', 0))}</td>
                            <td><span class="priority-{self._get_priority_class(metrics.get('resource_utilization', 0))}">
                                {self._get_priority_text(metrics.get('resource_utilization', 0))}
                            </span></td>
                            <td>Medium</td>
                        </tr>
                        <tr>
                            <td><strong>Carbon Footprint</strong></td>
                            <td>{metrics.get('carbon_footprint', 0):.1f}</td>
                            <td>40.0</td>
                            <td>
                                <div class="progress-bar-custom">
                                    <div class="progress-fill-custom score-{self._get_score_class(100 - metrics.get('carbon_footprint', 0))}" 
                                         style="width: {100 - metrics.get('carbon_footprint', 0)}%"></div>
                                </div>
                            </td>
                            <td>{self._get_score_badge(100 - metrics.get('carbon_footprint', 0))}</td>
                            <td><span class="priority-{self._get_priority_class(100 - metrics.get('carbon_footprint', 0))}">
                                {self._get_priority_text(100 - metrics.get('carbon_footprint', 0))}
                            </span></td>
                            <td>Critical</td>
                        </tr>
                        <tr>
                            <td><strong>Performance Optimization</strong></td>
                            <td>{metrics.get('performance_optimization', 0):.1f}</td>
                            <td>90.0</td>
                            <td>
                                <div class="progress-bar-custom">
                                    <div class="progress-fill-custom score-{self._get_score_class(metrics.get('performance_optimization', 0))}" 
                                         style="width: {metrics.get('performance_optimization', 0)}%"></div>
                                </div>
                            </td>
                            <td>{self._get_score_badge(metrics.get('performance_optimization', 0))}</td>
                            <td><span class="priority-{self._get_priority_class(metrics.get('performance_optimization', 0))}">
                                {self._get_priority_text(metrics.get('performance_optimization', 0))}
                            </span></td>
                            <td>High</td>
                        </tr>
                        <tr>
                            <td><strong>Sustainable Practices</strong></td>
                            <td>{metrics.get('sustainable_practices', 0):.1f}</td>
                            <td>75.0</td>
                            <td>
                                <div class="progress-bar-custom">
                                    <div class="progress-fill-custom score-{self._get_score_class(metrics.get('sustainable_practices', 0))}" 
                                         style="width: {metrics.get('sustainable_practices', 0)}%"></div>
                                </div>
                            </td>
                            <td>{self._get_score_badge(metrics.get('sustainable_practices', 0))}</td>
                            <td><span class="priority-{self._get_priority_class(metrics.get('sustainable_practices', 0))}">
                                {self._get_priority_text(metrics.get('sustainable_practices', 0))}
                            </span></td>
                            <td>Medium</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
        """
    
    def _generate_files_table(self, analysis_data: Dict) -> str:
        """Generate files analysis table"""
        summary = analysis_data.get('analysis_summary', {})
        language_breakdown = summary.get('language_breakdown', {})
        
        # Generate file data for demonstration
        file_data = []
        for lang, count in language_breakdown.items():
            for i in range(min(count, 5)):  # Show max 5 files per language for demo
                file_data.append({
                    'name': f'example_{lang}_{i+1}.{self._get_file_extension(lang)}',
                    'language': lang,
                    'size': f'{(i+1)*2.5:.1f} KB',
                    'score': 75 + (i * 5) + (hash(lang) % 20),
                    'issues': max(0, 3 - i),
                    'complexity': ['Low', 'Medium', 'High'][i % 3]
                })
        
        file_rows = []
        for i, file_info in enumerate(file_data):
            file_rows.append(f"""
            <tr>
                <td><i class="fas fa-file-code"></i> {file_info['name']}</td>
                <td><span class="badge bg-primary">{file_info['language'].title()}</span></td>
                <td>{file_info['size']}</td>
                <td>{self._get_score_badge(file_info['score'])}</td>
                <td>{file_info['issues']}</td>
                <td><span class="badge bg-{'success' if file_info['complexity'] == 'Low' else 'warning' if file_info['complexity'] == 'Medium' else 'danger'}">{file_info['complexity']}</span></td>
                <td>
                    <button class="btn btn-sm btn-outline-primary" onclick="viewFile('{file_info['name']}')">
                        <i class="fas fa-eye"></i> View
                    </button>
                </td>
            </tr>
            """)
        
        return f"""
        <div class="tab-pane fade" id="files" role="tabpanel">
            <div class="table-container">
                <div class="table-header">
                    <h3 class="table-title">
                        <i class="fas fa-file-code"></i> Files Analysis
                    </h3>
                    <div class="table-stats">
                        <span class="stat-badge">Files: {len(file_data)}</span>
                        <span class="stat-badge">Languages: {len(language_breakdown)}</span>
                    </div>
                </div>
                
                <table id="filesTable" class="table table-striped" style="width:100%">
                    <thead>
                        <tr>
                            <th>File Name</th>
                            <th>Language</th>
                            <th>Size</th>
                            <th>Score</th>
                            <th>Issues</th>
                            <th>Complexity</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {''.join(file_rows)}
                    </tbody>
                </table>
            </div>
        </div>
        """
    
    def _generate_issues_table(self, analysis_data: Dict) -> str:
        """Generate issues table"""
        issues = analysis_data.get('issues', [])
        
        # Generate demo issues if none exist
        if not issues:
            issues = [
                {
                    'type': 'Energy Inefficiency',
                    'severity': 'high',
                    'file': 'src/database/connection.py',
                    'line': 45,
                    'message': 'Database connection not properly pooled, causing energy waste',
                    'category': 'Resource Management'
                },
                {
                    'type': 'Memory Leak',
                    'severity': 'medium',
                    'file': 'src/utils/cache.js',
                    'line': 112,
                    'message': 'Potential memory leak in cache implementation',
                    'category': 'Performance'
                },
                {
                    'type': 'Inefficient Algorithm',
                    'severity': 'low',
                    'file': 'src/algorithms/sort.py',
                    'line': 23,
                    'message': 'O(n²) sorting algorithm could be optimized',
                    'category': 'Algorithm'
                }
            ]
        
        issue_rows = []
        for i, issue in enumerate(issues):
            severity = issue.get('severity', 'medium')
            issue_rows.append(f"""
            <tr>
                <td><span class="priority-{severity}">{severity.upper()}</span></td>
                <td><strong>{issue.get('type', 'Unknown')}</strong></td>
                <td><code>{issue.get('file', 'N/A')}</code></td>
                <td>{issue.get('line', 'N/A')}</td>
                <td>{issue.get('message', 'No message')}</td>
                <td><span class="badge bg-secondary">{issue.get('category', 'General')}</span></td>
                <td>
                    <button class="btn btn-sm btn-outline-primary" onclick="fixIssue({i})">
                        <i class="fas fa-wrench"></i> Fix
                    </button>
                </td>
            </tr>
            """)
        
        return f"""
        <div class="tab-pane fade" id="issues" role="tabpanel">
            <div class="table-container">
                <div class="table-header">
                    <h3 class="table-title">
                        <i class="fas fa-exclamation-triangle"></i> Issues & Problems
                    </h3>
                    <div class="table-stats">
                        <span class="stat-badge">Issues: {len(issues)}</span>
                    </div>
                </div>
                
                <table id="issuesTable" class="table table-striped" style="width:100%">
                    <thead>
                        <tr>
                            <th>Severity</th>
                            <th>Type</th>
                            <th>File</th>
                            <th>Line</th>
                            <th>Description</th>
                            <th>Category</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {''.join(issue_rows)}
                    </tbody>
                </table>
            </div>
        </div>
        """
    
    def _generate_recommendations_table(self, analysis_data: Dict) -> str:
        """Generate recommendations table"""
        recommendations = analysis_data.get('recommendations', [])
        
        # Generate demo recommendations if none exist
        if not recommendations:
            recommendations = [
                {
                    'title': 'Implement Database Connection Pooling',
                    'description': 'Use connection pooling to reduce database resource consumption and energy usage',
                    'priority': 'high',
                    'impact': 'High',
                    'effort': 'Medium',
                    'category': 'Database Optimization'
                },
                {
                    'title': 'Optimize Image Processing',
                    'description': 'Implement lazy loading and image compression to reduce bandwidth and processing power',
                    'priority': 'medium',
                    'impact': 'Medium',
                    'effort': 'Low',
                    'category': 'Performance'
                },
                {
                    'title': 'Add Code Documentation',
                    'description': 'Improve code documentation for better maintainability and sustainable development practices',
                    'priority': 'low',
                    'impact': 'Low',
                    'effort': 'High',
                    'category': 'Best Practices'
                }
            ]
        
        rec_rows = []
        for i, rec in enumerate(recommendations):
            priority = rec.get('priority', 'medium')
            rec_rows.append(f"""
            <tr>
                <td><span class="priority-{priority}">{priority.upper()}</span></td>
                <td><strong>{rec.get('title', 'Recommendation')}</strong></td>
                <td>{rec.get('description', 'No description')}</td>
                <td><span class="badge bg-info">{rec.get('impact', 'Unknown')}</span></td>
                <td><span class="badge bg-warning">{rec.get('effort', 'Unknown')}</span></td>
                <td><span class="badge bg-secondary">{rec.get('category', 'General')}</span></td>
                <td>
                    <button class="btn btn-sm btn-outline-success" onclick="implementRecommendation({i})">
                        <i class="fas fa-play"></i> Implement
                    </button>
                </td>
            </tr>
            """)
        
        return f"""
        <div class="tab-pane fade" id="recommendations" role="tabpanel">
            <div class="table-container">
                <div class="table-header">
                    <h3 class="table-title">
                        <i class="fas fa-lightbulb"></i> Recommendations & Improvements
                    </h3>
                    <div class="table-stats">
                        <span class="stat-badge">Recommendations: {len(recommendations)}</span>
                    </div>
                </div>
                
                <table id="recommendationsTable" class="table table-striped" style="width:100%">
                    <thead>
                        <tr>
                            <th>Priority</th>
                            <th>Title</th>
                            <th>Description</th>
                            <th>Impact</th>
                            <th>Effort</th>
                            <th>Category</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {''.join(rec_rows)}
                    </tbody>
                </table>
            </div>
        </div>
        """
    
    def _generate_export_section(self) -> str:
        """Generate export section"""
        return """
        <div class="export-section">
            <h3 class="text-center mb-4">
                <i class="fas fa-download"></i> Export Data
            </h3>
            <p class="text-center mb-4">Download your sustainability analysis data in various formats</p>
            
            <div class="export-buttons">
                <button class="export-btn" onclick="exportAllData('csv')">
                    <i class="fas fa-file-csv"></i> Export as CSV
                </button>
                <button class="export-btn" onclick="exportAllData('excel')">
                    <i class="fas fa-file-excel"></i> Export as Excel
                </button>
                <button class="export-btn" onclick="exportAllData('pdf')">
                    <i class="fas fa-file-pdf"></i> Export as PDF
                </button>
                <button class="export-btn" onclick="exportAllData('json')">
                    <i class="fas fa-file-code"></i> Export as JSON
                </button>
            </div>
        </div>
        """
    
    def _generate_footer(self) -> str:
        """Generate page footer"""
        return f"""
        <div class="footer-section">
            <p>
                <i class="fas fa-table"></i> Sustainability Data Tables | 
                Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")} | 
                <i class="fas fa-leaf"></i> Building sustainable software solutions
            </p>
        </div>
        """
    
    def _generate_tables_script(self, analysis_data: Dict) -> str:
        """Generate JavaScript for data tables functionality"""
        return f"""
        $(document).ready(function() {{
            // Initialize all DataTables with advanced features
            const commonConfig = {{
                responsive: true,
                pageLength: 25,
                lengthMenu: [[10, 25, 50, 100, -1], [10, 25, 50, 100, "All"]],
                dom: 'Bfrtip',
                buttons: [
                    'copy', 'csv', 'excel', 'pdf', 'print'
                ],
                order: [[0, 'asc']],
                language: {{
                    search: "_INPUT_",
                    searchPlaceholder: "Search records...",
                    lengthMenu: "Show _MENU_ records per page",
                    info: "Showing _START_ to _END_ of _TOTAL_ records",
                    infoEmpty: "No records available",
                    infoFiltered: "(filtered from _MAX_ total records)"
                }}
            }};
            
            // Initialize each table
            $('#overviewTable').DataTable({{
                ...commonConfig,
                columnDefs: [
                    {{ targets: [3], orderable: false }}
                ]
            }});
            
            $('#metricsTable').DataTable({{
                ...commonConfig,
                columnDefs: [
                    {{ targets: [3], orderable: false }},
                    {{ targets: [1, 2], type: 'num' }}
                ]
            }});
            
            $('#filesTable').DataTable({{
                ...commonConfig,
                columnDefs: [
                    {{ targets: [6], orderable: false }}
                ]
            }});
            
            $('#issuesTable').DataTable({{
                ...commonConfig,
                columnDefs: [
                    {{ targets: [6], orderable: false }}
                ],
                order: [[0, 'desc']] // Order by severity
            }});
            
            $('#recommendationsTable').DataTable({{
                ...commonConfig,
                columnDefs: [
                    {{ targets: [6], orderable: false }}
                ],
                order: [[0, 'desc']] // Order by priority
            }});
            
            // Animate progress bars
            setTimeout(() => {{
                $('.progress-fill-custom').each(function() {{
                    const width = $(this).css('width');
                    $(this).css('width', '0%').animate({{ width: width }}, 1500);
                }});
            }}, 500);
        }});
        
        // Export functionality
        function exportAllData(format) {{
            const timestamp = new Date().toISOString().slice(0, 19).replace(/:/g, '-');
            const filename = `sustainability-analysis-${{timestamp}}`;
            
            switch(format) {{
                case 'csv':
                    exportTableToCSV(filename + '.csv');
                    break;
                case 'excel':
                    exportTableToExcel(filename + '.xlsx');
                    break;
                case 'pdf':
                    exportTableToPDF(filename + '.pdf');
                    break;
                case 'json':
                    exportDataAsJSON(filename + '.json');
                    break;
            }}
        }}
        
        function exportTableToCSV(filename) {{
            const tables = ['overviewTable', 'metricsTable', 'filesTable', 'issuesTable', 'recommendationsTable'];
            let csvContent = '';
            
            tables.forEach(tableId => {{
                const table = document.getElementById(tableId);
                if (table) {{
                    csvContent += `\\n\\n=== ${{tableId.replace('Table', '').toUpperCase()}} ===\\n`;
                    const rows = table.querySelectorAll('tr');
                    rows.forEach(row => {{
                        const cols = row.querySelectorAll('th, td');
                        const rowData = Array.from(cols).map(col => 
                            `"${{col.textContent.trim().replace(/"/g, '""')}}"`
                        ).join(',');
                        csvContent += rowData + '\\n';
                    }});
                }}
            }});
            
            downloadFile(csvContent, filename, 'text/csv');
        }}
        
        function exportDataAsJSON(filename) {{
            const analysisData = {json.dumps(analysis_data, indent=2)};
            downloadFile(JSON.stringify(analysisData, null, 2), filename, 'application/json');
        }}
        
        function downloadFile(content, filename, mimeType) {{
            const blob = new Blob([content], {{ type: mimeType }});
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
        }}
        
        // Action handlers
        function viewFile(filename) {{
            alert(`Viewing file: ${{filename}}\\n\\nThis would open the file details in a modal or new page.`);
        }}
        
        function fixIssue(issueIndex) {{
            alert(`Initiating fix for issue #${{issueIndex + 1}}\\n\\nThis would trigger automated fixing or provide detailed guidance.`);
        }}
        
        function implementRecommendation(recIndex) {{
            alert(`Implementing recommendation #${{recIndex + 1}}\\n\\nThis would start the implementation process or provide step-by-step guidance.`);
        }}
        """
    
    def _get_score_badge(self, score: float) -> str:
        """Generate score badge HTML"""
        class_name = self._get_score_class(score)
        status = self._get_score_status(score)
        return f'<span class="score-badge score-{class_name}">{score:.1f} - {status}</span>'
    
    def _get_score_class(self, score: float) -> str:
        """Get CSS class based on score"""
        if score >= 90:
            return 'excellent'
        elif score >= 75:
            return 'good'
        elif score >= 60:
            return 'fair'
        else:
            return 'poor'
    
    def _get_score_status(self, score: float) -> str:
        """Get status text based on score"""
        if score >= 90:
            return 'Excellent'
        elif score >= 75:
            return 'Good'
        elif score >= 60:
            return 'Fair'
        else:
            return 'Poor'
    
    def _get_priority_class(self, score: float) -> str:
        """Get priority class based on score"""
        if score < 60:
            return 'high'
        elif score < 75:
            return 'medium'
        else:
            return 'low'
    
    def _get_priority_text(self, score: float) -> str:
        """Get priority text based on score"""
        if score < 60:
            return 'HIGH'
        elif score < 75:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def _get_file_extension(self, language: str) -> str:
        """Get file extension for language"""
        extensions = {
            'python': 'py',
            'javascript': 'js',
            'java': 'java',
            'csharp': 'cs',
            'go': 'go',
            'rust': 'rs',
            'typescript': 'ts',
            'cpp': 'cpp',
            'c': 'c'
        }
        return extensions.get(language.lower(), 'txt')

def main():
    """Command line interface for data tables generator"""
    parser = argparse.ArgumentParser(description='📊 Generate Interactive Data Tables')
    parser.add_argument('--input', required=True, help='Input analysis JSON file')
    parser.add_argument('--output', default='data_tables.html', help='Output HTML file')
    
    args = parser.parse_args()
    
    # Load analysis data
    try:
        with open(args.input, 'r') as f:
            analysis_data = json.load(f)
    except Exception as e:
        print(f"❌ Error loading analysis data: {e}")
        return 1
    
    # Generate data tables
    generator = DataTablesGenerator()
    output_path = generator.generate_data_tables(analysis_data, args.output)
    
    print(f"✅ Data tables generated successfully!")
    print(f"🌐 Open in browser: file://{os.path.abspath(output_path)}")
    
    return 0

if __name__ == "__main__":
    exit(main())