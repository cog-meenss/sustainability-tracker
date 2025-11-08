#!/usr/bin/env python3
"""
Comprehensive test suite for the Universal Carbon Footprint Analyzer.
Tests multiple project types and configurations.
"""

import sys
import os
sys.path.insert(0, 'src')

import json
import tempfile
from pathlib import Path
from carbon_analyzer import CarbonAnalyzer

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
from sklearn.linear_model import LinearRegression

def process_data(data):
    # Complex data processing
    for i in range(1000):
        data = data.transform(lambda x: x ** 2)
    return data

def train_model(X, y):
    model = LinearRegression()
    model.fit(X, y)
    return model

if __name__ == "__main__":
    data = pd.DataFrame({'x': range(100), 'y': range(100)})
    processed = process_data(data)
    model = train_model(processed[['x']], processed['y'])
    print("Model trained successfully")
""")
    
    (python_dir / "requirements.txt").write_text("""
pandas==1.5.0
numpy==1.24.0
scikit-learn==1.2.0
matplotlib==3.6.0
""")
    
    projects["python"] = str(python_dir)
    
    # 2. JavaScript/React Project
    js_dir = test_dir / "react_project"
    js_dir.mkdir(exist_ok=True)
    
    (js_dir / "package.json").write_text(json.dumps({
        "name": "test-react-app",
        "version": "1.0.0",
        "dependencies": {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "lodash": "^4.17.21",
            "axios": "^1.4.0",
            "moment": "^2.29.4"
        },
        "scripts": {
            "build": "react-scripts build",
            "start": "react-scripts start"
        }
    }, indent=2))
    
    (js_dir / "App.js").write_text("""
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import _ from 'lodash';
import moment from 'moment';

function App() {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);
    
    useEffect(() => {
        // Inefficient data fetching
        const fetchData = async () => {
            for (let i = 0; i < 100; i++) {
                const response = await axios.get('/api/data');
                setData(prev => [...prev, ...response.data]);
            }
            setLoading(false);
        };
        
        fetchData();
    }, []);
    
    const processData = (items) => {
        // Inefficient processing
        return items.map(item => {
            return _.cloneDeep(item);
        }).filter(item => {
            return moment(item.date).isAfter(moment().subtract(1, 'year'));
        });
    };
    
    if (loading) return <div>Loading...</div>;
    
    return (
        <div>
            <h1>React App</h1>
            {processData(data).map(item => (
                <div key={item.id}>{item.name}</div>
            ))}
        </div>
    );
}

export default App;
""")
    
    projects["react"] = str(js_dir)
    
    # 3. Java Project
    java_dir = test_dir / "java_project"
    java_dir.mkdir(exist_ok=True)
    
    (java_dir / "pom.xml").write_text("""
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.example</groupId>
    <artifactId>test-app</artifactId>
    <version>1.0.0</version>
    
    <dependencies>
        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-core</artifactId>
            <version>5.3.21</version>
        </dependency>
        <dependency>
            <groupId>org.apache.commons</groupId>
            <artifactId>commons-lang3</artifactId>
            <version>3.12.0</version>
        </dependency>
    </dependencies>
</project>
""")
    
    java_src_dir = java_dir / "src" / "main" / "java" / "com" / "example"
    java_src_dir.mkdir(parents=True, exist_ok=True)
    
    (java_src_dir / "Application.java").write_text("""
package com.example;

import org.apache.commons.lang3.StringUtils;
import org.springframework.context.ApplicationContext;

public class Application {
    
    public static void main(String[] args) {
        DataProcessor processor = new DataProcessor();
        processor.processLargeDataset();
    }
    
    public static class DataProcessor {
        
        public void processLargeDataset() {
            // Inefficient nested loops
            for (int i = 0; i < 1000; i++) {
                for (int j = 0; j < 1000; j++) {
                    String result = processString("data_" + i + "_" + j);
                    if (StringUtils.isNotEmpty(result)) {
                        System.out.println(result);
                    }
                }
            }
        }
        
        private String processString(String input) {
            // Inefficient string operations
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < input.length(); i++) {
                sb.append(input.charAt(i));
                sb.append("_");
            }
            return sb.toString();
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
    
    # Initialize analyzer
    analyzer = CarbonAnalyzer()
    
    # Create test projects
    print("\n📁 Creating test projects...")
    projects = create_test_projects()
    
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
                report_formats=['json', 'html']
            )
            
            results[project_type] = result
            
            # Print summary
            carbon = result['carbon_footprint']['total_carbon_kg']
            energy = result['carbon_footprint']['total_energy_kwh']
            language = result['analysis']['primary_language']
            files = result['analysis']['total_files']
            
            print(f"   ✅ Analysis complete!")
            print(f"   📊 Primary Language: {language}")
            print(f"   📁 Files Analyzed: {files}")
            print(f"   🌱 Carbon Footprint: {carbon:.6f} kg CO2")
            print(f"   ⚡ Energy Usage: {energy:.6f} kWh")
            
        except Exception as e:
            print(f"   ❌ Error analyzing {project_type}: {str(e)}")
            results[project_type] = {"error": str(e)}
    
    # Test code snippet analysis
    print(f"\n🔍 Testing CODE SNIPPET analysis...")
    try:
        snippet_result = analyzer.analyze_code_snippet(
            code="def fibonacci(n):\n    if n <= 1: return n\n    return fibonacci(n-1) + fibonacci(n-2)",
            language="python"
        )
        results["code_snippet"] = snippet_result
        print(f"   ✅ Snippet analysis complete!")
        print(f"   🌱 Carbon Footprint: {snippet_result['carbon_footprint']['total_carbon_kg']:.6f} kg CO2")
    except Exception as e:
        print(f"   ❌ Error analyzing code snippet: {str(e)}")
        results["code_snippet"] = {"error": str(e)}
    
    # Test project comparison
    if len([p for p in projects.values() if os.path.exists(p)]) >= 2:
        print(f"\n🔍 Testing PROJECT COMPARISON...")
        try:
            project_paths = [p for p in projects.values() if os.path.exists(p)][:2]
            comparison_result = analyzer.compare_projects(
                project_paths=project_paths,
                output_path="comprehensive_test_results/comparison"
            )
            results["comparison"] = comparison_result
            print(f"   ✅ Comparison complete!")
            print(f"   📊 Projects compared: {len(project_paths)}")
        except Exception as e:
            print(f"   ❌ Error comparing projects: {str(e)}")
            results["comparison"] = {"error": str(e)}
    
    # Generate overall summary
    print(f"\n📋 COMPREHENSIVE TEST SUMMARY")
    print("=" * 50)
    
    successful_tests = len([r for r in results.values() if "error" not in r])
    total_tests = len(results)
    
    print(f"✅ Successful Tests: {successful_tests}/{total_tests}")
    
    if successful_tests > 0:
        total_files = sum(r.get('analysis', {}).get('total_files', 0) for r in results.values() if "error" not in r)
        total_carbon = sum(r.get('carbon_footprint', {}).get('total_carbon_kg', 0) for r in results.values() if "error" not in r)
        
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
    print(f"\n🎉 COMPREHENSIVE TESTING COMPLETE!")
    
    return results

if __name__ == "__main__":
    run_comprehensive_tests()