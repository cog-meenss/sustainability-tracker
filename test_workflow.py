#!/usr/bin/env python3
"""
Test script to validate the comprehensive sustainability workflow components
"""

import json
import subprocess
import sys
import os
from pathlib import Path

def test_comprehensive_evaluator():
    """Test that the comprehensive evaluator runs successfully"""
    print("🧪 Testing comprehensive sustainability evaluator...")
    
    try:
        # Test JSON output
        result = subprocess.run([
            sys.executable, 
            'comprehensive_sustainability_evaluator.py',
            '--path', '.',
            '--format', 'json',
            '--output', 'test_comprehensive_report.json'
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode != 0:
            print(f"❌ Comprehensive evaluator failed: {result.stderr}")
            return False
        
        # Validate JSON structure
        with open('test_comprehensive_report.json', 'r') as f:
            data = json.load(f)
        
        required_keys = [
            'sustainability_metrics',
            'detailed_analysis',
            'report_metadata'
        ]
        
        for key in required_keys:
            if key not in data:
                print(f"❌ Missing required key: {key}")
                return False
        
        # Validate metrics structure
        metrics = data['sustainability_metrics']
        required_metrics = [
            'overall_score',
            'energy_efficiency',
            'resource_utilization',
            'carbon_footprint'
        ]
        
        for metric in required_metrics:
            if metric not in metrics:
                print(f"❌ Missing metric: {metric}")
                return False
        
        print(f"✅ Comprehensive evaluator working - Score: {metrics['overall_score']:.1f}/100")
        return True
        
    except Exception as e:
        print(f"❌ Error testing comprehensive evaluator: {e}")
        return False
    finally:
        # Clean up test file
        if os.path.exists('test_comprehensive_report.json'):
            os.remove('test_comprehensive_report.json')

def test_workflow_metric_extraction():
    """Test the metric extraction commands from the workflow"""
    print("🧪 Testing workflow metric extraction...")
    
    try:
        # Generate test report
        subprocess.run([
            sys.executable,
            'comprehensive_sustainability_evaluator.py', 
            '--path', '.',
            '--format', 'json',
            '--output', 'test_workflow_report.json'
        ], capture_output=True, timeout=60)
        
        # Test extraction commands like in the workflow
        commands = [
            """
import json
with open('test_workflow_report.json') as f:
    data = json.load(f)
print(f'{data["sustainability_metrics"]["overall_score"]:.1f}')
            """,
            """
import json
with open('test_workflow_report.json') as f:
    data = json.load(f)
patterns = data.get('detailed_analysis', {}).get('code_patterns', {})
issues = patterns.get('async_patterns', 0) + patterns.get('loop_optimizations', 0) + patterns.get('console_logs', 0)
print(issues)
            """,
            """
import json
with open('test_workflow_report.json') as f:
    data = json.load(f)
print(f'{data["report_metadata"]["analysis_time"]:.3f}')
            """
        ]
        
        for i, command in enumerate(commands):
            result = subprocess.run([
                sys.executable, '-c', command.strip()
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"❌ Metric extraction {i+1} failed: {result.stderr}")
                return False
        
        print("✅ Workflow metric extraction working")
        return True
        
    except Exception as e:
        print(f"❌ Error testing metric extraction: {e}")
        return False
    finally:
        # Clean up test file
        if os.path.exists('test_workflow_report.json'):
            os.remove('test_workflow_report.json')

def test_workflow_files():
    """Test that all required workflow files exist"""
    print("🧪 Testing workflow file structure...")
    
    required_files = [
        '.github/workflows/sustainability-analysis.yml',
        'comprehensive_sustainability_evaluator.py',
        'COMPREHENSIVE_SUSTAINABILITY_WORKFLOW_GUIDE.md'
    ]
    
    all_exist = True
    for file_path in required_files:
        if not Path(file_path).exists():
            print(f"❌ Missing required file: {file_path}")
            all_exist = False
        else:
            print(f"✅ Found: {file_path}")
    
    return all_exist

def main():
    """Run all tests"""
    print("🌱 Testing Comprehensive Sustainability GitHub Workflow")
    print("=" * 60)
    
    tests = [
        test_workflow_files,
        test_comprehensive_evaluator,
        test_workflow_metric_extraction
    ]
    
    results = []
    for test in tests:
        print()
        results.append(test())
    
    print()
    print("=" * 60)
    if all(results):
        print("🎉 All tests passed! GitHub workflow ready to use.")
        print()
        print("Next steps:")
        print("1. git push to trigger the workflow")
        print("2. Check Actions tab for comprehensive sustainability analysis")
        print("3. Download artifacts for interactive HTML reports")
        sys.exit(0)
    else:
        print("❌ Some tests failed. Please fix issues before using the workflow.")
        sys.exit(1)

if __name__ == "__main__":
    main()