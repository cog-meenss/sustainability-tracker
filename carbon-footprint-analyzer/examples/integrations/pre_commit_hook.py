#!/usr/bin/env python3
"""
Pre-commit hook for carbon footprint analysis
"""

import subprocess
import sys
import json
from pathlib import Path

def main():
    """Main pre-commit hook function"""
    
    print("🌱 Running carbon footprint pre-commit check...")
    
    try:
        # Get the git root directory
        git_root = subprocess.check_output(
            ['git', 'rev-parse', '--show-toplevel'],
            text=True
        ).strip()
        
        # Run quick carbon analysis
        analyzer_path = Path(__file__).parent.parent / 'cli.py'
        
        result = subprocess.run([
            'python3', str(analyzer_path),
            git_root,
            '--format', 'json',
            '--config', 'basic_config.json'
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"❌ Carbon analysis failed: {result.stderr}")
            return 1
        
        # Parse results
        output_file = Path('./carbon_reports/complete_analysis.json')
        if output_file.exists():
            with open(output_file, 'r') as f:
                analysis = json.load(f)
            
            carbon_kg = analysis.get('carbon_footprint', {}).get('total_carbon_kg', 0)
            impact_level = analysis.get('carbon_footprint', {}).get('comparison_metrics', {}).get('impact_level', 'unknown')
            
            # Check if carbon footprint increased significantly
            previous_carbon = get_previous_carbon_footprint()
            
            if previous_carbon and carbon_kg > previous_carbon * 1.1:  # 10% increase threshold
                increase_percent = ((carbon_kg / previous_carbon) - 1) * 100
                print(f"⚠️  Carbon footprint increased by {increase_percent:.1f}%")
                print(f"   Previous: {previous_carbon:.6f} kg CO2")
                print(f"   Current:  {carbon_kg:.6f} kg CO2")
                print("")
                print("Consider reviewing your changes for performance impact.")
                print("To proceed anyway, use: git commit --no-verify")
                return 1
            
            # Store current footprint for next run
            store_carbon_footprint(carbon_kg)
            
            print(f"✅ Carbon footprint: {carbon_kg:.6f} kg CO2 ({impact_level} impact)")
            
            # Show quick recommendations if impact is high
            if impact_level in ['high', 'very_high']:
                recommendations = analysis.get('recommendations', [])[:2]
                if recommendations:
                    print("💡 Quick optimization tips:")
                    for rec in recommendations:
                        print(f"   • {rec}")
            
            return 0
        
    except Exception as e:
        print(f"❌ Pre-commit carbon check failed: {e}")
        return 1

def get_previous_carbon_footprint() -> float:
    """Get the previously stored carbon footprint"""
    try:
        carbon_file = Path('.git/carbon-footprint')
        if carbon_file.exists():
            with open(carbon_file, 'r') as f:
                return float(f.read().strip())
    except:
        pass
    return 0.0

def store_carbon_footprint(carbon_kg: float):
    """Store carbon footprint for next comparison"""
    try:
        carbon_file = Path('.git/carbon-footprint')
        with open(carbon_file, 'w') as f:
            f.write(str(carbon_kg))
    except:
        pass

if __name__ == '__main__':
    sys.exit(main())