#!/usr/bin/env python3
"""
🚀 Run Complete Sustainability Analysis with Visual Dashboard
Demo script to test the complete analysis and dashboard generation
"""

import os
import sys
from pathlib import Path

# Add current directory to path for testing
current_dir = Path(__file__).parent
sys.path.append(str(current_dir.parent / 'analyzer'))

def run_demo_analysis():
    """Run demo analysis on the current project"""
    
    print("🌱 Sustainability Analysis Demo")
    print("=" * 50)
    
    # Use current project as demo
    project_path = str(current_dir.parent.parent)  # Go up to Tracker directory
    output_dir = current_dir / "demo_output"
    
    print(f"📁 Analyzing project: {project_path}")
    print(f"📊 Output directory: {output_dir}")
    
    # Create demo analysis data
    demo_data = {
        "sustainability_metrics": {
            "overall_score": 78.5,
            "energy_efficiency": 82.3,
            "resource_utilization": 76.8,
            "carbon_footprint": 45.2,
            "performance_optimization": 85.1,
            "sustainable_practices": 72.9
        },
        "analysis_summary": {
            "file_count": 25,
            "execution_time": 1.234,
            "timestamp": "2024-01-15T10:30:00Z",
            "language_breakdown": {
                "javascript": 12,
                "python": 8,
                "html": 3,
                "css": 2
            }
        },
        "issues": [
            {
                "type": "Energy Inefficiency",
                "severity": "high",
                "file": "src/TrainingTab.js",
                "line": 145,
                "message": "Inefficient data processing loop could consume unnecessary CPU cycles",
                "category": "Performance"
            },
            {
                "type": "Memory Leak",
                "severity": "medium", 
                "file": "src/RevenueFteTab.js",
                "line": 89,
                "message": "Event listeners not properly cleaned up on component unmount",
                "category": "Resource Management"
            },
            {
                "type": "Suboptimal Algorithm",
                "severity": "low",
                "file": "backend/server.js",
                "line": 234,
                "message": "O(n²) sorting algorithm could be optimized to O(n log n)",
                "category": "Algorithm"
            }
        ],
        "recommendations": [
            {
                "title": "Implement Virtual Scrolling",
                "description": "Use virtual scrolling in data grids to reduce memory usage and improve performance with large datasets",
                "priority": "high",
                "impact": "High",
                "effort": "Medium",
                "category": "Performance"
            },
            {
                "title": "Add Code Splitting",
                "description": "Implement code splitting to reduce initial bundle size and improve loading performance",
                "priority": "medium",
                "impact": "Medium", 
                "effort": "Low",
                "category": "Optimization"
            },
            {
                "title": "Optimize Bundle Size",
                "description": "Remove unused dependencies and optimize webpack configuration for smaller bundles",
                "priority": "low",
                "impact": "Low",
                "effort": "High",
                "category": "Build Process"
            }
        ]
    }
    
    # Create output directory
    output_dir.mkdir(exist_ok=True)
    
    # Save demo analysis data
    analysis_file = output_dir / "demo_analysis.json"
    with open(analysis_file, 'w') as f:
        import json
        json.dump(demo_data, f, indent=2)
    
    print(f"💾 Demo analysis data saved: {analysis_file}")
    
    # Generate visual dashboard
    try:
        from visual_dashboard_generator import VisualDashboardGenerator
        
        visual_generator = VisualDashboardGenerator()
        visual_dashboard = output_dir / "visual_dashboard.html"
        visual_generator.generate_visual_dashboard(demo_data, str(visual_dashboard))
        print(f"🎨 Visual dashboard generated: {visual_dashboard}")
        
    except ImportError as e:
        print(f"⚠️  Visual dashboard generator not available: {e}")
    
    # Generate data tables
    try:
        from data_tables_generator import DataTablesGenerator
        
        tables_generator = DataTablesGenerator() 
        data_tables = output_dir / "data_tables.html"
        tables_generator.generate_data_tables(demo_data, str(data_tables))
        print(f"📊 Data tables generated: {data_tables}")
        
    except ImportError as e:
        print(f"⚠️  Data tables generator not available: {e}")
    
    # Create simple index page
    index_html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>🌱 Sustainability Analysis Demo</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 2rem;
        }}
        .container {{
            background: white;
            border-radius: 15px;
            padding: 3rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }}
        .score-display {{
            font-size: 4rem;
            font-weight: bold;
            color: #28a745;
            text-align: center;
            margin: 2rem 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1 class="text-center">🌱 Sustainability Analysis Demo</h1>
        <p class="text-center lead">Comprehensive Code Sustainability Assessment</p>
        
        <div class="score-display">{demo_data['sustainability_metrics']['overall_score']}/100</div>
        <p class="text-center fs-4">Overall Sustainability Score</p>
        
        <div class="row mt-5">
            <div class="col-md-4 text-center mb-3">
                <a href="visual_dashboard.html" class="btn btn-primary btn-lg">
                    📊 Visual Dashboard
                </a>
            </div>
            <div class="col-md-4 text-center mb-3">
                <a href="data_tables.html" class="btn btn-success btn-lg">
                    📋 Data Tables  
                </a>
            </div>
            <div class="col-md-4 text-center mb-3">
                <a href="demo_analysis.json" class="btn btn-info btn-lg" download>
                    💾 Raw Data
                </a>
            </div>
        </div>
        
        <hr class="my-5">
        
        <div class="row">
            <div class="col-md-6">
                <h3>🎯 Key Metrics</h3>
                <ul class="list-group">
                    <li class="list-group-item d-flex justify-content-between">
                        Energy Efficiency <strong>{demo_data['sustainability_metrics']['energy_efficiency']}</strong>
                    </li>
                    <li class="list-group-item d-flex justify-content-between">
                        Resource Usage <strong>{demo_data['sustainability_metrics']['resource_utilization']}</strong>
                    </li>
                    <li class="list-group-item d-flex justify-content-between">
                        Performance <strong>{demo_data['sustainability_metrics']['performance_optimization']}</strong>
                    </li>
                </ul>
            </div>
            <div class="col-md-6">
                <h3>📈 Project Stats</h3>
                <ul class="list-group">
                    <li class="list-group-item d-flex justify-content-between">
                        Total Files <strong>{demo_data['analysis_summary']['file_count']}</strong>
                    </li>
                    <li class="list-group-item d-flex justify-content-between">
                        Languages <strong>{len(demo_data['analysis_summary']['language_breakdown'])}</strong>
                    </li>
                    <li class="list-group-item d-flex justify-content-between">
                        Issues Found <strong>{len(demo_data['issues'])}</strong>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</body>
</html>
"""
    
    index_file = output_dir / "index.html"
    with open(index_file, 'w') as f:
        f.write(index_html)
    
    print(f"🏠 Index page created: {index_file}")
    print(f"\n✅ Demo analysis complete!")
    print(f"🌐 Open in browser: file://{index_file.absolute()}")
    
    # Try to open in browser
    try:
        import webbrowser
        webbrowser.open(f"file://{index_file.absolute()}")
        print("🚀 Opening in browser...")
    except Exception as e:
        print(f"⚠️  Could not auto-open browser: {e}")
    
    return str(output_dir)

if __name__ == "__main__":
    run_demo_analysis()