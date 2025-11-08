#!/usr/bin/env python3
"""
Test the Carbon Footprint Analyzer with the Tracker project
"""

import sys
import json
from pathlib import Path

# Add analyzer to path
analyzer_root = Path(__file__).parent
sys.path.insert(0, str(analyzer_root / 'src'))

try:
    from src.carbon_analyzer import CarbonAnalyzer
    print("✅ Successfully imported CarbonAnalyzer")
except ImportError as e:
    print(f"❌ Failed to import CarbonAnalyzer: {e}")
    sys.exit(1)

def test_tracker_project():
    """Test the analyzer with the Tracker project"""
    
    # Path to the Tracker project (parent directory)
    tracker_path = analyzer_root.parent
    
    print(f"🔍 Testing Carbon Footprint Analyzer with Tracker project")
    print(f"   Tracker path: {tracker_path}")
    print(f"   Analyzer path: {analyzer_root}")
    
    try:
        # Initialize analyzer with web app config
        config_path = analyzer_root / 'examples' / 'configs' / 'web_app_config.json'
        analyzer = CarbonAnalyzer(config_path if config_path.exists() else None)
        
        print("✅ CarbonAnalyzer initialized successfully")
        
        # Test language detection first
        print("\n📊 Testing language detection...")
        language_data = analyzer.language_detector.detect_languages(tracker_path)
        
        print(f"   Primary language: {language_data.get('primary_language', 'Unknown')}")
        print(f"   Total files: {language_data.get('total_files', 0)}")
        print(f"   Project type: {language_data.get('project_type', 'Unknown')}")
        print(f"   Complexity: {language_data.get('complexity_indicator', 'Unknown')}")
        
        detected_languages = language_data.get('languages', {})
        if detected_languages:
            print("   Languages found:")
            for lang, stats in detected_languages.items():
                print(f"     • {lang}: {stats['files']} files")
        
        # Test full analysis
        print("\n🌱 Running full carbon footprint analysis...")
        
        # Create output directory
        output_path = analyzer_root / 'test_results'
        output_path.mkdir(exist_ok=True)
        
        results = analyzer.analyze_project(
            project_path=tracker_path,
            output_path=output_path,
            report_formats=['json', 'html'],
            grid_type='global_average',
            include_detailed_breakdown=True
        )
        
        print("✅ Full analysis completed successfully!")
        
        # Display key results
        display_analysis_results(results)
        
        # Test code snippet analysis
        print("\n🔬 Testing code snippet analysis...")
        test_code_snippet_analysis(analyzer)
        
        return True
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def display_analysis_results(results):
    """Display key analysis results"""
    
    carbon_data = results.get('carbon_footprint', {})
    summary = results.get('analysis_summary', {})
    
    print(f"\n📊 ANALYSIS RESULTS:")
    print(f"   🌱 Carbon Emissions: {carbon_data.get('total_carbon_kg', 0):.6f} kg CO2")
    print(f"   ⚡ Energy Consumption: {carbon_data.get('total_energy_kwh', 0):.6f} kWh")
    print(f"   📈 Impact Level: {summary.get('impact_level', 'unknown').title()}")
    print(f"   💻 Primary Language: {summary.get('primary_language', 'Unknown')}")
    print(f"   📁 Files Analyzed: {summary.get('total_files', 0):,}")
    
    # Component breakdown
    components = carbon_data.get('components', {})
    if components:
        print(f"\n🔍 COMPONENT BREAKDOWN:")
        for component, data in components.items():
            if isinstance(data, dict) and data.get('percentage', 0) > 0:
                percentage = data.get('percentage', 0)
                energy = data.get('energy_kwh', 0)
                print(f"   • {component.title().replace('_', ' ')}: {percentage:.1f}% ({energy:.6f} kWh)")
    
    # Language breakdown
    language_breakdown = carbon_data.get('language_breakdown', {})
    if language_breakdown:
        print(f"\n💻 LANGUAGE BREAKDOWN:")
        for lang, data in language_breakdown.items():
            files = data.get('files', 0)
            carbon = data.get('estimated_carbon_kg', 0)
            percentage = data.get('percentage_of_total', 0)
            print(f"   • {lang}: {files} files, {carbon:.8f} kg CO2 ({percentage:.1f}%)")
    
    # Optimization potential
    optimization = carbon_data.get('optimization_potential', {})
    potential = optimization.get('potential_reduction_percentage', 0)
    if potential > 0:
        print(f"\n⚡ OPTIMIZATION POTENTIAL:")
        print(f"   • Potential Reduction: {potential:.1f}%")
        print(f"   • Estimated Savings: {optimization.get('total_potential_reduction_kg', 0):.6f} kg CO2")
    
    # Top recommendations
    recommendations = results.get('recommendations', [])
    if recommendations:
        print(f"\n💡 TOP RECOMMENDATIONS:")
        for i, rec in enumerate(recommendations[:5], 1):
            print(f"   {i}. {rec}")

