#!/usr/bin/env python3
"""
Enhanced Sustainability Report Generator
Focuses on actual project files, excludes node_modules and evaluator
"""

import json
import os
from pathlib import Path
from datetime import datetime
import re

def analyze_project_files():
    """Analyze relevant project files excluding node_modules and evaluator"""
    project_root = Path('.')
    
    # Define file patterns to include
    include_patterns = ['*.py', '*.js', '*.jsx', '*.ts', '*.tsx', '*.java', '*.cpp', '*.c', '*.cs', '*.go', '*.rs']
    
    # Define directories to exclude
    exclude_dirs = {
        'node_modules', '.git', '__pycache__', '.vscode', 
        '.pytest_cache', 'dist', 'build', 'coverage'
    }
    
    # Define specific files to exclude
    exclude_files = {
        'sustainability_evaluator.py',
        'comprehensive_sustainability_evaluator.py',
        'runtime_sustainability_reporter.py'
    }
    
    analyzed_files = []
    total_lines = 0
    total_size = 0
    
    # Analyze frontend files
    frontend_dir = project_root / 'frontend' / 'src'
    if frontend_dir.exists():
        for file in frontend_dir.rglob('*'):
            if (file.is_file() and 
                file.suffix in ['.js', '.jsx', '.ts', '.tsx', '.css', '.json'] and
                file.name not in exclude_files):
                
                try:
                    with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        lines = len(content.splitlines())
                        total_lines += lines
                        total_size += file.stat().st_size
                        
                        analyzed_files.append({
                            'path': str(file.relative_to(project_root)),
                            'type': 'Frontend',
                            'language': file.suffix[1:].upper() if file.suffix else 'Unknown',
                            'lines': lines,
                            'size': file.stat().st_size,
                            'complexity': calculate_complexity(content),
                            'sustainability_score': analyze_sustainability_patterns(content, file.suffix)
                        })
                except Exception as e:
                    print(f"Error analyzing {file}: {e}")
    
    # Analyze backend files
    backend_dir = project_root / 'backend'
    if backend_dir.exists():
        for file in backend_dir.rglob('*'):
            if (file.is_file() and 
                not any(excluded in file.parts for excluded in exclude_dirs) and
                file.suffix in ['.js', '.ts', '.py', '.json'] and
                file.name not in exclude_files):
                
                try:
                    with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        lines = len(content.splitlines())
                        total_lines += lines
                        total_size += file.stat().st_size
                        
                        analyzed_files.append({
                            'path': str(file.relative_to(project_root)),
                            'type': 'Backend',
                            'language': file.suffix[1:].upper() if file.suffix else 'Unknown',
                            'lines': lines,
                            'size': file.stat().st_size,
                            'complexity': calculate_complexity(content),
                            'sustainability_score': analyze_sustainability_patterns(content, file.suffix)
                        })
                except Exception as e:
                    print(f"Error analyzing {file}: {e}")
    
    # Analyze root level files (excluding evaluators)
    for file in project_root.glob('*'):
        if (file.is_file() and 
            file.suffix in ['.py', '.js', '.ts', '.md', '.json'] and
            file.name not in exclude_files and
            not file.name.startswith('.')):
            
            try:
                with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    lines = len(content.splitlines())
                    total_lines += lines
                    total_size += file.stat().st_size
                    
                    analyzed_files.append({
                        'path': str(file.name),
                        'type': 'Root',
                        'language': file.suffix[1:].upper() if file.suffix else 'Unknown',
                        'lines': lines,
                        'size': file.stat().st_size,
                        'complexity': calculate_complexity(content),
                        'sustainability_score': analyze_sustainability_patterns(content, file.suffix)
                    })
            except Exception as e:
                print(f"Error analyzing {file}: {e}")
    
    return analyzed_files, total_lines, total_size

def calculate_complexity(content):
    """Calculate basic complexity metrics"""
    lines = content.splitlines()
    complexity_indicators = [
        'if ', 'else', 'elif', 'for ', 'while ', 'try:', 'except:', 
        'function ', 'def ', 'class ', '&&', '||', 'switch', 'case'
    ]
    
    complexity_score = 0
    for line in lines:
        line_lower = line.lower().strip()
        for indicator in complexity_indicators:
            if indicator in line_lower:
                complexity_score += 1
    
    return min(complexity_score, 100)  # Cap at 100

