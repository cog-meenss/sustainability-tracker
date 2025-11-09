#!/usr/bin/env python3
"""
🌱 Quick Test Script for Sustainability Analyzer
Demonstrates the analyzer functionality on the current project
"""

import os
import sys
import json
from pathlib import Path

# Add analyzer to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'analyzer'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'reports'))

def run_quick_test():
    """Run a quick test of the sustainability analyzer"""
    
    print("🌱 Starting Sustainability Analyzer Quick Test")
    print("=" * 50)
    
    try:
        # Import analyzer components
        from sustainability_analyzer import SustainabilityAnalyzer
        from html_generator import SustainabilityDashboardGenerator
        from azure_publisher import AzureDevOpsReportPublisher
        
        # Initialize analyzer
        config_path = os.path.join(os.path.dirname(__file__), 'config', 'analyzer_config.json')
        analyzer = SustainabilityAnalyzer(config_path=config_path)
        
        # Analyze current project (excluding analyzer itself)
        project_path = os.path.join(os.path.dirname(__file__), '..')
        print(f"📁 Analyzing project: {project_path}")
        
        # Run analysis
        result = analyzer.analyze_project(project_path)
        
        # Create output directory
        output_dir = os.path.join(os.path.dirname(__file__), 'test-results')
        os.makedirs(output_dir, exist_ok=True)
        
        # Save JSON results
        analysis_data = {
            'sustainability_metrics': result.metrics.to_dict(),
            'analysis_summary': {
                'file_count': result.file_count,
                'language_breakdown': result.language_breakdown,
                'execution_time': result.execution_time,
                'timestamp': result.timestamp
            },
            'issues': result.issues,
            'recommendations': result.recommendations
        }
        
        json_path = os.path.join(output_dir, 'analysis_results.json')
        with open(json_path, 'w') as f:
            json.dump(analysis_data, f, indent=2)
        
        print(f"💾 Analysis results saved to: {json_path}")
        
        # Generate HTML dashboard
        dashboard_generator = SustainabilityDashboardGenerator()
        html_path = os.path.join(output_dir, 'sustainability_dashboard.html')
        dashboard_generator.generate_dashboard(analysis_data, html_path, 'comprehensive')
        
        print(f"📊 Dashboard generated: {html_path}")
        
        # Generate Azure DevOps reports
        azure_publisher = AzureDevOpsReportPublisher()
        azure_reports = azure_publisher.publish_report(analysis_data, output_dir)
        
        print(f"☁️  Azure DevOps reports generated:")
        for report_type, path in azure_reports.items():
            print(f"   📄 {report_type}: {path}")
        
        # Print summary
        print("\n🎉 SUSTAINABILITY ANALYSIS COMPLETE!")
        print("=" * 50)
        print(f"📊 Overall Score: {result.metrics.overall_score:.1f}/100")
        print(f"⚡ Energy Efficiency: {result.metrics.energy_efficiency:.1f}/100")
        print(f"💾 Resource Utilization: {result.metrics.resource_utilization:.1f}/100")
        print(f"🌍 Carbon Footprint: {result.metrics.carbon_footprint:.1f}/100 (lower is better)")
        print(f"🚀 Performance: {result.metrics.performance_optimization:.1f}/100")
        print(f"♻️  Practices: {result.metrics.sustainable_practices:.1f}/100")
        print(f"\n📁 Analyzed {result.file_count} files in {result.execution_time:.2f}s")
        print(f"🔍 Found {len(result.issues)} issues")
        print(f"💡 Generated {len(result.recommendations)} recommendations")
        
        if result.recommendations:
            print(f"\n🌟 TOP RECOMMENDATIONS:")
            for i, rec in enumerate(result.recommendations[:3], 1):
                print(f"  {i}. {rec['title']} ({rec['priority']} priority)")
        
        print(f"\n🌐 Open the dashboard: file://{html_path}")
        print(f"📋 View Azure report: file://{azure_reports.get('html_report', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()
        return False

def create_sample_azure_pipeline():
    """Create a sample Azure pipeline configuration"""
    
    pipeline_content = '''# 🌱 Sample Azure DevOps Pipeline with Sustainability Analysis
# Copy this to your azure-pipelines.yml file

trigger:
  branches:
    include:
    - main
    - develop

variables:
  sustainabilityThreshold: 75

pool:
  vmImage: 'ubuntu-latest'

stages:
- stage: Build
  jobs:
  - job: BuildAndTest
    steps:
    - checkout: self
      fetchDepth: 0
    
    - task: UsePythonVersion@0
      inputs:
        versionSpec: '3.9'
    
    - script: |
        pip install -r sustainability-analyzer/requirements.txt
      displayName: 'Install Dependencies'
    
    - script: |
        mkdir -p $(Build.ArtifactStagingDirectory)/sustainability-reports
        
        # Run sustainability analysis
        python sustainability-analyzer/analyzer/sustainability_analyzer.py \\
          --path $(Build.SourcesDirectory) \\
          --output $(Build.ArtifactStagingDirectory)/sustainability-reports/analysis.json \\
          --format json
        
        # Generate reports
        python sustainability-analyzer/reports/html_generator.py \\
          --input $(Build.ArtifactStagingDirectory)/sustainability-reports/analysis.json \\
          --output $(Build.ArtifactStagingDirectory)/sustainability-reports/dashboard.html
        
        python sustainability-analyzer/reports/azure_publisher.py \\
          --input $(Build.ArtifactStagingDirectory)/sustainability-reports/analysis.json \\
          --output $(Build.ArtifactStagingDirectory)/sustainability-reports/
      displayName: 'Run Sustainability Analysis'
    
    - task: PublishBuildArtifacts@1
      inputs:
        PathtoPublish: '$(Build.ArtifactStagingDirectory)/sustainability-reports'
        ArtifactName: 'SustainabilityReports'
      displayName: 'Publish Reports'
'''
    
    sample_path = os.path.join(os.path.dirname(__file__), 'sample-azure-pipelines.yml')
    with open(sample_path, 'w') as f:
        f.write(pipeline_content)
    
    print(f"📝 Sample Azure pipeline created: {sample_path}")

if __name__ == "__main__":
    print("🚀 Sustainability Code Evaluation Analyzer")
    print("Testing framework components...")
    
    # Run the test
    success = run_quick_test()
    
    # Create sample pipeline
    create_sample_azure_pipeline()
    
    if success:
        print("\n✅ All tests completed successfully!")
        print("📖 Check the README.md for detailed usage instructions")
        exit(0)
    else:
        print("\n❌ Some tests failed")
        exit(1)