def test_code_snippet_analysis(analyzer):
    """Test code snippet analysis with sample code"""
    
    test_snippets = [
        {
            'language': 'javascript',
            'code': '''
// React component example
import React, { useState, useEffect } from 'react';
import { DataGrid } from '@mui/x-data-grid';

const ExcelProcessor = () => {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(false);
    
    useEffect(() => {
        fetchData();
    }, []);
    
    const fetchData = async () => {
        setLoading(true);
        try {
            const response = await fetch('/api/data');
            const result = await response.json();
            setData(result);
        } catch (error) {
            console.error('Error:', error);
        } finally {
            setLoading(false);
        }
    };
    
    return (
        <div>
            <DataGrid 
                rows={data} 
                loading={loading}
                pageSize={100}
            />
        </div>
    );
};

export default ExcelProcessor;
'''
        },
        {
            'language': 'python',
            'code': '''
import pandas as pd
import numpy as np
from pathlib import Path

def process_excel_data(file_path, sheet_name='Sheet1'):
    """Process Excel data and return cleaned results"""
    
    # Read Excel file
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    
    # Data cleaning
    df = df.dropna()
    df = df.drop_duplicates()
    
    # Complex calculations
    for column in df.select_dtypes(include=[np.number]).columns:
        df[f'{column}_normalized'] = (df[column] - df[column].mean()) / df[column].std()
    
    # Group by operations
    summary = df.groupby('category').agg({
        'value': ['mean', 'sum', 'count'],
        'date': ['min', 'max']
    }).round(2)
    
    return {
        'processed_data': df.to_dict('records'),
        'summary': summary.to_dict(),
        'row_count': len(df),
        'column_count': len(df.columns)
    }

# Example usage
if __name__ == '__main__':
    result = process_excel_data('data/input.xlsx')
    print(f"Processed {result['row_count']} rows")
'''
        }
    ]
    
    for snippet in test_snippets:
        language = snippet['language']
        code = snippet['code']
        
        print(f"   Testing {language} snippet ({len(code)} characters)...")
        
        try:
            results = analyzer.analyze_code_snippet(code, language, f"test.{language[:2]}")
            
            carbon_kg = results.get('carbon_footprint', {}).get('total_carbon_kg', 0)
            complexity = results.get('code_analysis', {}).get('complexity_score', 0)
            
            print(f"     • Carbon: {carbon_kg:.8f} kg CO2")
            print(f"     • Complexity: {complexity:.2f}")
            
            recommendations = results.get('recommendations', [])
            if recommendations:
                print(f"     • Recommendations: {len(recommendations)} found")
                print(f"       - {recommendations[0]}")
            
        except Exception as e:
            print(f"     ❌ Failed: {e}")

def test_individual_components():
    """Test individual analyzer components"""
    
    print("\n🔧 Testing individual components...")
    
    try:
        # Test LanguageDetector
        from src.core.detector import LanguageDetector
        detector = LanguageDetector()
        
        supported_languages = detector.get_supported_languages()
        print(f"   ✅ LanguageDetector: {len(supported_languages)} languages supported")
        
        # Test CarbonCalculator
        from src.core.metrics import CarbonCalculator
        calculator = CarbonCalculator()
        
        # Test with sample data
        sample_analysis = {
            'language_detection': {
                'primary_language': 'javascript',
                'languages': {'javascript': {'files': 10, 'size_bytes': 50000}},
                'complexity_indicator': 'medium'
            },
            'project_structure': {
                'total_files': 10,
                'file_complexities': {}
            },
            'dependencies': {'total_dependencies': 20, 'heavy_dependencies': ['react', 'lodash']},
            'framework_info': {'detected_frameworks': ['react', 'express']}
        }
        
        carbon_result = calculator.calculate_carbon_footprint(sample_analysis)
        print(f"   ✅ CarbonCalculator: {carbon_result.get('total_carbon_kg', 0):.6f} kg CO2 calculated")
        
        # Test ReportGenerator
        from src.core.reporter import ReportGenerator
        reporter = ReportGenerator()
        
        # Generate a test report
        test_results = {
            'carbon_footprint': carbon_result,
            'analysis_summary': {
                'primary_language': 'javascript',
                'total_files': 10,
                'impact_level': 'low'
            },
            'recommendations': ['Test recommendation 1', 'Test recommendation 2']
        }
        
        report_content = reporter.generate_report(test_results, 'executive_summary', 'json')
        print(f"   ✅ ReportGenerator: Generated report ({len(report_content)} characters)")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Component test failed: {e}")
        return False

def run_comprehensive_test():
    """Run comprehensive test suite"""
    
    print("="*80)
    print("🌱 CARBON FOOTPRINT ANALYZER - COMPREHENSIVE TEST")
    print("="*80)
    
    test_results = []
    
    # Test 1: Component tests
    print("\n1️⃣ Testing individual components...")
    component_success = test_individual_components()
    test_results.append(('Component Tests', component_success))
    
    # Test 2: Tracker project analysis
    print("\n2️⃣ Testing with Tracker project...")
    tracker_success = test_tracker_project()
    test_results.append(('Tracker Analysis', tracker_success))
    
    # Results summary
    print("\n" + "="*80)
    print("📊 TEST RESULTS SUMMARY")
    print("="*80)
    
    all_passed = True
    for test_name, success in test_results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"   {test_name}: {status}")
        if not success:
            all_passed = False
    
    if all_passed:
        print(f"\n🎉 ALL TESTS PASSED! The Carbon Footprint Analyzer is working correctly.")
        print(f"\n📄 Check the test_results/ directory for generated reports.")
        print(f"🌐 Open test_results/complete_analysis.html in your browser to view the report.")
    else:
        print(f"\n⚠️  Some tests failed. Please check the error messages above.")
    
    return all_passed

if __name__ == '__main__':
    success = run_comprehensive_test()
    sys.exit(0 if success else 1)