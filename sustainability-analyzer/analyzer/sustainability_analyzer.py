#!/usr/bin/env python3
"""
Sustainability Code Evaluation Analyzer
Core analysis engine for evaluating code sustainability metrics
"""

import os
import sys
import json
import argparse
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path
import hashlib
from dataclasses import dataclass, asdict

@dataclass
class SustainabilityMetrics:
 """Core sustainability metrics data structure"""
 energy_efficiency: float = 0.0
 resource_utilization: float = 0.0 
 carbon_footprint: float = 0.0
 performance_optimization: float = 0.0
 sustainable_practices: float = 0.0
 overall_score: float = 0.0
 
 def to_dict(self) -> Dict[str, float]:
 return asdict(self)

@dataclass 
class AnalysisResult:
 """Complete analysis result structure"""
 metrics: SustainabilityMetrics
 file_count: int = 0
 language_breakdown: Dict[str, int] = None
 issues: List[Dict[str, Any]] = None
 recommendations: List[Dict[str, Any]] = None
 execution_time: float = 0.0
 timestamp: str = ""
 
 def __post_init__(self):
 if self.language_breakdown is None:
 self.language_breakdown = {}
 if self.issues is None:
 self.issues = []
 if self.recommendations is None:
 self.recommendations = []
 if not self.timestamp:
 self.timestamp = datetime.now().isoformat()

