"""
Carbon Footprint Analyzer - Universal code carbon footprint analysis tool
"""

from .carbon_analyzer import CarbonAnalyzer
from .core.detector import LanguageDetector
from .core.metrics import CarbonCalculator
from .core.reporter import ReportGenerator

__version__ = "1.0.0"
__author__ = "Carbon Footprint Analyzer Team"
__description__ = "Universal carbon footprint analyzer for software projects"

# Main exports
__all__ = [
    'CarbonAnalyzer',
    'LanguageDetector', 
    'CarbonCalculator',
    'ReportGenerator'
]

# Convenience function for quick analysis
def analyze_project(project_path, **kwargs):
    """
    Quick project analysis function
    
    Args:
        project_path: Path to project directory
        **kwargs: Additional arguments passed to CarbonAnalyzer.analyze_project()
    
    Returns:
        Analysis results dictionary
    """
    analyzer = CarbonAnalyzer()
    return analyzer.analyze_project(project_path, **kwargs)

def analyze_code(code, language, **kwargs):
    """
    Quick code snippet analysis function
    
    Args:
        code: Code content to analyze
        language: Programming language
        **kwargs: Additional arguments passed to CarbonAnalyzer.analyze_code_snippet()
    
    Returns:
        Analysis results dictionary
    """
    analyzer = CarbonAnalyzer()
    return analyzer.analyze_code_snippet(code, language, **kwargs)