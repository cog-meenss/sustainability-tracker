"""
Base analyzer class for language-specific carbon footprint analysis
"""

import os
import re
from pathlib import Path
from typing import Dict, Any, List, Tuple
from abc import ABC, abstractmethod

class BaseAnalyzer(ABC):
    """Base class for language-specific carbon footprint analyzers"""
    
    def __init__(self, project_path: Path, config: Dict[str, Any]):
        """
        Initialize base analyzer
        
        Args:
            project_path: Path to project directory
            config: Configuration dictionary
        """
        self.project_path = Path(project_path)
        self.config = config
        self.language = "generic"
        self.file_extensions = []
        self.framework = None
        
    def analyze_project_structure(self) -> Dict[str, Any]:
        """
        Analyze project structure and file statistics
        
        Returns:
            Dictionary containing project structure data
        """
        structure = {
            'total_files': 0,
            'source_files': 0,
            'total_lines': 0,
            'total_size_bytes': 0,
            'file_types': {},
            'file_sizes': {},
            'directories': [],
            'dependencies': {},
            'framework_info': {}
        }
        
        # Walk through project directory
        for root, dirs, files in os.walk(self.project_path):
            # Skip common ignore patterns
            dirs[:] = [d for d in dirs if not self._should_ignore_directory(d)]
            
            rel_root = os.path.relpath(root, self.project_path)
            if rel_root != '.':
                structure['directories'].append(rel_root)
            
            for file in files:
                if self._should_ignore_file(file):
                    continue
                    
                file_path = Path(root) / file
                rel_file_path = os.path.relpath(file_path, self.project_path)
                
                try:
                    file_size = file_path.stat().st_size
                    structure['total_files'] += 1
                    structure['total_size_bytes'] += file_size
                    structure['file_sizes'][rel_file_path] = file_size
                    
                    # Count by extension
                    ext = file_path.suffix.lower()
                    if ext not in structure['file_types']:
                        structure['file_types'][ext] = {'count': 0, 'size': 0, 'lines': 0}
                    structure['file_types'][ext]['count'] += 1
                    structure['file_types'][ext]['size'] += file_size
                    
                    # Count source files and lines
                    if self._is_source_file(file_path):
                        structure['source_files'] += 1
                        lines = self._count_lines(file_path)
                        structure['total_lines'] += lines
                        structure['file_types'][ext]['lines'] += lines
                        
                except (OSError, PermissionError):
                    continue
        
        # Analyze dependencies
        structure['dependencies'] = self._analyze_dependencies()
        
        # Detect framework
        structure['framework_info'] = self._detect_framework()
        
        return structure
    
    def calculate_complexity_metrics(self) -> Dict[str, Any]:
        """
        Calculate code complexity metrics
        
        Returns:
            Dictionary containing complexity metrics
        """
        complexity = {
            'total_complexity_score': 0,
            'average_complexity': 0,
            'file_complexities': {},
            'language_features': {
                'functions': 0,
                'classes': 0,
                'loops': 0,
                'conditionals': 0,
                'imports': 0
            },
            'cyclomatic_complexity': 0,
            'cognitive_complexity': 0
        }
        
        total_files = 0
        total_score = 0
        
        # Analyze each source file
        for root, dirs, files in os.walk(self.project_path):
            dirs[:] = [d for d in dirs if not self._should_ignore_directory(d)]
            
            for file in files:
                file_path = Path(root) / file
                
                if not self._is_source_file(file_path):
                    continue
                
                try:
                    file_complexity = self._calculate_file_complexity(file_path)
                    rel_path = os.path.relpath(file_path, self.project_path)
                    complexity['file_complexities'][rel_path] = file_complexity
                    
                    # Aggregate metrics
                    file_score = file_complexity.get('complexity_score', 0)
                    total_score += file_score
                    total_files += 1
                    
                    # Sum language features
                    for feature, count in file_complexity.get('features', {}).items():
                        if feature in complexity['language_features']:
                            complexity['language_features'][feature] += count
                    
                except Exception:
                    continue
        
        # Calculate averages
        if total_files > 0:
            complexity['average_complexity'] = total_score / total_files
        complexity['total_complexity_score'] = total_score
        
        return complexity
    
    def _analyze_code_content(self, content: str, filename: str) -> Dict[str, Any]:
        """Analyze code content string (for snippet analysis)"""
        
        complexity = {
            'complexity_score': 0,
            'features': {},
            'lines': 0,
            'cyclomatic_complexity': 1,
            'language': self.language
        }
        
        # Basic analysis for code content
        lines = content.split('\n')
        complexity['lines'] = len([line for line in lines if line.strip()])
        
        # Basic complexity estimation
        complexity['complexity_score'] = complexity['lines'] * 0.1
        
        return complexity
    
    def generate_recommendations(self, structure: Dict[str, Any], 
                               energy_data: Dict[str, Any]) -> List[str]:
        """
        Generate optimization recommendations
        
        Args:
            structure: Project structure data
            energy_data: Energy consumption data
            
        Returns:
            List of optimization recommendations
        """
        recommendations = []
        
        # Generic recommendations based on structure
        if structure['total_lines'] > 10000:
            recommendations.append(
                "🔧 Large codebase detected - consider modularization to reduce compilation energy"
            )
        
        if structure['total_size_bytes'] > 100 * 1024 * 1024:  # 100MB
            recommendations.append(
                "📦 Large project size - implement build optimization and asset compression"
            )
        
        # Dependency-based recommendations
        dep_count = sum(len(deps) for deps in structure.get('dependencies', {}).values())
        if dep_count > 50:
            recommendations.append(
                f"📚 High dependency count ({dep_count}) - audit and remove unused dependencies"
            )
        
        # Energy-based recommendations
        total_energy = energy_data.get('total_energy_kwh', 0)
        if total_energy > 1.0:
            recommendations.append(
                "⚡ High energy consumption - profile and optimize computational hotspots"
            )
        
        # Add language-specific recommendations
        recommendations.extend(self._get_language_specific_recommendations(structure, energy_data))
        
        return recommendations
    
    def _should_ignore_directory(self, dirname: str) -> bool:
        """Check if directory should be ignored during analysis"""
        ignore_patterns = [
            '.git', '.svn', '.hg',  # Version control
            'node_modules', '__pycache__', '.pytest_cache',  # Dependencies/cache
            'build', 'dist', 'target', 'bin', 'obj',  # Build artifacts  
            '.idea', '.vscode', '.vs',  # IDE files
            'coverage', 'htmlcov', '.nyc_output',  # Coverage reports
            'logs', 'temp', 'tmp'  # Temporary files
        ]
        return dirname.lower() in [p.lower() for p in ignore_patterns]
    
    def _should_ignore_file(self, filename: str) -> bool:
        """Check if file should be ignored during analysis"""
        ignore_patterns = [
            '.DS_Store', 'Thumbs.db',  # OS files
            '*.log', '*.tmp', '*.temp',  # Temporary files
            '*.pyc', '*.pyo', '*.class',  # Compiled files
            '*.min.js', '*.min.css',  # Minified files
            'package-lock.json', 'yarn.lock', 'Pipfile.lock'  # Lock files
        ]
        
        filename_lower = filename.lower()
        for pattern in ignore_patterns:
            if pattern.startswith('*.'):
                if filename_lower.endswith(pattern[1:]):
                    return True
            elif filename_lower == pattern.lower():
                return True
        return False
    
    def _is_source_file(self, file_path: Path) -> bool:
        """Check if file is a source code file"""
        if not self.file_extensions:
            # Generic source file detection
            source_extensions = [
                '.py', '.js', '.jsx', '.ts', '.tsx', '.java', '.c', '.cpp', '.h', '.hpp',
                '.cs', '.go', '.rs', '.rb', '.php', '.swift', '.kt', '.scala', '.clj',
                '.hs', '.ml', '.fs', '.vb', '.pl', '.r', '.m', '.mm', '.dart'
            ]
            return file_path.suffix.lower() in source_extensions
        else:
            return file_path.suffix.lower() in self.file_extensions
    
    def _count_lines(self, file_path: Path) -> int:
        """Count non-empty, non-comment lines in a file"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            non_empty_lines = 0
            for line in lines:
                stripped = line.strip()
                if stripped and not self._is_comment_line(stripped):
                    non_empty_lines += 1
            
            return non_empty_lines
        except Exception:
            return 0
    
    def _is_comment_line(self, line: str) -> bool:
        """Check if line is a comment (basic implementation)"""
        comment_prefixes = ['//', '#', '/*', '*', '--', '%', ';']
        return any(line.startswith(prefix) for prefix in comment_prefixes)
    
    @abstractmethod
    def _calculate_file_complexity(self, file_path: Path) -> Dict[str, Any]:
        """Calculate complexity metrics for a single file"""
        pass
    
    @abstractmethod
    def _analyze_dependencies(self) -> Dict[str, Any]:
        """Analyze project dependencies"""
        pass
    
    @abstractmethod
    def _detect_framework(self) -> Dict[str, Any]:
        """Detect framework being used"""
        pass
    
    @abstractmethod
    def _get_language_specific_recommendations(self, structure: Dict[str, Any], 
                                            energy_data: Dict[str, Any]) -> List[str]:
        """Get language-specific optimization recommendations"""
        pass
    
    def analyze(self) -> Dict[str, Any]:
        """
        Main analysis method that orchestrates all analysis steps
        
        Returns:
            Complete analysis results
        """
        # Analyze project structure
        structure = self.analyze_project_structure()
        
        # Analyze dependencies
        dependencies = self._analyze_dependencies()
        structure['dependencies'] = dependencies
        
        # Detect framework
        framework_info = self._detect_framework()
        structure['framework_info'] = framework_info
        
        return {
            'language': self.language,
            'structure': structure,
            'framework': framework_info,
            'dependencies': dependencies
        }