class SustainabilityAnalyzer:
 """Main sustainability code analyzer"""
 
 # Language file extensions mapping
 LANGUAGE_EXTENSIONS = {
 'python': ['.py', '.pyw', '.pyx'],
 'javascript': ['.js', '.mjs', '.jsx', '.ts', '.tsx'],
 'java': ['.java'],
 'csharp': ['.cs'],
 'go': ['.go'],
 'rust': ['.rs'],
 'cpp': ['.cpp', '.cc', '.cxx', '.c'],
 'php': ['.php'],
 'ruby': ['.rb'],
 'kotlin': ['.kt', '.kts']
 }
 
 # Sustainability rules by language
 SUSTAINABILITY_RULES = {
 'python': {
 'async_patterns': {
 'positive': ['async def', 'await ', 'asyncio', 'aiohttp'],
 'negative': ['time.sleep(', 'requests.get(', 'urllib.request'],
 'weight': 15
 },
 'memory_efficiency': {
 'positive': ['__slots__', 'generator', 'yield ', 'itertools'],
 'negative': ['global ', 'import *', 'exec(', 'eval('],
 'weight': 20
 },
 'performance_patterns': {
 'positive': ['list comprehension', 'numpy', 'pandas.vectorized', 'cython'],
 'negative': ['nested loops', 'repeated string concatenation'],
 'weight': 25
 }
 },
 'javascript': {
 'async_patterns': {
 'positive': ['async function', 'await ', 'Promise.all', 'Promise.race'],
 'negative': ['XMLHttpRequest', 'setTimeout', 'setInterval'],
 'weight': 15
 },
 'bundle_optimization': {
 'positive': ['import()', 'dynamic import', 'tree shaking', 'code splitting'],
 'negative': ['require()', 'import entire library'],
 'weight': 20
 },
 'dom_efficiency': {
 'positive': ['document fragment', 'virtual DOM', 'requestAnimationFrame'],
 'negative': ['innerHTML', 'document.write', 'synchronous DOM'],
 'weight': 18
 }
 },
 'java': {
 'memory_management': {
 'positive': ['StringBuilder', 'ArrayList', 'HashMap', 'Stream API'],
 'negative': ['String concatenation', 'Vector', 'Hashtable'],
 'weight': 22
 },
 'concurrency': {
 'positive': ['CompletableFuture', 'parallel streams', 'ExecutorService'],
 'negative': ['synchronized blocks', 'Thread.sleep'],
 'weight': 18
 }
 }
 }
 
 def __init__(self, config_path: Optional[str] = None):
 """Initialize analyzer with optional config"""
 self.config = self._load_config(config_path) if config_path else self._default_config()
 self.start_time = time.time()
 
 def _default_config(self) -> Dict[str, Any]:
 """Default configuration"""
 return {
 'sustainability_thresholds': {
 'energy_efficiency_min': 75,
 'resource_utilization_max': 85, 
 'carbon_footprint_max': 50,
 'performance_optimization_min': 80
 },
 'analysis_depth': 'comprehensive',
 'generate_recommendations': True,
 'include_file_details': True
 }
 
 def _load_config(self, config_path: str) -> Dict[str, Any]:
 """Load configuration from JSON file"""
 try:
 with open(config_path, 'r') as f:
 return json.load(f)
 except Exception as e:
 print(f"Warning: Could not load config {config_path}: {e}")
 return self._default_config()
 
 def analyze_project(self, project_path: str) -> AnalysisResult:
 """Analyze entire project for sustainability metrics"""
 print(f"Starting sustainability analysis of: {project_path}")
 
 # Initialize result structure
 metrics = SustainabilityMetrics()
 language_breakdown = {}
 issues = []
 recommendations = []
 file_count = 0
 
 # Walk through all files in project
 for root, dirs, files in os.walk(project_path):
 # Skip common ignore directories
 dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '__pycache__', 
 '.venv', 'venv', 'build', 'dist', 'target']]
 
 for file in files:
 file_path = os.path.join(root, file)
 language = self._detect_language(file)
 
 if language:
 file_count += 1
 language_breakdown[language] = language_breakdown.get(language, 0) + 1
 
 # Analyze individual file
 file_metrics, file_issues, file_recommendations = self._analyze_file(
 file_path, language
 )
 
 # Aggregate metrics
 self._aggregate_metrics(metrics, file_metrics, language)
 issues.extend(file_issues)
 recommendations.extend(file_recommendations)
 
 # Calculate final scores
 self._calculate_final_scores(metrics, file_count, language_breakdown)
 
 # Generate recommendations
 if self.config.get('generate_recommendations', True):
 recommendations.extend(self._generate_project_recommendations(metrics, language_breakdown))
 
 execution_time = time.time() - self.start_time
 
 print(f"Analysis complete! Processed {file_count} files in {execution_time:.2f}s")
 print(f"Overall Sustainability Score: {metrics.overall_score:.1f}/100")
 
 return AnalysisResult(
 metrics=metrics,
 file_count=file_count,
 language_breakdown=language_breakdown,
 issues=issues,
 recommendations=recommendations,
 execution_time=execution_time
 )
 
 def _detect_language(self, filename: str) -> Optional[str]:
 """Detect programming language from file extension"""
 file_ext = Path(filename).suffix.lower()
 
 for language, extensions in self.LANGUAGE_EXTENSIONS.items():
 if file_ext in extensions:
 return language
 return None
 
 def _analyze_file(self, file_path: str, language: str) -> tuple:
 """Analyze individual file for sustainability patterns"""
 try:
 with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
 content = f.read()
 except Exception as e:
 return SustainabilityMetrics(), [], []
 
 metrics = SustainabilityMetrics()
 issues = []
 recommendations = []
 
 # Get language-specific rules
 rules = self.SUSTAINABILITY_RULES.get(language, {})
 
 # Analyze patterns in file content
 for rule_name, rule_config in rules.items():
 positive_patterns = rule_config.get('positive', [])
 negative_patterns = rule_config.get('negative', [])
 weight = rule_config.get('weight', 10)
 
 positive_count = sum(content.count(pattern) for pattern in positive_patterns)
 negative_count = sum(content.count(pattern) for pattern in negative_patterns)
 
 # Calculate rule score (0-100)
 total_patterns = positive_count + negative_count
 if total_patterns > 0:
 rule_score = (positive_count / total_patterns) * 100
 else:
 rule_score = 50 # Neutral if no patterns found
 
 # Map rule to metrics
 self._map_rule_to_metrics(metrics, rule_name, rule_score, weight)
 
 # Generate issues for negative patterns
 if negative_count > 0:
 issues.append({
 'type': 'sustainability_concern',
 'file': file_path,
 'rule': rule_name,
 'severity': 'medium' if negative_count < 5 else 'high',
 'count': negative_count,
 'message': f"Found {negative_count} sustainability concerns in {rule_name}"
 })
 
 # Basic file-level metrics
 lines = content.split('\n')
 metrics.performance_optimization += self._analyze_code_complexity(content, language)
 
 return metrics, issues, recommendations
 
 def _map_rule_to_metrics(self, metrics: SustainabilityMetrics, rule_name: str, 
 score: float, weight: int):
 """Map rule analysis to sustainability metrics"""
 weighted_score = (score * weight) / 100
 
 if 'async' in rule_name or 'concurrency' in rule_name:
 metrics.energy_efficiency += weighted_score
 elif 'memory' in rule_name or 'optimization' in rule_name:
 metrics.resource_utilization += weighted_score 
 elif 'bundle' in rule_name or 'dom' in rule_name:
 metrics.carbon_footprint += (100 - weighted_score) # Lower is better
 else:
 metrics.sustainable_practices += weighted_score
 
 def _analyze_code_complexity(self, content: str, language: str) -> float:
 """Analyze code complexity for performance implications"""
 lines = content.split('\n')
 
 # Basic complexity indicators
 complexity_indicators = {
 'nested_loops': 0,
 'recursive_calls': 0,
 'database_queries': 0,
 'file_operations': 0
 }
 
 for line in lines:
 line = line.strip().lower()
 
 # Nested loops detection (simplified)
 if any(keyword in line for keyword in ['for ', 'while ']):
 if ' for' in content or ' while' in content: # Indented = nested
 complexity_indicators['nested_loops'] += 1
 
 # Database operations
 if any(keyword in line for keyword in ['select ', 'insert ', 'update ', 'delete ']):
 complexity_indicators['database_queries'] += 1
 
 # File operations 
 if any(keyword in line for keyword in ['open(', 'read(', 'write(']):
 complexity_indicators['file_operations'] += 1
 
 # Calculate complexity score (higher complexity = lower sustainability)
 total_complexity = sum(complexity_indicators.values())
 total_lines = len([l for l in lines if l.strip()])
 
 if total_lines == 0:
 return 50
 
 complexity_ratio = total_complexity / total_lines
 return max(0, 100 - (complexity_ratio * 1000)) # Scale and invert
 
 def _aggregate_metrics(self, total_metrics: SustainabilityMetrics, 
 file_metrics: SustainabilityMetrics, language: str):
 """Aggregate file metrics into total project metrics"""
 # Weight by language importance (could be configurable)
 weight = 1.0
 
 total_metrics.energy_efficiency += file_metrics.energy_efficiency * weight
 total_metrics.resource_utilization += file_metrics.resource_utilization * weight
 total_metrics.carbon_footprint += file_metrics.carbon_footprint * weight
 total_metrics.performance_optimization += file_metrics.performance_optimization * weight
 total_metrics.sustainable_practices += file_metrics.sustainable_practices * weight
 
 def _calculate_final_scores(self, metrics: SustainabilityMetrics, file_count: int, 
 language_breakdown: Dict[str, int]):
 """Calculate final normalized scores"""
 if file_count == 0:
 return
 
 # Normalize by file count
 metrics.energy_efficiency = min(100, metrics.energy_efficiency / file_count)
 metrics.resource_utilization = min(100, metrics.resource_utilization / file_count)
 metrics.carbon_footprint = min(100, metrics.carbon_footprint / file_count)
 metrics.performance_optimization = min(100, metrics.performance_optimization / file_count)
 metrics.sustainable_practices = min(100, metrics.sustainable_practices / file_count)
 
 # Calculate overall score (weighted average)
 weights = {
 'energy_efficiency': 0.25,
 'resource_utilization': 0.25,
 'carbon_footprint': 0.20, # Lower is better, so invert
 'performance_optimization': 0.20,
 'sustainable_practices': 0.10
 }
 
 metrics.overall_score = (
 metrics.energy_efficiency * weights['energy_efficiency'] +
 metrics.resource_utilization * weights['resource_utilization'] +
 (100 - metrics.carbon_footprint) * weights['carbon_footprint'] + # Invert carbon footprint
 metrics.performance_optimization * weights['performance_optimization'] +
 metrics.sustainable_practices * weights['sustainable_practices']
 )
 
 def _generate_project_recommendations(self, metrics: SustainabilityMetrics, 
 language_breakdown: Dict[str, int]) -> List[Dict[str, Any]]:
 """Generate actionable sustainability recommendations"""
 recommendations = []
 
 # Energy Efficiency Recommendations
 if metrics.energy_efficiency < 70:
 recommendations.append({
 'category': 'energy_efficiency',
 'priority': 'high',
 'title': 'Improve Async Patterns',
 'description': 'Implement more asynchronous programming patterns to reduce CPU blocking and improve energy efficiency.',
 'impact': 'High',
 'effort': 'Medium'
 })
 
 # Resource Utilization Recommendations
 if metrics.resource_utilization < 70:
 recommendations.append({
 'category': 'resource_utilization',
 'priority': 'high', 
 'title': 'Optimize Memory Usage',
 'description': 'Review memory allocation patterns and implement more efficient data structures.',
 'impact': 'High',
 'effort': 'Medium'
 })
 
 # Carbon Footprint Recommendations
 if metrics.carbon_footprint > 60:
 recommendations.append({
 'category': 'carbon_footprint',
 'priority': 'medium',
 'title': 'Reduce Runtime Complexity',
 'description': 'Optimize algorithms to reduce execution time and energy consumption.',
 'impact': 'Medium',
 'effort': 'High'
 })
 
 # Language-specific recommendations
 for language, count in language_breakdown.items():
 if language == 'javascript' and count > 10:
 recommendations.append({
 'category': 'javascript_optimization',
 'priority': 'medium',
 'title': 'Bundle Size Optimization',
 'description': 'Implement code splitting and tree shaking to reduce JavaScript bundle size.',
 'impact': 'Medium',
 'effort': 'Low'
 })
 
 return recommendations

