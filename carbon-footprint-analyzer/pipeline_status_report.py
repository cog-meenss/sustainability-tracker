#!/usr/bin/env python3
"""
Comprehensive Carbon Footprint Pipeline Status Report
Shows all available automation methods and their current status
"""

import os
import json
import subprocess
from datetime import datetime
from pathlib import Path

def check_git_status():
    """Check git repository status and recent commits"""
    try:
        # Check if we're in a git repository
        result = subprocess.run(['git', 'rev-parse', '--git-dir'], 
                              capture_output=True, text=True, cwd='..')
        if result.returncode != 0:
            return {'status': '❌ NOT A GIT REPOSITORY', 'commits': []}
        
        # Get recent commits
        result = subprocess.run(['git', 'log', '--oneline', '-5'], 
                              capture_output=True, text=True, cwd='..')
        commits = result.stdout.strip().split('\n') if result.stdout.strip() else []
        
        # Check if git hooks triggered recently
        hook_triggered = any('carbon' in commit.lower() or 'hook' in commit.lower() for commit in commits)
        
        return {
            'status': '✅ GIT REPOSITORY ACTIVE',
            'commits': commits,
            'hook_evidence': hook_triggered
        }
    except Exception as e:
        return {'status': f'❌ ERROR: {e}', 'commits': []}

def check_automation_methods():
    """Comprehensive check of all automation methods"""
    methods = {}
    
    # 1. Git Hooks
    git_hook_path = '../.git/hooks/pre-commit'
    if os.path.exists(git_hook_path):
        try:
            with open(git_hook_path, 'r') as f:
                content = f.read()
            if 'carbon' in content.lower():
                methods['git_hooks'] = {
                    'status': '✅ ACTIVE AND CONFIGURED',
                    'description': 'Runs carbon analysis automatically on every git commit',
                    'trigger': 'git commit',
                    'output': 'carbon-reports/',
                    'last_modified': datetime.fromtimestamp(os.path.getmtime(git_hook_path)).strftime('%Y-%m-%d %H:%M:%S')
                }
            else:
                methods['git_hooks'] = {
                    'status': '⚠️ EXISTS BUT NOT CARBON-ENABLED',
                    'description': 'Pre-commit hook exists but not configured for carbon analysis'
                }
        except Exception as e:
            methods['git_hooks'] = {
                'status': f'❌ ERROR READING HOOK: {e}',
                'description': 'Could not read pre-commit hook file'
            }
    else:
        methods['git_hooks'] = {
            'status': '❌ NOT INSTALLED',
            'description': 'No pre-commit hook found',
            'setup': 'Run ./setup-carbon-automation.sh to install'
        }
    
    # 2. Manual Analysis Script
    manual_script = '../analyze-carbon-now.sh'
    if os.path.exists(manual_script):
        methods['manual_analysis'] = {
            'status': '✅ AVAILABLE',
            'description': 'On-demand carbon analysis with timestamped reports',
            'usage': './analyze-carbon-now.sh',
            'output': 'carbon-analysis-TIMESTAMP/',
            'last_modified': datetime.fromtimestamp(os.path.getmtime(manual_script)).strftime('%Y-%m-%d %H:%M:%S')
        }
    else:
        methods['manual_analysis'] = {
            'status': '❌ NOT FOUND',
            'description': 'Manual analysis script not available',
            'setup': 'Run ./setup-carbon-automation.sh to create'
        }
    
    # 3. Live Monitoring
    monitor_script = '../carbon-monitor.py'
    if os.path.exists(monitor_script):
        methods['live_monitor'] = {
            'status': '✅ AVAILABLE',
            'description': 'Continuous file monitoring with automatic analysis',
            'usage': 'python3 carbon-monitor.py',
            'output': 'carbon-reports-live/',
            'last_modified': datetime.fromtimestamp(os.path.getmtime(monitor_script)).strftime('%Y-%m-%d %H:%M:%S')
        }
    else:
        methods['live_monitor'] = {
            'status': '❌ NOT FOUND',
            'description': 'Live monitoring script not available',
            'setup': 'Run ./setup-carbon-automation.sh to create'
        }
    
    # 4. GitHub Actions
    gh_actions = '../.github/workflows/carbon-analysis.yml'
    if os.path.exists(gh_actions):
        methods['github_actions'] = {
            'status': '✅ CONFIGURED',
            'description': 'Cloud-based CI/CD with free GitHub runners',
            'trigger': 'git push to GitHub',
            'output': 'GitHub Artifacts',
            'last_modified': datetime.fromtimestamp(os.path.getmtime(gh_actions)).strftime('%Y-%m-%d %H:%M:%S')
        }
    else:
        methods['github_actions'] = {
            'status': '❌ NOT CONFIGURED',
            'description': 'GitHub Actions workflow not set up',
            'setup': 'Push to GitHub repository and run setup script'
        }
    
    # 5. Setup Script
    setup_script = '../setup-carbon-automation.sh'
    if os.path.exists(setup_script):
        methods['setup_script'] = {
            'status': '✅ AVAILABLE',
            'description': 'One-click setup for all automation methods',
            'usage': './setup-carbon-automation.sh',
            'last_modified': datetime.fromtimestamp(os.path.getmtime(setup_script)).strftime('%Y-%m-%d %H:%M:%S')
        }
    else:
        methods['setup_script'] = {
            'status': '❌ NOT FOUND',
            'description': 'Automation setup script missing'
        }
    
    return methods

