"""
Java-specific carbon footprint analyzer
"""

import re
from pathlib import Path
from typing import Dict, Any, List
import xml.etree.ElementTree as ET
from .base_analyzer import BaseAnalyzer

class JavaAnalyzer(BaseAnalyzer):
    """Specialized analyzer for Java projects"""
    
    def __init__(self, project_path: Path, config: Dict[str, Any]):
        super().__init__(project_path, config)
        self.language = "java"
        self.file_extensions = ['.java', '.kt', '.scala']
    
    def _calculate_file_complexity(self, file_path: Path) -> Dict[str, Any]:
        """Calculate Java-specific complexity metrics"""
        complexity = {
            'complexity_score': 0,
            'features': {
                'classes': 0,
                'interfaces': 0,
                'methods': 0,
                'loops': 0,
                'conditionals': 0,
                'imports': 0,
                'annotations': 0,
                'lambda_expressions': 0,
                'streams': 0,
                'exceptions': 0,
            },
            'lines': 0,
            'cyclomatic_complexity': 1,
            'depth_of_inheritance': 0,
            'method_count': 0,
            'nested_classes': 0
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Count lines (excluding comments and empty lines)
            lines = content.split('\n')
            complexity['lines'] = len([
                line for line in lines 
                if line.strip() and not line.strip().startswith('//') and not line.strip().startswith('*')
            ])
            
            # Java-specific patterns
            patterns = {
                'classes': [
                    r'\bclass\s+\w+',
                    r'\benum\s+\w+',
                    r'\brecord\s+\w+'  # Java 14+
                ],
                'interfaces': [r'\binterface\s+\w+'],
                'methods': [
                    r'\b(?:public|private|protected|static|final|abstract|native|synchronized|)\s*(?:public|private|protected|static|final|abstract|native|synchronized|)\s*(?:\w+\s+)*\w+\s+\w+\s*\([^)]*\)\s*(?:throws\s+\w+(?:\s*,\s*\w+)*)?\s*\{',
                    r'\b(?:public|private|protected)\s+(?:static\s+)?(?:final\s+)?(?:abstract\s+)?(?:synchronized\s+)?(?:\w+\s+)*\w+\s+\w+\s*\([^)]*\)'
                ],
                'loops': [
                    r'\bfor\s*\(',
                    r'\bwhile\s*\(',
                    r'\bdo\s*\{.*?\}\s*while',
                    r'\.forEach\s*\(',
                    r'\.stream\(\).*?\.forEach'
                ],
                'conditionals': [
                    r'\bif\s*\(',
                    r'\belse\s+if\s*\(',
                    r'\bswitch\s*\(',
                    r'\bcase\s+\w+:',
                    r'\?.*?:'  # Ternary operator
                ],
                'imports': [
                    r'\bimport\s+(?:static\s+)?\w+(?:\.\w+)*(?:\.\*)?;'
                ],
                'annotations': [r'@\w+(?:\([^)]*\))?'],
                'lambda_expressions': [
                    r'\([^)]*\)\s*->\s*',
                    r'\w+\s*->\s*',
                    r'::\w+'  # Method references
                ],
                'streams': [
                    r'\.stream\(\)',
                    r'\.parallelStream\(\)',
                    r'Stream\.',
                    r'\.collect\(',
                    r'\.map\(',
                    r'\.filter\(',
                    r'\.reduce\('
                ],
                'exceptions': [
                    r'\btry\s*\{',
                    r'\bcatch\s*\(',
                    r'\bfinally\s*\{',
                    r'\bthrows?\s+\w+',
                    r'\bthrow\s+new\s+'
                ]
            }
            
            # Count pattern occurrences
            for feature, feature_patterns in patterns.items():
                count = 0
                for pattern in feature_patterns:
                    matches = re.findall(pattern, content, re.MULTILINE | re.DOTALL)
                    count += len(matches)
                complexity['features'][feature] = count
            
            # Calculate cyclomatic complexity (simplified)
            complexity_contributors = [
                r'\bif\s*\(',
                r'\belse\s+if\s*\(',
                r'\bfor\s*\(',
                r'\bwhile\s*\(',
                r'\bcase\s+\w+:',
                r'\bcatch\s*\(',
                r'\?\s*.*?\s*:',  # Ternary
                r'&&',
                r'\|\|'
            ]
            
            cyclomatic = 1  # Base complexity
            for pattern in complexity_contributors:
                matches = re.findall(pattern, content, re.MULTILINE)
                cyclomatic += len(matches)
            
            complexity['cyclomatic_complexity'] = cyclomatic
            
            # Detect nested classes
            nested_class_pattern = r'\bclass\s+\w+.*?\{(?:[^{}]*\{[^{}]*\})*[^{}]*\bclass\s+\w+'
            nested_matches = re.findall(nested_class_pattern, content, re.DOTALL)
            complexity['nested_classes'] = len(nested_matches)
            
            # Estimate inheritance depth from extends/implements
            inheritance_patterns = [
                r'\bextends\s+\w+',
                r'\bimplements\s+\w+(?:\s*,\s*\w+)*'
            ]
            inheritance_count = 0
            for pattern in inheritance_patterns:
                matches = re.findall(pattern, content)
                inheritance_count += len(matches)
            complexity['depth_of_inheritance'] = inheritance_count
            
            complexity['method_count'] = complexity['features']['methods']
            
            # Calculate complexity score
            base_score = complexity['lines'] * 0.1
            
            feature_score = (
                complexity['features']['classes'] * 5 +
                complexity['features']['interfaces'] * 3 +
                complexity['features']['methods'] * 2 +
                complexity['features']['loops'] * 2 +
                complexity['features']['conditionals'] * 1.5 +
                complexity['features']['annotations'] * 1 +
                complexity['features']['lambda_expressions'] * 1.5 +
                complexity['features']['streams'] * 1 +
                complexity['features']['exceptions'] * 2 +
                complexity['nested_classes'] * 3
            )
            
            cyclomatic_score = complexity['cyclomatic_complexity'] * 1.5
            inheritance_penalty = complexity['depth_of_inheritance'] * 2
            
            complexity['complexity_score'] = base_score + feature_score + cyclomatic_score + inheritance_penalty
            
        except Exception:
            pass
        
        return complexity
    
    def _analyze_dependencies(self) -> Dict[str, Any]:
        """Analyze Java dependencies from various build files"""
        dependencies = {
            'package_managers': {},
            'total_dependencies': 0,
            'heavy_dependencies': [],
            'dependency_files': []
        }
        
        # Java dependency files
        dep_files = {
            'pom.xml': 'maven',
            'build.gradle': 'gradle',
            'build.gradle.kts': 'gradle',
            'ivy.xml': 'ivy',
            'project.clj': 'leiningen'  # Clojure
        }
        
        for dep_file, manager in dep_files.items():
            dep_path = self.project_path / dep_file
            if dep_path.exists():
                dependencies['dependency_files'].append(dep_file)
                deps_info = self._parse_java_dependencies(dep_path, manager)
                dependencies['package_managers'][manager] = deps_info
                dependencies['total_dependencies'] += deps_info.get('count', 0)
        
        # Heavy Java packages/frameworks (high carbon footprint)
        heavy_java_packages = [
            'spring-boot-starter',  # Spring Boot
            'spring-webmvc',        # Spring MVC
            'hibernate',            # ORM
            'elasticsearch',        # Search engine
            'kafka',               # Message broker
            'cassandra',           # NoSQL database
            'hadoop',              # Big data
            'spark',               # Big data processing
            'selenium',            # Web automation
            'tomcat',              # Application server
            'jetty',               # Web server
            'netty',               # Network framework
            'jackson',             # JSON processing
            'lucene',              # Search library
            'junit-jupiter',       # Testing (heavy setup)
            'testcontainers',      # Integration testing
        ]
        
        for manager_info in dependencies['package_managers'].values():
            artifacts = manager_info.get('artifacts', [])
            for artifact in artifacts:
                if any(heavy_pkg in artifact.lower() for heavy_pkg in heavy_java_packages):
                    dependencies['heavy_dependencies'].append(artifact)
        
        return dependencies
    
    def _parse_java_dependencies(self, file_path: Path, manager: str) -> Dict[str, Any]:
        """Parse Java dependency files"""
        deps_info = {
            'count': 0,
            'artifacts': [],
            'manager': manager
        }
        
        try:
            if manager == 'maven' and file_path.name == 'pom.xml':
                deps_info = self._parse_maven_pom(file_path)
            
            elif manager == 'gradle' and 'gradle' in file_path.name:
                deps_info = self._parse_gradle_build(file_path)
            
            elif manager == 'ivy' and file_path.name == 'ivy.xml':
                deps_info = self._parse_ivy_xml(file_path)
        
        except Exception:
            pass
        
        deps_info['manager'] = manager
        return deps_info
    
    def _parse_maven_pom(self, pom_path: Path) -> Dict[str, Any]:
        """Parse Maven pom.xml file"""
        deps_info = {
            'count': 0,
            'artifacts': [],
            'parent': None,
            'properties': {}
        }
        
        try:
            tree = ET.parse(pom_path)
            root = tree.getroot()
            
            # Handle XML namespaces
            namespace = ''
            if root.tag.startswith('{'):
                namespace = root.tag.split('}')[0] + '}'
            
            # Get parent information
            parent_elem = root.find(f'{namespace}parent')
            if parent_elem is not None:
                parent_artifact = parent_elem.find(f'{namespace}artifactId')
                if parent_artifact is not None:
                    deps_info['parent'] = parent_artifact.text
            
            # Get properties
            properties_elem = root.find(f'{namespace}properties')
            if properties_elem is not None:
                for prop in properties_elem:
                    prop_name = prop.tag.replace(namespace, '')
                    deps_info['properties'][prop_name] = prop.text
            
            # Get dependencies
            dependencies_elem = root.find(f'{namespace}dependencies')
            if dependencies_elem is not None:
                for dep in dependencies_elem.findall(f'{namespace}dependency'):
                    group_id = dep.find(f'{namespace}groupId')
                    artifact_id = dep.find(f'{namespace}artifactId')
                    
                    if group_id is not None and artifact_id is not None:
                        artifact_name = f"{group_id.text}:{artifact_id.text}"
                        deps_info['artifacts'].append(artifact_name)
                        deps_info['count'] += 1
        
        except Exception:
            pass
        
        return deps_info
    
    def _parse_gradle_build(self, gradle_path: Path) -> Dict[str, Any]:
        """Parse Gradle build file (basic parsing)"""
        deps_info = {
            'count': 0,
            'artifacts': []
        }
        
        try:
            with open(gradle_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract dependencies from dependencies block
            deps_pattern = r'dependencies\s*\{(.*?)\}'
            deps_match = re.search(deps_pattern, content, re.DOTALL)
            
            if deps_match:
                deps_block = deps_match.group(1)
                
                # Find dependency declarations
                # Handles: implementation 'group:artifact:version'
                # Handles: compile "group:artifact:version"
                # Handles: testImplementation group: 'com.example', name: 'artifact', version: '1.0'
                
                simple_deps = re.findall(r'(?:implementation|compile|api|runtimeOnly|testImplementation|testCompile)\s+["\']([^"\']+)["\']', deps_block)
                deps_info['artifacts'].extend(simple_deps)
                
                # Handle map-style dependencies
                map_deps = re.findall(r'group:\s*["\']([^"\']+)["\'],\s*name:\s*["\']([^"\']+)["\']', deps_block)
                for group, name in map_deps:
                    deps_info['artifacts'].append(f"{group}:{name}")
                
                deps_info['count'] = len(deps_info['artifacts'])
        
        except Exception:
            pass
        
        return deps_info
    
    def _parse_ivy_xml(self, ivy_path: Path) -> Dict[str, Any]:
        """Parse Ivy ivy.xml file"""
        deps_info = {
            'count': 0,
            'artifacts': []
        }
        
        try:
            tree = ET.parse(ivy_path)
            root = tree.getroot()
            
            dependencies_elem = root.find('dependencies')
            if dependencies_elem is not None:
                for dep in dependencies_elem.findall('dependency'):
                    org = dep.get('org', '')
                    name = dep.get('name', '')
                    if org and name:
                        deps_info['artifacts'].append(f"{org}:{name}")
                        deps_info['count'] += 1
        
        except Exception:
            pass
        
        return deps_info
    
    def _detect_framework(self) -> Dict[str, Any]:
        """Detect Java framework being used"""
        framework_info = {
            'detected_frameworks': [],
            'confidence': 'low',
            'evidence': [],
            'java_version': None,
            'build_tool': None
        }
        
        # Framework detection based on dependencies and files
        framework_indicators = {
            'spring-boot': ['spring-boot', 'application.properties', 'application.yml', '@SpringBootApplication'],
            'spring': ['spring-core', 'spring-context', '@Controller', '@Service', '@Component'],
            'hibernate': ['hibernate-core', 'hibernate-entitymanager', '@Entity', '@Table'],
            'jpa': ['javax.persistence', 'jakarta.persistence', '@Entity', '@Repository'],
            'struts': ['struts2-core', 'struts.xml'],
            'jsf': ['javax.faces', 'faces-config.xml', 'xhtml'],
            'jersey': ['jersey-server', 'jersey-client', '@Path', '@GET', '@POST'],
            'junit': ['junit-jupiter', 'junit', '@Test', '@BeforeEach'],
            'maven': ['pom.xml'],
            'gradle': ['build.gradle', 'build.gradle.kts'],
            'android': ['android.app', 'AndroidManifest.xml', 'res/layout'],
        }
        
        # Check dependencies
        deps = self._analyze_dependencies()
        all_artifacts = []
        for manager_info in deps['package_managers'].values():
            all_artifacts.extend(manager_info.get('artifacts', []))
        
        # Check for build tool
        if 'pom.xml' in deps['dependency_files']:
            framework_info['build_tool'] = 'maven'
        elif any('gradle' in f for f in deps['dependency_files']):
            framework_info['build_tool'] = 'gradle'
        
        for framework, indicators in framework_indicators.items():
            evidence_count = 0
            evidence_found = []
            
            for indicator in indicators:
                # Check artifacts/dependencies
                if any(indicator in artifact.lower() for artifact in all_artifacts):
                    evidence_count += 1
                    evidence_found.append(f"Dependency: {indicator}")
                
                # Check files
                if '.' in indicator and not indicator.startswith('@'):
                    if indicator.startswith('*.'):  # Extension
                        ext = indicator[1:]
                        if list(self.project_path.rglob(f"*{ext}")):
                            evidence_count += 1
                            evidence_found.append(f"File: {indicator}")
                    else:  # Specific file or path
                        if (self.project_path / indicator).exists() or list(self.project_path.rglob(indicator)):
                            evidence_count += 1
                            evidence_found.append(f"File: {indicator}")
                
                # Check for annotations in source files
                elif indicator.startswith('@'):
                    java_files = list(self.project_path.rglob("*.java"))
                    for java_file in java_files[:10]:  # Check first 10 files for performance
                        try:
                            with open(java_file, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read()
                            if indicator in content:
                                evidence_count += 1
                                evidence_found.append(f"Annotation: {indicator}")
                                break
                        except Exception:
                            continue
            
            if evidence_count > 0:
                framework_info['detected_frameworks'].append(framework)
                framework_info['evidence'].extend(evidence_found)
                
                if evidence_count >= 3:
                    framework_info['confidence'] = 'high'
                elif evidence_count >= 2:
                    framework_info['confidence'] = 'medium'
        
        # Detect Java version from build files
        self._detect_java_version(framework_info)
        
        return framework_info
    
    def _detect_java_version(self, framework_info: Dict[str, Any]):
        """Detect Java version from build files"""
        # Check Maven pom.xml
        pom_path = self.project_path / 'pom.xml'
        if pom_path.exists():
            try:
                with open(pom_path, 'r') as f:
                    content = f.read()
                
                # Look for Java version in properties or compiler plugin
                version_patterns = [
                    r'<java\.version>([0-9.]+)</java\.version>',
                    r'<maven\.compiler\.source>([0-9.]+)</maven\.compiler\.source>',
                    r'<maven\.compiler\.target>([0-9.]+)</maven\.compiler\.target>',
                    r'<source>([0-9.]+)</source>',
                    r'<target>([0-9.]+)</target>'
                ]
                
                for pattern in version_patterns:
                    match = re.search(pattern, content)
                    if match:
                        framework_info['java_version'] = match.group(1)
                        break
            except Exception:
                pass
        
        # Check Gradle build files
        for gradle_file in ['build.gradle', 'build.gradle.kts']:
            gradle_path = self.project_path / gradle_file
            if gradle_path.exists():
                try:
                    with open(gradle_path, 'r') as f:
                        content = f.read()
                    
                    version_patterns = [
                        r'sourceCompatibility\s*=\s*["\']?([0-9.]+)["\']?',
                        r'targetCompatibility\s*=\s*["\']?([0-9.]+)["\']?',
                        r'JavaVersion\.VERSION_([0-9_]+)',
                        r'jvmTarget\s*=\s*["\']([0-9.]+)["\']'  # Kotlin
                    ]
                    
                    for pattern in version_patterns:
                        match = re.search(pattern, content)
                        if match:
                            version = match.group(1).replace('_', '.')
                            framework_info['java_version'] = version
                            break
                except Exception:
                    pass
    
    def _get_language_specific_recommendations(self, structure: Dict[str, Any], 
                                            energy_data: Dict[str, Any]) -> List[str]:
        """Get Java-specific optimization recommendations"""
        recommendations = []
        
        frameworks = structure.get('framework_info', {}).get('detected_frameworks', [])
        dependencies = structure.get('dependencies', {})
        java_version = structure.get('framework_info', {}).get('java_version')
        
        # Spring Boot recommendations
        if 'spring-boot' in frameworks or 'spring' in frameworks:
            recommendations.extend([
                "🌱 Spring: Use @Lazy annotation for beans that are not immediately needed",
                "💾 Spring: Implement Spring Boot's caching with @Cacheable annotations",
                "📊 Spring: Use Spring Data JPA pagination for large datasets",
                "🔄 Spring: Enable Spring Boot's actuator for monitoring and optimization",
                "⚡ Spring: Consider using Spring WebFlux for reactive programming"
            ])
        
        # Hibernate/JPA recommendations
        if 'hibernate' in frameworks or 'jpa' in frameworks:
            recommendations.extend([
                "💾 Hibernate: Use fetch joins and batch fetching to reduce N+1 queries",
                "📊 Hibernate: Implement second-level caching for frequently accessed entities",
                "🔧 Hibernate: Use @BatchSize annotation for collection fetching optimization"
            ])
        
        # Build tool recommendations
        build_tool = structure.get('framework_info', {}).get('build_tool')
        if build_tool == 'gradle':
            recommendations.extend([
                "🏗️ Gradle: Use Gradle daemon and parallel builds for faster compilation",
                "💾 Gradle: Enable build caching with --build-cache flag",
                "⚡ Gradle: Use incremental compilation and avoid-task-execution"
            ])
        elif build_tool == 'maven':
            recommendations.extend([
                "🏗️ Maven: Use Maven daemon (mvnd) for faster builds",
                "💾 Maven: Enable parallel builds with -T flag",
                "⚡ Maven: Use Maven build cache extension"
            ])
        
        # Java version specific recommendations
        if java_version:
            try:
                version_num = float(java_version)
                if version_num >= 17:
                    recommendations.append(
                        "☕ Java 17+: Great choice! Use record classes and sealed classes for efficiency"
                    )
                elif version_num >= 11:
                    recommendations.append(
                        "☕ Java 11+: Consider upgrading to Java 17+ for better performance and new features"
                    )
                else:
                    recommendations.append(
                        "☕ Java Version: Consider upgrading to Java 17+ LTS for significant performance improvements"
                    )
            except (ValueError, TypeError):
                pass
        
        # Performance recommendations based on code complexity
        total_complexity = sum(
            file_info.get('cyclomatic_complexity', 1)
            for file_info in structure.get('file_complexities', {}).values()
        )
        
        if total_complexity > 200:
            recommendations.extend([
                "🏗️ Java: High cyclomatic complexity detected - consider refactoring",
                "🔧 Java: Use design patterns like Strategy or Command to reduce complexity",
                "⚡ Java: Consider using static analysis tools like SpotBugs or PMD"
            ])
        
        # Stream and lambda recommendations
        total_streams = sum(
            file_info.get('features', {}).get('streams', 0)
            for file_info in structure.get('file_complexities', {}).values()
        )
        
        total_lambdas = sum(
            file_info.get('features', {}).get('lambda_expressions', 0)
            for file_info in structure.get('file_complexities', {}).values()
        )
        
        if total_streams > 20:
            recommendations.append(
                "🌊 Java Streams: Good use of streams! Consider parallel streams for CPU-intensive operations"
            )
        
        if total_lambdas > 30:
            recommendations.append(
                "λ Java Lambdas: Extensive lambda usage detected - ensure they're not creating memory leaks"
            )
        
        # Memory and GC recommendations
        heavy_deps = dependencies.get('heavy_dependencies', [])
        if len(heavy_deps) > 5:
            recommendations.extend([
                "💾 Java: Many heavy dependencies detected - consider GC tuning",
                "🔧 Java: Use G1GC or ZGC for applications with large heaps",
                "⚡ Java: Monitor memory usage with JVM flags -XX:+PrintGCDetails"
            ])
        
        # Testing recommendations
        if 'junit' in frameworks:
            recommendations.extend([
                "🧪 JUnit: Use @ParameterizedTest for data-driven tests",
                "⚡ Testing: Consider TestContainers for integration testing efficiency",
                "🔧 Testing: Use test slices (@WebMvcTest, @DataJpaTest) for faster tests"
            ])
        
        return recommendations