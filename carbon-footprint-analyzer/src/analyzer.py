#!/usr/bin/env python3
"""
Universal Carbon Footprint Analyzer
Analyzes carbon footprint for projects in any programming language
"""

import os
import json
import argparse
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional, Union

# Import analyzers
from analyzers.javascript import JavaScriptAnalyzer
from analyzers.python import PythonAnalyzer
from analyzers.java import JavaAnalyzer
from analyzers.generic import GenericAnalyzer
from core.detector import LanguageDetector
from core.metrics import CarbonCalculator
from core.reporter import ReportGenerator

class CarbonAnalyzer:
    """Universal Carbon Footprint Analyzer for any programming language"""
    
    # Language analyzer mapping
    ANALYZERS = {
        'javascript': JavaScriptAnalyzer,
        'typescript': JavaScriptAnalyzer,
        'python': PythonAnalyzer,
        'java': JavaAnalyzer,
        'generic': GenericAnalyzer
    }
    
    def __init__(self, project_path: str, language: str = "auto", 
                 config_file: str = None, output_dir: str = "./reports"):
        """
        Initialize the Carbon Analyzer
        
        Args:
            project_path: Path to the project to analyze
            language: Programming language ('auto' for detection)
            config_file: Custom configuration file path
            output_dir: Output directory for reports
        """
        self.project_path = Path(project_path).resolve()
        self.language = language
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Load configuration
        self.config = self._load_config(config_file)
        
        # Initialize components
        self.detector = LanguageDetector(self.config)
        self.calculator = CarbonCalculator(self.config)
        self.reporter = ReportGenerator(self.config)
        
        # Analysis results
        self.results = None
        
    def _load_config(self, config_file: str = None) -> Dict[str, Any]:
        """Load configuration from file or use defaults"""
        default_config_path = Path(__file__).parent.parent / "configs" / "default.json"
        
        if config_file:
            config_path = Path(config_file)
        else:
            config_path = default_config_path
            
        if config_path.exists():
            with open(config_path, 'r') as f:
                return json.load(f)
        else:
            # Return minimal default config
            return {
                "energy_factors": {
                    "cpu_per_second": 0.0001,
                    "memory_per_mb": 0.00001,
                    "network_per_mb": 0.00005,
                    "storage_per_gb": 0.002
                },
                "co2_factors": {
                    "kwh_to_kg_co2": 0.5,
                    "server_efficiency": 1.2
                },
                "language_multipliers": {
                    "javascript": 1.0,
                    "python": 1.2,
                    "java": 1.5,
                    "generic": 1.1
                }
            }
    
    def analyze(self) -> Dict[str, Any]:
        """
        Run complete carbon footprint analysis
        
        Returns:
            Dictionary containing analysis results
        """
        print(f"🌱 Starting Carbon Footprint Analysis")
        print(f"📁 Project: {self.project_path}")
        print("=" * 60)
        
        # Step 1: Detect language if auto
        if self.language == "auto":
            print("🔍 Detecting programming language...")
            detected_info = self.detector.detect_language(self.project_path)
            self.language = detected_info['primary_language']
            framework = detected_info.get('framework', 'none')
            print(f"   Detected: {self.language} ({framework})")
        
        # Step 2: Initialize appropriate analyzer
        print(f"🔧 Initializing {self.language} analyzer...")
        AnalyzerClass = self.ANALYZERS.get(self.language, GenericAnalyzer)
        analyzer = AnalyzerClass(self.project_path, self.config)
        
        # Step 3: Analyze project structure
        print("📊 Analyzing project structure...")
        structure = analyzer.analyze_project_structure()
        
        # Step 4: Calculate complexity metrics
        print("🧮 Calculating complexity metrics...")
        complexity = analyzer.calculate_complexity_metrics()
        
        # Step 5: Estimate energy consumption
        print("⚡ Estimating energy consumption...")
        energy_data = self.calculator.calculate_energy_consumption(
            structure, complexity, self.language
        )
        
        # Step 6: Generate recommendations
        print("💡 Generating optimization recommendations...")
        recommendations = analyzer.generate_recommendations(structure, energy_data)
        
        # Step 7: Compile results
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'project_path': str(self.project_path),
            'language': self.language,
            'framework': detected_info.get('framework', 'none') if self.language == "auto" else 'unknown',
            'project_structure': structure,
            'complexity_metrics': complexity,
            'energy_consumption': energy_data,
            'recommendations': recommendations,
            'summary': {
                'total_files_analyzed': structure.get('total_files', 0),
                'lines_of_code': structure.get('total_lines', 0),
                'estimated_co2_emissions_kg': energy_data.get('estimated_co2_kg', 0),
                'total_energy_consumption_kwh': energy_data.get('total_energy_kwh', 0),
                'language': self.language,
                'carbon_intensity': self._calculate_carbon_intensity()
            }
        }
        
        print("✅ Analysis complete!")
        return self.results
    
    def _calculate_carbon_intensity(self) -> str:
        """Calculate carbon intensity rating"""
        if not self.results:
            return "unknown"
            
        co2_per_loc = (self.results['summary']['estimated_co2_emissions_kg'] / 
                      max(self.results['summary']['lines_of_code'], 1))
        
        if co2_per_loc < 0.00001:
            return "excellent"
        elif co2_per_loc < 0.00005:
            return "good" 
        elif co2_per_loc < 0.0001:
            return "moderate"
        else:
            return "high"
    
    def generate_dashboard(self, port: int = 8080) -> str:
        """
        Generate and serve interactive dashboard
        
        Args:
            port: Port number for web server
            
        Returns:
            URL of the dashboard
        """
        if not self.results:
            raise ValueError("No analysis results available. Run analyze() first.")
        
        print(f"🎨 Generating interactive dashboard...")
        
        # Generate dashboard files
        dashboard_path = self.reporter.generate_dashboard(
            self.results, 
            output_dir=self.output_dir / "dashboard"
        )
        
        # Start web server
        import subprocess
        server_script = Path(__file__).parent.parent / "dashboard" / "server.py"
        
        print(f"🚀 Starting dashboard server on port {port}...")
        print(f"🌐 Dashboard URL: http://localhost:{port}")
        
        # Run server in background
        subprocess.Popen([
            sys.executable, str(server_script),
            "--port", str(port),
            "--directory", str(dashboard_path)
        ])
        
        return f"http://localhost:{port}"
    
    def export_report(self, format_type: str = "json", 
                     output_file: str = None) -> str:
        """
        Export analysis results to various formats
        
        Args:
            format_type: Export format ('json', 'csv', 'html', 'pdf')
            output_file: Output file path (auto-generated if None)
            
        Returns:
            Path to exported file
        """
        if not self.results:
            raise ValueError("No analysis results available. Run analyze() first.")
        
        if output_file is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = self.output_dir / f"carbon_report_{timestamp}.{format_type}"
        
        print(f"📄 Exporting {format_type.upper()} report to {output_file}")
        
        if format_type == "json":
            with open(output_file, 'w') as f:
                json.dump(self.results, f, indent=2, default=str)
                
        elif format_type == "csv":
            self.reporter.export_csv(self.results, output_file)
            
        elif format_type == "html":
            self.reporter.export_html(self.results, output_file)
            
        elif format_type == "pdf":
            self.reporter.export_pdf(self.results, output_file)
            
        else:
            raise ValueError(f"Unsupported format: {format_type}")
        
        return str(output_file)
    
    def compare_with(self, other_results: Union[str, Dict]) -> Dict[str, Any]:
        """
        Compare current analysis with previous results
        
        Args:
            other_results: Path to previous results JSON or results dict
            
        Returns:
            Comparison analysis
        """
        if isinstance(other_results, str):
            with open(other_results, 'r') as f:
                other_data = json.load(f)
        else:
            other_data = other_results
        
        if not self.results:
            raise ValueError("No current analysis results. Run analyze() first.")
        
        return self.calculator.compare_results(self.results, other_data)

