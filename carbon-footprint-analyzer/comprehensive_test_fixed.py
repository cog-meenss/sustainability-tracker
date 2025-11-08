#!/usr/bin/env python3
"""
Comprehensive test suite for the Universal Carbon Footprint Analyzer.
Tests multiple project types and configurations.
"""

import sys
import os

# Add src directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

import json
import tempfile
from pathlib import Path

# Import main analyzer
sys.path.append('.')
from src.carbon_analyzer import CarbonAnalyzer

def create_test_projects():
    """Create sample projects for testing different languages."""
    test_dir = Path("comprehensive_test_projects")
    test_dir.mkdir(exist_ok=True)
    
    projects = {}
    
    # 1. Python Project
    python_dir = test_dir / "python_project"
    python_dir.mkdir(exist_ok=True)
    
    (python_dir / "main.py").write_text("""
import pandas as pd
import numpy as np

def process_data(data):
    # Complex data processing
    for i in range(100):
        data = data * 2
    return data

def analyze_performance():
    data = [i for i in range(1000)]
    processed = process_data(data)
    return sum(processed)

if __name__ == "__main__":
    result = analyze_performance()
    print(f"Analysis complete: {result}")
""")
    
    (python_dir / "requirements.txt").write_text("""
pandas==1.5.0
numpy==1.24.0
requests==2.28.0
""")
    
    projects["python"] = str(python_dir)
    
    # 2. JavaScript Project
    js_dir = test_dir / "javascript_project"
    js_dir.mkdir(exist_ok=True)
    
    (js_dir / "package.json").write_text(json.dumps({
        "name": "test-js-app",
        "version": "1.0.0",
        "dependencies": {
            "express": "^4.18.0",
            "lodash": "^4.17.21",
            "axios": "^1.4.0"
        },
        "scripts": {
            "start": "node server.js"
        }
    }, indent=2))
    
    (js_dir / "server.js").write_text("""
const express = require('express');
const _ = require('lodash');
const axios = require('axios');

const app = express();
const port = 3000;

// Inefficient route handler
app.get('/api/data', async (req, res) => {
    const data = [];
    
    // Inefficient loop
    for (let i = 0; i < 1000; i++) {
        const item = {
            id: i,
            value: Math.random(),
            processed: processValue(i)
        };
        data.push(item);
    }
    
    res.json(data);
});

function processValue(value) {
    // Inefficient processing
    let result = value;
    for (let i = 0; i < 100; i++) {
        result = Math.sqrt(result + 1);
    }
    return result;
}

app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});
""")
    
    projects["javascript"] = str(js_dir)
    
    # 3. Java Project (minimal)
    java_dir = test_dir / "java_project"
    java_dir.mkdir(exist_ok=True)
    
    java_src_dir = java_dir / "src" / "main" / "java"
    java_src_dir.mkdir(parents=True, exist_ok=True)
    
    (java_src_dir / "Application.java").write_text("""
public class Application {
    
    public static void main(String[] args) {
        DataProcessor processor = new DataProcessor();
        processor.processData();
    }
    
    static class DataProcessor {
        
        public void processData() {
            // Inefficient nested loops
            for (int i = 0; i < 100; i++) {
                for (int j = 0; j < 100; j++) {
                    String result = "data_" + i + "_" + j;
                    System.out.println(result.length());
                }
            }
        }
    }
}
""")
    
    projects["java"] = str(java_dir)
    
    return projects

