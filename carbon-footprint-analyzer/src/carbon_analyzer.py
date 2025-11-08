"""
Main Carbon Footprint Analyzer
"""

import time
import json
from pathlib import Path
from typing import Dict, Any, Optional, List, Union
from datetime import datetime

from .core.detector import LanguageDetector
from .core.metrics import CarbonCalculator  
from .core.reporter import ReportGenerator
from .analyzers.generic import GenericAnalyzer
from .analyzers.javascript import JavaScriptAnalyzer
from .analyzers.python import PythonAnalyzer
from .analyzers.java import JavaAnalyzer

class CarbonAnalyzer:
    """
    Main analyzer class that orchestrates carbon footprint analysis for any programming language
    """
    
    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize the Carbon Analyzer
        
        Args:
            config_path: Path to configuration file (optional)
        """
        self.version = "1.0.0"
        self.config = self._load_config(config_path)
        
        # Initialize components
        self.language_detector = LanguageDetector()
        self.carbon_calculator = CarbonCalculator()
        self.report_generator = ReportGenerator()
        
        # Initialize language-specific analyzers
        self.analyzers = {
            'javascript': JavaScriptAnalyzer,
            'typescript': JavaScriptAnalyzer,  # TypeScript uses same analyzer
            'python': PythonAnalyzer,
            'java': JavaAnalyzer,
            'kotlin': JavaAnalyzer,  # Kotlin uses Java analyzer
            'generic': GenericAnalyzer  # Fallback for unsupported languages
        }
        
        # Analysis metadata
        self.analysis_metadata = {
            'analyzer_version': self.version,
            'analysis_start_time': None,
            'analysis_duration': 0,
            'files_analyzed': 0,
            'errors_encountered': []
        }
    
    def analyze_project(self, 
                       project_path: Union[str, Path],
                       output_path: Optional[Union[str, Path]] = None,
                       report_formats: List[str] = None,
                       grid_type: str = 'global_average',
                       development_hours: Optional[float] = None,
                       include_detailed_breakdown: bool = True) -> Dict[str, Any]:
        """
        Perform complete carbon footprint analysis of a software project
        
        Args:
            project_path: Path to the project directory to analyze
            output_path: Directory to save analysis reports (optional)
            report_formats: List of report formats to generate ('json', 'html', 'markdown', 'csv')
            grid_type: Electricity grid type for carbon calculations
            development_hours: Estimated development time for the project
            include_detailed_breakdown: Whether to include detailed per-file analysis
            
        Returns:
            Complete analysis results dictionary
        """
        
        project_path = Path(project_path)
        if not project_path.exists():
            raise FileNotFoundError(f"Project path does not exist: {project_path}")
        
        if report_formats is None:
            report_formats = ['json']
        
        # Start analysis timing
        self.analysis_metadata['analysis_start_time'] = datetime.now()
        start_time = time.time()
        
        try:
            print(f"🔍 Starting carbon footprint analysis of: {project_path}")
            
            # Step 1: Detect languages and project structure
            print("📊 Detecting languages and analyzing project structure...")
            language_detection = self.language_detector.detect_languages(
                project_path, 
                self.config.get('ignore_patterns', [])
            )
            
            # Step 2: Perform language-specific analysis
            print("🔬 Performing detailed code analysis...")
            project_analysis = self._perform_detailed_analysis(project_path, language_detection)
            
            # Step 3: Calculate carbon footprint
            print("🌱 Calculating carbon footprint...")
            carbon_footprint = self.carbon_calculator.calculate_carbon_footprint(
                project_analysis,
                grid_type=grid_type,
                development_hours=development_hours
            )
            
            # Step 4: Generate recommendations
            print("💡 Generating optimization recommendations...")
            recommendations = self._generate_recommendations(project_analysis, carbon_footprint)
            
            # Step 5: Compile complete results
            complete_results = {
                'metadata': self._finalize_metadata(time.time() - start_time),
                'project_info': self._extract_project_info(project_path),
                'language_detection': language_detection,
                'project_structure': project_analysis.get('project_structure', {}),
                'dependencies': project_analysis.get('dependencies', {}),
                'framework_info': project_analysis.get('framework_info', {}),
                'carbon_footprint': carbon_footprint,
                'recommendations': recommendations,
                'analysis_summary': self._generate_analysis_summary(
                    language_detection, carbon_footprint, recommendations
                )
            }
            
            # Remove detailed breakdown if not requested
            if not include_detailed_breakdown:
                complete_results['project_structure'].pop('file_complexities', None)
            
            # Step 6: Generate and save reports
            if output_path:
                print("📄 Generating reports...")
                self._save_reports(complete_results, output_path, report_formats)
            
            print("✅ Analysis completed successfully!")
            self._print_summary(complete_results)
            
            return complete_results
            
        except Exception as e:
            self.analysis_metadata['errors_encountered'].append(str(e))
            print(f"❌ Analysis failed: {e}")
            raise
    
    def analyze_code_snippet(self, 
                           code: str, 
                           language: str,
                           filename: str = "snippet") -> Dict[str, Any]:
        """
        Analyze a code snippet for carbon footprint
        
        Args:
            code: Code content to analyze
            language: Programming language of the code
            filename: Optional filename for the snippet
            
        Returns:
            Analysis results for the code snippet
        """
        
        # Create temporary analysis structure
        temp_analysis = {
            'language_detection': {
                'primary_language': language,
                'languages': {language: {'files': 1, 'size_bytes': len(code)}},
                'complexity_indicator': 'medium'
            },
            'project_structure': {
                'total_files': 1,
                'file_complexities': {}
            },
            'dependencies': {'total_dependencies': 0, 'heavy_dependencies': []},
            'framework_info': {'detected_frameworks': []}
        }
        
        # Get appropriate analyzer
        analyzer_class = self.analyzers.get(language, self.analyzers['generic'])
        analyzer = analyzer_class(Path('.'), self.config)
        
        # Analyze the code snippet
        snippet_complexity = analyzer._analyze_code_content(code, filename)
        temp_analysis['project_structure']['file_complexities'][filename] = {
            **snippet_complexity,
            'language': language
        }
        
        # Calculate carbon footprint
        carbon_footprint = self.carbon_calculator.calculate_carbon_footprint(temp_analysis)
        
        return {
            'code_analysis': snippet_complexity,
            'carbon_footprint': carbon_footprint,
            'recommendations': self._generate_recommendations(temp_analysis, carbon_footprint)
        }
    
    def compare_projects(self, 
                        project_paths: List[Union[str, Path]],
                        output_path: Optional[Union[str, Path]] = None) -> Dict[str, Any]:
        """
        Compare carbon footprints of multiple projects
        
        Args:
            project_paths: List of project directories to compare
            output_path: Directory to save comparison report
            
        Returns:
            Comparison analysis results
        """
        
        print(f"🔍 Comparing {len(project_paths)} projects...")
        
        project_results = {}
        
        # Analyze each project
        for i, project_path in enumerate(project_paths):
            project_path = Path(project_path)
            project_name = project_path.name
            
            print(f"📊 Analyzing project {i+1}/{len(project_paths)}: {project_name}")
            
            try:
                results = self.analyze_project(
                    project_path,
                    include_detailed_breakdown=False  # Skip detailed breakdown for comparison
                )
                project_results[project_name] = results
            except Exception as e:
                print(f"⚠️ Failed to analyze {project_name}: {e}")
                project_results[project_name] = {'error': str(e)}
        
        # Generate comparison report
        comparison_data = self._generate_comparison_data(project_results)
        
        if output_path:
            comparison_report = self.report_generator.generate_report(
                comparison_data,
                report_type='comparison_report',
                output_format='html',
                output_path=Path(output_path) / 'comparison_report.html'
            )
            print(f"📄 Comparison report saved: {comparison_report}")
        
        return comparison_data
    
    def _load_config(self, config_path: Optional[Path]) -> Dict[str, Any]:
        """Load configuration from file or use defaults"""
        default_config = {
            'ignore_patterns': [
                'node_modules', '.git', '.svn', '.hg', '__pycache__',
                '.pytest_cache', 'target', 'build', 'dist', '.gradle',
                'vendor', '.vscode', '.idea', '*.min.js', '*.min.css'
            ],
            'analysis_depth': 'detailed',  # 'basic', 'detailed', 'comprehensive'
            'carbon_calculation': {
                'default_grid_type': 'global_average',
                'include_development_energy': False,
                'include_deployment_energy': False
            },
            'reporting': {
                'default_formats': ['json'],
                'include_optimization_guide': True,
                'include_comparison_metrics': True
            }
        }
        
        if config_path and config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    user_config = json.load(f)
                
                # Merge user config with defaults
                default_config.update(user_config)
            except Exception as e:
                print(f"⚠️ Failed to load config file: {e}. Using defaults.")
        
        return default_config
    
    def _perform_detailed_analysis(self, project_path: Path, 
                                 language_detection: Dict[str, Any]) -> Dict[str, Any]:
        """Perform detailed analysis using language-specific analyzers"""
        
        primary_language = language_detection.get('primary_language', 'generic')
        
        # Get appropriate analyzer
        analyzer_class = self.analyzers.get(primary_language, self.analyzers['generic'])
        analyzer = analyzer_class(project_path, self.config)
        
        # Perform analysis
        try:
            analysis_results = analyzer.analyze()
            self.analysis_metadata['files_analyzed'] = analysis_results.get('total_files', 0)
            return analysis_results
        except Exception as e:
            print(f"⚠️ Detailed analysis failed, falling back to generic analyzer: {e}")
            self.analysis_metadata['errors_encountered'].append(f"Detailed analysis error: {e}")
            
            # Fallback to generic analyzer
            generic_analyzer = self.analyzers['generic'](project_path, self.config)
            return generic_analyzer.analyze()
    
    def _generate_recommendations(self, project_analysis: Dict[str, Any], 
                                carbon_footprint: Dict[str, Any]) -> List[str]:
        """Generate optimization recommendations"""
        
        recommendations = []
        
        # Get language-specific recommendations from analyzer
        primary_language = project_analysis.get('language_detection', {}).get('primary_language')
        if primary_language in self.analyzers:
            analyzer_class = self.analyzers[primary_language]
            analyzer = analyzer_class(Path('.'), self.config)
            
            language_recommendations = analyzer._get_language_specific_recommendations(
                project_analysis.get('project_structure', {}),
                carbon_footprint
            )
            recommendations.extend(language_recommendations)
        
        # Add general recommendations
        general_recommendations = self._get_general_recommendations(project_analysis, carbon_footprint)
        recommendations.extend(general_recommendations)
        
        return recommendations
    
    def _get_general_recommendations(self, project_analysis: Dict[str, Any], 
                                   carbon_footprint: Dict[str, Any]) -> List[str]:
        """Generate general optimization recommendations"""
        
        recommendations = []
        
        # Based on carbon footprint breakdown
        components = carbon_footprint.get('components', {})
        
        # Dependencies recommendations
        dependency_percentage = components.get('dependencies', {}).get('percentage', 0)
        if dependency_percentage > 20:
            recommendations.extend([
                "📦 High dependency impact detected - audit and remove unused packages",
                "🔍 Consider lighter alternatives to heavy dependencies",
                "📊 Implement dependency analysis in your CI/CD pipeline"
            ])
        
        # Framework recommendations
        framework_percentage = components.get('frameworks', {}).get('percentage', 0)
        if framework_percentage > 30:
            recommendations.extend([
                "🏗️ Framework overhead is significant - evaluate alternatives",
                "⚙️ Optimize framework configuration and remove unused features",
                "📈 Consider micro-framework or modular approaches"
            ])
        
        # Build system recommendations
        build_percentage = components.get('build_system', {}).get('percentage', 0)
        if build_percentage > 15:
            recommendations.extend([
                "🔧 Build system overhead detected - optimize build configuration",
                "⚡ Enable build caching and incremental builds",
                "🚀 Consider faster build tools or parallel builds"
            ])
        
        # Code complexity recommendations
        complexity = project_analysis.get('language_detection', {}).get('complexity_indicator', 'medium')
        if complexity in ['high', 'very_high']:
            recommendations.extend([
                "🧹 High code complexity - refactor complex functions and classes",
                "📏 Implement cyclomatic complexity limits in code quality tools",
                "🎯 Focus on single responsibility principle and clean code practices"
            ])
        
        # Project size recommendations
        total_files = project_analysis.get('project_structure', {}).get('total_files', 0)
        if total_files > 1000:
            recommendations.extend([
                "📁 Large project size - consider modularization",
                "🔄 Implement lazy loading and code splitting",
                "📊 Use static analysis tools to identify dead code"
            ])
        
        return recommendations
    
    def _extract_project_info(self, project_path: Path) -> Dict[str, Any]:
        """Extract basic project information"""
        
        return {
            'name': project_path.name,
            'path': str(project_path),
            'analysis_date': datetime.now().isoformat(),
            'analyzer_version': self.version
        }
    
    def _finalize_metadata(self, duration_seconds: float) -> Dict[str, Any]:
        """Finalize analysis metadata"""
        
        self.analysis_metadata['analysis_duration'] = round(duration_seconds, 2)
        return self.analysis_metadata.copy()
    
    def _generate_analysis_summary(self, language_detection: Dict[str, Any],
                                 carbon_footprint: Dict[str, Any],
                                 recommendations: List[str]) -> Dict[str, Any]:
        """Generate a high-level summary of the analysis"""
        
        return {
            'primary_language': language_detection.get('primary_language', 'Unknown'),
            'total_files': language_detection.get('total_files', 0),
            'project_complexity': language_detection.get('complexity_indicator', 'medium'),
            'carbon_emissions_kg': carbon_footprint.get('total_carbon_kg', 0),
            'energy_consumption_kwh': carbon_footprint.get('total_energy_kwh', 0),
            'impact_level': carbon_footprint.get('comparison_metrics', {}).get('impact_level', 'unknown'),
            'optimization_potential_percentage': carbon_footprint.get('optimization_potential', {}).get('potential_reduction_percentage', 0),
            'recommendation_count': len(recommendations),
            'top_recommendation_categories': self._categorize_recommendations(recommendations)
        }
    
    def _categorize_recommendations(self, recommendations: List[str]) -> List[str]:
        """Extract top recommendation categories"""
        
        categories = {}
        
        for rec in recommendations:
            if 'dependency' in rec.lower() or 'package' in rec.lower():
                categories['Dependencies'] = categories.get('Dependencies', 0) + 1
            elif 'framework' in rec.lower():
                categories['Frameworks'] = categories.get('Frameworks', 0) + 1
            elif 'build' in rec.lower() or 'compile' in rec.lower():
                categories['Build System'] = categories.get('Build System', 0) + 1
            elif 'complexity' in rec.lower() or 'refactor' in rec.lower():
                categories['Code Quality'] = categories.get('Code Quality', 0) + 1
            else:
                categories['Performance'] = categories.get('Performance', 0) + 1
        
        # Return top 3 categories
        sorted_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)
        return [category for category, count in sorted_categories[:3]]
    
    def _save_reports(self, results: Dict[str, Any], 
                     output_path: Union[str, Path], 
                     formats: List[str]):
        """Save analysis reports in multiple formats"""
        
        output_path = Path(output_path)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Generate different report types
        report_types = {
            'technical_details': 'complete_analysis',
            'executive_summary': 'executive_summary', 
            'optimization_guide': 'optimization_guide'
        }
        
        for report_type, filename_base in report_types.items():
            for format_type in formats:
                try:
                    file_extension = format_type
                    filename = f"{filename_base}.{file_extension}"
                    
                    report_path = self.report_generator.generate_report(
                        results,
                        report_type=report_type,
                        output_format=format_type,
                        output_path=output_path / filename
                    )
                    
                    print(f"📄 Generated {report_type} report: {report_path}")
                    
                except Exception as e:
                    print(f"⚠️ Failed to generate {report_type} report in {format_type} format: {e}")
    
    def _generate_comparison_data(self, project_results: Dict[str, Dict]) -> Dict[str, Any]:
        """Generate comparison data for multiple projects"""
        
        comparison = {
            'comparison_type': 'Multi-Project Carbon Footprint Analysis',
            'generated_at': datetime.now().isoformat(),
            'projects_analyzed': len(project_results),
            'projects': {},
            'summary': {
                'most_efficient': None,
                'least_efficient': None,
                'average_carbon_kg': 0,
                'total_carbon_kg': 0
            },
            'recommendations': {
                'best_practices': [],
                'common_issues': [],
                'optimization_opportunities': []
            }
        }
        
        valid_projects = {}
        carbon_values = []
        
        # Process each project
        for project_name, results in project_results.items():
            if 'error' not in results:
                carbon_kg = results.get('carbon_footprint', {}).get('total_carbon_kg', 0)
                carbon_values.append(carbon_kg)
                
                valid_projects[project_name] = {
                    'carbon_kg': carbon_kg,
                    'energy_kwh': results.get('carbon_footprint', {}).get('total_energy_kwh', 0),
                    'primary_language': results.get('language_detection', {}).get('primary_language', 'Unknown'),
                    'complexity': results.get('language_detection', {}).get('complexity_indicator', 'medium'),
                    'files_count': results.get('language_detection', {}).get('total_files', 0)
                }
        
        comparison['projects'] = valid_projects
        
        # Calculate summary statistics
        if carbon_values:
            comparison['summary']['average_carbon_kg'] = sum(carbon_values) / len(carbon_values)
            comparison['summary']['total_carbon_kg'] = sum(carbon_values)
            
            # Find most and least efficient
            min_carbon = min(carbon_values)
            max_carbon = max(carbon_values)
            
            for name, data in valid_projects.items():
                if data['carbon_kg'] == min_carbon:
                    comparison['summary']['most_efficient'] = name
                if data['carbon_kg'] == max_carbon:
                    comparison['summary']['least_efficient'] = name
        
        return comparison
    
    def _print_summary(self, results: Dict[str, Any]):
        """Print a summary of the analysis results"""
        
        summary = results.get('analysis_summary', {})
        carbon_data = results.get('carbon_footprint', {})
        
        print("\n" + "="*60)
        print("📊 CARBON FOOTPRINT ANALYSIS SUMMARY")
        print("="*60)
        
        print(f"🎯 Project: {results.get('project_info', {}).get('name', 'Unknown')}")
        print(f"💻 Primary Language: {summary.get('primary_language', 'Unknown')}")
        print(f"📁 Total Files: {summary.get('total_files', 0):,}")
        print(f"🔧 Complexity: {summary.get('project_complexity', 'medium').title()}")
        
        print("\n🌱 CARBON IMPACT:")
        print(f"   • Total Emissions: {summary.get('carbon_emissions_kg', 0):.6f} kg CO2")
        print(f"   • Energy Consumption: {summary.get('energy_consumption_kwh', 0):.6f} kWh") 
        print(f"   • Impact Level: {summary.get('impact_level', 'unknown').title()}")
        
        # Show component breakdown
        components = carbon_data.get('components', {})
        if components:
            print("\n📊 BREAKDOWN:")
            for component, data in components.items():
                if isinstance(data, dict) and data.get('percentage', 0) > 0:
                    print(f"   • {component.title().replace('_', ' ')}: {data.get('percentage', 0):.1f}%")
        
        # Show optimization potential
        optimization = carbon_data.get('optimization_potential', {})
        if optimization.get('potential_reduction_percentage', 0) > 0:
            print(f"\n⚡ OPTIMIZATION POTENTIAL: {optimization.get('potential_reduction_percentage', 0):.1f}% reduction possible")
        
        # Show top recommendations
        recommendations = results.get('recommendations', [])
        if recommendations:
            print(f"\n💡 TOP RECOMMENDATIONS:")
            for i, rec in enumerate(recommendations[:3], 1):
                print(f"   {i}. {rec}")
        
        print("\n" + "="*60)