def main():
 """Command line interface for sustainability analyzer"""
 parser = argparse.ArgumentParser(description='Sustainability Code Evaluation Analyzer')
 parser.add_argument('--path', default='.', help='Path to analyze (default: current directory)')
 parser.add_argument('--output', default='sustainability_analysis.json', 
 help='Output file for analysis results')
 parser.add_argument('--config', help='Path to configuration file')
 parser.add_argument('--format', choices=['json', 'summary'], default='json',
 help='Output format')
 
 args = parser.parse_args()
 
 # Initialize and run analyzer
 analyzer = SustainabilityAnalyzer(config_path=args.config)
 result = analyzer.analyze_project(args.path)
 
 # Output results
 if args.format == 'json':
 output_data = {
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
 
 with open(args.output, 'w') as f:
 json.dump(output_data, f, indent=2)
 print(f"Results saved to: {args.output}")
 
 elif args.format == 'summary':
 print(f"\nSUSTAINABILITY ANALYSIS SUMMARY")
 print(f"{'='*50}")
 print(f"Overall Score: {result.metrics.overall_score:.1f}/100")
 print(f"Energy Efficiency: {result.metrics.energy_efficiency:.1f}/100")
 print(f"Resource Utilization: {result.metrics.resource_utilization:.1f}/100") 
 print(f"Carbon Footprint: {result.metrics.carbon_footprint:.1f}/100 (lower is better)")
 print(f"Performance Optimization: {result.metrics.performance_optimization:.1f}/100")
 print(f"Sustainable Practices: {result.metrics.sustainable_practices:.1f}/100")
 print(f"\nAnalyzed {result.file_count} files")
 print(f"Execution time: {result.execution_time:.2f}s")
 
 if result.recommendations:
 print(f"\nTOP RECOMMENDATIONS:")
 for i, rec in enumerate(result.recommendations[:3], 1):
 print(f" {i}. {rec['title']} ({rec['priority']} priority)")

if __name__ == "__main__":
 main()