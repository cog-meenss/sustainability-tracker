#!/usr/bin/env python3
"""
Azure DevOps Pipeline Carbon Analysis Helper Script
Extracts and displays carbon footprint metrics from analysis results
"""

import json
import sys
import os

def display_pipeline_summary(data):
    """Display comprehensive carbon analysis summary for pipeline"""
    print("📊 CARBON FOOTPRINT ANALYSIS RESULTS")
    print("=" * 50)
    
    # Language Analysis
    lang_analysis = data.get('language_analysis', {})
    if lang_analysis:
        print(f"🔍 PROJECT ANALYSIS:")
        print("-" * 40)
        print(f"Primary Language:  {lang_analysis.get('primary_language', 'Unknown')}")
        print(f"Total Files:       {lang_analysis.get('total_files', 0):,}")
        print(f"Lines of Code:     {lang_analysis.get('total_lines', 0):,}")
        print(f"File Size:         {lang_analysis.get('total_size_mb', 0):.2f} MB")
    
    # Carbon Footprint
    carbon_data = data.get('carbon_footprint', {})
    if carbon_data:
        print(f"\n⚡ CARBON FOOTPRINT:")
        print("-" * 40)
        print(f"Total Emissions: {carbon_data.get('total_carbon_kg', 0):.6f} kg CO2")
        print(f"Energy Usage:    {carbon_data.get('total_energy_kwh', 0):.6f} kWh")
        print(f"Grid Type:       {carbon_data.get('grid_type', 'Unknown')}")
        print(f"Impact Level:    {carbon_data.get('comparison_metrics', {}).get('impact_level', 'Unknown').upper()}")
        
        # Components Breakdown
        components = carbon_data.get('components', {})
        if components:
            print(f"\n📈 EMISSION BREAKDOWN:")
            print("-" * 40)
            for component, details in components.items():
                if isinstance(details, dict) and details.get('percentage', 0) > 0:
                    name = component.replace('_', ' ').title()
                    percentage = details.get('percentage', 0)
                    carbon_kg = details.get('carbon_kg', 0)
                    print(f"{name.ljust(20)}: {percentage:5.1f}% ({carbon_kg:.6f} kg CO2)")
        
        # Threshold Check
        threshold = float(os.environ.get('CARBON_THRESHOLD', '0.1'))
        current_carbon = carbon_data.get('total_carbon_kg', 0)
        print(f"\n🎯 THRESHOLD ANALYSIS:")
        print("-" * 40)
        print(f"Current Emissions: {current_carbon:.6f} kg CO2")
        print(f"Threshold Limit:   {threshold:.6f} kg CO2")
        
        if current_carbon > threshold:
            print(f"Status: ⚠️  EXCEEDS THRESHOLD by {((current_carbon/threshold - 1) * 100):.1f}%")
            print("Action: Review optimization recommendations below")
        else:
            remaining = ((threshold - current_carbon) / threshold) * 100
            print(f"Status: ✅ WITHIN THRESHOLD ({remaining:.1f}% remaining)")
        
        # Environmental Comparisons
        comparisons = carbon_data.get('comparison_metrics', {}).get('comparisons', {})
        if comparisons:
            print(f"\n🌍 ENVIRONMENTAL COMPARISONS:")
            print("-" * 40)
            
            smartphone = comparisons.get('smartphone_charging', {})
            if smartphone:
                print(f"Smartphone Charges: {smartphone.get('value', 0):.1f}")
            
            car = comparisons.get('car_distance', {})
            if car:
                print(f"Car Distance:       {car.get('value', 0):.3f} km")
            
            light_bulb = comparisons.get('light_bulb', {})
            if light_bulb:
                print(f"60W Light Bulb:     {light_bulb.get('value', 0):.2f} hours")
    
    # Optimization Recommendations
    recommendations = data.get('optimization_recommendations', [])
    if recommendations:
        print(f"\n💡 OPTIMIZATION RECOMMENDATIONS:")
        print("-" * 40)
        for i, rec in enumerate(recommendations[:5], 1):
            print(f"{i}. {rec}")
    
    print("\n" + "=" * 50)