def check_recent_reports():
    """Check for recent carbon analysis reports"""
    report_dirs = []
    
    # Check main carbon-reports
    if os.path.exists('../carbon-reports'):
        report_dirs.append({
            'name': 'carbon-reports',
            'path': '../carbon-reports',
            'type': 'Main Reports',
            'last_modified': datetime.fromtimestamp(os.path.getmtime('../carbon-reports')).strftime('%Y-%m-%d %H:%M:%S')
        })
    
    # Check for timestamped reports
    parent_dir = Path('..')
    for item in parent_dir.iterdir():
        if item.is_dir() and item.name.startswith('carbon-analysis-'):
            report_dirs.append({
                'name': item.name,
                'path': str(item),
                'type': 'Timestamped Report',
                'last_modified': datetime.fromtimestamp(item.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            })
    
    return sorted(report_dirs, key=lambda x: x['last_modified'], reverse=True)

def display_pipeline_status_report():
    """Display comprehensive pipeline status report"""
    print("🚀 CARBON FOOTPRINT PIPELINE STATUS REPORT")
    print("=" * 60)
    print(f"📅 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🔍 Project: Universal Carbon Footprint Analyzer")
    print("=" * 60)
    
    # Git Status
    git_status = check_git_status()
    print(f"\n📂 GIT REPOSITORY STATUS:")
    print("-" * 40)
    print(f"Status: {git_status['status']}")
    if git_status['commits']:
        print("Recent commits:")
        for i, commit in enumerate(git_status['commits'][:3], 1):
            print(f"  {i}. {commit}")
        if git_status['hook_evidence']:
            print("🎣 Evidence of git hook activity detected!")
    
    # Automation Methods
    methods = check_automation_methods()
    print(f"\n🤖 AUTOMATION METHODS STATUS:")
    print("-" * 40)
    
    active_methods = 0
    for method_name, details in methods.items():
        status = details['status']
        if status.startswith('✅'):
            active_methods += 1
        
        method_display = method_name.replace('_', ' ').title()
        print(f"\n🔧 {method_display}:")
        print(f"   Status: {status}")
        print(f"   Description: {details['description']}")
        
        if 'usage' in details:
            print(f"   Usage: {details['usage']}")
        if 'trigger' in details:
            print(f"   Trigger: {details['trigger']}")
        if 'output' in details:
            print(f"   Output: {details['output']}")
        if 'setup' in details:
            print(f"   Setup: {details['setup']}")
        if 'last_modified' in details:
            print(f"   Last Modified: {details['last_modified']}")
    
    print(f"\n📊 AUTOMATION SUMMARY:")
    print(f"   Active Methods: {active_methods}/5")
    print(f"   Coverage: {(active_methods/5)*100:.0f}%")
    
    if active_methods >= 3:
        print("   Status: 🎉 EXCELLENT - Multiple automation methods active!")
    elif active_methods >= 1:
        print("   Status: ✅ GOOD - Basic automation available")
    else:
        print("   Status: ⚠️ NEEDS SETUP - Run ./setup-carbon-automation.sh")
    
    # Recent Reports
    reports = check_recent_reports()
    print(f"\n📊 RECENT CARBON ANALYSIS REPORTS:")
    print("-" * 40)
    if reports:
        for i, report in enumerate(reports[:5], 1):
            print(f"{i}. {report['name']} ({report['type']})")
            print(f"   Last Updated: {report['last_modified']}")
        
        # Show latest analysis if available
        latest_report = reports[0]
        json_file = os.path.join(latest_report['path'], 'complete_analysis.json')
        if os.path.exists(json_file):
            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)
                
                carbon_data = data.get('carbon_footprint', {})
                print(f"\n📈 LATEST ANALYSIS SUMMARY:")
                print(f"   Carbon Footprint: {carbon_data.get('total_carbon_kg', 0):.6f} kg CO2")
                print(f"   Energy Usage: {carbon_data.get('total_energy_kwh', 0):.6f} kWh")
                print(f"   Impact Level: {carbon_data.get('comparison_metrics', {}).get('impact_level', 'Unknown').upper()}")
            except:
                print("   (Could not parse latest analysis data)")
    else:
        print("   No reports found - run analysis to generate reports")
    
    # Recommendations
    print(f"\n💡 RECOMMENDATIONS:")
    print("-" * 40)
    
    if methods['git_hooks']['status'].startswith('✅'):
        print("✅ Git hooks active - carbon analysis runs automatically!")
    else:
        print("🔧 Install git hooks for automatic analysis on commits")
    
    if methods['manual_analysis']['status'].startswith('✅'):
        print("✅ Manual analysis available - run './analyze-carbon-now.sh' anytime")
    else:
        print("🔧 Set up manual analysis script for on-demand reports")
    
    if not methods['github_actions']['status'].startswith('✅'):
        print("🌐 Consider GitHub Actions for cloud-based CI/CD")
    
    print(f"\n🎯 NEXT STEPS:")
    if active_methods == 0:
        print("   1. Run: ./setup-carbon-automation.sh")
        print("   2. Test with: ./analyze-carbon-now.sh")
        print("   3. Make a git commit to test hooks")
    elif active_methods < 3:
        print("   1. Run setup script to enable more automation")
        print("   2. Consider GitHub Actions for cloud CI/CD")
    else:
        print("   1. Make code changes and commit to see automation")
        print("   2. View reports in generated directories")
        print("   3. Monitor carbon footprint trends over time")
    
    print("\n" + "=" * 60)
    print("🌱 Carbon analysis automation is available - no Azure parallelism needed!")
    print("=" * 60)

if __name__ == "__main__":
    display_pipeline_status_report()