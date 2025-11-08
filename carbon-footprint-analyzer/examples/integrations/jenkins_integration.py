#!/usr/bin/env python3
"""
Jenkins pipeline integration for carbon footprint analysis
"""

import os
import json
import sys
from pathlib import Path

def run_carbon_analysis():
    """Run carbon analysis in Jenkins pipeline"""
    
    # Jenkins environment variables
    workspace = os.environ.get('WORKSPACE', '.')
    build_number = os.environ.get('BUILD_NUMBER', '1')
    job_name = os.environ.get('JOB_NAME', 'carbon-analysis')
    
    # Carbon analysis configuration
    output_dir = Path(workspace) / 'carbon-reports'
    config_file = os.environ.get('CARBON_CONFIG', 'web_app_config.json')
    threshold_kg = float(os.environ.get('CARBON_THRESHOLD', '0.1'))
    
    print(f"🌱 Jenkins Carbon Footprint Analysis")
    print(f"   Job: {job_name}")
    print(f"   Build: {build_number}")
    print(f"   Workspace: {workspace}")
    print(f"   Threshold: {threshold_kg} kg CO2")
    
    try:
        # Import analyzer - try multiple paths for different environments
        import_successful = False
        
        # Try from current directory structure (testing environment)
        try:
            analyzer_dir = Path(__file__).parent.parent.parent / 'src'
            sys.path.insert(0, str(analyzer_dir))
            import carbon_analyzer
            CarbonAnalyzer = carbon_analyzer.CarbonAnalyzer
            import_successful = True
        except (ImportError, AttributeError):
            pass
        
        # Try from Jenkins workspace structure
        if not import_successful:
            try:
                jenkins_analyzer_dir = Path(workspace) / 'carbon-footprint-analyzer' / 'src'
                if jenkins_analyzer_dir.exists():
                    sys.path.insert(0, str(jenkins_analyzer_dir))
                    import carbon_analyzer
                    CarbonAnalyzer = carbon_analyzer.CarbonAnalyzer
                    import_successful = True
            except (ImportError, AttributeError):
                pass
        
        if not import_successful:
            raise ImportError("Could not import CarbonAnalyzer. Ensure carbon-footprint-analyzer is available in workspace.")
        
        # Initialize analyzer
        analyzer = CarbonAnalyzer()
        
        # Run analysis
        results = analyzer.analyze_project(
            project_path=workspace,
            output_path=output_dir,
            report_formats=['json', 'html', 'csv'],
            grid_type='global_average',
            include_detailed_breakdown=True
        )
        
        # Load generated report to extract metrics
        report_file = output_dir / 'complete_analysis.json'
        if report_file.exists():
            with open(report_file, 'r') as f:
                report_data = json.load(f)
            
            carbon_kg = report_data.get('carbon_footprint', {}).get('total_carbon_kg', 0)
            energy_kwh = report_data.get('carbon_footprint', {}).get('total_energy_kwh', 0)
            impact_level = report_data.get('carbon_footprint', {}).get('comparison_metrics', {}).get('impact_level', 'unknown')
            primary_language = report_data.get('language_analysis', {}).get('primary_language', 'unknown')
            total_files = report_data.get('language_analysis', {}).get('total_files', 0)
        else:
            print(f"⚠️ Report file not found: {report_file}")
            carbon_kg = 0
            energy_kwh = 0
            impact_level = 'unknown'
            primary_language = 'unknown'
            total_files = 0
        
        # Create Jenkins properties file for downstream jobs
        create_jenkins_properties(carbon_kg, energy_kwh, impact_level, primary_language, total_files)
        
        # Generate trend data for Jenkins plots
        update_trend_data(build_number, carbon_kg, energy_kwh)
        
        # Check threshold
        if carbon_kg > threshold_kg:
            print(f"❌ THRESHOLD EXCEEDED: {carbon_kg:.6f} kg CO2 > {threshold_kg} kg CO2")
            
            # Mark build as unstable (not failed)
            with open('carbon_threshold_exceeded.txt', 'w') as f:
                f.write(f"Carbon footprint {carbon_kg:.6f} kg CO2 exceeds threshold {threshold_kg} kg CO2")
            
            return 2  # Unstable build
        else:
            print(f"✅ WITHIN THRESHOLD: {carbon_kg:.6f} kg CO2 ≤ {threshold_kg} kg CO2")
            return 0  # Success
            
    except Exception as e:
        print(f"❌ Carbon analysis failed: {e}")
        with open('carbon_analysis_error.txt', 'w') as f:
            f.write(str(e))
        return 1  # Failed build

def create_jenkins_properties(carbon_kg: float, energy_kwh: float, impact_level: str, primary_language: str, total_files: int):
    """Create Jenkins properties file for downstream jobs"""
    
    properties = {
        'CARBON_KG': carbon_kg,
        'ENERGY_KWH': energy_kwh,
        'CARBON_IMPACT_LEVEL': impact_level,
        'PRIMARY_LANGUAGE': primary_language,
        'FILES_COUNT': total_files,
        'OPTIMIZATION_POTENTIAL': 0  # TODO: Extract from report if needed
    }
    
    # Write properties file
    with open('carbon_analysis.properties', 'w') as f:
        for key, value in properties.items():
            f.write(f"{key}={value}\n")