def set_pipeline_variables():
    """Set Azure DevOps pipeline variables from analysis results"""
    report_path = '../carbon-reports/complete_analysis.json'
    
    try:
        with open(report_path, 'r') as f:
            data = json.load(f)
        
        # Extract key metrics
        carbon_kg = data.get('carbon_footprint', {}).get('total_carbon_kg', 0)
        energy_kwh = data.get('carbon_footprint', {}).get('total_energy_kwh', 0)
        files = data.get('language_analysis', {}).get('total_files', 0)
        lang = data.get('language_analysis', {}).get('primary_language', 'Unknown')
        
        # Set Azure DevOps variables
        print('##vso[task.setvariable variable=CarbonFootprint;isOutput=true]{:.6f}'.format(carbon_kg))
        print('##vso[task.setvariable variable=EnergyUsage;isOutput=true]{:.6f}'.format(energy_kwh))
        print('##vso[task.setvariable variable=FilesAnalyzed;isOutput=true]{}'.format(files))
        print('##vso[task.setvariable variable=PrimaryLanguage;isOutput=true]{}'.format(lang))
        
        # Check threshold and set build result
        threshold = float(os.environ.get('CARBON_THRESHOLD', '0.1'))
        if carbon_kg > threshold:
            print('##vso[task.logissue type=warning]Carbon footprint {:.6f} kg CO2 exceeds threshold {:.6f} kg CO2'.format(carbon_kg, threshold))
            print('##vso[task.complete result=SucceededWithIssues;]Carbon analysis completed with threshold exceeded')
        else:
            print('##vso[task.logissue type=info]Carbon footprint {:.6f} kg CO2 is within threshold {:.6f} kg CO2'.format(carbon_kg, threshold))
            
    except Exception as e:
        print('##vso[task.logissue type=error]Failed to set pipeline variables: {}'.format(e))

def start_pipeline_server():
    """Start the pipeline reporter server"""
    import subprocess
    import signal
    import time
    
    try:
        print('🚀 Starting Carbon Footprint Pipeline Reporter...')
        
        # Start the reporter process
        process = subprocess.Popen([
            sys.executable, 'pipeline_reporter.py',
            '--report-path', '../carbon-reports/complete_analysis.json',
            '--port', '8080',
            '--auto-start'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        print(f'📊 Pipeline Reporter started with PID: {process.pid}')
        print('🌐 Dashboard available at: http://localhost:8080')
        
        # Let it run for a few seconds
        time.sleep(3)
        
        # Check if process is still running
        if process.poll() is None:
            print('✅ Reporter is running successfully')
        else:
            stdout, stderr = process.communicate()
            print(f'❌ Reporter process exited with code: {process.returncode}')
            if stderr:
                print(f'Error: {stderr}')
                
    except Exception as e:
        print(f'❌ Error starting pipeline reporter: {e}')

def main():
    """Main function to run the pipeline helper"""
    import sys
    
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == '--set-variables':
            set_pipeline_variables()
            return
        elif sys.argv[1] == '--start-server':
            start_pipeline_server()
            return
    
    # Default behavior - show summary
    print("🚀 Carbon Footprint Pipeline Helper")
    print("=" * 40)
    
    # Check if analysis results exist
    report_path = '../carbon-reports/complete_analysis.json'
    if not os.path.exists(report_path):
        print("❌ No carbon analysis results found")
        print(f"   Expected: {report_path}")
        return
    
    try:
        # Load and display the analysis results
        with open(report_path, 'r') as f:
            data = json.load(f)
        
        # Display the summary
        display_pipeline_summary(data)
        
    except Exception as e:
        print(f"❌ Error processing results: {e}")
        return

if __name__ == "__main__":
    main()

def set_pipeline_variables():
    """Set Azure DevOps pipeline variables from analysis results"""
    
    try:
        with open('carbon-reports/complete_analysis.json', 'r') as f:
            data = json.load(f)
        
        carbon_kg = data.get('carbon_footprint', {}).get('total_carbon_kg', 0)
        energy_kwh = data.get('carbon_footprint', {}).get('total_energy_kwh', 0)
        files = data.get('language_analysis', {}).get('total_files', 0)
        lang = data.get('language_analysis', {}).get('primary_language', 'Unknown')
        
        print(f'##vso[task.setvariable variable=CarbonFootprint;isOutput=true]{carbon_kg:.6f}')
        print(f'##vso[task.setvariable variable=EnergyUsage;isOutput=true]{energy_kwh:.6f}')
        print(f'##vso[task.setvariable variable=FilesAnalyzed;isOutput=true]{files}')
        print(f'##vso[task.setvariable variable=PrimaryLanguage;isOutput=true]{lang}')
        
        # Set build result based on threshold
        threshold = float(os.environ.get('CARBON_THRESHOLD', '0.1'))
        if carbon_kg > threshold:
            print(f'##vso[task.logissue type=warning]Carbon footprint {carbon_kg:.6f} kg CO2 exceeds threshold {threshold:.6f} kg CO2')
            print('##vso[task.complete result=SucceededWithIssues;]Carbon analysis completed with threshold exceeded')
        else:
            print(f'##vso[task.logissue type=info]Carbon footprint {carbon_kg:.6f} kg CO2 is within threshold {threshold:.6f} kg CO2')
            
    except Exception as e:
        print(f'##vso[task.logissue type=error]Failed to set pipeline variables: {e}')

if __name__ == "__main__":
    main()