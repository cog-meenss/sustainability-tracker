#!/usr/bin/env python3
"""
Command-line interface for Carbon Footprint Analyzer
"""

import sys
import argparse
import json
from pathlib import Path
from typing import List, Optional

# Add src to path for local imports
sys.path.insert(0, str(Path(__file__).parent / 'src'))

try:
    from src.carbon_analyzer import CarbonAnalyzer
except ImportError:
    # Fallback for installed package
    from carbon_footprint_analyzer import CarbonAnalyzer

def main():
    """Main CLI entry point"""
    
    parser = argparse.ArgumentParser(
        description='Universal Carbon Footprint Analyzer for Software Projects',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic analysis
  carbon-analyzer /path/to/project
  
  # Analysis with HTML report
  carbon-analyzer /path/to/project --output ./reports --format html json
  
  # Analysis with custom config
  carbon-analyzer /path/to/project --config web_app_config.json
  
  # Compare multiple projects
  carbon-analyzer --compare project1/ project2/ project3/ --output ./comparison
  
  # Analyze code snippet
  carbon-analyzer --code "console.log('hello')" --language javascript
        """
    )
    
    # Main command options
    parser.add_argument(
        'project_path',
        nargs='?',
        help='Path to the project directory to analyze'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        help='Output directory for reports (default: ./carbon_reports)'
    )
    
    parser.add_argument(
        '--format', '-f',
        nargs='+',
        choices=['json', 'html', 'markdown', 'csv'],
        default=['json'],
        help='Report output formats (default: json)'
    )
    
    parser.add_argument(
        '--config', '-c',
        type=str,
        help='Path to configuration file'
    )
    
    parser.add_argument(
        '--grid-type', '-g',
        choices=['global_average', 'renewable_heavy', 'coal_heavy', 'natural_gas', 'nuclear'],
        default='global_average',
        help='Electricity grid type for carbon calculations (default: global_average)'
    )
    
    parser.add_argument(
        '--dev-hours',
        type=float,
        help='Estimated development hours for the project'
    )
    
    parser.add_argument(
        '--detailed',
        action='store_true',
        help='Include detailed per-file analysis in reports'
    )
    
    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Suppress output except for errors'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    
    # Code snippet analysis
    parser.add_argument(
        '--code',
        type=str,
        help='Analyze a code snippet instead of a project'
    )
    
    parser.add_argument(
        '--language', '-l',
        type=str,
        help='Programming language for code snippet analysis'
    )
    
    # Comparison mode
    parser.add_argument(
        '--compare',
        nargs='+',
        help='Compare multiple projects (provide multiple project paths)'
    )
    
    # Configuration helpers
    parser.add_argument(
        '--list-configs',
        action='store_true',
        help='List available example configurations'
    )
    
    parser.add_argument(
        '--list-languages',
        action='store_true',
        help='List supported programming languages'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='Carbon Footprint Analyzer 1.0.0'
    )
    
    args = parser.parse_args()
    
    # Handle special commands
    if args.list_configs:
        list_example_configs()
        return
    
    if args.list_languages:
        list_supported_languages()
        return
    
    # Validate arguments
    if not args.code and not args.project_path and not args.compare:
        parser.error("Must provide either project_path, --code, or --compare")
    
    if args.code and not args.language:
        parser.error("--language is required when using --code")
    
    # Set up output directory
    output_path = Path(args.output) if args.output else Path('./carbon_reports')
    
    # Load configuration
    config_path = None
    if args.config:
        config_path = Path(args.config)
        if not config_path.exists():
            # Try looking in examples/configs
            example_config = Path(__file__).parent / 'examples' / 'configs' / args.config
            if example_config.exists():
                config_path = example_config
            else:
                print(f"❌ Configuration file not found: {args.config}", file=sys.stderr)
                sys.exit(1)
    
    try:
        # Initialize analyzer
        analyzer = CarbonAnalyzer(config_path)
        
        if not args.quiet:
            print("🌱 Carbon Footprint Analyzer v1.0.0")
            print("=" * 50)
        
        # Handle different modes
        if args.code:
            # Code snippet analysis
            results = analyze_code_snippet(analyzer, args.code, args.language, args.quiet)
            
            if output_path:
                save_snippet_results(results, output_path, args.format)
        
        elif args.compare:
            # Comparison mode
            results = compare_projects(analyzer, args.compare, output_path, args.quiet)
        
        else:
            # Single project analysis
            results = analyze_single_project(
                analyzer,
                args.project_path,
                output_path,
                args.format,
                args.grid_type,
                args.dev_hours,
                args.detailed,
                args.quiet
            )
        
        if not args.quiet:
            print("\n✅ Analysis completed successfully!")
            if output_path:
                print(f"📄 Reports saved to: {output_path}")
    
    except KeyboardInterrupt:
        print("\n⚠️ Analysis interrupted by user", file=sys.stderr)
        sys.exit(1)
    
    except Exception as e:
        print(f"❌ Analysis failed: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

def analyze_single_project(analyzer: CarbonAnalyzer,
                         project_path: str,
                         output_path: Path,
                         formats: List[str],
                         grid_type: str,
                         dev_hours: Optional[float],
                         detailed: bool,
                         quiet: bool) -> dict:
    """Analyze a single project"""
    
    project_path = Path(project_path)
    
    if not project_path.exists():
        raise FileNotFoundError(f"Project path does not exist: {project_path}")
    
    if not quiet:
        print(f"🔍 Analyzing project: {project_path}")
    
    results = analyzer.analyze_project(
        project_path=project_path,
        output_path=output_path,
        report_formats=formats,
        grid_type=grid_type,
        development_hours=dev_hours,
        include_detailed_breakdown=detailed
    )
    
    return results

def analyze_code_snippet(analyzer: CarbonAnalyzer,
                        code: str,
                        language: str,
                        quiet: bool) -> dict:
    """Analyze a code snippet"""
    
    if not quiet:
        print(f"🔍 Analyzing {language} code snippet ({len(code)} characters)")
    
    results = analyzer.analyze_code_snippet(code, language)
    
    # Print snippet results
    if not quiet:
        carbon_kg = results.get('carbon_footprint', {}).get('total_carbon_kg', 0)
        energy_kwh = results.get('carbon_footprint', {}).get('total_energy_kwh', 0)
        
        print(f"\n📊 SNIPPET ANALYSIS RESULTS:")
        print(f"   • Carbon Emissions: {carbon_kg:.8f} kg CO2")
        print(f"   • Energy Consumption: {energy_kwh:.8f} kWh")
        
        # Show top recommendations
        recommendations = results.get('recommendations', [])
        if recommendations:
            print(f"\n💡 RECOMMENDATIONS:")
            for i, rec in enumerate(recommendations[:3], 1):
                print(f"   {i}. {rec}")
    
    return results

def compare_projects(analyzer: CarbonAnalyzer,
                    project_paths: List[str],
                    output_path: Path,
                    quiet: bool) -> dict:
    """Compare multiple projects"""
    
    if not quiet:
        print(f"🔍 Comparing {len(project_paths)} projects...")
    
    results = analyzer.compare_projects(project_paths, output_path)
    
    # Print comparison results
    if not quiet and 'projects' in results:
        print(f"\n📊 COMPARISON RESULTS:")
        
        projects_data = results['projects']
        if projects_data:
            # Sort by carbon footprint
            sorted_projects = sorted(
                projects_data.items(),
                key=lambda x: x[1].get('carbon_kg', 0)
            )
            
            print(f"   Most Efficient → Least Efficient:")
            for i, (name, data) in enumerate(sorted_projects, 1):
                carbon = data.get('carbon_kg', 0)
                language = data.get('primary_language', 'Unknown')
                files = data.get('files_count', 0)
                print(f"   {i}. {name}: {carbon:.6f} kg CO2 ({language}, {files} files)")
    
    return results

def save_snippet_results(results: dict, output_path: Path, formats: List[str]):
    """Save code snippet analysis results"""
    
    output_path.mkdir(parents=True, exist_ok=True)
    
    for format_type in formats:
        if format_type == 'json':
            output_file = output_path / 'code_snippet_analysis.json'
            with open(output_file, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"📄 Snippet analysis saved: {output_file}")

def list_example_configs():
    """List available example configurations"""
    
    print("📋 Available Example Configurations:")
    print("=" * 50)
    
    configs_dir = Path(__file__).parent / 'examples' / 'configs'
    
    if not configs_dir.exists():
        print("No example configurations found.")
        return
    
    config_files = list(configs_dir.glob('*.json'))
    
    for config_file in sorted(config_files):
        try:
            with open(config_file, 'r') as f:
                config_data = json.load(f)
            
            description = config_data.get('description', 'No description')
            project_type = config_data.get('project_type', 'general')
            
            print(f"📄 {config_file.name}")
            print(f"   Type: {project_type}")
            print(f"   Description: {description}")
            print()
        except Exception:
            print(f"📄 {config_file.name} (failed to load)")
    
    print("Usage: carbon-analyzer /path/to/project --config <config_name>")

def list_supported_languages():
    """List supported programming languages"""
    
    print("💻 Supported Programming Languages:")
    print("=" * 50)
    
    try:
        try:
            from src.core.detector import LanguageDetector
        except ImportError:
            from carbon_footprint_analyzer.core.detector import LanguageDetector
        
        detector = LanguageDetector()
        languages = detector.get_supported_languages()
        
        # Group languages by category
        web_langs = [lang for lang in languages if lang in ['javascript', 'typescript', 'html', 'css']]
        backend_langs = [lang for lang in languages if lang in ['python', 'java', 'go', 'rust', 'csharp', 'php', 'ruby']]
        mobile_langs = [lang for lang in languages if lang in ['swift', 'kotlin', 'dart', 'objc']]
        systems_langs = [lang for lang in languages if lang in ['c', 'cpp', 'rust', 'go']]
        other_langs = [lang for lang in languages if lang not in web_langs + backend_langs + mobile_langs + systems_langs]
        
        categories = [
            ("🌐 Web Technologies", web_langs),
            ("🖥️ Backend Languages", backend_langs), 
            ("📱 Mobile Development", mobile_langs),
            ("⚙️ Systems Programming", systems_langs),
            ("🔧 Other Languages", other_langs)
        ]
        
        for category_name, lang_list in categories:
            if lang_list:
                print(f"\n{category_name}:")
                for lang in sorted(lang_list):
                    print(f"   • {lang}")
        
        print(f"\n📊 Total: {len(languages)} languages supported")
        print("\nNote: Generic analyzer available for unsupported languages")
        
    except Exception as e:
        print(f"❌ Failed to load language list: {e}")

if __name__ == '__main__':
    main()