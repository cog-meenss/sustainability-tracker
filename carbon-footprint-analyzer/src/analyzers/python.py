"""
Python-specific carbon footprint analyzer
"""

import re
import ast
from pathlib import Path
from typing import Dict, Any, List
from .base_analyzer import BaseAnalyzer

class PythonAnalyzer(BaseAnalyzer):
    """Specialized analyzer for Python projects"""
    
    def __init__(self, project_path: Path, config: Dict[str, Any]):
        super().__init__(project_path, config)
        self.language = "python"
        self.file_extensions = ['.py', '.pyx', '.pyi']
    
    def _calculate_file_complexity(self, file_path: Path) -> Dict[str, Any]:
        """Calculate Python-specific complexity metrics using AST"""
        complexity = {
            'complexity_score': 0,
            'features': {
                'functions': 0,
                'classes': 0,
                'loops': 0,
                'conditionals': 0,
                'imports': 0,
                'comprehensions': 0,
                'decorators': 0,
                'generators': 0,
            },
            'lines': 0,
            'cyclomatic_complexity': 1,
            'depth_of_inheritance': 0,
            'method_count': 0
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Count lines (excluding comments and empty lines)
            lines = content.split('\n')
            complexity['lines'] = len([
                line for line in lines 
                if line.strip() and not line.strip().startswith('#')
            ])
            
            # Parse AST for accurate analysis
            try:
                tree = ast.parse(content)
                visitor = PythonComplexityVisitor()
                visitor.visit(tree)
                
                complexity['features']['functions'] = visitor.function_count
                complexity['features']['classes'] = visitor.class_count
                complexity['features']['loops'] = visitor.loop_count
                complexity['features']['conditionals'] = visitor.conditional_count
                complexity['features']['imports'] = visitor.import_count
                complexity['features']['comprehensions'] = visitor.comprehension_count
                complexity['features']['decorators'] = visitor.decorator_count
                complexity['features']['generators'] = visitor.generator_count
                complexity['cyclomatic_complexity'] = visitor.cyclomatic_complexity
                complexity['depth_of_inheritance'] = visitor.max_inheritance_depth
                complexity['method_count'] = visitor.method_count
                
            except SyntaxError:
                # Fallback to regex if AST parsing fails
                complexity = self._regex_based_analysis(content, complexity)
            
            # Calculate complexity score
            base_score = complexity['lines'] * 0.1
            
            feature_score = (
                complexity['features']['functions'] * 2 +
                complexity['features']['classes'] * 3 +
                complexity['features']['loops'] * 2 +
                complexity['features']['conditionals'] * 1.5 +
                complexity['features']['comprehensions'] * 1.5 +
                complexity['features']['decorators'] * 1 +
                complexity['features']['generators'] * 2
            )
            
            cyclomatic_score = complexity['cyclomatic_complexity'] * 1.2
            inheritance_penalty = complexity['depth_of_inheritance'] * 2
            
            complexity['complexity_score'] = base_score + feature_score + cyclomatic_score + inheritance_penalty
            
        except Exception:
            pass
        
        return complexity
    
    def _regex_based_analysis(self, content: str, complexity: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback regex-based analysis for Python"""
        patterns = {
            'functions': [r'\bdef\s+\w+\s*\('],
            'classes': [r'\bclass\s+\w+'],
            'loops': [r'\bfor\s+\w+\s+in\s+', r'\bwhile\s+.+:'],
            'conditionals': [r'\bif\s+.+:', r'\belif\s+.+:', r'\belse\s*:'],
            'imports': [r'\bimport\s+', r'\bfrom\s+\w+\s+import\s+'],
            'comprehensions': [r'\[[^\]]*for\s+\w+\s+in\s+[^\]]*\]', r'\{[^}]*for\s+\w+\s+in\s+[^}]*\}'],
            'decorators': [r'@\w+'],
            'generators': [r'\byield\s+']
        }
        
        for feature, feature_patterns in patterns.items():
            count = 0
            for pattern in feature_patterns:
                matches = re.findall(pattern, content, re.MULTILINE)
                count += len(matches)
            complexity['features'][feature] = count
        
        return complexity
    
    def _analyze_dependencies(self) -> Dict[str, Any]:
        """Analyze Python dependencies"""
        dependencies = {
            'package_managers': {},
            'total_dependencies': 0,
            'heavy_dependencies': [],
            'dependency_files': []
        }
        
        # Python dependency files
        dep_files = {
            'requirements.txt': 'pip',
            'Pipfile': 'pipenv',
            'pyproject.toml': 'poetry/pip',
            'setup.py': 'setuptools',
            'conda.yml': 'conda',
            'environment.yml': 'conda'
        }
        
        for dep_file, manager in dep_files.items():
            dep_path = self.project_path / dep_file
            if dep_path.exists():
                dependencies['dependency_files'].append(dep_file)
                deps_info = self._parse_python_dependencies(dep_path, manager)
                dependencies['package_managers'][manager] = deps_info
                dependencies['total_dependencies'] += deps_info.get('count', 0)
        
        # Heavy Python packages (high carbon footprint)
        heavy_python_packages = [
            'tensorflow', 'torch', 'pytorch',  # ML frameworks
            'numpy', 'scipy', 'pandas',       # Scientific computing
            'matplotlib', 'seaborn', 'plotly', # Visualization
            'opencv-python', 'pillow',        # Image processing
            'scikit-learn', 'xgboost',        # ML libraries
            'jupyter', 'notebook',            # Interactive computing
            'django', 'flask-sqlalchemy',     # Web frameworks with ORM
            'celery', 'dask',                # Distributed computing
        ]
        
        for manager_info in dependencies['package_managers'].values():
            packages = manager_info.get('packages', [])
            for pkg in packages:
                if any(heavy_pkg in pkg.lower() for heavy_pkg in heavy_python_packages):
                    dependencies['heavy_dependencies'].append(pkg)
        
        return dependencies
    
    def _parse_python_dependencies(self, file_path: Path, manager: str) -> Dict[str, Any]:
        """Parse Python dependency files"""
        deps_info = {
            'count': 0,
            'packages': [],
            'manager': manager
        }
        
        try:
            if file_path.name == 'requirements.txt':
                with open(file_path, 'r') as f:
                    lines = f.readlines()
                
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith('#') and not line.startswith('-'):
                        # Extract package name (before ==, >=, etc.)
                        pkg_name = re.split(r'[><=!~]', line)[0].strip()
                        if pkg_name:
                            deps_info['packages'].append(pkg_name)
                            deps_info['count'] += 1
            
            elif file_path.name == 'setup.py':
                with open(file_path, 'r') as f:
                    content = f.read()
                
                # Extract install_requires
                requires_match = re.search(r'install_requires\s*=\s*\[(.*?)\]', content, re.DOTALL)
                if requires_match:
                    requires_str = requires_match.group(1)
                    packages = re.findall(r'["\']([^"\'>=<!\s]+)', requires_str)
                    deps_info['packages'].extend(packages)
                    deps_info['count'] = len(packages)
            
            elif file_path.suffix == '.toml':
                # Basic TOML parsing for pyproject.toml
                with open(file_path, 'r') as f:
                    content = f.read()
                
                # Look for dependencies section
                deps_match = re.search(r'\[tool\.poetry\.dependencies\](.*?)(?=\[|\Z)', content, re.DOTALL)
                if not deps_match:
                    deps_match = re.search(r'\[project\].*?dependencies\s*=\s*\[(.*?)\]', content, re.DOTALL)
                
                if deps_match:
                    deps_section = deps_match.group(1)
                    packages = re.findall(r'["\']([^"\'>=<!\s]+)', deps_section)
                    deps_info['packages'].extend(packages)
                    deps_info['count'] = len(packages)
        
        except Exception:
            pass
        
        return deps_info
    
    def _detect_framework(self) -> Dict[str, Any]:
        """Detect Python framework being used"""
        framework_info = {
            'detected_frameworks': [],
            'confidence': 'low',
            'evidence': [],
            'python_version': None
        }
        
        # Framework detection based on dependencies and files
        framework_indicators = {
            'django': ['django', 'manage.py', 'settings.py', 'urls.py'],
            'flask': ['flask', 'app.py', 'application.py'],
            'fastapi': ['fastapi', 'main.py'],
            'tornado': ['tornado'],
            'pyramid': ['pyramid'],
            'bottle': ['bottle'],
            'cherrypy': ['cherrypy'],
            'jupyter': ['jupyter', 'notebook', '*.ipynb'],
            'streamlit': ['streamlit'],
            'dash': ['dash'],
        }
        
        # Check dependencies
        deps = self._analyze_dependencies()
        all_packages = []
        for manager_info in deps['package_managers'].values():
            all_packages.extend(manager_info.get('packages', []))
        
        for framework, indicators in framework_indicators.items():
            evidence_count = 0
            evidence_found = []
            
            for indicator in indicators:
                # Check packages
                if any(indicator in pkg.lower() for pkg in all_packages):
                    evidence_count += 1
                    evidence_found.append(f"Package: {indicator}")
                
                # Check files
                if '.' in indicator:
                    if indicator.startswith('*.'):  # Extension
                        ext = indicator[1:]
                        if list(self.project_path.rglob(f"*{ext}")):
                            evidence_count += 1
                            evidence_found.append(f"File: {indicator}")
                    else:  # Specific file
                        if (self.project_path / indicator).exists():
                            evidence_count += 1
                            evidence_found.append(f"File: {indicator}")
            
            if evidence_count > 0:
                framework_info['detected_frameworks'].append(framework)
                framework_info['evidence'].extend(evidence_found)
                framework_info['confidence'] = 'high' if evidence_count >= 2 else 'medium'
        
        # Detect Python version from pyproject.toml or other files
        for version_file in ['pyproject.toml', 'setup.py', '.python-version']:
            version_path = self.project_path / version_file
            if version_path.exists():
                try:
                    with open(version_path, 'r') as f:
                        content = f.read()
                    
                    version_match = re.search(r'python\s*[><=~]\s*["\']?([0-9.]+)', content, re.IGNORECASE)
                    if version_match:
                        framework_info['python_version'] = version_match.group(1)
                        break
                except Exception:
                    continue
        
        return framework_info
    
    def _get_language_specific_recommendations(self, structure: Dict[str, Any], 
                                            energy_data: Dict[str, Any]) -> List[str]:
        """Get Python-specific optimization recommendations"""
        recommendations = []
        
        frameworks = structure.get('framework_info', {}).get('detected_frameworks', [])
        dependencies = structure.get('dependencies', {})
        
        # Django-specific recommendations
        if 'django' in frameworks:
            recommendations.extend([
                "🐍 Django: Use select_related() and prefetch_related() for database optimization",
                "💾 Django: Implement Django's caching framework for expensive operations",
                "📊 Django: Use database indexes for frequently queried fields",
                "🔄 Django: Consider using Django Debug Toolbar to identify slow queries"
            ])
        
        # Flask-specific recommendations
        if 'flask' in frameworks:
            recommendations.extend([
                "🌶️ Flask: Use Flask-Caching for expensive computations",
                "📊 Flask: Implement database connection pooling with SQLAlchemy",
                "🔄 Flask: Use application factory pattern for better resource management"
            ])
        
        # FastAPI-specific recommendations
        if 'fastapi' in frameworks:
            recommendations.extend([
                "⚡ FastAPI: Use async/await for I/O operations",
                "📊 FastAPI: Implement dependency injection for resource management",
                "💾 FastAPI: Use Pydantic models for data validation efficiency"
            ])
        
        # Data science recommendations
        heavy_deps = dependencies.get('heavy_dependencies', [])
        data_science_libs = ['numpy', 'pandas', 'tensorflow', 'torch', 'scikit-learn']
        if any(lib in ' '.join(heavy_deps).lower() for lib in data_science_libs):
            recommendations.extend([
                "📊 Data Science: Use numpy vectorized operations instead of loops",
                "💾 Data Science: Consider using pandas chunking for large datasets",
                "⚡ Data Science: Use multiprocessing for CPU-intensive tasks",
                "🔧 Data Science: Profile memory usage with memory_profiler"
            ])
        
        # General Python recommendations
        total_complexity = sum(
            file_info.get('cyclomatic_complexity', 1)
            for file_info in structure.get('file_complexities', {}).values()
        )
        
        if total_complexity > 100:
            recommendations.extend([
                "🏗️ Python: High cyclomatic complexity detected - refactor complex functions",
                "🔧 Python: Use type hints for better code optimization by interpreters",
                "⚡ Python: Consider using __slots__ for classes with many instances"
            ])
        
        # Performance recommendations based on features
        total_comprehensions = sum(
            file_info.get('features', {}).get('comprehensions', 0)
            for file_info in structure.get('file_complexities', {}).values()
        )
        
        if total_comprehensions > 10:
            recommendations.append(
                "🔄 Python: Many comprehensions detected - ensure they're not nested excessively"
            )
        
        total_generators = sum(
            file_info.get('features', {}).get('generators', 0)
            for file_info in structure.get('file_complexities', {}).values()
        )
        
        if total_generators > 5:
            recommendations.append(
                "⚡ Python: Good use of generators detected - continue using for memory efficiency"
            )
        
        return recommendations


class PythonComplexityVisitor(ast.NodeVisitor):
    """AST visitor to calculate Python complexity metrics"""
    
    def __init__(self):
        self.function_count = 0
        self.class_count = 0
        self.loop_count = 0
        self.conditional_count = 0
        self.import_count = 0
        self.comprehension_count = 0
        self.decorator_count = 0
        self.generator_count = 0
        self.cyclomatic_complexity = 1  # Base complexity
        self.max_inheritance_depth = 0
        self.method_count = 0
        self.current_class_depth = 0
    
    def visit_FunctionDef(self, node):
        self.function_count += 1
        if self.current_class_depth > 0:
            self.method_count += 1
        
        # Count decorators
        self.decorator_count += len(node.decorator_list)
        
        self.generic_visit(node)
    
    def visit_AsyncFunctionDef(self, node):
        self.function_count += 1
        if self.current_class_depth > 0:
            self.method_count += 1
        
        # Count decorators
        self.decorator_count += len(node.decorator_list)
        
        self.generic_visit(node)
    
    def visit_ClassDef(self, node):
        self.class_count += 1
        
        # Calculate inheritance depth
        if node.bases:
            self.max_inheritance_depth = max(self.max_inheritance_depth, len(node.bases))
        
        # Count decorators
        self.decorator_count += len(node.decorator_list)
        
        # Track class depth for method counting
        self.current_class_depth += 1
        self.generic_visit(node)
        self.current_class_depth -= 1
    
    def visit_For(self, node):
        self.loop_count += 1
        self.cyclomatic_complexity += 1
        self.generic_visit(node)
    
    def visit_While(self, node):
        self.loop_count += 1
        self.cyclomatic_complexity += 1
        self.generic_visit(node)
    
    def visit_If(self, node):
        self.conditional_count += 1
        self.cyclomatic_complexity += 1
        self.generic_visit(node)
    
    def visit_Import(self, node):
        self.import_count += len(node.names)
        self.generic_visit(node)
    
    def visit_ImportFrom(self, node):
        self.import_count += len(node.names)
        self.generic_visit(node)
    
    def visit_ListComp(self, node):
        self.comprehension_count += 1
        self.generic_visit(node)
    
    def visit_DictComp(self, node):
        self.comprehension_count += 1
        self.generic_visit(node)
    
    def visit_SetComp(self, node):
        self.comprehension_count += 1
        self.generic_visit(node)
    
    def visit_GeneratorExp(self, node):
        self.comprehension_count += 1
        self.generic_visit(node)
    
    def visit_Yield(self, node):
        self.generator_count += 1
        self.generic_visit(node)
    
    def visit_YieldFrom(self, node):
        self.generator_count += 1
        self.generic_visit(node)