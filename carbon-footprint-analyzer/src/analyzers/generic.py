"""
Generic analyzer for any programming language
"""

import re
import json
from pathlib import Path
from typing import Dict, Any, List
from .base_analyzer import BaseAnalyzer

class GenericAnalyzer(BaseAnalyzer):
    """Generic analyzer that works with any programming language"""
    
    def __init__(self, project_path: Path, config: Dict[str, Any]):
        super().__init__(project_path, config)
        self.language = "generic"
        
        # Common patterns for different languages
        self.language_patterns = {
            'functions': [
                r'\bfunction\s+\w+',  # JavaScript
                r'\bdef\s+\w+',       # Python
                r'\b(public|private|protected)?\s*(static\s+)?\w+\s+\w+\s*\(',  # Java/C#
                r'\bfn\s+\w+',       # Rust
                r'\bfunc\s+\w+',     # Go
            ],
            'classes': [
                r'\bclass\s+\w+',    # Most languages
                r'\bstruct\s+\w+',   # C/C++/Rust/Go
                r'\binterface\s+\w+', # Java/C#/TypeScript
            ],
            'loops': [
                r'\b(for|while|foreach)\s*\(',  # Most C-like languages
                r'\bfor\s+\w+\s+in\s+',        # Python/Ruby
                r'\bloop\s*\{',                 # Rust
            ],
            'conditionals': [
                r'\bif\s*\(',        # Most languages
                r'\belse\s*(if)?\s*(\(|\{)',  # else/elif
                r'\bswitch\s*\(',    # C-like languages
                r'\bmatch\s+',       # Rust/Scala
            ],
            'imports': [
                r'\bimport\s+',      # Python/Java
                r'\bfrom\s+\w+\s+import\s+',  # Python
                r'\brequire\s*\(',   # JavaScript/Node.js
                r'\b#include\s+',    # C/C++
                r'\buse\s+',         # Rust
            ]
        }
    
    def _calculate_file_complexity(self, file_path: Path) -> Dict[str, Any]:
        """Calculate complexity metrics for any source file"""
        complexity = {
            'complexity_score': 0,
            'features': {
                'functions': 0,
                'classes': 0,
                'loops': 0,
                'conditionals': 0,
                'imports': 0
            },
            'lines': 0,
            'estimated_runtime_complexity': 'O(n)'
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Count lines
            complexity['lines'] = len([line for line in content.split('\n') 
                                     if line.strip() and not self._is_comment_line(line.strip())])
            
            # Count language features using generic patterns
            total_matches = 0
            for feature, patterns in self.language_patterns.items():
                count = 0
                for pattern in patterns:
                    matches = re.findall(pattern, content, re.MULTILINE | re.IGNORECASE)
                    count += len(matches)
                
                complexity['features'][feature] = count
                total_matches += count
            
            # Calculate complexity score
            # Base score from lines of code
            base_score = complexity['lines'] * 0.1
            
            # Add complexity from language constructs
            construct_score = (
                complexity['features']['functions'] * 2 +
                complexity['features']['classes'] * 3 +
                complexity['features']['loops'] * 2 +
                complexity['features']['conditionals'] * 1.5 +
                complexity['features']['imports'] * 0.5
            )
            
            complexity['complexity_score'] = base_score + construct_score
            
            # Estimate runtime complexity based on nested loops
            nested_loop_patterns = [
                r'for\s*\([^}]*for\s*\(',  # Nested for loops
                r'while\s*\([^}]*while\s*\(',  # Nested while loops
            ]
            
            nested_loops = 0
            for pattern in nested_loop_patterns:
                nested_loops += len(re.findall(pattern, content, re.MULTILINE | re.IGNORECASE))
            
            if nested_loops > 2:
                complexity['estimated_runtime_complexity'] = 'O(n³) or higher'
            elif nested_loops > 0:
                complexity['estimated_runtime_complexity'] = 'O(n²)'
            elif complexity['features']['loops'] > 5:
                complexity['estimated_runtime_complexity'] = 'O(n log n)'
            else:
                complexity['estimated_runtime_complexity'] = 'O(n)'
            
        except Exception:
            pass
        
        return complexity
    
    def _analyze_dependencies(self) -> Dict[str, Any]:
        """Analyze dependencies for generic projects"""
        dependencies = {
            'package_managers': {},
            'total_dependencies': 0,
            'heavy_dependencies': [],
            'dependency_files': []
        }
        
        # Common dependency files across languages
        dependency_files = {
            'package.json': 'npm/yarn (JavaScript)',
            'requirements.txt': 'pip (Python)',
            'Pipfile': 'pipenv (Python)',
            'pyproject.toml': 'poetry/pip (Python)',
            'pom.xml': 'maven (Java)',
            'build.gradle': 'gradle (Java)',
            'Cargo.toml': 'cargo (Rust)',
            'go.mod': 'go modules (Go)',
            'Gemfile': 'bundler (Ruby)',
            'composer.json': 'composer (PHP)',
            'packages.config': 'NuGet (C#)',
            'project.json': '.NET Core (C#)',
        }
        
        for dep_file, manager in dependency_files.items():
            dep_path = self.project_path / dep_file
            if dep_path.exists():
                dependencies['dependency_files'].append(dep_file)
                deps_info = self._parse_dependency_file(dep_path, manager)
                dependencies['package_managers'][manager] = deps_info
                dependencies['total_dependencies'] += deps_info.get('count', 0)
        
        # Identify heavy dependencies (heuristic)
        heavy_indicators = [
            'tensorflow', 'pytorch', 'numpy', 'scipy',  # Data science (Python)
            'react', 'angular', '@angular', 'vue',      # Frontend frameworks
            'spring', 'hibernate',                      # Java frameworks
            'boost',                                    # C++ libraries
            'tokio', 'serde',                          # Rust libraries
        ]
        
        for manager_info in dependencies['package_managers'].values():
            packages = manager_info.get('packages', [])
            for pkg in packages:
                if any(indicator in pkg.lower() for indicator in heavy_indicators):
                    dependencies['heavy_dependencies'].append(pkg)
        
        return dependencies
    
    def _parse_dependency_file(self, file_path: Path, manager: str) -> Dict[str, Any]:
        """Parse dependency file and extract package information"""
        deps_info = {
            'count': 0,
            'packages': [],
            'manager': manager
        }
        
        try:
            if file_path.suffix == '.json':
                with open(file_path, 'r') as f:
                    data = json.load(f)
                
                if 'dependencies' in data:
                    deps = data['dependencies']
                    deps_info['count'] += len(deps)
                    deps_info['packages'].extend(deps.keys())
                
                if 'devDependencies' in data:
                    dev_deps = data['devDependencies']
                    deps_info['count'] += len(dev_deps)
                    deps_info['packages'].extend(dev_deps.keys())
            
            elif file_path.suffix == '.txt':
                # requirements.txt format
                with open(file_path, 'r') as f:
                    lines = f.readlines()
                
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        pkg_name = line.split('==')[0].split('>=')[0].split('~=')[0].strip()
                        if pkg_name:
                            deps_info['packages'].append(pkg_name)
                            deps_info['count'] += 1
            
            elif file_path.suffix == '.toml':
                # Basic TOML parsing for dependencies
                with open(file_path, 'r') as f:
                    content = f.read()
                
                # Look for [dependencies] section
                deps_match = re.search(r'\[dependencies\](.*?)(?=\[|\Z)', content, re.DOTALL)
                if deps_match:
                    deps_section = deps_match.group(1)
                    # Extract package names (basic regex)
                    packages = re.findall(r'^(\w[\w\-_]*)\s*=', deps_section, re.MULTILINE)
                    deps_info['packages'].extend(packages)
                    deps_info['count'] = len(packages)
            
            elif file_path.suffix == '.xml':
                # Basic XML parsing for Maven pom.xml
                with open(file_path, 'r') as f:
                    content = f.read()
                
                # Extract dependencies from XML (basic regex)
                deps = re.findall(r'<artifactId>(.*?)</artifactId>', content)
                deps_info['packages'].extend(deps)
                deps_info['count'] = len(deps)
        
        except Exception:
            pass
        
        return deps_info
    
    def _detect_framework(self) -> Dict[str, Any]:
        """Detect framework being used (generic detection)"""
        framework_info = {
            'detected_frameworks': [],
            'confidence': 'low',
            'evidence': []
        }
        
        # Framework detection patterns
        framework_patterns = {
            'react': ['react', 'jsx', 'react-dom'],
            'vue': ['vue', '.vue', 'vue-cli'],
            'angular': ['@angular', 'angular.json', 'ng-'],
            'django': ['django', 'manage.py', 'settings.py'],
            'flask': ['flask', 'app.py', '@app.route'],
            'spring': ['springframework', 'spring-boot', '@SpringBootApplication'],
            'rails': ['rails', 'Gemfile', 'config/routes.rb'],
            'laravel': ['laravel', 'artisan', 'composer.json'],
            'express': ['express', 'app.js', 'server.js'],
        }
        
        # Check dependency files
        for framework, indicators in framework_patterns.items():
            evidence_count = 0
            evidence_found = []
            
            for indicator in indicators:
                # Check in dependency files
                for dep_info in self._analyze_dependencies()['package_managers'].values():
                    if any(indicator.lower() in pkg.lower() for pkg in dep_info.get('packages', [])):
                        evidence_count += 1
                        evidence_found.append(f"Package: {indicator}")
                
                # Check for specific files
                if '.' in indicator:  # File extension or specific file
                    if indicator.startswith('.'):  # Extension
                        for file_path in self.project_path.rglob(f"*{indicator}"):
                            evidence_count += 1
                            evidence_found.append(f"File: {file_path.name}")
                            break
                    else:  # Specific file
                        if (self.project_path / indicator).exists():
                            evidence_count += 1
                            evidence_found.append(f"File: {indicator}")
            
            if evidence_count > 0:
                framework_info['detected_frameworks'].append(framework)
                framework_info['evidence'].extend(evidence_found)
                
                if evidence_count >= 2:
                    framework_info['confidence'] = 'high'
                elif evidence_count == 1:
                    framework_info['confidence'] = 'medium'
        
        return framework_info
    
    def _get_language_specific_recommendations(self, structure: Dict[str, Any], 
                                            energy_data: Dict[str, Any]) -> List[str]:
        """Get generic optimization recommendations"""
        recommendations = []
        
        # Based on detected frameworks
        frameworks = structure.get('framework_info', {}).get('detected_frameworks', [])
        
        if 'react' in frameworks:
            recommendations.extend([
                "⚛️ React detected - use React.memo for expensive components",
                "📦 Implement code splitting with React.lazy",
                "🔄 Use useCallback and useMemo for optimization"
            ])
        
        if 'vue' in frameworks:
            recommendations.extend([
                "🖖 Vue detected - use v-memo for expensive list rendering",
                "📦 Implement dynamic imports for route-based code splitting"
            ])
        
        if 'django' in frameworks:
            recommendations.extend([
                "🐍 Django detected - optimize database queries with select_related",
                "💾 Use Django's caching framework for expensive operations",
                "📊 Consider using database indexes for frequently queried fields"
            ])
        
        if 'spring' in frameworks:
            recommendations.extend([
                "☕ Spring detected - use @Cacheable for expensive method calls",
                "🔄 Implement connection pooling for database operations",
                "📦 Use Spring Boot's actuator for monitoring"
            ])
        
        # Generic recommendations based on complexity
        total_complexity = sum(
            file_info.get('complexity_score', 0) 
            for file_info in structure.get('file_complexities', {}).values()
        )
        
        if total_complexity > 1000:
            recommendations.append(
                "🏗️ High code complexity detected - consider refactoring into smaller modules"
            )
        
        # Dependency-based recommendations
        heavy_deps = structure.get('dependencies', {}).get('heavy_dependencies', [])
        if len(heavy_deps) > 3:
            recommendations.append(
                f"📚 Heavy dependencies detected: {', '.join(heavy_deps[:3])}... - consider alternatives"
            )
        
        return recommendations