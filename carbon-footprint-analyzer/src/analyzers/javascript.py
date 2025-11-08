"""
JavaScript/TypeScript/Node.js specific carbon footprint analyzer
"""

import re
import json
from pathlib import Path
from typing import Dict, Any, List
from .base_analyzer import BaseAnalyzer

class JavaScriptAnalyzer(BaseAnalyzer):
    """Specialized analyzer for JavaScript/TypeScript projects"""
    
    def __init__(self, project_path: Path, config: Dict[str, Any]):
        super().__init__(project_path, config)
        self.language = "javascript"
        self.file_extensions = ['.js', '.jsx', '.ts', '.tsx', '.mjs', '.cjs']
        
        # JavaScript-specific patterns
        self.js_patterns = {
            'functions': [
                r'\bfunction\s+\w+\s*\(',
                r'\bconst\s+\w+\s*=\s*\([^)]*\)\s*=>\s*\{',
                r'\blet\s+\w+\s*=\s*\([^)]*\)\s*=>\s*\{',
                r'\b\w+\s*:\s*function\s*\(',
                r'\b\w+\s*:\s*\([^)]*\)\s*=>\s*\{',
            ],
            'classes': [
                r'\bclass\s+\w+',
                r'\binterface\s+\w+',  # TypeScript
                r'\btype\s+\w+\s*=',   # TypeScript
            ],
            'loops': [
                r'\bfor\s*\(',
                r'\bwhile\s*\(',
                r'\bdo\s*\{.*?\}\s*while',
                r'\.forEach\s*\(',
                r'\.map\s*\(',
                r'\.filter\s*\(',
                r'\.reduce\s*\(',
            ],
            'async_operations': [
                r'\basync\s+function',
                r'\bawait\s+',
                r'\.then\s*\(',
                r'\.catch\s*\(',
                r'\bnew\s+Promise\s*\(',
                r'setTimeout\s*\(',
                r'setInterval\s*\(',
            ],
            'dom_operations': [
                r'document\.',
                r'window\.',
                r'querySelector',
                r'getElementById',
                r'createElement',
                r'addEventListener',
            ],
            'api_calls': [
                r'\bfetch\s*\(',
                r'axios\.',
                r'XMLHttpRequest',
                r'\.get\s*\(',
                r'\.post\s*\(',
            ],
        }
    
    def _calculate_file_complexity(self, file_path: Path) -> Dict[str, Any]:
        """Calculate JavaScript-specific complexity metrics"""
        complexity = {
            'complexity_score': 0,
            'features': {
                'functions': 0,
                'classes': 0,
                'loops': 0,
                'conditionals': 0,
                'imports': 0,
                'async_operations': 0,
                'dom_operations': 0,
                'api_calls': 0,
            },
            'lines': 0,
            'cyclomatic_complexity': 1,  # Base complexity
            'jsx_complexity': 0,
            'typescript_features': 0
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Count lines (excluding comments and empty lines)
            lines = content.split('\n')
            complexity['lines'] = len([
                line for line in lines 
                if line.strip() and not self._is_js_comment_line(line.strip())
            ])
            
            # Count JavaScript-specific patterns
            for feature, patterns in self.js_patterns.items():
                count = 0
                for pattern in patterns:
                    matches = re.findall(pattern, content, re.MULTILINE | re.IGNORECASE)
                    count += len(matches)
                complexity['features'][feature] = count
            
            # Calculate cyclomatic complexity (simplified)
            decision_points = [
                r'\bif\s*\(',
                r'\belse\s+if\s*\(',
                r'\belse\s*\{',
                r'\bswitch\s*\(',
                r'\bcase\s+',
                r'\bfor\s*\(',
                r'\bwhile\s*\(',
                r'\btry\s*\{',
                r'\bcatch\s*\(',
                r'\?\s*.*?\s*:',  # Ternary operator
            ]
            
            for pattern in decision_points:
                matches = re.findall(pattern, content, re.MULTILINE)
                complexity['cyclomatic_complexity'] += len(matches)
            
            # JSX complexity (for React files)
            if file_path.suffix in ['.jsx', '.tsx']:
                jsx_patterns = [
                    r'<\w+[^>]*>',  # JSX elements
                    r'\{[^}]+\}',   # JSX expressions
                    r'useState\s*\(',
                    r'useEffect\s*\(',
                    r'useCallback\s*\(',
                    r'useMemo\s*\(',
                ]
                
                for pattern in jsx_patterns:
                    matches = re.findall(pattern, content)
                    complexity['jsx_complexity'] += len(matches)
            
            # TypeScript complexity (for .ts/.tsx files)
            if file_path.suffix in ['.ts', '.tsx']:
                ts_patterns = [
                    r'\binterface\s+\w+',
                    r'\btype\s+\w+\s*=',
                    r'\benum\s+\w+',
                    r'\bnamespace\s+\w+',
                    r'<[A-Z]\w*>',  # Generic types
                    r':\s*\w+\[\]',  # Array types
                ]
                
                for pattern in ts_patterns:
                    matches = re.findall(pattern, content)
                    complexity['typescript_features'] += len(matches)
            
            # Calculate overall complexity score
            base_score = complexity['lines'] * 0.1
            
            feature_score = (
                complexity['features']['functions'] * 2 +
                complexity['features']['classes'] * 3 +
                complexity['features']['loops'] * 2 +
                complexity['features']['async_operations'] * 3 +
                complexity['features']['dom_operations'] * 1.5 +
                complexity['features']['api_calls'] * 2.5
            )
            
            jsx_score = complexity['jsx_complexity'] * 0.5
            ts_score = complexity['typescript_features'] * 0.3
            cyclomatic_score = complexity['cyclomatic_complexity'] * 1.2
            
            complexity['complexity_score'] = base_score + feature_score + jsx_score + ts_score + cyclomatic_score
            
        except Exception:
            pass
        
        return complexity
    
    def _is_js_comment_line(self, line: str) -> bool:
        """Check if line is a JavaScript comment"""
        return (line.startswith('//') or 
                line.startswith('/*') or 
                line.startswith('*') or
                line.startswith('*/'))
    
    def _analyze_dependencies(self) -> Dict[str, Any]:
        """Analyze JavaScript dependencies from package.json"""
        dependencies = {
            'package_managers': {},
            'total_dependencies': 0,
            'heavy_dependencies': [],
            'dependency_files': []
        }
        
        package_files = ['package.json', 'yarn.lock', 'package-lock.json']
        
        for pkg_file in package_files:
            pkg_path = self.project_path / pkg_file
            if pkg_path.exists():
                dependencies['dependency_files'].append(pkg_file)
                
                if pkg_file == 'package.json':
                    try:
                        with open(pkg_path, 'r') as f:
                            package_data = json.load(f)
                        
                        deps_info = {
                            'count': 0,
                            'packages': [],
                            'dev_packages': [],
                            'peer_packages': [],
                            'manager': 'npm/yarn'
                        }
                        
                        # Production dependencies
                        if 'dependencies' in package_data:
                            deps = package_data['dependencies']
                            deps_info['count'] += len(deps)
                            deps_info['packages'].extend(deps.keys())
                        
                        # Development dependencies
                        if 'devDependencies' in package_data:
                            dev_deps = package_data['devDependencies']
                            deps_info['count'] += len(dev_deps)
                            deps_info['dev_packages'].extend(dev_deps.keys())
                        
                        # Peer dependencies
                        if 'peerDependencies' in package_data:
                            peer_deps = package_data['peerDependencies']
                            deps_info['peer_packages'].extend(peer_deps.keys())
                        
                        dependencies['package_managers']['npm/yarn'] = deps_info
                        dependencies['total_dependencies'] = deps_info['count']
                        
                        # Identify heavy JavaScript dependencies
                        heavy_js_packages = [
                            'react', 'vue', 'angular', '@angular/',
                            'lodash', 'moment', 'date-fns',
                            'chart.js', 'd3', 'three.js',
                            'webpack', 'babel', 'typescript',
                            'express', 'koa', 'fastify',
                            'socket.io', 'ws',
                            'mongoose', 'sequelize',
                            'sharp', 'canvas'
                        ]
                        
                        all_packages = deps_info['packages'] + deps_info['dev_packages']
                        for pkg in all_packages:
                            if any(heavy_pkg in pkg.lower() for heavy_pkg in heavy_js_packages):
                                dependencies['heavy_dependencies'].append(pkg)
                        
                    except Exception:
                        pass
        
        return dependencies
    
    def _detect_framework(self) -> Dict[str, Any]:
        """Detect JavaScript framework being used"""
        framework_info = {
            'detected_frameworks': [],
            'confidence': 'low',
            'evidence': [],
            'build_tools': [],
            'runtime': 'browser'
        }
        
        # Check package.json for framework indicators
        package_path = self.project_path / 'package.json'
        if package_path.exists():
            try:
                with open(package_path, 'r') as f:
                    package_data = json.load(f)
                
                all_deps = {}
                all_deps.update(package_data.get('dependencies', {}))
                all_deps.update(package_data.get('devDependencies', {}))
                
                # Framework detection
                framework_patterns = {
                    'react': ['react', 'react-dom', 'react-scripts'],
                    'vue': ['vue', '@vue/', 'vue-cli'],
                    'angular': ['@angular/', 'angular'],
                    'svelte': ['svelte', 'svelte-kit'],
                    'express': ['express'],
                    'fastify': ['fastify'],
                    'koa': ['koa'],
                    'next.js': ['next'],
                    'nuxt.js': ['nuxt'],
                    'gatsby': ['gatsby'],
                }
                
                for framework, indicators in framework_patterns.items():
                    for indicator in indicators:
                        if any(indicator in dep for dep in all_deps.keys()):
                            framework_info['detected_frameworks'].append(framework)
                            framework_info['evidence'].append(f"Package: {indicator}")
                            framework_info['confidence'] = 'high'
                            break
                
                # Build tools detection
                build_tools = {
                    'webpack': 'webpack',
                    'vite': 'vite',
                    'rollup': 'rollup',
                    'parcel': 'parcel',
                    'esbuild': 'esbuild'
                }
                
                for tool, pkg_name in build_tools.items():
                    if pkg_name in all_deps:
                        framework_info['build_tools'].append(tool)
                
                # Runtime detection
                if any(pkg in all_deps for pkg in ['express', 'koa', 'fastify', 'node']):
                    framework_info['runtime'] = 'node.js'
                
            except Exception:
                pass
        
        # Check for specific configuration files
        config_files = {
            'webpack.config.js': 'webpack',
            'vite.config.js': 'vite',
            'rollup.config.js': 'rollup',
            'next.config.js': 'next.js',
            'nuxt.config.js': 'nuxt.js',
            'svelte.config.js': 'svelte',
            'angular.json': 'angular',
        }
        
        for config_file, framework in config_files.items():
            if (self.project_path / config_file).exists():
                if framework not in framework_info['detected_frameworks']:
                    framework_info['detected_frameworks'].append(framework)
                framework_info['evidence'].append(f"Config: {config_file}")
                framework_info['confidence'] = 'high'
        
        return framework_info
    
    def _get_language_specific_recommendations(self, structure: Dict[str, Any], 
                                            energy_data: Dict[str, Any]) -> List[str]:
        """Get JavaScript-specific optimization recommendations"""
        recommendations = []
        
        frameworks = structure.get('framework_info', {}).get('detected_frameworks', [])
        dependencies = structure.get('dependencies', {})
        
        # React-specific recommendations
        if 'react' in frameworks:
            recommendations.extend([
                "⚛️ React: Use React.memo() for expensive components to prevent unnecessary re-renders",
                "📦 React: Implement code splitting with React.lazy() and Suspense",
                "🔄 React: Use useCallback and useMemo hooks for expensive computations",
                "🎯 React: Consider using React DevTools Profiler to identify performance bottlenecks"
            ])
        
        # Vue-specific recommendations
        if 'vue' in frameworks:
            recommendations.extend([
                "🖖 Vue: Use v-memo directive for expensive list rendering",
                "📦 Vue: Implement route-based code splitting with dynamic imports",
                "🔄 Vue: Use computed properties instead of methods for expensive calculations"
            ])
        
        # Node.js-specific recommendations
        if structure.get('framework_info', {}).get('runtime') == 'node.js':
            recommendations.extend([
                "🟢 Node.js: Use clustering to utilize multiple CPU cores",
                "💾 Node.js: Implement connection pooling for database operations",
                "🔄 Node.js: Use streaming for large file operations to reduce memory usage",
                "📊 Node.js: Consider using PM2 for production process management"
            ])
        
        # Bundle size recommendations
        heavy_deps = dependencies.get('heavy_dependencies', [])
        if len(heavy_deps) > 3:
            recommendations.extend([
                f"📦 Bundle size: Heavy dependencies detected: {', '.join(heavy_deps[:3])}...",
                "🔧 Bundle size: Use webpack-bundle-analyzer to identify large dependencies",
                "📉 Bundle size: Consider using lighter alternatives or tree shaking"
            ])
        
        # Async operations recommendations
        total_async = sum(
            file_data.get('features', {}).get('async_operations', 0)
            for file_data in structure.get('file_complexities', {}).values()
        )
        
        if total_async > 20:
            recommendations.extend([
                "🔄 Async: High number of async operations detected",
                "⚡ Async: Consider using Promise.all() for parallel operations",
                "🎯 Async: Implement proper error handling to prevent memory leaks"
            ])
        
        # DOM operations recommendations
        total_dom = sum(
            file_data.get('features', {}).get('dom_operations', 0)
            for file_data in structure.get('file_complexities', {}).values()
        )
        
        if total_dom > 15:
            recommendations.extend([
                "🖥️ DOM: High number of DOM operations detected",
                "⚡ DOM: Use requestAnimationFrame for animations",
                "💾 DOM: Consider virtual scrolling for large lists",
                "🎯 DOM: Minimize DOM queries by caching element references"
            ])
        
        return recommendations