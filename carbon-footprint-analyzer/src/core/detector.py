"""
Language detection module for carbon footprint analyzer
"""

from pathlib import Path
from typing import Dict, List, Tuple
import json

class LanguageDetector:
    """Detects programming languages in a project"""
    
    def __init__(self):
        self.language_mappings = {
            # Web Technologies
            '.js': 'javascript',
            '.jsx': 'javascript', 
            '.ts': 'typescript',
            '.tsx': 'typescript',
            '.vue': 'javascript',
            '.html': 'html',
            '.htm': 'html',
            '.css': 'css',
            '.scss': 'css',
            '.sass': 'css',
            '.less': 'css',
            
            # Python
            '.py': 'python',
            '.pyx': 'python',
            '.pyi': 'python',
            '.ipynb': 'jupyter',
            
            # Java/JVM
            '.java': 'java',
            '.kt': 'kotlin',
            '.kts': 'kotlin',
            '.scala': 'scala',
            '.groovy': 'groovy',
            '.clj': 'clojure',
            
            # C/C++
            '.c': 'c',
            '.h': 'c',
            '.cpp': 'cpp',
            '.cxx': 'cpp',
            '.cc': 'cpp',
            '.hpp': 'cpp',
            '.hxx': 'cpp',
            
            # C#/.NET
            '.cs': 'csharp',
            '.vb': 'vbnet',
            '.fs': 'fsharp',
            
            # Go
            '.go': 'go',
            
            # Rust
            '.rs': 'rust',
            
            # Ruby
            '.rb': 'ruby',
            '.rbw': 'ruby',
            
            # PHP
            '.php': 'php',
            '.php3': 'php',
            '.php4': 'php',
            '.php5': 'php',
            '.phtml': 'php',
            
            # Swift
            '.swift': 'swift',
            
            # Objective-C
            '.m': 'objc',
            '.mm': 'objc',
            
            # R
            '.r': 'r',
            '.R': 'r',
            
            # MATLAB
            '.m': 'matlab',  # Note: conflicts with Objective-C
            
            # Shell
            '.sh': 'shell',
            '.bash': 'shell',
            '.zsh': 'shell',
            '.fish': 'shell',
            
            # Dart
            '.dart': 'dart',
            
            # Lua
            '.lua': 'lua',
            
            # Perl
            '.pl': 'perl',
            '.pm': 'perl',
            
            # Haskell
            '.hs': 'haskell',
            '.lhs': 'haskell',
            
            # Erlang/Elixir
            '.erl': 'erlang',
            '.ex': 'elixir',
            '.exs': 'elixir',
            
            # Configuration/Data
            '.json': 'json',
            '.yaml': 'yaml',
            '.yml': 'yaml',
            '.xml': 'xml',
            '.toml': 'toml',
            '.ini': 'ini',
            '.cfg': 'config',
            '.conf': 'config',
            
            # Documentation
            '.md': 'markdown',
            '.rst': 'rst',
            '.tex': 'latex',
            
            # SQL
            '.sql': 'sql',
        }
        
        # Language groups for analysis purposes
        self.language_groups = {
            'web_frontend': ['javascript', 'typescript', 'html', 'css'],
            'web_backend': ['javascript', 'python', 'java', 'php', 'ruby', 'go', 'csharp'],
            'mobile': ['java', 'kotlin', 'swift', 'objc', 'dart'],
            'systems': ['c', 'cpp', 'rust', 'go'],
            'data_science': ['python', 'r', 'matlab', 'sql'],
            'functional': ['haskell', 'clojure', 'fsharp', 'elixir'],
            'scripting': ['python', 'ruby', 'shell', 'perl', 'lua'],
        }
        
        # Framework indicators for more accurate detection
        self.framework_indicators = {
            'javascript': {
                'react': ['package.json', 'src/App.js', 'src/App.jsx', 'public/index.html'],
                'vue': ['package.json', 'src/App.vue', 'vue.config.js'],
                'angular': ['package.json', 'angular.json', 'src/app/app.module.ts'],
                'node': ['package.json', 'server.js', 'app.js', 'index.js'],
                'express': ['package.json', 'app.js', 'server.js'],
                'nextjs': ['next.config.js', 'pages/', 'app/'],
                'nuxt': ['nuxt.config.js', 'pages/', 'layouts/']
            },
            'python': {
                'django': ['manage.py', 'settings.py', 'urls.py', 'requirements.txt'],
                'flask': ['app.py', 'application.py', 'requirements.txt'],
                'fastapi': ['main.py', 'requirements.txt'],
                'jupyter': ['*.ipynb'],
                'data_science': ['requirements.txt', '*.ipynb', 'data/', 'notebooks/']
            },
            'java': {
                'spring': ['pom.xml', 'build.gradle', 'src/main/java/'],
                'android': ['AndroidManifest.xml', 'app/build.gradle', 'res/'],
                'maven': ['pom.xml'],
                'gradle': ['build.gradle', 'build.gradle.kts']
            }
        }
    
    def detect_languages(self, project_path: Path, 
                        ignore_patterns: List[str] = None) -> Dict[str, any]:
        """
        Detect all programming languages used in a project
        
        Args:
            project_path: Path to the project directory
            ignore_patterns: List of patterns to ignore (e.g., ['node_modules', '.git'])
        
        Returns:
            Dictionary with language statistics and detected frameworks
        """
        if ignore_patterns is None:
            ignore_patterns = [
                'node_modules', '.git', '.svn', '.hg',
                '__pycache__', '.pytest_cache', 
                'target', 'build', 'dist', '.gradle',
                'vendor', '.vscode', '.idea',
                '*.min.js', '*.min.css'
            ]
        
        language_stats = {}
        file_counts = {}
        total_files = 0
        
        # Scan all files
        for file_path in self._scan_files(project_path, ignore_patterns):
            total_files += 1
            extension = file_path.suffix.lower()
            
            if extension in self.language_mappings:
                language = self.language_mappings[extension]
                
                # Handle conflicts (e.g., .m for Objective-C vs MATLAB)
                if extension == '.m':
                    language = self._resolve_m_extension_conflict(file_path)
                
                if language not in language_stats:
                    language_stats[language] = {
                        'files': 0,
                        'size_bytes': 0,
                        'extensions': set(),
                        'paths': []
                    }
                
                language_stats[language]['files'] += 1
                language_stats[language]['size_bytes'] += self._get_file_size(file_path)
                language_stats[language]['extensions'].add(extension)
                language_stats[language]['paths'].append(str(file_path.relative_to(project_path)))
                
                file_counts[language] = language_stats[language]['files']
        
        # Convert sets to lists for JSON serialization
        for lang_data in language_stats.values():
            lang_data['extensions'] = list(lang_data['extensions'])
        
        # Determine primary language
        primary_language = self._determine_primary_language(language_stats)
        
        # Detect project type and frameworks
        project_type = self._detect_project_type(project_path, language_stats)
        frameworks = self._detect_frameworks(project_path, language_stats)
        
        return {
            'primary_language': primary_language,
            'languages': language_stats,
            'total_files': total_files,
            'project_type': project_type,
            'frameworks': frameworks,
            'language_distribution': self._calculate_distribution(language_stats),
            'complexity_indicator': self._estimate_complexity(language_stats, frameworks)
        }
    
    def _scan_files(self, project_path: Path, ignore_patterns: List[str]) -> List[Path]:
        """Scan directory for files, respecting ignore patterns"""
        files = []
        
        def should_ignore(path: Path) -> bool:
            path_str = str(path)
            for pattern in ignore_patterns:
                if pattern in path_str or path.name.startswith('.'):
                    return True
            return False
        
        for item in project_path.rglob('*'):
            if item.is_file() and not should_ignore(item):
                files.append(item)
        
        return files
    
    def _get_file_size(self, file_path: Path) -> int:
        """Get file size in bytes"""
        try:
            return file_path.stat().st_size
        except:
            return 0
    
    def _resolve_m_extension_conflict(self, file_path: Path) -> str:
        """Resolve .m extension conflict between Objective-C and MATLAB"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(1000)  # Read first 1000 chars
            
            # Objective-C indicators
            objc_indicators = [
                '#import', '#include', '@interface', '@implementation',
                '@property', '@synthesize', 'NSString', 'NSArray'
            ]
            
            # MATLAB indicators
            matlab_indicators = [
                'function', 'end', '%', 'clear all', 'clc', 'plot',
                'matrix', 'disp(', 'fprintf'
            ]
            
            objc_score = sum(1 for indicator in objc_indicators if indicator in content)
            matlab_score = sum(1 for indicator in matlab_indicators if indicator in content)
            
            return 'objc' if objc_score > matlab_score else 'matlab'
        
        except:
            # Default to Objective-C if we can't determine
            return 'objc'
    
    def _determine_primary_language(self, language_stats: Dict) -> str:
        """Determine the primary programming language of the project"""
        if not language_stats:
            return 'unknown'
        
        # Exclude certain file types from primary language consideration
        exclude_from_primary = ['json', 'yaml', 'xml', 'markdown', 'html', 'css']
        
        # Calculate scores based on file count and size
        scores = {}
        for language, stats in language_stats.items():
            if language not in exclude_from_primary:
                # Weight by both file count and total size
                file_score = stats['files'] * 2
                size_score = stats['size_bytes'] / 1000  # Convert to KB
                scores[language] = file_score + size_score
        
        if not scores:
            # Fallback to any language if all are excluded
            return max(language_stats.keys(), key=lambda x: language_stats[x]['files'])
        
        return max(scores.keys(), key=scores.get)
    
    def _detect_project_type(self, project_path: Path, language_stats: Dict) -> str:
        """Detect the type of project based on files and structure"""
        # Check for specific project indicators
        project_indicators = {
            'web_app': ['package.json', 'index.html', 'src/', 'public/'],
            'mobile_app': ['AndroidManifest.xml', 'ios/', 'android/', 'pubspec.yaml'],
            'desktop_app': ['*.desktop', 'setup.py', '*.exe', 'CMakeLists.txt'],
            'library': ['setup.py', 'pyproject.toml', 'pom.xml', 'build.gradle', 'Cargo.toml'],
            'api_service': ['requirements.txt', 'Dockerfile', 'docker-compose.yml'],
            'data_analysis': ['*.ipynb', 'data/', 'datasets/', 'analysis/'],
            'game': ['Assets/', 'Resources/', 'Scenes/', '*.unity'],
            'cli_tool': ['bin/', 'cli/', 'command/', 'src/main.py', 'src/main.js']
        }
        
        detected_types = []
        
        for project_type, indicators in project_indicators.items():
            score = 0
            for indicator in indicators:
                if indicator.startswith('*.'):
                    # Extension pattern
                    ext = indicator[1:]
                    if list(project_path.rglob(f"*{ext}")):
                        score += 1
                elif indicator.endswith('/'):
                    # Directory pattern
                    if (project_path / indicator.rstrip('/')).exists():
                        score += 2
                else:
                    # File pattern
                    if (project_path / indicator).exists():
                        score += 1
            
            if score >= 2:  # Threshold for detection
                detected_types.append((project_type, score))
        
        if detected_types:
            # Return the type with highest score
            return max(detected_types, key=lambda x: x[1])[0]
        
        # Fallback based on primary language
        primary = self._determine_primary_language(language_stats)
        if primary in ['javascript', 'typescript', 'html', 'css']:
            return 'web_app'
        elif primary in ['python']:
            return 'script'
        elif primary in ['java', 'kotlin']:
            return 'application'
        else:
            return 'general'
    
    def _detect_frameworks(self, project_path: Path, language_stats: Dict) -> Dict[str, List[str]]:
        """Detect frameworks used in the project"""
        detected_frameworks = {}
        
        for language in language_stats.keys():
            if language in self.framework_indicators:
                frameworks = []
                
                for framework, indicators in self.framework_indicators[language].items():
                    evidence_count = 0
                    
                    for indicator in indicators:
                        if indicator.startswith('*.'):
                            # Extension pattern
                            ext = indicator[1:]
                            if list(project_path.rglob(f"*{ext}")):
                                evidence_count += 1
                        elif indicator.endswith('/'):
                            # Directory pattern
                            if (project_path / indicator.rstrip('/')).exists():
                                evidence_count += 2
                        else:
                            # File pattern
                            if (project_path / indicator).exists():
                                evidence_count += 1
                    
                    # Check package.json for JS frameworks
                    if language in ['javascript', 'typescript']:
                        package_json = project_path / 'package.json'
                        if package_json.exists():
                            try:
                                with open(package_json, 'r') as f:
                                    package_data = json.load(f)
                                
                                deps = {**package_data.get('dependencies', {}), 
                                       **package_data.get('devDependencies', {})}
                                
                                if framework in deps or f"@{framework}" in deps:
                                    evidence_count += 2
                            except:
                                pass
                    
                    if evidence_count >= 1:
                        frameworks.append(framework)
                
                if frameworks:
                    detected_frameworks[language] = frameworks
        
        return detected_frameworks
    
    def _calculate_distribution(self, language_stats: Dict) -> Dict[str, float]:
        """Calculate percentage distribution of languages by file count"""
        total_files = sum(stats['files'] for stats in language_stats.values())
        
        if total_files == 0:
            return {}
        
        distribution = {}
        for language, stats in language_stats.items():
            percentage = (stats['files'] / total_files) * 100
            distribution[language] = round(percentage, 2)
        
        return distribution
    
    def _estimate_complexity(self, language_stats: Dict, frameworks: Dict) -> str:
        """Estimate project complexity based on languages and frameworks"""
        complexity_scores = {
            # Language complexity multipliers
            'javascript': 2, 'typescript': 3, 'python': 2, 'java': 4,
            'cpp': 5, 'c': 4, 'csharp': 4, 'go': 3, 'rust': 5,
            'php': 2, 'ruby': 2, 'swift': 3, 'kotlin': 3,
            'html': 1, 'css': 1, 'json': 0.5, 'yaml': 0.5
        }
        
        total_score = 0
        total_files = sum(stats['files'] for stats in language_stats.values())
        
        # Calculate base score from languages
        for language, stats in language_stats.items():
            multiplier = complexity_scores.get(language, 2)
            total_score += stats['files'] * multiplier
        
        # Add framework complexity
        framework_bonus = len([fw for fw_list in frameworks.values() for fw in fw_list]) * 10
        total_score += framework_bonus
        
        # Normalize by total files
        if total_files > 0:
            avg_score = total_score / total_files
        else:
            avg_score = 0
        
        # Categorize complexity
        if avg_score < 2:
            return 'low'
        elif avg_score < 5:
            return 'medium'
        elif avg_score < 10:
            return 'high'
        else:
            return 'very_high'
    
    def get_supported_languages(self) -> List[str]:
        """Get list of all supported programming languages"""
        return sorted(set(self.language_mappings.values()))
    
    def get_language_for_extension(self, extension: str) -> str:
        """Get language for a specific file extension"""
        return self.language_mappings.get(extension.lower(), 'unknown')