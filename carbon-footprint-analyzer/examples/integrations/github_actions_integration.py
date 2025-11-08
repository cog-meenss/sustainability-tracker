#!/usr/bin/env python3
"""
GitHub Actions workflow integration for carbon footprint analysis
"""

import os
import json
import sys
from pathlib import Path

# Add analyzer to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))
from carbon_analyzer import CarbonAnalyzer

def main():
    """Main function for GitHub Actions integration"""
    
    # Get environment variables
    workspace_path = os.environ.get('GITHUB_WORKSPACE', '.')
    output_path = os.environ.get('CARBON_OUTPUT_PATH', './carbon-reports')
    config_path = os.environ.get('CARBON_CONFIG_PATH')
    grid_type = os.environ.get('CARBON_GRID_TYPE', 'global_average')
    threshold_kg = float(os.environ.get('CARBON_THRESHOLD_KG', '0.1'))
    
    print(f"🌱 Running Carbon Footprint Analysis")
    print(f"   Workspace: {workspace_path}")
    print(f"   Output: {output_path}")
    print(f"   Grid Type: {grid_type}")
    print(f"   Threshold: {threshold_kg} kg CO2")
    
    try:
        # Initialize analyzer
        config_file = Path(config_path) if config_path else None
        analyzer = CarbonAnalyzer(config_file)
        
        # Run analysis
        results = analyzer.analyze_project(
            project_path=workspace_path,
            output_path=output_path,
            report_formats=['json', 'html'],
            grid_type=grid_type,
            include_detailed_breakdown=True
        )
        
        # Extract key metrics
        carbon_kg = results.get('carbon_footprint', {}).get('total_carbon_kg', 0)
        energy_kwh = results.get('carbon_footprint', {}).get('total_energy_kwh', 0)
        impact_level = results.get('carbon_footprint', {}).get('comparison_metrics', {}).get('impact_level', 'unknown')
        
        # Set GitHub Actions outputs
        set_github_output('carbon_kg', carbon_kg)
        set_github_output('energy_kwh', energy_kwh)
        set_github_output('impact_level', impact_level)
        set_github_output('reports_path', output_path)
        
        # Create PR comment data
        pr_comment = create_pr_comment(results)
        set_github_output('pr_comment', pr_comment)
        
        # Check against threshold
        if carbon_kg > threshold_kg:
            print(f"❌ Carbon footprint ({carbon_kg:.6f} kg CO2) exceeds threshold ({threshold_kg} kg)")
            
            # Create summary for GitHub Actions
            summary = f"""
## ⚠️ Carbon Footprint Alert

**Current Emissions:** {carbon_kg:.6f} kg CO2  
**Threshold:** {threshold_kg} kg CO2  
**Status:** EXCEEDED by {((carbon_kg/threshold_kg - 1) * 100):.1f}%

### Optimization Recommendations:
"""
            recommendations = results.get('recommendations', [])[:3]
            for i, rec in enumerate(recommendations, 1):
                summary += f"\n{i}. {rec}"
            
            set_github_output('threshold_exceeded', 'true')
            set_github_output('alert_summary', summary)
            
            # Fail the workflow if threshold exceeded
            sys.exit(1)
        else:
            print(f"✅ Carbon footprint ({carbon_kg:.6f} kg CO2) is within threshold")
            set_github_output('threshold_exceeded', 'false')
            
    except Exception as e:
        print(f"❌ Carbon analysis failed: {e}")
        set_github_output('error', str(e))
        sys.exit(1)

def set_github_output(name: str, value: str):
    """Set GitHub Actions output variable"""
    github_output = os.environ.get('GITHUB_OUTPUT')
    if github_output:
        with open(github_output, 'a') as f:
            f.write(f"{name}={value}\n")
    else:
        print(f"::set-output name={name}::{value}")

def create_pr_comment(results: dict) -> str:
    """Create formatted PR comment with analysis results"""
    
    carbon_data = results.get('carbon_footprint', {})
    summary = results.get('analysis_summary', {})
    
    comment = f"""
## 🌱 Carbon Footprint Analysis

| Metric | Value |
|--------|-------|
| **Carbon Emissions** | {carbon_data.get('total_carbon_kg', 0):.6f} kg CO2 |
| **Energy Consumption** | {carbon_data.get('total_energy_kwh', 0):.6f} kWh |
| **Impact Level** | {summary.get('impact_level', 'unknown').title()} |
| **Primary Language** | {summary.get('primary_language', 'Unknown')} |
| **Files Analyzed** | {summary.get('total_files', 0):,} |

### 🔍 Component Breakdown
"""
    
    components = carbon_data.get('components', {})
    for component, data in components.items():
        if isinstance(data, dict) and data.get('percentage', 0) > 0:
            percentage = data.get('percentage', 0)
            comment += f"- **{component.title().replace('_', ' ')}**: {percentage:.1f}%\\n"
    
    # Add optimization potential
    optimization = carbon_data.get('optimization_potential', {})
    potential = optimization.get('potential_reduction_percentage', 0)
    if potential > 0:
        comment += f"\\n### ⚡ Optimization Potential\\n"
        comment += f"Up to **{potential:.1f}%** carbon reduction possible\\n"
    
    # Add top recommendations
    recommendations = results.get('recommendations', [])[:3]
    if recommendations:
        comment += f"\\n### 💡 Top Recommendations\\n"
        for i, rec in enumerate(recommendations, 1):
            comment += f"{i}. {rec}\\n"
    
    comment += f"\\n---\\n*Analysis by Carbon Footprint Analyzer v1.0.0*"
    
    return comment

if __name__ == '__main__':
    main()