def analyze_sustainability_patterns(content, file_extension):
    """Analyze sustainability patterns in code"""
    
    sustainability_patterns = {
        'efficient_loops': r'(for\s+\w+\s+in\s+range|forEach|map\(|filter\(|reduce\()',
        'lazy_loading': r'(lazy|defer|async|await|Promise)',
        'caching': r'(cache|memoize|localStorage|sessionStorage|Redis)',
        'memory_optimization': r'(del\s+|gc\.|WeakMap|WeakSet|cleanup)',
        'energy_efficient': r'(setTimeout|setInterval|debounce|throttle)',
        'resource_cleanup': r'(close\(\)|dispose\(\)|cleanup|finally:)',
    }
    
    positive_score = 0
    
    # Check for positive patterns
    for pattern_name, pattern in sustainability_patterns.items():
        matches = len(re.findall(pattern, content, re.IGNORECASE))
        positive_score += matches * 5  # 5 points per positive pattern
    
    # Check for negative patterns
    negative_patterns = {
        'blocking_calls': r'(time\.sleep|Thread\.sleep|synchronous)',
        'inefficient_loops': r'(while\s+True|for.*in.*for.*in)',
        'memory_leaks': r'(global\s+\w+\s*=|var\s+\w+\s*=.*new)',
    }
    
    negative_score = 0
    for pattern_name, pattern in negative_patterns.items():
        matches = len(re.findall(pattern, content, re.IGNORECASE))
        negative_score += matches * 3  # 3 points deduction per negative pattern
    
    # Calculate final score (0-100)
    final_score = max(0, min(100, positive_score - negative_score + 50))  # Base score of 50
    return final_score

def calculate_overall_metrics(analyzed_files):
    """Calculate overall project metrics"""
    if not analyzed_files:
        return {
            'overall_score': 25,
            'energy_efficiency': 40,
            'code_quality': 50,
            'performance': 60,
            'green_coding_score': 75
        }
    
    total_sustainability = sum(f['sustainability_score'] for f in analyzed_files)
    avg_sustainability = total_sustainability / len(analyzed_files)
    
    # Calculate different metric categories
    frontend_files = [f for f in analyzed_files if f['type'] == 'Frontend']
    backend_files = [f for f in analyzed_files if f['type'] == 'Backend']
    
    frontend_score = sum(f['sustainability_score'] for f in frontend_files) / max(len(frontend_files), 1)
    backend_score = sum(f['sustainability_score'] for f in backend_files) / max(len(backend_files), 1)
    
    return {
        'overall_score': round(avg_sustainability, 1),
        'energy_efficiency': round((frontend_score + backend_score) / 2, 1),
        'code_quality': round(avg_sustainability * 0.9, 1),
        'performance': round(avg_sustainability * 1.1, 1),
        'green_coding_score': round(avg_sustainability * 0.95, 1),
        'frontend_score': round(frontend_score, 1),
        'backend_score': round(backend_score, 1)
    }

def generate_recommendations(analyzed_files):
    """Generate actionable recommendations"""
    recommendations = []
    
    low_score_files = [f for f in analyzed_files if f['sustainability_score'] < 60]
    
    if low_score_files:
        recommendations.append({
            'priority': 'High',
            'category': 'Code Optimization',
            'description': f'Optimize {len(low_score_files)} files with low sustainability scores',
            'files': [f['path'] for f in low_score_files[:5]],
            'impact': 'Medium'
        })
    
    large_files = [f for f in analyzed_files if f['lines'] > 200]
    if large_files:
        recommendations.append({
            'priority': 'Medium',
            'category': 'Code Structure',
            'description': f'Consider breaking down {len(large_files)} large files for better maintainability',
            'files': [f['path'] for f in large_files[:3]],
            'impact': 'Low'
        })
    
    complex_files = [f for f in analyzed_files if f['complexity'] > 50]
    if complex_files:
        recommendations.append({
            'priority': 'Medium',
            'category': 'Complexity Reduction',
            'description': f'Reduce complexity in {len(complex_files)} files',
            'files': [f['path'] for f in complex_files[:3]],
            'impact': 'Medium'
        })
    
    return recommendations

def main():
    print("🌱 Generating Enhanced Sustainability Report...")
    
    # Analyze project files
    analyzed_files, total_lines, total_size = analyze_project_files()
    
    print(f"📊 Analyzed {len(analyzed_files)} files ({total_lines} lines, {total_size/1024:.1f}KB)")
    
    # Calculate metrics
    metrics = calculate_overall_metrics(analyzed_files)
    recommendations = generate_recommendations(analyzed_files)
    
    # Generate JSON report
    report_data = {
        'timestamp': datetime.now().isoformat(),
        'project_name': 'Sustainability Tracker',
        'summary': {
            'total_files': len(analyzed_files),
            'total_lines': total_lines,
            'total_size': total_size,
            'files_by_type': {
                'Frontend': len([f for f in analyzed_files if f['type'] == 'Frontend']),
                'Backend': len([f for f in analyzed_files if f['type'] == 'Backend']),
                'Root': len([f for f in analyzed_files if f['type'] == 'Root'])
            }
        },
        'sustainability_metrics': metrics,
        'analyzed_files': analyzed_files,
        'recommendations': recommendations
    }
    
    # Save JSON report
    os.makedirs('sustainability-reports', exist_ok=True)
    with open('sustainability-reports/project-analysis.json', 'w') as f:
        json.dump(report_data, f, indent=2)
    
    print(f"✅ Report generated: sustainability-reports/project-analysis.json")
    print(f"📊 Overall Score: {metrics['overall_score']}/100")
    print(f"🎯 Frontend Score: {metrics['frontend_score']}/100")
    print(f"🔧 Backend Score: {metrics['backend_score']}/100")
    
    return report_data

if __name__ == "__main__":
    main()