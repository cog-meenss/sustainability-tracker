#!/usr/bin/env python3
"""
VS Code extension integration for carbon footprint analysis
"""

import json
import os
from pathlib import Path
from typing import Dict, Any

class VSCodeCarbonExtension:
    """VS Code extension integration for carbon footprint analysis"""
    
    def __init__(self):
        self.workspace_path = None
        self.config = {}
        
    def analyze_workspace(self, workspace_path: str) -> Dict[str, Any]:
        """Analyze the current workspace"""
        
        self.workspace_path = Path(workspace_path)
        
        # Import analyzer (adjust path as needed)
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))
        from carbon_analyzer import CarbonAnalyzer
        
        # Initialize analyzer
        analyzer = CarbonAnalyzer()
        
        # Run lightweight analysis for real-time feedback
        results = analyzer.analyze_project(
            project_path=self.workspace_path,
            report_formats=['json'],
            include_detailed_breakdown=False
        )
        
        # Format for VS Code display
        return self.format_for_vscode(results)
    
    def analyze_current_file(self, file_path: str) -> Dict[str, Any]:
        """Analyze the currently open file"""
        
        file_path = Path(file_path)
        
        if not file_path.exists():
            return {'error': 'File not found'}
        
        # Determine language from extension
        language_map = {
            '.js': 'javascript',
            '.jsx': 'javascript',
            '.ts': 'typescript', 
            '.tsx': 'typescript',
            '.py': 'python',
            '.java': 'java',
            '.kt': 'kotlin'
        }
        
        language = language_map.get(file_path.suffix.lower(), 'generic')
        
        # Read file content
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Import analyzer
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))
        from carbon_analyzer import CarbonAnalyzer
        
        analyzer = CarbonAnalyzer()
        results = analyzer.analyze_code_snippet(content, language, file_path.name)
        
        return self.format_file_analysis(results, file_path)
    
    def format_for_vscode(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Format analysis results for VS Code display"""
        
        carbon_data = results.get('carbon_footprint', {})
        summary = results.get('analysis_summary', {})
        
        return {
            'status': 'success',
            'summary': {
                'carbon_kg': carbon_data.get('total_carbon_kg', 0),
                'energy_kwh': carbon_data.get('total_energy_kwh', 0),
                'impact_level': summary.get('impact_level', 'unknown'),
                'primary_language': summary.get('primary_language', 'Unknown'),
                'files_count': summary.get('total_files', 0)
            },
            'breakdown': {
                component: data.get('percentage', 0)
                for component, data in carbon_data.get('components', {}).items()
                if isinstance(data, dict) and data.get('percentage', 0) > 0
            },
            'recommendations': results.get('recommendations', [])[:5],
            'optimization_potential': carbon_data.get('optimization_potential', {}).get('potential_reduction_percentage', 0),
            'status_icon': self.get_status_icon(summary.get('impact_level', 'unknown')),
            'status_color': self.get_status_color(summary.get('impact_level', 'unknown'))
        }
    
    def format_file_analysis(self, results: Dict[str, Any], file_path: Path) -> Dict[str, Any]:
        """Format single file analysis for VS Code"""
        
        code_analysis = results.get('code_analysis', {})
        carbon_data = results.get('carbon_footprint', {})
        
        return {
            'status': 'success',
            'file_info': {
                'path': str(file_path),
                'name': file_path.name,
                'size_bytes': file_path.stat().st_size if file_path.exists() else 0
            },
            'metrics': {
                'lines': code_analysis.get('lines', 0),
                'complexity_score': code_analysis.get('complexity_score', 0),
                'carbon_kg': carbon_data.get('total_carbon_kg', 0),
                'energy_kwh': carbon_data.get('total_energy_kwh', 0)
            },
            'features': code_analysis.get('features', {}),
            'recommendations': results.get('recommendations', [])[:3],
            'status_icon': self.get_file_status_icon(code_analysis.get('complexity_score', 0)),
            'diagnostics': self.generate_diagnostics(code_analysis, results.get('recommendations', []))
        }
    
    def get_status_icon(self, impact_level: str) -> str:
        """Get status icon based on impact level"""
        icons = {
            'minimal': '🟢',
            'low': '🟡', 
            'medium': '🟠',
            'high': '🔴',
            'very_high': '⚠️'
        }
        return icons.get(impact_level, '❓')
    
    def get_status_color(self, impact_level: str) -> str:
        """Get status color for VS Code theming"""
        colors = {
            'minimal': 'green',
            'low': 'yellow',
            'medium': 'orange', 
            'high': 'red',
            'very_high': 'red'
        }
        return colors.get(impact_level, 'gray')
    
    def get_file_status_icon(self, complexity_score: float) -> str:
        """Get file status icon based on complexity"""
        if complexity_score < 10:
            return '🟢'
        elif complexity_score < 25:
            return '🟡'
        elif complexity_score < 50:
            return '🟠'
        else:
            return '🔴'
    
    def generate_diagnostics(self, code_analysis: Dict[str, Any], 
                           recommendations: list) -> list:
        """Generate VS Code diagnostics for the file"""
        
        diagnostics = []
        
        # High complexity warning
        complexity = code_analysis.get('complexity_score', 0)
        if complexity > 50:
            diagnostics.append({
                'severity': 'warning',
                'message': f'High carbon complexity detected ({complexity:.1f}). Consider refactoring.',
                'range': {'start': {'line': 0, 'character': 0}, 'end': {'line': 1, 'character': 0}},
                'source': 'carbon-analyzer'
            })
        
        # Add recommendations as info diagnostics
        for i, rec in enumerate(recommendations[:2]):
            diagnostics.append({
                'severity': 'info',
                'message': f'Carbon optimization: {rec}',
                'range': {'start': {'line': i, 'character': 0}, 'end': {'line': i+1, 'character': 0}},
                'source': 'carbon-analyzer'
            })
        
        return diagnostics
    
    def get_workspace_config(self) -> Dict[str, Any]:
        """Get VS Code workspace configuration for carbon analysis"""
        
        if not self.workspace_path:
            return {}
        
        # Look for VS Code settings
        vscode_settings = self.workspace_path / '.vscode' / 'settings.json'
        
        config = {
            'carbon.enabled': True,
            'carbon.realTimeAnalysis': False,
            'carbon.showInStatusBar': True,
            'carbon.gridType': 'global_average',
            'carbon.thresholdKg': 0.1,
            'carbon.autoAnalyze': ['onSave', 'onOpen'],
            'carbon.excludePatterns': [
                'node_modules/**',
                'build/**',
                'dist/**',
                '.git/**'
            ]
        }
        
        if vscode_settings.exists():
            try:
                with open(vscode_settings, 'r') as f:
                    user_settings = json.load(f)
                
                # Merge carbon-specific settings
                for key, value in user_settings.items():
                    if key.startswith('carbon.'):
                        config[key] = value
            except:
                pass
        
        return config

# Example VS Code extension package.json configuration
VSCODE_PACKAGE_CONFIG = {
    "name": "carbon-footprint-analyzer",
    "displayName": "Carbon Footprint Analyzer",
    "description": "Analyze and optimize the carbon footprint of your code",
    "version": "1.0.0",
    "engines": {
        "vscode": "^1.60.0"
    },
    "categories": ["Other", "Linters"],
    "keywords": ["carbon", "sustainability", "green", "optimization", "environment"],
    "activationEvents": [
        "onStartupFinished"
    ],
    "main": "./out/extension.js",
    "contributes": {
        "commands": [
            {
                "command": "carbon.analyzeWorkspace",
                "title": "Analyze Workspace Carbon Footprint",
                "category": "Carbon"
            },
            {
                "command": "carbon.analyzeCurrentFile", 
                "title": "Analyze Current File",
                "category": "Carbon"
            },
            {
                "command": "carbon.showReport",
                "title": "Show Carbon Report",
                "category": "Carbon"
            },
            {
                "command": "carbon.optimizationGuide",
                "title": "Show Optimization Guide", 
                "category": "Carbon"
            }
        ],
        "configuration": {
            "title": "Carbon Footprint Analyzer",
            "properties": {
                "carbon.enabled": {
                    "type": "boolean",
                    "default": True,
                    "description": "Enable carbon footprint analysis"
                },
                "carbon.realTimeAnalysis": {
                    "type": "boolean", 
                    "default": False,
                    "description": "Enable real-time analysis (may impact performance)"
                },
                "carbon.showInStatusBar": {
                    "type": "boolean",
                    "default": True,
                    "description": "Show carbon footprint in status bar"
                },
                "carbon.gridType": {
                    "type": "string",
                    "enum": ["global_average", "renewable_heavy", "coal_heavy", "natural_gas", "nuclear"],
                    "default": "global_average",
                    "description": "Electricity grid type for carbon calculations"
                },
                "carbon.thresholdKg": {
                    "type": "number",
                    "default": 0.1,
                    "description": "Carbon footprint threshold (kg CO2) for warnings"
                }
            }
        },
        "menus": {
            "explorer/context": [
                {
                    "command": "carbon.analyzeWorkspace",
                    "group": "carbon"
                }
            ],
            "editor/context": [
                {
                    "command": "carbon.analyzeCurrentFile",
                    "group": "carbon"
                }
            ]
        },
        "statusBar": [
            {
                "id": "carbon.status",
                "name": "Carbon Footprint",
                "alignment": "right",
                "priority": 100
            }
        ]
    },
    "scripts": {
        "compile": "tsc -p ./",
        "watch": "tsc -watch -p ./"
    },
    "devDependencies": {
        "@types/vscode": "^1.60.0",
        "@types/node": "^16.0.0",
        "typescript": "^4.5.0"
    }
}

if __name__ == '__main__':
    # Example usage
    extension = VSCodeCarbonExtension()
    
    # Simulate workspace analysis
    workspace_result = extension.analyze_workspace('/path/to/project')
    print("Workspace Analysis:")
    print(json.dumps(workspace_result, indent=2))
    
    # Simulate file analysis  
    file_result = extension.analyze_current_file('/path/to/project/src/main.js')
    print("\nFile Analysis:")
    print(json.dumps(file_result, indent=2))