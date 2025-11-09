#!/bin/bash
# 🌱 Instant Carbon Analysis Setup - No Azure Parallelism Required!
# This script sets up multiple automation options for carbon footprint analysis

echo "🌱 CARBON FOOTPRINT AUTOMATION SETUP"
echo "===================================="
echo ""

# Check if we're in the right directory
if [ ! -f "carbon-footprint-analyzer/cli.py" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    echo "   Expected to find: carbon-footprint-analyzer/cli.py"
    exit 1
fi

echo "✅ Found carbon analyzer"

# 1. Setup Git Pre-commit Hook
echo ""
echo "📎 Setting up Git pre-commit hook..."
if [ -d ".git" ]; then
    mkdir -p .git/hooks
    cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
echo "🌱 Running automatic carbon footprint analysis..."
cd "$(git rev-parse --show-toplevel)"
python3 carbon-footprint-analyzer/cli.py . --output carbon-reports --format json html --detailed
if [ $? -eq 0 ]; then
    echo "✅ Carbon analysis completed successfully!"
    echo "📊 Reports updated in carbon-reports/"
else
    echo "⚠️  Carbon analysis had issues, but continuing with commit..."
fi
EOF
    chmod +x .git/hooks/pre-commit
    echo "✅ Git hook installed - analysis will run on every commit"
else
    echo "⚠️  No .git directory found - skipping git hook"
fi

# 2. Create Manual Analysis Script
echo ""
echo "🔧 Creating manual analysis script..."
cat > analyze-carbon-now.sh << 'EOF'
#!/bin/bash
echo "🌱 Carbon Footprint Analysis"
echo "============================"
echo ""

# Create timestamped output directory
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
OUTPUT_DIR="carbon-analysis-$TIMESTAMP"

echo "📊 Running analysis..."
echo "📁 Output directory: $OUTPUT_DIR"
echo ""

# Run the carbon analyzer
python3 carbon-footprint-analyzer/cli.py . --output "$OUTPUT_DIR" --format json html --detailed

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Analysis completed successfully!"
    echo "📊 Reports saved to: $OUTPUT_DIR/"
    echo "🌐 View results: open $OUTPUT_DIR/complete_analysis.html"
    echo ""
    
    # Show quick summary
    if [ -f "$OUTPUT_DIR/complete_analysis.json" ]; then
        echo "📋 Quick Summary:"
        cd carbon-footprint-analyzer
        python3 pipeline_helper.py --report "../$OUTPUT_DIR/complete_analysis.json" 2>/dev/null || echo "   Check the HTML report for detailed results"
        cd ..
    fi
else
    echo "❌ Analysis failed. Please check the error messages above."
fi
EOF
chmod +x analyze-carbon-now.sh
echo "✅ Manual analysis script created: ./analyze-carbon-now.sh"

# 3. Create GitHub Actions Workflow (if this is a GitHub repo)
echo ""
echo "🐙 Checking for GitHub integration..."
if grep -q "github" .git/config 2>/dev/null; then
    echo "📁 Creating GitHub Actions workflow..."
    mkdir -p .github/workflows
    cat > .github/workflows/carbon-analysis.yml << 'EOF'
name: Carbon Footprint Analysis

on:
  push:
    branches: [ main, master, develop ]
  pull_request:
    branches: [ main, master ]
  workflow_dispatch:  # Allow manual trigger

jobs:
  carbon-analysis:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.x'
        
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install requests pyyaml
        
    - name: Run Carbon Footprint Analysis
      run: |
        echo "🌱 Starting Carbon Footprint Analysis..."
        cd carbon-footprint-analyzer
        python cli.py .. --output ../carbon-reports --format json html --detailed
        
    - name: Display Analysis Results
      run: |
        cd carbon-footprint-analyzer
        python pipeline_helper.py || echo "✅ Analysis completed - check artifacts for detailed results"
        
    - name: Upload Carbon Analysis Reports
      uses: actions/upload-artifact@v4
      if: always()
      with:
        name: carbon-footprint-reports-${{ github.sha }}
        path: carbon-reports/
        retention-days: 30
        
    - name: Upload Analysis Summary
      if: always()
      run: |
        echo "📊 Carbon Analysis Summary" > analysis-summary.txt
        echo "=========================" >> analysis-summary.txt
        echo "Commit: ${{ github.sha }}" >> analysis-summary.txt
        echo "Branch: ${{ github.ref_name }}" >> analysis-summary.txt
        echo "Date: $(date)" >> analysis-summary.txt
        echo "" >> analysis-summary.txt
        if [ -f "carbon-reports/complete_analysis.json" ]; then
          echo "✅ Analysis completed successfully" >> analysis-summary.txt
          echo "📁 Reports available in artifacts" >> analysis-summary.txt
        else
          echo "❌ Analysis may have encountered issues" >> analysis-summary.txt
        fi
        
    - name: Upload Summary
      uses: actions/upload-artifact@v4
      if: always()
      with:
        name: analysis-summary-${{ github.sha }}
        path: analysis-summary.txt
EOF
    echo "✅ GitHub Actions workflow created"
    echo "   → Automatic analysis on every push/PR"
    echo "   → Manual trigger available in GitHub Actions tab"
else
    echo "ℹ️  Not a GitHub repository - skipping GitHub Actions setup"
fi

# 4. Create Monitoring Script
echo ""
echo "👀 Creating continuous monitoring script..."
cat > carbon-monitor.py << 'EOF'
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
EOF
chmod +x carbon-monitor.py
echo "✅ Continuous monitor created: ./carbon-monitor.py"

# 5. Summary and Usage Instructions
echo ""
echo "🎉 SETUP COMPLETE!"
echo "=================="
echo ""
echo "Your carbon footprint automation is ready! Here's what you can do:"
echo ""
echo "🔄 AUTOMATIC ANALYSIS:"
echo "   • Every git commit → Automatic analysis (via git hook)"
if grep -q "github" .git/config 2>/dev/null; then
    echo "   • Every GitHub push → Cloud analysis (via GitHub Actions)"
fi
echo ""
echo "🔧 MANUAL ANALYSIS:"
echo "   • Run: ./analyze-carbon-now.sh"
echo "   • Creates timestamped reports"
echo ""
echo "👀 LIVE MONITORING:"
echo "   • Run: python3 carbon-monitor.py"
echo "   • Watches for file changes, auto-analyzes"
echo ""
echo "📊 VIEW RESULTS:"
echo "   • Open any generated complete_analysis.html file"
echo "   • Check carbon-reports/ or timestamped directories"
echo ""
echo "🚀 TEST IT NOW:"
echo "   ./analyze-carbon-now.sh"
echo ""
echo "✨ No Azure DevOps parallelism needed - you're fully automated!"
EOF
chmod +x setup-carbon-automation.sh
echo "✅ Setup script created: ./setup-carbon-automation.sh"