def run_comprehensive_tests():
    """Run tests on multiple project types."""
    print("🧪 COMPREHENSIVE CARBON FOOTPRINT ANALYZER TESTS")
    print("=" * 50)
    
    try:
        # Initialize analyzer
        analyzer = CarbonAnalyzer()
        print("✅ Carbon Analyzer initialized successfully")
        
        # Create test projects
        print("\n📁 Creating test projects...")
        projects = create_test_projects()
        print(f"✅ Created {len(projects)} test projects")
        
        results = {}
        
        # Test each project type
        for project_type, project_path in projects.items():
            print(f"\n🔍 Testing {project_type.upper()} project...")
            print(f"   Path: {project_path}")
            
            try:
                # Create output directory
                output_dir = f"comprehensive_test_results/{project_type}"
                os.makedirs(output_dir, exist_ok=True)
                
                # Analyze project
                result = analyzer.analyze_project(
                    project_path=project_path,
                    output_path=output_dir,
                    report_formats=['json']
                )
                
                results[project_type] = result
                
                # Load the generated report to get detailed results
                report_path = f"{output_dir}/complete_analysis.json"
                if os.path.exists(report_path):
                    with open(report_path, 'r') as f:
                        report_data = json.load(f)
                    
                    # Extract data from the report
                    language = report_data.get('language_analysis', {}).get('primary_language', 'Unknown')
                    files = report_data.get('language_analysis', {}).get('total_files', 0)
                    carbon_data = report_data.get('carbon_footprint', {})
                    carbon = carbon_data.get('total_carbon_kg', 0)
                    energy = carbon_data.get('total_energy_kwh', 0)
                    
                    # Update results with parsed data
                    results[project_type] = {
                        'analysis': {
                            'primary_language': language,
                            'total_files': files
                        },
                        'carbon_footprint': {
                            'total_carbon_kg': carbon,
                            'total_energy_kwh': energy
                        }
                    }
                    
                    print(f"   ✅ Analysis complete!")
                    print(f"   📊 Primary Language: {language}")
                    print(f"   📁 Files Analyzed: {files}")
                    print(f"   🌱 Carbon Footprint: {carbon:.6f} kg CO2")
                    print(f"   ⚡ Energy Usage: {energy:.6f} kWh")
                else:
                    print(f"   ⚠️ Report file not found: {report_path}")
                    results[project_type] = {"error": "Report file not generated"}
                
            except Exception as e:
                print(f"   ❌ Error analyzing {project_type}: {str(e)}")
                results[project_type] = {"error": str(e)}
        
        # Test code snippet analysis
        print(f"\n🔍 Testing CODE SNIPPET analysis...")
        try:
            snippet_result = analyzer.analyze_code_snippet(
                code="""
function fibonacci(n) {
    if (n <= 1) return n;
    return fibonacci(n-1) + fibonacci(n-2);
}

for (let i = 0; i < 30; i++) {
    console.log(fibonacci(i));
}
""",
                language="javascript"
            )
            results["code_snippet"] = snippet_result
            print(f"   ✅ Snippet analysis complete!")
            print(f"   🌱 Carbon Footprint: {snippet_result['carbon_footprint']['total_carbon_kg']:.6f} kg CO2")
        except Exception as e:
            print(f"   ❌ Error analyzing code snippet: {str(e)}")
            results["code_snippet"] = {"error": str(e)}
        
        # Generate overall summary
        print(f"\n📋 COMPREHENSIVE TEST SUMMARY")
        print("=" * 50)
        
        successful_tests = len([r for r in results.values() if "error" not in r])
        total_tests = len(results)
        
        print(f"✅ Successful Tests: {successful_tests}/{total_tests}")
        
        if successful_tests > 0:
            total_files = sum(r.get('analysis', {}).get('total_files', 0) for r in results.values() if "error" not in r and 'analysis' in r)
            total_carbon = sum(r.get('carbon_footprint', {}).get('total_carbon_kg', 0) for r in results.values() if "error" not in r and 'carbon_footprint' in r)
            
            print(f"📁 Total Files Analyzed: {total_files}")
            print(f"🌱 Total Carbon Footprint: {total_carbon:.6f} kg CO2")
            
            print(f"\n🎯 LANGUAGE BREAKDOWN:")
            for project_type, result in results.items():
                if "error" not in result and "analysis" in result:
                    lang = result['analysis'].get('primary_language', 'Unknown')
                    carbon = result['carbon_footprint']['total_carbon_kg']
                    print(f"   • {project_type.title()}: {lang} - {carbon:.6f} kg CO2")
        
        # Save comprehensive results
        results_file = "comprehensive_test_results/comprehensive_results.json"
        os.makedirs(os.path.dirname(results_file), exist_ok=True)
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"\n📄 Detailed results saved to: {results_file}")
        
        if successful_tests == total_tests:
            print(f"\n🎉 ALL COMPREHENSIVE TESTS PASSED!")
        else:
            print(f"\n⚠️  {total_tests - successful_tests} tests failed - check error messages above")
        
        return results
        
    except Exception as e:
        print(f"❌ Critical error in comprehensive testing: {str(e)}")
        import traceback
        traceback.print_exc()
        return {"critical_error": str(e)}

if __name__ == "__main__":
    run_comprehensive_tests()