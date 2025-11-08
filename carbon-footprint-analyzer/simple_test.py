#!/usr/bin/env python3
"""
Simple test for the Carbon Footprint Analyzer using the Tracker project
"""

import sys
import os
from pathlib import Path

# Add src directory to Python path
project_root = Path(__file__).parent
src_path = project_root / 'src'
sys.path.insert(0, str(src_path))

def test_basic_functionality():
    """Test basic functionality without complex imports"""
    
    print("🌱 Testing Carbon Footprint Analyzer - Basic Test")
    print("="*60)
    
    try:
        # Test language detection
        print("1️⃣ Testing LanguageDetector...")
        from core.detector import LanguageDetector
        
        detector = LanguageDetector()
        
        # Test with the Tracker project
        tracker_path = project_root.parent
        print(f"   Analyzing: {tracker_path}")
        
        language_data = detector.detect_languages(tracker_path)
        
        print(f"   ✅ Primary language: {language_data.get('primary_language', 'Unknown')}")
        print(f"   ✅ Total files: {language_data.get('total_files', 0)}")
        print(f"   ✅ Project type: {language_data.get('project_type', 'Unknown')}")
        
        languages = language_data.get('languages', {})
        print(f"   ✅ Languages found: {list(languages.keys())}")
        
        print("\n2️⃣ Testing CarbonCalculator...")
        from core.metrics import CarbonCalculator
        
        calculator = CarbonCalculator()
        
        # Create sample analysis data
        sample_analysis = {
            'language_detection': language_data,
            'project_structure': {
                'total_files': language_data.get('total_files', 0),
                'file_complexities': {}
            },
            'dependencies': {
                'total_dependencies': 15,
                'heavy_dependencies': ['react', '@mui/x-data-grid', 'exceljs']
            },
            'framework_info': {
                'detected_frameworks': ['react', 'express']
            }
        }
        
        carbon_results = calculator.calculate_carbon_footprint(sample_analysis)
        
        carbon_kg = carbon_results.get('total_carbon_kg', 0)
        energy_kwh = carbon_results.get('total_energy_kwh', 0)
        
        print(f"   ✅ Carbon emissions calculated: {carbon_kg:.6f} kg CO2")
        print(f"   ✅ Energy consumption: {energy_kwh:.6f} kWh")
        
        print("\n3️⃣ Testing ReportGenerator...")
        from core.reporter import ReportGenerator
        
        reporter = ReportGenerator()
        
        # Combine results
        complete_results = {
            'language_detection': language_data,
            'carbon_footprint': carbon_results,
            'analysis_summary': {
                'primary_language': language_data.get('primary_language', 'Unknown'),
                'total_files': language_data.get('total_files', 0),
                'impact_level': carbon_results.get('comparison_metrics', {}).get('impact_level', 'medium'),
                'carbon_emissions_kg': carbon_kg,
                'energy_consumption_kwh': energy_kwh
            },
            'recommendations': [
                '📦 Consider reducing bundle size by removing unused dependencies',
                '⚡ Implement code splitting for better performance',
                '🔄 Use React.memo for component optimization'
            ]
        }
        
        # Generate JSON report
        json_report = reporter.generate_report(
            complete_results,
            report_type='executive_summary',
            output_format='json'
        )
        
        print(f"   ✅ JSON report generated ({len(json_report)} characters)")
        
        # Save report
        output_dir = project_root / 'simple_test_results'
        output_dir.mkdir(exist_ok=True)
        
        report_file = output_dir / 'carbon_analysis.json'
        with open(report_file, 'w') as f:
            f.write(json_report)
        
        print(f"   ✅ Report saved: {report_file}")
        
        # Generate HTML report
        html_report = reporter.generate_report(
            complete_results,
            report_type='executive_summary',
            output_format='html'
        )
        
        html_file = output_dir / 'carbon_analysis.html'
        with open(html_file, 'w') as f:
            f.write(html_report)
        
        print(f"   ✅ HTML report saved: {html_file}")
        
        print("\n4️⃣ Testing GenericAnalyzer...")
        from analyzers.generic import GenericAnalyzer
        
        analyzer = GenericAnalyzer(tracker_path, {})
        
        # Get some basic stats
        js_files = list(tracker_path.rglob("*.js"))[:5]  # Test with first 5 JS files
        
        if js_files:
            sample_file = js_files[0]
            complexity = analyzer._calculate_file_complexity(sample_file)
            
            print(f"   ✅ Analyzed file: {sample_file.name}")
            print(f"   ✅ Lines: {complexity.get('lines', 0)}")
            print(f"   ✅ Complexity score: {complexity.get('complexity_score', 0):.2f}")
        else:
            print("   ✅ No JS files found to analyze")
        
        print("\n🎉 ALL BASIC TESTS PASSED!")
        print("\nSummary:")
        print(f"   • Project analyzed: {tracker_path.name}")
        print(f"   • Primary language: {language_data.get('primary_language', 'Unknown')}")
        print(f"   • Total files: {language_data.get('total_files', 0):,}")
        print(f"   • Carbon footprint: {carbon_kg:.6f} kg CO2")
        print(f"   • Energy consumption: {energy_kwh:.6f} kWh")
        print(f"   • Impact level: {carbon_results.get('comparison_metrics', {}).get('impact_level', 'unknown').title()}")
        
        # Show comparison metrics
        comparisons = carbon_results.get('comparison_metrics', {}).get('comparisons', {})
        if comparisons:
            print(f"\n🌍 Real-world comparisons:")
            if 'smartphone_charging' in comparisons:
                charges = comparisons['smartphone_charging']['value']
                print(f"   • Equivalent to {charges:.1f} smartphone charges")
            if 'car_distance' in comparisons:
                distance = comparisons['car_distance']['value']
                print(f"   • Equivalent to {distance:.3f} km by car")
        
        print(f"\n📄 Reports saved in: {output_dir}")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_basic_functionality()
    
    if success:
        print(f"\n✅ Carbon Footprint Analyzer is working correctly!")
        print(f"🌐 Open simple_test_results/carbon_analysis.html to view the report")
    else:
        print(f"\n❌ Tests failed. Please check the errors above.")
    
    sys.exit(0 if success else 1)