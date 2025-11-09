#!/usr/bin/env python3
"""
Continuous Carbon Footprint Monitor
Watches for file changes and runs analysis automatically
"""

import os
import subprocess
import time
from datetime import datetime
from pathlib import Path

def run_carbon_analysis():
    """Run the carbon footprint analysis"""
    print(f"🌱 [{datetime.now().strftime('%H:%M:%S')}] Running carbon analysis...")
    
    try:
        result = subprocess.run([
            'python3', 'carbon-footprint-analyzer/cli.py', 
            '.', '--output', 'carbon-reports-live', 
            '--format', 'json', 'html', '--detailed'
        ], capture_output=True, text=True, cwd='.')
        
        if result.returncode == 0:
            print("✅ Analysis completed successfully!")
            print("📊 Live reports updated in carbon-reports-live/")
            
            # Show quick summary
            try:
                summary_result = subprocess.run([
                    'python3', 'pipeline_helper.py'
                ], cwd='carbon-footprint-analyzer', capture_output=True, text=True)
                if summary_result.returncode == 0:
                    print("📋 Quick Summary:")
                    # Show first few lines of summary
                    lines = summary_result.stdout.split('\n')[:10]
                    for line in lines:
                        if line.strip():
                            print(f"   {line}")
            except:
                pass
                
        else:
            print(f"❌ Analysis failed: {result.stderr}")
            
    except Exception as e:
        print(f"❌ Error running analysis: {e}")

def monitor_project():
    """Monitor project files for changes"""
    print("🔍 Carbon Footprint Live Monitor")
    print("================================")
    print("👀 Watching for code file changes...")
    print("📁 Will update carbon-reports-live/ automatically")
    print("⏹️  Press Ctrl+C to stop")
    print("-" * 50)
    
    # Run initial analysis
    run_carbon_analysis()
    print("-" * 50)
    
    last_check = time.time()
    
    try:
        while True:
            current_time = time.time()
            
            # Find recently modified code files
            changed_files = []
            for root, dirs, files in os.walk('.'):
                # Skip hidden directories and reports
                dirs[:] = [d for d in dirs if not d.startswith('.') and 'carbon-reports' not in d]
                
                for file in files:
                    if file.endswith(('.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp', '.c', '.go', '.rs', '.php', '.rb', '.cs')):
                        filepath = os.path.join(root, file)
                        try:
                            if os.path.getmtime(filepath) > last_check:
                                changed_files.append(filepath)
                        except:
                            pass
            
            if changed_files:
                print(f"📁 [{datetime.now().strftime('%H:%M:%S')}] Detected changes in {len(changed_files)} files")
                for file in changed_files[:3]:
                    print(f"   • {file}")
                if len(changed_files) > 3:
                    print(f"   • ... and {len(changed_files) - 3} more")
                    
                run_carbon_analysis()
                print("-" * 50)
            
            last_check = current_time
            time.sleep(10)  # Check every 10 seconds
            
    except KeyboardInterrupt:
        print("\n🛑 Monitor stopped")
        print("📊 Final reports available in carbon-reports-live/")

if __name__ == "__main__":
    monitor_project()