def main():
    """Command-line interface for the Carbon Analyzer"""
    parser = argparse.ArgumentParser(
        description="Universal Carbon Footprint Analyzer for any programming language",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python analyzer.py --project-path ./my-app
  python analyzer.py --project-path ./my-app --language python --framework django
  python analyzer.py --project-path ./my-app --output-format json,html --dashboard
  python analyzer.py --project-path ./my-app --threshold 0.5 --fail-on-threshold
        """
    )
    
    # Core options
    parser.add_argument('--project-path', '-p', 
                       default='.', 
                       help='Path to project directory (default: current directory)')
    
    parser.add_argument('--language', '-l',
                       default='auto',
                       choices=['auto', 'javascript', 'typescript', 'python', 'java', 'generic'],
                       help='Programming language (default: auto-detect)')
    
    parser.add_argument('--framework', '-f',
                       help='Specific framework (react, django, spring, etc.)')
    
    parser.add_argument('--config', '-c',
                       help='Custom configuration file path')
    
    # Output options
    parser.add_argument('--output-dir', '-o',
                       default='./reports',
                       help='Output directory for reports (default: ./reports)')
    
    parser.add_argument('--output-format',
                       default='json',
                       help='Export formats: json,csv,html,pdf (comma-separated)')
    
    parser.add_argument('--dashboard', '-d',
                       action='store_true',
                       help='Generate interactive dashboard')
    
    parser.add_argument('--port',
                       type=int,
                       default=8080,
                       help='Dashboard port number (default: 8080)')
    
    # Analysis options
    parser.add_argument('--threshold',
                       type=float,
                       help='CO2 threshold in kg (fail if exceeded)')
    
    parser.add_argument('--fail-on-threshold',
                       action='store_true',
                       help='Exit with error code if threshold exceeded')
    
    parser.add_argument('--compare-with',
                       help='Compare with previous results JSON file')
    
    parser.add_argument('--verbose', '-v',
                       action='store_true',
                       help='Enable verbose output')
    
    args = parser.parse_args()
    
    try:
        # Initialize analyzer
        analyzer = CarbonAnalyzer(
            project_path=args.project_path,
            language=args.language,
            config_file=args.config,
            output_dir=args.output_dir
        )
        
        # Run analysis
        results = analyzer.analyze()
        
        # Export reports
        formats = args.output_format.split(',')
        exported_files = []
        
        for format_type in formats:
            format_type = format_type.strip()
            if format_type:
                file_path = analyzer.export_report(format_type)
                exported_files.append(file_path)
        
        # Generate dashboard if requested
        if args.dashboard:
            dashboard_url = analyzer.generate_dashboard(args.port)
            print(f"🌐 Dashboard available at: {dashboard_url}")
        
        # Compare with previous results
        if args.compare_with:
            comparison = analyzer.compare_with(args.compare_with)
            print(f"📊 Comparison results: {comparison}")
        
        # Check threshold
        co2_emissions = results['summary']['estimated_co2_emissions_kg']
        if args.threshold and co2_emissions > args.threshold:
            print(f"❌ CO2 emissions ({co2_emissions:.6f} kg) exceed threshold ({args.threshold} kg)")
            if args.fail_on_threshold:
                sys.exit(1)
        
        # Print summary
        print("\\n" + "=" * 60)
        print("🌱 ANALYSIS SUMMARY")
        print("=" * 60)
        summary = results['summary']
        print(f"📊 Files Analyzed: {summary['total_files_analyzed']}")
        print(f"📝 Lines of Code: {summary['lines_of_code']:,}")
        print(f"⚡ Energy: {summary['total_energy_consumption_kwh']:.6f} kWh")
        print(f"🌍 CO2 Emissions: {co2_emissions:.6f} kg")
        print(f"🏷️ Language: {summary['language']}")
        print(f"📈 Carbon Intensity: {summary['carbon_intensity']}")
        
        print(f"\\n📄 Reports generated:")
        for file_path in exported_files:
            print(f"   • {file_path}")
        
        if args.dashboard:
            print(f"\\n🌐 Interactive dashboard: {dashboard_url}")
            
        print("\\n🌱 Analysis complete!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()