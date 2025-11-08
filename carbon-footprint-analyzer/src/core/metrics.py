"""
Carbon footprint metrics calculator
"""

from typing import Dict, Any, List, Tuple
from pathlib import Path
import json
from datetime import datetime

class CarbonCalculator:
    """Calculates carbon footprint metrics for software projects"""
    
    def __init__(self):
        # Energy consumption factors (kWh per unit)
        self.energy_factors = {
            # Base factors per line of code
            'lines_of_code': {
                'javascript': 0.0001,   # JS engines are optimized
                'typescript': 0.00012,  # Slightly more than JS due to compilation
                'python': 0.0002,       # Interpreted language
                'java': 0.00015,        # JVM overhead
                'cpp': 0.0001,          # Compiled, efficient
                'c': 0.00008,           # Most efficient
                'csharp': 0.00016,      # .NET runtime
                'go': 0.00011,          # Efficient compiled
                'rust': 0.0001,         # Very efficient
                'php': 0.0003,          # Web context overhead
                'ruby': 0.00025,        # Interpreted
                'swift': 0.00012,       # Mobile optimized
                'kotlin': 0.00015,      # JVM based
                'dart': 0.00013,        # Flutter/web
                'default': 0.0002       # Average factor
            },
            
            # Complexity multipliers
            'complexity': {
                'low': 1.0,
                'medium': 1.5,
                'high': 2.0,
                'very_high': 3.0
            },
            
            # Framework overhead (additional kWh per framework)
            'frameworks': {
                'react': 0.005,         # Frontend framework
                'vue': 0.004,           # Lighter than React
                'angular': 0.008,       # Heavy framework
                'django': 0.006,        # Full-stack framework
                'flask': 0.003,         # Lightweight
                'fastapi': 0.004,       # Modern, efficient
                'spring': 0.01,         # Heavy Java framework
                'express': 0.003,       # Lightweight Node.js
                'nextjs': 0.006,        # Full-stack React
                'nuxt': 0.005,          # Full-stack Vue
                'android': 0.008,       # Mobile framework
                'ios': 0.007,           # Native mobile
                'default': 0.005        # Average framework
            },
            
            # Development activities (kWh per hour)
            'activities': {
                'coding': 0.1,          # Active development
                'compilation': 0.3,     # CPU intensive
                'testing': 0.15,        # Running tests
                'debugging': 0.12,      # IDE + profiling
                'deployment': 0.25,     # CI/CD processes
                'code_review': 0.08,    # Reading code
            },
            
            # File type processing overhead
            'file_processing': {
                'source_code': 0.00001, # Per file
                'config': 0.000005,     # Configuration files
                'assets': 0.000002,     # Static assets
                'documentation': 0.000001 # Docs
            }
        }
        
        # Carbon intensity factors (kg CO2 per kWh)
        # Based on global electricity grid mix
        self.carbon_intensity = {
            'global_average': 0.475,    # Global average
            'renewable_heavy': 0.200,   # Renewable energy grids
            'coal_heavy': 0.820,        # Coal-heavy grids
            'natural_gas': 0.350,       # Natural gas grids
            'nuclear': 0.012,           # Nuclear power
            'default': 0.475            # Use global average as default
        }
        
        # Dependencies impact (additional energy per dependency)
        self.dependency_factors = {
            'heavy_dependencies': 0.001,     # Per heavy dependency
            'medium_dependencies': 0.0005,   # Per medium dependency
            'light_dependencies': 0.0001,    # Per light dependency
        }
        
        # Build and runtime factors
        self.build_factors = {
            'maven': 1.8,               # Java build tool multiplier
            'gradle': 1.6,              # More efficient than Maven
            'webpack': 1.5,             # JavaScript bundler
            'npm': 1.2,                 # Package manager
            'pip': 1.1,                 # Python package manager
            'cargo': 1.3,               # Rust build system
            'go_build': 1.2,            # Go compiler
            'default': 1.0              # No build system
        }
    
    def calculate_carbon_footprint(self, 
                                 project_analysis: Dict[str, Any],
                                 grid_type: str = 'global_average',
                                 development_hours: float = None) -> Dict[str, Any]:
        """
        Calculate comprehensive carbon footprint for a software project
        
        Args:
            project_analysis: Complete project analysis from analyzers
            grid_type: Type of electricity grid (affects carbon intensity)
            development_hours: Estimated development time (if known)
        
        Returns:
            Detailed carbon footprint breakdown
        """
        
        # Extract data from project analysis
        language_data = project_analysis.get('language_detection', {})
        structure_data = project_analysis.get('project_structure', {})
        dependencies = project_analysis.get('dependencies', {})
        framework_info = project_analysis.get('framework_info', {})
        
        # Calculate different components
        code_energy = self._calculate_code_energy(language_data, structure_data)
        framework_energy = self._calculate_framework_energy(framework_info)
        dependency_energy = self._calculate_dependency_energy(dependencies)
        build_energy = self._calculate_build_energy(framework_info, structure_data)
        
        # Development activities energy (if development hours provided)
        development_energy = 0
        if development_hours:
            development_energy = self._calculate_development_energy(
                development_hours, project_analysis
            )
        
        # Total energy consumption (kWh)
        total_energy_kwh = (
            code_energy + 
            framework_energy + 
            dependency_energy + 
            build_energy + 
            development_energy
        )
        
        # Convert to carbon emissions
        carbon_intensity_factor = self.carbon_intensity.get(grid_type, 
                                                           self.carbon_intensity['default'])
        total_carbon_kg = total_energy_kwh * carbon_intensity_factor
        
        # Create detailed breakdown
        breakdown = {
            'total_carbon_kg': round(total_carbon_kg, 6),
            'total_energy_kwh': round(total_energy_kwh, 6),
            'carbon_intensity_kg_per_kwh': carbon_intensity_factor,
            'grid_type': grid_type,
            'timestamp': datetime.now().isoformat(),
            
            'components': {
                'code_execution': {
                    'energy_kwh': round(code_energy, 6),
                    'carbon_kg': round(code_energy * carbon_intensity_factor, 6),
                    'percentage': round((code_energy / total_energy_kwh) * 100, 2) if total_energy_kwh > 0 else 0
                },
                'frameworks': {
                    'energy_kwh': round(framework_energy, 6),
                    'carbon_kg': round(framework_energy * carbon_intensity_factor, 6),
                    'percentage': round((framework_energy / total_energy_kwh) * 100, 2) if total_energy_kwh > 0 else 0
                },
                'dependencies': {
                    'energy_kwh': round(dependency_energy, 6),
                    'carbon_kg': round(dependency_energy * carbon_intensity_factor, 6),
                    'percentage': round((dependency_energy / total_energy_kwh) * 100, 2) if total_energy_kwh > 0 else 0
                },
                'build_system': {
                    'energy_kwh': round(build_energy, 6),
                    'carbon_kg': round(build_energy * carbon_intensity_factor, 6),
                    'percentage': round((build_energy / total_energy_kwh) * 100, 2) if total_energy_kwh > 0 else 0
                },
                'development': {
                    'energy_kwh': round(development_energy, 6),
                    'carbon_kg': round(development_energy * carbon_intensity_factor, 6),
                    'percentage': round((development_energy / total_energy_kwh) * 100, 2) if total_energy_kwh > 0 else 0,
                    'hours_estimated': development_hours or 0
                }
            },
            
            'language_breakdown': self._calculate_language_breakdown(
                language_data, code_energy, carbon_intensity_factor
            ),
            
            'optimization_potential': self._calculate_optimization_potential(
                project_analysis, total_carbon_kg
            ),
            
            'comparison_metrics': self._generate_comparison_metrics(total_carbon_kg),
            
            'methodology': {
                'calculation_approach': 'Static analysis with energy modeling',
                'factors_used': ['lines_of_code', 'complexity', 'frameworks', 'dependencies'],
                'limitations': [
                    'Does not measure actual runtime energy',
                    'Based on estimated factors and industry averages',
                    'Does not include infrastructure or deployment energy'
                ]
            }
        }
        
        return breakdown
    
    def _calculate_code_energy(self, language_data: Dict, structure_data: Dict) -> float:
        """Calculate energy consumption from code execution"""
        total_energy = 0
        
        languages = language_data.get('languages', {})
        complexity = language_data.get('complexity_indicator', 'medium')
        
        # Base energy from lines of code
        for language, stats in languages.items():
            lines = sum(
                file_data.get('lines', 0) 
                for file_data in structure_data.get('file_complexities', {}).values()
                if file_data.get('language') == language
            )
            
            if lines > 0:
                base_factor = self.energy_factors['lines_of_code'].get(
                    language, 
                    self.energy_factors['lines_of_code']['default']
                )
                
                complexity_multiplier = self.energy_factors['complexity'].get(complexity, 1.0)
                
                language_energy = lines * base_factor * complexity_multiplier
                total_energy += language_energy
        
        return total_energy
    
    def _calculate_framework_energy(self, framework_info: Dict) -> float:
        """Calculate energy overhead from frameworks"""
        total_energy = 0
        
        detected_frameworks = framework_info.get('detected_frameworks', [])
        
        for framework in detected_frameworks:
            framework_energy = self.energy_factors['frameworks'].get(
                framework,
                self.energy_factors['frameworks']['default']
            )
            total_energy += framework_energy
        
        return total_energy
    
    def _calculate_dependency_energy(self, dependencies: Dict) -> float:
        """Calculate energy impact from dependencies"""
        total_energy = 0
        
        # Heavy dependencies
        heavy_deps = len(dependencies.get('heavy_dependencies', []))
        total_energy += heavy_deps * self.dependency_factors['heavy_dependencies']
        
        # All dependencies (medium impact)
        total_deps = dependencies.get('total_dependencies', 0)
        medium_deps = max(0, total_deps - heavy_deps)
        total_energy += medium_deps * self.dependency_factors['medium_dependencies']
        
        return total_energy
    
    def _calculate_build_energy(self, framework_info: Dict, structure_data: Dict) -> float:
        """Calculate energy from build systems"""
        build_tool = framework_info.get('build_tool')
        
        if not build_tool:
            return 0
        
        # Base build energy (per 1000 lines of code)
        total_lines = sum(
            file_data.get('lines', 0)
            for file_data in structure_data.get('file_complexities', {}).values()
        )
        
        build_multiplier = self.build_factors.get(build_tool, self.build_factors['default'])
        base_build_energy = (total_lines / 1000) * 0.01  # Base factor
        
        return base_build_energy * build_multiplier
    
    def _calculate_development_energy(self, hours: float, project_analysis: Dict) -> float:
        """Calculate energy from development activities"""
        # Estimate activity breakdown
        activity_breakdown = {
            'coding': 0.4,          # 40% coding
            'debugging': 0.2,       # 20% debugging
            'testing': 0.15,        # 15% testing
            'compilation': 0.1,     # 10% compilation/build
            'code_review': 0.1,     # 10% code review
            'deployment': 0.05      # 5% deployment
        }
        
        total_energy = 0
        for activity, percentage in activity_breakdown.items():
            activity_hours = hours * percentage
            energy_per_hour = self.energy_factors['activities'].get(activity, 0.1)
            total_energy += activity_hours * energy_per_hour
        
        return total_energy
    
    def _calculate_language_breakdown(self, language_data: Dict, 
                                    total_code_energy: float, 
                                    carbon_intensity: float) -> Dict[str, Dict]:
        """Calculate per-language energy and carbon breakdown"""
        breakdown = {}
        languages = language_data.get('languages', {})
        total_files = sum(stats['files'] for stats in languages.values())
        
        if total_files == 0:
            return breakdown
        
        for language, stats in languages.items():
            # Estimate proportion of total energy
            file_proportion = stats['files'] / total_files
            estimated_energy = total_code_energy * file_proportion
            estimated_carbon = estimated_energy * carbon_intensity
            
            breakdown[language] = {
                'files': stats['files'],
                'estimated_energy_kwh': round(estimated_energy, 6),
                'estimated_carbon_kg': round(estimated_carbon, 6),
                'percentage_of_total': round(file_proportion * 100, 2)
            }
        
        return breakdown
    
    def _calculate_optimization_potential(self, project_analysis: Dict, 
                                       current_carbon_kg: float) -> Dict[str, Any]:
        """Estimate potential carbon reduction through optimization"""
        
        # Analyze project characteristics for optimization potential
        complexity = project_analysis.get('language_detection', {}).get('complexity_indicator', 'medium')
        dependencies = project_analysis.get('dependencies', {})
        frameworks = project_analysis.get('framework_info', {}).get('detected_frameworks', [])
        
        potential_savings = 0
        optimizations = []
        
        # High complexity projects have more optimization potential
        if complexity in ['high', 'very_high']:
            potential_savings += current_carbon_kg * 0.25  # 25% potential savings
            optimizations.append({
                'category': 'code_complexity',
                'description': 'Reduce algorithmic complexity and refactor inefficient code',
                'potential_reduction_percentage': 25
            })
        
        # Heavy dependencies optimization
        heavy_deps = len(dependencies.get('heavy_dependencies', []))
        if heavy_deps > 5:
            potential_savings += current_carbon_kg * 0.15  # 15% potential savings
            optimizations.append({
                'category': 'dependencies',
                'description': 'Remove unused dependencies and replace heavy libraries',
                'potential_reduction_percentage': 15
            })
        
        # Framework optimization
        heavy_frameworks = ['angular', 'spring', 'django']
        if any(fw in frameworks for fw in heavy_frameworks):
            potential_savings += current_carbon_kg * 0.10  # 10% potential savings
            optimizations.append({
                'category': 'frameworks',
                'description': 'Consider lighter alternative frameworks or optimization',
                'potential_reduction_percentage': 10
            })
        
        return {
            'total_potential_reduction_kg': round(potential_savings, 6),
            'potential_reduction_percentage': round((potential_savings / current_carbon_kg) * 100, 2) if current_carbon_kg > 0 else 0,
            'optimization_opportunities': optimizations,
            'quick_wins': self._suggest_quick_wins(project_analysis)
        }
    
    def _suggest_quick_wins(self, project_analysis: Dict) -> List[str]:
        """Suggest quick optimization wins"""
        suggestions = []
        
        # Check for common inefficiencies
        languages = project_analysis.get('language_detection', {}).get('languages', {})
        
        if 'javascript' in languages:
            suggestions.append("Enable tree-shaking and dead code elimination in your build process")
            suggestions.append("Use code splitting to reduce initial bundle size")
        
        if 'python' in languages:
            suggestions.append("Use list comprehensions instead of loops where applicable")
            suggestions.append("Consider using generators for memory-efficient iteration")
        
        if 'java' in languages:
            suggestions.append("Enable JVM optimizations and use appropriate garbage collector")
            suggestions.append("Use primitive collections where appropriate")
        
        # General suggestions
        suggestions.extend([
            "Enable compiler/interpreter optimizations",
            "Use efficient algorithms and data structures",
            "Implement caching for frequently accessed data",
            "Profile your application to identify bottlenecks"
        ])
        
        return suggestions
    
    def _generate_comparison_metrics(self, carbon_kg: float) -> Dict[str, Any]:
        """Generate comparative metrics to help understand the carbon impact"""
        
        # Real-world comparisons
        comparisons = {
            'smartphone_charging': {
                'value': round(carbon_kg / 0.00001, 2),  # ~0.01g per charge
                'unit': 'smartphone charges',
                'description': 'Equivalent to charging a smartphone'
            },
            'car_distance': {
                'value': round(carbon_kg / 0.404, 2),  # Average car emissions per km
                'unit': 'kilometers by car',
                'description': 'Equivalent to driving by car'
            },
            'light_bulb': {
                'value': round(carbon_kg / 0.0036, 2),  # 60W bulb for 1 hour
                'unit': 'hours of 60W light bulb',
                'description': 'Equivalent to running a 60W light bulb'
            },
            'tree_absorption': {
                'value': round(carbon_kg / 22, 6),  # Average tree absorption per year
                'unit': 'years of tree CO2 absorption',
                'description': 'Would require a tree to absorb for'
            }
        }
        
        # Categorize impact level
        if carbon_kg < 0.001:  # Less than 1g
            impact_level = 'minimal'
        elif carbon_kg < 0.01:  # Less than 10g
            impact_level = 'low'
        elif carbon_kg < 0.1:   # Less than 100g
            impact_level = 'medium'
        elif carbon_kg < 1.0:   # Less than 1kg
            impact_level = 'high'
        else:
            impact_level = 'very_high'
        
        return {
            'impact_level': impact_level,
            'comparisons': comparisons,
            'annual_projection': {
                'carbon_kg_per_year': round(carbon_kg * 365, 3),  # Assuming daily usage
                'description': 'If this software runs daily for a year'
            }
        }
    
    def estimate_runtime_carbon(self, 
                              execution_time_seconds: float,
                              cpu_utilization_percent: float = 50,
                              memory_mb: int = 100,
                              grid_type: str = 'global_average') -> Dict[str, float]:
        """
        Estimate carbon footprint for actual runtime execution
        
        Args:
            execution_time_seconds: How long the software runs
            cpu_utilization_percent: Average CPU utilization during execution
            memory_mb: Memory usage in megabytes
            grid_type: Electricity grid type for carbon intensity
        
        Returns:
            Runtime carbon footprint breakdown
        """
        
        # Typical computer power consumption
        base_power_watts = 65  # Typical laptop power consumption
        cpu_power_watts = 95   # Additional CPU power under load
        memory_power_per_gb = 3  # Watts per GB of RAM
        
        # Calculate power consumption
        cpu_power = cpu_power_watts * (cpu_utilization_percent / 100)
        memory_power = memory_power_per_gb * (memory_mb / 1000)
        total_power_watts = base_power_watts + cpu_power + memory_power
        
        # Convert to energy consumption
        execution_time_hours = execution_time_seconds / 3600
        energy_kwh = (total_power_watts / 1000) * execution_time_hours
        
        # Calculate carbon emissions
        carbon_intensity_factor = self.carbon_intensity.get(grid_type, 
                                                           self.carbon_intensity['default'])
        carbon_kg = energy_kwh * carbon_intensity_factor
        
        return {
            'execution_time_seconds': execution_time_seconds,
            'energy_consumption_kwh': round(energy_kwh, 6),
            'carbon_emissions_kg': round(carbon_kg, 6),
            'power_breakdown_watts': {
                'base_system': base_power_watts,
                'cpu_load': round(cpu_power, 2),
                'memory': round(memory_power, 2),
                'total': round(total_power_watts, 2)
            },
            'carbon_intensity_kg_per_kwh': carbon_intensity_factor,
            'grid_type': grid_type
        }