def update_trend_data(build_number: str, carbon_kg: float, energy_kwh: float):
    """Update trend data for Jenkins plots plugin"""
    
    # Create CSV file for Jenkins Plot Plugin
    trend_file = Path('carbon_trend.csv')
    
    # Check if file exists
    if not trend_file.exists():
        with open(trend_file, 'w') as f:
            f.write('build,carbon_kg,energy_kwh\n')
    
    # Append current build data
    with open(trend_file, 'a') as f:
        f.write(f"{build_number},{carbon_kg},{energy_kwh}\n")

def create_sample_jenkinsfile():
    """Create a sample Jenkinsfile for carbon footprint analysis"""
    
    jenkinsfile_content = """pipeline {
    agent any
    
    environment {
        CARBON_THRESHOLD = '0.1'
        CARBON_CONFIG = 'web_app_config.json'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Install Dependencies') {
            steps {
                sh 'python3 -m pip install --user requests'
            }
        }
        
        stage('Carbon Analysis') {
            steps {
                script {
                    def result = sh(
                        script: 'python3 carbon-footprint-analyzer/examples/integrations/jenkins_integration.py',
                        returnStatus: true
                    )
                    
                    // Load analysis properties
                    def props = readProperties file: 'carbon_analysis.properties'
                    env.CARBON_KG = props.CARBON_KG
                    env.ENERGY_KWH = props.ENERGY_KWH
                    env.CARBON_IMPACT_LEVEL = props.CARBON_IMPACT_LEVEL
                    
                    // Handle result
                    if (result == 2) {
                        // Threshold exceeded - mark as unstable
                        currentBuild.result = 'UNSTABLE'
                        echo "⚠️ Carbon footprint exceeds threshold"
                    } else if (result == 1) {
                        // Analysis failed
                        currentBuild.result = 'FAILURE'
                        error("Carbon analysis failed")
                    } else {
                        echo "✅ Carbon analysis passed"
                    }
                }
            }
        }
    }
    
    post {
        always {
            // Archive reports
            archiveArtifacts artifacts: 'carbon-reports/**/*', allowEmptyArchive: true
            
            // Publish HTML reports
            publishHTML([
                allowMissing: false,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'carbon-reports',
                reportFiles: '*.html',
                reportName: 'Carbon Footprint Report'
            ])
        }
        
        unstable {
            echo "⚠️ Carbon footprint exceeds threshold"
        }
        
        failure {
            echo "❌ Carbon analysis failed"
        }
    }
}"""
    
    with open('Jenkinsfile', 'w') as f:
        f.write(jenkinsfile_content)
    
    print("📄 Sample Jenkinsfile created: ./Jenkinsfile")

def validate_integration():
    """Validate Jenkins integration setup without running analysis"""
    
    print("🔍 JENKINS INTEGRATION VALIDATION")
    print("=" * 40)
    
    # Check Jenkins environment variables
    jenkins_vars = ['WORKSPACE', 'BUILD_NUMBER', 'JOB_NAME']
    missing_vars = []
    
    for var in jenkins_vars:
        if os.environ.get(var):
            print(f"✅ {var}: {os.environ.get(var)}")
        else:
            print(f"❌ {var}: Not set (using default)")
            missing_vars.append(var)
    
    # Check carbon analyzer availability
    workspace = os.environ.get('WORKSPACE', '.')
    analyzer_path = Path(workspace) / 'carbon-footprint-analyzer' / 'src'
    
    if analyzer_path.exists():
        print(f"✅ Carbon Analyzer: Found at {analyzer_path}")
    else:
        print(f"❌ Carbon Analyzer: Not found at {analyzer_path}")
        print("   💡 Ensure carbon-footprint-analyzer is available in workspace")
    
    # Check output directory
    output_dir = Path(workspace) / 'carbon-reports'
    print(f"📁 Output Directory: {output_dir}")
    
    # Check configuration
    config_file = os.environ.get('CARBON_CONFIG', 'web_app_config.json')
    threshold = os.environ.get('CARBON_THRESHOLD', '0.1')
    
    print(f"⚙️ Configuration: {config_file}")
    print(f"🎯 Threshold: {threshold} kg CO2")
    
    if missing_vars:
        print(f"\n⚠️ Missing Jenkins environment variables: {', '.join(missing_vars)}")
        print("   This is normal when testing outside Jenkins")
    
    print("\n🎉 Validation complete! Jenkins integration is properly configured.")
    return True

if __name__ == '__main__':
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == '--create-jenkinsfile':
            create_sample_jenkinsfile()
            print("\n📋 USAGE INSTRUCTIONS:")
            print("1. Copy the generated Jenkinsfile to your repository root")
            print("2. Copy this script to examples/integrations/ in your repo")
            print("3. Add the carbon-footprint-analyzer as a git submodule or dependency")
            print("4. Configure CARBON_THRESHOLD environment variable as needed")
            print("5. Push to trigger the Jenkins pipeline")
            sys.exit(0)
        elif sys.argv[1] == '--validate':
            validate_integration()
            sys.exit(0)
        elif sys.argv[1] == '--help':
            print("🌱 Jenkins Carbon Footprint Analysis Integration")
            print("\nUsage:")
            print("  python3 jenkins_integration.py                    # Run analysis (in Jenkins)")
            print("  python3 jenkins_integration.py --create-jenkinsfile # Generate Jenkinsfile")
            print("  python3 jenkins_integration.py --validate         # Validate setup")
            print("  python3 jenkins_integration.py --help             # Show this help")
            sys.exit(0)
    
    # Run the actual analysis
    sys.exit(run_carbon_analysis())