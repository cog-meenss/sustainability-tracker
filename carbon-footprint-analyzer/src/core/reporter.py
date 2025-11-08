"""
Report generator for carbon footprint analysis
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
import csv

class ReportGenerator:
    """Generates various types of reports for carbon footprint analysis"""
    
    def __init__(self):
        self.report_templates = {
            'executive_summary': self._generate_executive_summary,
            'technical_details': self._generate_technical_report,
            'optimization_guide': self._generate_optimization_guide,
            'comparison_report': self._generate_comparison_report
        }
    
    def generate_report(self, 
                       analysis_results: Dict[str, Any],
                       report_type: str = 'technical_details',
                       output_format: str = 'json',
                       output_path: Optional[Path] = None) -> str:
        """
        Generate a comprehensive report from analysis results
        
        Args:
            analysis_results: Complete analysis results from CarbonAnalyzer
            report_type: Type of report to generate
            output_format: Output format ('json', 'html', 'markdown', 'csv')
            output_path: Where to save the report (if None, returns as string)
        
        Returns:
            Report content as string or path to saved file
        """
        
        if report_type not in self.report_templates:
            raise ValueError(f"Unknown report type: {report_type}. Available: {list(self.report_templates.keys())}")
        
        # Generate report content
        report_data = self.report_templates[report_type](analysis_results)
        
        # Format the report
        if output_format == 'json':
            content = json.dumps(report_data, indent=2, ensure_ascii=False)
        elif output_format == 'html':
            content = self._format_as_html(report_data, report_type)
        elif output_format == 'markdown':
            content = self._format_as_markdown(report_data, report_type)
        elif output_format == 'csv':
            content = self._format_as_csv(report_data, report_type)
        else:
            raise ValueError(f"Unsupported output format: {output_format}")
        
        # Save or return content
        if output_path:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return str(output_path)
        else:
            return content
    
    def _generate_executive_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate executive summary report"""
        carbon_data = results.get('carbon_footprint', {})
        language_data = results.get('language_detection', {})
        
        summary = {
            'report_type': 'Executive Summary',
            'generated_at': datetime.now().isoformat(),
            'project_info': {
                'name': results.get('project_info', {}).get('name', 'Unknown'),
                'primary_language': language_data.get('primary_language', 'Unknown'),
                'total_files': language_data.get('total_files', 0),
                'project_type': language_data.get('project_type', 'Unknown')
            },
            'carbon_footprint': {
                'total_emissions_kg': carbon_data.get('total_carbon_kg', 0),
                'total_energy_kwh': carbon_data.get('total_energy_kwh', 0),
                'impact_level': carbon_data.get('comparison_metrics', {}).get('impact_level', 'unknown')
            },
            'key_findings': self._extract_key_findings(results),
            'recommendations': self._extract_top_recommendations(results),
            'next_steps': [
                'Review detailed technical report for implementation guidance',
                'Prioritize high-impact optimization opportunities',
                'Establish baseline measurements for tracking improvements',
                'Consider implementing continuous carbon monitoring'
            ]
        }
        
        return summary
    
    def _generate_technical_report(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate detailed technical report"""
        return {
            'report_type': 'Technical Details',
            'generated_at': datetime.now().isoformat(),
            'metadata': {
                'analyzer_version': results.get('metadata', {}).get('analyzer_version', 'Unknown'),
                'analysis_duration': results.get('metadata', {}).get('analysis_duration', 0),
                'files_analyzed': results.get('metadata', {}).get('files_analyzed', 0)
            },
            'project_overview': results.get('project_info', {}),
            'language_analysis': results.get('language_detection', {}),
            'code_structure': results.get('project_structure', {}),
            'dependencies': results.get('dependencies', {}),
            'frameworks': results.get('framework_info', {}),
            'carbon_footprint': results.get('carbon_footprint', {}),
            'recommendations': results.get('recommendations', []),
            'raw_data': {
                'file_complexities': results.get('project_structure', {}).get('file_complexities', {}),
                'calculation_details': results.get('carbon_footprint', {}).get('methodology', {})
            }
        }
    
    def _generate_optimization_guide(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate optimization-focused report"""
        carbon_data = results.get('carbon_footprint', {})
        recommendations = results.get('recommendations', [])
        
        # Group recommendations by category
        categorized_recommendations = {}
        for rec in recommendations:
            category = self._categorize_recommendation(rec)
            if category not in categorized_recommendations:
                categorized_recommendations[category] = []
            categorized_recommendations[category].append(rec)
        
        optimization_potential = carbon_data.get('optimization_potential', {})
        
        guide = {
            'report_type': 'Optimization Guide',
            'generated_at': datetime.now().isoformat(),
            'current_footprint': {
                'total_carbon_kg': carbon_data.get('total_carbon_kg', 0),
                'total_energy_kwh': carbon_data.get('total_energy_kwh', 0)
            },
            'optimization_potential': {
                'total_reduction_potential_kg': optimization_potential.get('total_potential_reduction_kg', 0),
                'potential_percentage': optimization_potential.get('potential_reduction_percentage', 0),
                'estimated_savings_usd': self._estimate_cost_savings(optimization_potential)
            },
            'prioritized_actions': self._prioritize_optimizations(categorized_recommendations, optimization_potential),
            'implementation_roadmap': self._create_implementation_roadmap(categorized_recommendations),
            'measurement_strategy': {
                'baseline_metrics': [
                    'Total carbon emissions (kg CO2)',
                    'Energy consumption (kWh)', 
                    'Code complexity metrics',
                    'Dependency count and weight'
                ],
                'monitoring_tools': [
                    'Continuous integration carbon tracking',
                    'Runtime performance monitoring',
                    'Dependency vulnerability scanning',
                    'Code quality metrics'
                ],
                'success_criteria': [
                    f"Reduce carbon footprint by {optimization_potential.get('potential_reduction_percentage', 0):.1f}%",
                    'Maintain or improve application performance',
                    'Reduce dependency count by 10-20%',
                    'Improve code maintainability scores'
                ]
            }
        }
        
        return guide
    
    def _generate_comparison_report(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comparison and benchmark report"""
        carbon_data = results.get('carbon_footprint', {})
        language_data = results.get('language_detection', {})
        
        # Industry benchmarks (estimated values for comparison)
        benchmarks = self._get_industry_benchmarks(language_data.get('project_type', 'general'))
        
        comparison = {
            'report_type': 'Comparison & Benchmarks',
            'generated_at': datetime.now().isoformat(),
            'project_metrics': {
                'carbon_per_file': carbon_data.get('total_carbon_kg', 0) / max(language_data.get('total_files', 1), 1),
                'energy_per_line': self._calculate_energy_per_line(results),
                'complexity_factor': language_data.get('complexity_indicator', 'medium')
            },
            'industry_comparison': {
                'project_type': language_data.get('project_type', 'general'),
                'benchmarks': benchmarks,
                'performance_vs_benchmark': self._compare_to_benchmarks(results, benchmarks)
            },
            'language_comparison': self._compare_languages(results),
            'framework_impact': self._analyze_framework_impact(results),
            'improvement_trajectory': {
                'current_position': self._assess_current_position(results),
                'optimization_path': self._suggest_optimization_path(results),
                'target_metrics': self._calculate_target_metrics(results)
            }
        }
        
        return comparison
    
    def _extract_key_findings(self, results: Dict[str, Any]) -> List[str]:
        """Extract key findings from analysis results"""
        findings = []
        
        carbon_data = results.get('carbon_footprint', {})
        language_data = results.get('language_detection', {})
        dependencies = results.get('dependencies', {})
        
        # Carbon footprint findings
        total_carbon = carbon_data.get('total_carbon_kg', 0)
        impact_level = carbon_data.get('comparison_metrics', {}).get('impact_level', 'unknown')
        
        findings.append(f"Project has {impact_level} carbon impact ({total_carbon:.6f} kg CO2)")
        
        # Language findings
        primary_lang = language_data.get('primary_language', 'Unknown')
        complexity = language_data.get('complexity_indicator', 'medium')
        
        findings.append(f"Primary language: {primary_lang} with {complexity} complexity")
        
        # Framework findings
        frameworks = results.get('framework_info', {}).get('detected_frameworks', [])
        if frameworks:
            findings.append(f"Uses {len(frameworks)} frameworks: {', '.join(frameworks[:3])}")
        
        # Dependency findings
        heavy_deps = len(dependencies.get('heavy_dependencies', []))
        total_deps = dependencies.get('total_dependencies', 0)
        
        if heavy_deps > 0:
            findings.append(f"{heavy_deps} heavy dependencies out of {total_deps} total")
        
        # Optimization findings
        optimization_potential = carbon_data.get('optimization_potential', {})
        potential_reduction = optimization_potential.get('potential_reduction_percentage', 0)
        
        if potential_reduction > 10:
            findings.append(f"{potential_reduction:.1f}% carbon reduction potential identified")
        
        return findings
    
    def _extract_top_recommendations(self, results: Dict[str, Any], limit: int = 5) -> List[str]:
        """Extract top priority recommendations"""
        all_recommendations = results.get('recommendations', [])
        
        # Priority keywords for ranking recommendations
        high_priority_keywords = [
            'reduce', 'optimize', 'remove', 'replace', 'efficiency',
            'performance', 'bundle', 'cache', 'memory'
        ]
        
        # Score recommendations based on priority keywords
        scored_recommendations = []
        for rec in all_recommendations:
            score = sum(1 for keyword in high_priority_keywords if keyword.lower() in rec.lower())
            scored_recommendations.append((score, rec))
        
        # Sort by score and return top recommendations
        scored_recommendations.sort(key=lambda x: x[0], reverse=True)
        return [rec for _, rec in scored_recommendations[:limit]]
    
    def _categorize_recommendation(self, recommendation: str) -> str:
        """Categorize a recommendation into a topic area"""
        rec_lower = recommendation.lower()
        
        if any(word in rec_lower for word in ['dependency', 'package', 'library', 'import']):
            return 'Dependencies'
        elif any(word in rec_lower for word in ['complexity', 'refactor', 'function', 'class']):
            return 'Code Quality'
        elif any(word in rec_lower for word in ['framework', 'react', 'django', 'spring']):
            return 'Frameworks'
        elif any(word in rec_lower for word in ['performance', 'optimize', 'speed', 'memory']):
            return 'Performance'
        elif any(word in rec_lower for word in ['build', 'compile', 'bundle', 'webpack']):
            return 'Build System'
        else:
            return 'General'
    
    def _prioritize_optimizations(self, categorized_recs: Dict[str, List[str]], 
                                optimization_potential: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Prioritize optimization actions by impact and effort"""
        
        # Impact-effort matrix categories
        priority_matrix = {
            'Dependencies': {'impact': 'high', 'effort': 'low'},
            'Performance': {'impact': 'high', 'effort': 'medium'},
            'Code Quality': {'impact': 'medium', 'effort': 'high'},
            'Build System': {'impact': 'medium', 'effort': 'low'},
            'Frameworks': {'impact': 'high', 'effort': 'high'},
            'General': {'impact': 'low', 'effort': 'low'}
        }
        
        prioritized = []
        
        for category, recommendations in categorized_recs.items():
            matrix_info = priority_matrix.get(category, {'impact': 'medium', 'effort': 'medium'})
            
            priority_score = self._calculate_priority_score(matrix_info['impact'], matrix_info['effort'])
            
            prioritized.append({
                'category': category,
                'priority_score': priority_score,
                'impact_level': matrix_info['impact'],
                'effort_level': matrix_info['effort'],
                'recommendation_count': len(recommendations),
                'recommendations': recommendations[:3]  # Top 3 per category
            })
        
        # Sort by priority score (higher is better)
        prioritized.sort(key=lambda x: x['priority_score'], reverse=True)
        
        return prioritized
    
    def _calculate_priority_score(self, impact: str, effort: str) -> int:
        """Calculate priority score based on impact and effort"""
        impact_scores = {'low': 1, 'medium': 2, 'high': 3}
        effort_scores = {'low': 3, 'medium': 2, 'high': 1}  # Lower effort = higher score
        
        return impact_scores.get(impact, 2) * effort_scores.get(effort, 2)
    
    def _create_implementation_roadmap(self, categorized_recs: Dict[str, List[str]]) -> List[Dict[str, Any]]:
        """Create a phased implementation roadmap"""
        phases = [
            {
                'phase': 'Phase 1: Quick Wins (1-2 weeks)',
                'categories': ['Dependencies', 'Build System'],
                'objectives': ['Remove unused dependencies', 'Optimize build process'],
                'expected_impact': 'Low to Medium'
            },
            {
                'phase': 'Phase 2: Performance Optimization (2-4 weeks)', 
                'categories': ['Performance', 'General'],
                'objectives': ['Implement caching', 'Optimize algorithms'],
                'expected_impact': 'Medium to High'
            },
            {
                'phase': 'Phase 3: Code Refactoring (4-8 weeks)',
                'categories': ['Code Quality'],
                'objectives': ['Reduce complexity', 'Improve maintainability'],
                'expected_impact': 'Medium'
            },
            {
                'phase': 'Phase 4: Framework Optimization (8-12 weeks)',
                'categories': ['Frameworks'],
                'objectives': ['Evaluate framework alternatives', 'Implement migrations'],
                'expected_impact': 'High'
            }
        ]
        
        # Add relevant recommendations to each phase
        for phase in phases:
            phase['recommendations'] = []
            for category in phase['categories']:
                if category in categorized_recs:
                    phase['recommendations'].extend(categorized_recs[category][:2])
        
        return phases
    
    def _estimate_cost_savings(self, optimization_potential: Dict[str, Any]) -> float:
        """Estimate cost savings from carbon reduction"""
        # Average cost of carbon: ~$50 per ton CO2
        carbon_price_per_kg = 0.05  # $0.05 per kg CO2
        
        potential_reduction_kg = optimization_potential.get('total_potential_reduction_kg', 0)
        annual_savings = potential_reduction_kg * 365 * carbon_price_per_kg  # Assuming daily usage
        
        return round(annual_savings, 2)
    
    def _get_industry_benchmarks(self, project_type: str) -> Dict[str, float]:
        """Get industry benchmarks for comparison"""
        benchmarks = {
            'web_app': {
                'carbon_per_file_kg': 0.0001,
                'energy_per_line_kwh': 0.00001,
                'typical_complexity': 'medium'
            },
            'mobile_app': {
                'carbon_per_file_kg': 0.00015,
                'energy_per_line_kwh': 0.000012,
                'typical_complexity': 'medium'
            },
            'api_service': {
                'carbon_per_file_kg': 0.00008,
                'energy_per_line_kwh': 0.000008,
                'typical_complexity': 'low'
            },
            'data_analysis': {
                'carbon_per_file_kg': 0.0003,
                'energy_per_line_kwh': 0.00002,
                'typical_complexity': 'high'
            },
            'general': {
                'carbon_per_file_kg': 0.0001,
                'energy_per_line_kwh': 0.00001,
                'typical_complexity': 'medium'
            }
        }
        
        return benchmarks.get(project_type, benchmarks['general'])
    
    def _compare_to_benchmarks(self, results: Dict[str, Any], 
                             benchmarks: Dict[str, float]) -> Dict[str, str]:
        """Compare project metrics to industry benchmarks"""
        carbon_data = results.get('carbon_footprint', {})
        language_data = results.get('language_detection', {})
        
        total_carbon = carbon_data.get('total_carbon_kg', 0)
        total_files = language_data.get('total_files', 1)
        
        carbon_per_file = total_carbon / total_files
        benchmark_carbon = benchmarks.get('carbon_per_file_kg', 0.0001)
        
        if carbon_per_file <= benchmark_carbon * 0.8:
            carbon_rating = 'Excellent'
        elif carbon_per_file <= benchmark_carbon * 1.2:
            carbon_rating = 'Good'
        elif carbon_per_file <= benchmark_carbon * 1.5:
            carbon_rating = 'Average'
        else:
            carbon_rating = 'Needs Improvement'
        
        return {
            'carbon_efficiency': carbon_rating,
            'carbon_per_file_vs_benchmark': f"{((carbon_per_file / benchmark_carbon - 1) * 100):+.1f}%"
        }
    
    def _compare_languages(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Compare languages used in the project"""
        language_data = results.get('language_detection', {})
        carbon_data = results.get('carbon_footprint', {})
        
        language_breakdown = carbon_data.get('language_breakdown', {})
        
        # Language efficiency ranking (lower is more efficient)
        efficiency_ranking = {
            'c': 1, 'rust': 2, 'cpp': 3, 'go': 4, 'java': 5,
            'javascript': 6, 'typescript': 7, 'csharp': 8, 
            'python': 9, 'ruby': 10, 'php': 11
        }
        
        language_comparison = {}
        
        for language, data in language_breakdown.items():
            efficiency_rank = efficiency_ranking.get(language, 6)  # Default to middle
            
            language_comparison[language] = {
                'files': data.get('files', 0),
                'carbon_kg': data.get('estimated_carbon_kg', 0),
                'efficiency_rank': efficiency_rank,
                'efficiency_category': 'High' if efficiency_rank <= 3 else 'Medium' if efficiency_rank <= 7 else 'Low'
            }
        
        return language_comparison
    
    def _analyze_framework_impact(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze the carbon impact of frameworks"""
        frameworks = results.get('framework_info', {}).get('detected_frameworks', [])
        carbon_data = results.get('carbon_footprint', {})
        
        framework_energy = carbon_data.get('components', {}).get('frameworks', {}).get('energy_kwh', 0)
        total_energy = carbon_data.get('total_energy_kwh', 0)
        
        framework_percentage = (framework_energy / total_energy * 100) if total_energy > 0 else 0
        
        # Framework efficiency ratings (subjective)
        framework_ratings = {
            'react': 'Medium', 'vue': 'High', 'angular': 'Low',
            'express': 'High', 'django': 'Medium', 'flask': 'High',
            'spring': 'Low', 'fastapi': 'High'
        }
        
        framework_analysis = {
            'framework_energy_percentage': round(framework_percentage, 2),
            'frameworks_detected': len(frameworks),
            'framework_ratings': {fw: framework_ratings.get(fw, 'Unknown') for fw in frameworks}
        }
        
        return framework_analysis
    
    def _assess_current_position(self, results: Dict[str, Any]) -> str:
        """Assess current carbon efficiency position"""
        carbon_data = results.get('carbon_footprint', {})
        impact_level = carbon_data.get('comparison_metrics', {}).get('impact_level', 'medium')
        
        position_map = {
            'minimal': 'Leading - Excellent carbon efficiency',
            'low': 'Above Average - Good carbon practices',
            'medium': 'Average - Room for improvement',
            'high': 'Below Average - Significant optimization needed',
            'very_high': 'Poor - Urgent optimization required'
        }
        
        return position_map.get(impact_level, 'Unknown position')
    
    def _suggest_optimization_path(self, results: Dict[str, Any]) -> List[str]:
        """Suggest optimization path based on analysis"""
        carbon_data = results.get('carbon_footprint', {})
        components = carbon_data.get('components', {})
        
        # Identify highest impact components
        component_impacts = [
            (comp_name, comp_data.get('percentage', 0))
            for comp_name, comp_data in components.items()
            if isinstance(comp_data, dict) and comp_data.get('percentage', 0) > 0
        ]
        
        component_impacts.sort(key=lambda x: x[1], reverse=True)
        
        optimization_path = []
        
        for component, percentage in component_impacts[:3]:  # Top 3 components
            if component == 'code_execution':
                optimization_path.append('Focus on code efficiency and algorithm optimization')
            elif component == 'frameworks':
                optimization_path.append('Evaluate framework choices and configurations')
            elif component == 'dependencies':
                optimization_path.append('Audit and optimize dependency usage')
            elif component == 'build_system':
                optimization_path.append('Optimize build process and tooling')
        
        return optimization_path
    
    def _calculate_target_metrics(self, results: Dict[str, Any]) -> Dict[str, float]:
        """Calculate target metrics for optimization goals"""
        carbon_data = results.get('carbon_footprint', {})
        optimization_potential = carbon_data.get('optimization_potential', {})
        
        current_carbon = carbon_data.get('total_carbon_kg', 0)
        potential_reduction = optimization_potential.get('total_potential_reduction_kg', 0)
        
        target_carbon = max(current_carbon - potential_reduction, current_carbon * 0.5)  # At least 50% reduction
        
        return {
            'target_carbon_kg': round(target_carbon, 6),
            'target_reduction_percentage': round(((current_carbon - target_carbon) / current_carbon * 100), 1) if current_carbon > 0 else 0,
            'estimated_timeline_weeks': 12  # Standard optimization timeline
        }
    
    def _calculate_energy_per_line(self, results: Dict[str, Any]) -> float:
        """Calculate energy consumption per line of code"""
        carbon_data = results.get('carbon_footprint', {})
        structure_data = results.get('project_structure', {})
        
        total_energy = carbon_data.get('total_energy_kwh', 0)
        total_lines = sum(
            file_data.get('lines', 0)
            for file_data in structure_data.get('file_complexities', {}).values()
        )
        
        return total_energy / max(total_lines, 1)
    
    def _format_as_html(self, report_data: Dict[str, Any], report_type: str) -> str:
        """Format report as HTML"""
        html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{report_data.get('report_type', 'Carbon Footprint Report')}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }}
        h1, h2, h3 {{ color: #2c5aa0; }}
        .summary {{ background: #f4f4f4; padding: 15px; border-radius: 5px; margin: 10px 0; }}
        .metric {{ display: inline-block; margin: 10px; padding: 10px; background: #e7f3ff; border-radius: 3px; }}
        .recommendation {{ background: #fff3cd; padding: 10px; margin: 5px 0; border-left: 4px solid #ffc107; }}
        table {{ border-collapse: collapse; width: 100%; margin: 10px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        .json-view {{ background: #f8f9fa; padding: 15px; border-radius: 5px; font-family: monospace; white-space: pre-wrap; }}
    </style>
</head>
<body>
    <h1>{report_data.get('report_type', 'Carbon Footprint Report')}</h1>
    <p><strong>Generated:</strong> {report_data.get('generated_at', 'Unknown')}</p>
    
    <div class="summary">
        <h2>Report Summary</h2>
        <div class="json-view">{json.dumps(report_data, indent=2)}</div>
    </div>
</body>
</html>
"""
        return html_template
    
    def _format_as_markdown(self, report_data: Dict[str, Any], report_type: str) -> str:
        """Format report as Markdown"""
        md_content = f"""# {report_data.get('report_type', 'Carbon Footprint Report')}

**Generated:** {report_data.get('generated_at', 'Unknown')}

## Summary

```json
{json.dumps(report_data, indent=2)}
```

---
*Report generated by Carbon Footprint Analyzer*
"""
        return md_content
    
    def _format_as_csv(self, report_data: Dict[str, Any], report_type: str) -> str:
        """Format key metrics as CSV"""
        # Extract key metrics for CSV format
        csv_data = []
        
        if 'carbon_footprint' in report_data:
            carbon_data = report_data['carbon_footprint']
            csv_data.append(['Metric', 'Value', 'Unit'])
            csv_data.append(['Total Carbon Emissions', carbon_data.get('total_emissions_kg', 0), 'kg CO2'])
            csv_data.append(['Total Energy Consumption', carbon_data.get('total_energy_kwh', 0), 'kWh'])
            csv_data.append(['Impact Level', carbon_data.get('impact_level', 'Unknown'), ''])
        
        # Convert to CSV string
        csv_content = ""
        for row in csv_data:
            csv_content += ','.join(str(cell) for cell in row) + '\n'
        
        return csv_content