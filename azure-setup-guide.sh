#!/bin/bash
# 🎯 Azure DevOps Quick Setup Script
# Helps you set up the sustainability analysis pipeline in Azure DevOps

echo "🌱 Azure DevOps Pipeline Quick Setup"
echo "===================================="
echo ""

# Check current status
echo "📋 Current Setup Status:"
echo "----------------------"

# Check if azure-pipelines.yml exists
if [ -f "azure-pipelines.yml" ]; then
    echo "✅ Pipeline configuration: azure-pipelines.yml found"
else
    echo "❌ Pipeline configuration: azure-pipelines.yml missing"
    echo "   Creating symlink..."
    ln -sf sustainability-analyzer/pipeline/azure-pipelines.yml azure-pipelines.yml
    echo "✅ Pipeline configuration: Created azure-pipelines.yml"
fi

# Check git status
if git status &>/dev/null; then
    echo "✅ Git repository: Initialized"
    
    # Check if files are committed
    if git diff --staged --quiet && git diff --quiet; then
        echo "✅ Git status: All files committed"
    else
        echo "⚠️  Git status: Uncommitted changes detected"
        echo "   Run: git add . && git commit -m 'Add sustainability analysis'"
    fi
else
    echo "❌ Git repository: Not initialized"
    echo "   Run: git init"
fi

# Check sustainability analyzer files
if [ -d "sustainability-analyzer" ]; then
    echo "✅ Sustainability analyzer: Files present"
    file_count=$(find sustainability-analyzer -name "*.py" | wc -l)
    echo "   Found $file_count Python files"
else
    echo "❌ Sustainability analyzer: Missing files"
fi

echo ""
echo "🚀 Azure DevOps Setup Instructions:"
echo "=================================="
echo ""

echo "🌐 METHOD 1: Web Portal (Recommended - 5 minutes)"
echo "================================================"
echo ""
echo "Step 1: Open Azure DevOps"
echo "   • Go to: https://dev.azure.com/[your-organization]/[your-project]"
echo "   • Click: Pipelines → New Pipeline"
echo ""
echo "Step 2: Select Repository"
echo "   • Choose your repository source (GitHub, Azure Repos, etc.)"
echo "   • Select this repository: $(basename $(pwd))"
echo ""
echo "Step 3: Configure Pipeline"
echo "   • Select: 'Existing Azure Pipelines YAML file'"
echo "   • Branch: main (or your default branch)"
echo "   • Path: azure-pipelines.yml"
echo "   • Click: Continue"
echo ""
echo "Step 4: Review and Run"
echo "   • Review the pipeline configuration"
echo "   • Click: 'Run' to create and start the pipeline"
echo ""
echo "Step 5: Add Variables (Optional)"
echo "   • After creation, click: 'Edit' → 'Variables'"
echo "   • Add: sustainabilityThreshold = 75"
echo "   • Add: reportFormat = all"
echo "   • Add: TeamsWebhookUrl = [your-webhook] (optional)"
echo ""

echo "💻 METHOD 2: Azure CLI (Advanced - 3 minutes)"
echo "============================================="
echo ""
echo "Prerequisites:"
echo "   brew install azure-cli              # Install Azure CLI"
echo "   az login                           # Login to Azure"
echo "   az extension add --name azure-devops  # Add DevOps extension"
echo ""
echo "Setup Commands:"
cat << 'EOF'
   # Configure defaults (replace with your org/project)
   az devops configure --defaults \
     organization=https://dev.azure.com/YourOrg \
     project=YourProject

   # Create pipeline
   az pipelines create \
     --name "Sustainability-Analysis" \
     --description "Code sustainability evaluation" \
     --repository "Tracker" \
     --branch "main" \
     --yaml-path "azure-pipelines.yml"

   # Set variables
   az pipelines variable create \
     --pipeline-name "Sustainability-Analysis" \
     --name "sustainabilityThreshold" \
     --value "75"

   # Run pipeline
   az pipelines run --name "Sustainability-Analysis"
EOF
echo ""

echo "📊 What Happens Next:"
echo "===================="
echo ""
echo "🔄 Pipeline Execution (10-15 minutes total):"
echo "   Stage 1: Sustainability Analysis (5-10 min)"
echo "   Stage 2: Quality Gate Evaluation (1 min)"
echo "   Stage 3: Report Generation (2-3 min)"
echo "   Stage 4: Notification & Publishing (1 min)"
echo ""
echo "📦 Generated Artifacts:"
echo "   • Interactive HTML Dashboard"
echo "   • Advanced Data Tables"
echo "   • Executive Summary PDF"
echo "   • Raw JSON Analysis Data"
echo "   • Azure DevOps Test Results"
echo ""
echo "🎯 Quality Gate Results:"
echo "   • Overall Sustainability Score: X/100"
echo "   • Pass/Fail based on threshold (default: 75)"
echo "   • Detailed breakdown by metric categories"
echo ""

echo "⚡ Pipeline Triggers:"
echo "==================="
echo ""
echo "✅ Automatic Triggers:"
echo "   • Push to main/develop branches"
echo "   • Pull requests to main/develop"
echo "   • Weekly schedule (Monday 2 AM UTC)"
echo ""
echo "▶️  Manual Triggers:"
echo "   • 'Run pipeline' button in Azure DevOps"
echo "   • Azure CLI: az pipelines run"
echo ""

echo "🛠️  Customization Options:"
echo "========================="
echo ""
echo "📊 Adjust Quality Thresholds:"
echo "   sustainabilityThreshold: 75    # Overall score minimum"
echo "   energyThreshold: 80           # Energy efficiency"
echo "   carbonMaximum: 40             # Carbon footprint maximum"
echo ""
echo "📋 Choose Report Formats:"
echo "   reportFormat: 'all'           # All formats"
echo "   reportFormat: 'html'          # HTML dashboard only"
echo "   reportFormat: 'json,azure'    # JSON + Azure format"
echo ""
echo "🔔 Teams Notifications:"
echo "   1. Create Teams incoming webhook"
echo "   2. Add TeamsWebhookUrl variable"
echo "   3. Get notifications on quality gate failures"
echo ""

echo "🎉 Success Verification:"
echo "======================="
echo ""
echo "After pipeline setup, check:"
echo "   □ Pipeline appears in Azure DevOps Pipelines list"
echo "   □ Pipeline runs successfully (green checkmark)"
echo "   □ Build summary shows sustainability metrics"
echo "   □ Artifacts contain generated reports"
echo "   □ Test results show sustainability analysis"
echo "   □ Quality gate evaluates correctly"
echo ""

echo "📚 Additional Resources:"
echo "======================"
echo ""
echo "📖 Detailed Setup Guide:"
echo "   cat AZURE_DEVOPS_SETUP.md"
echo ""
echo "🧪 Test Locally First:"
echo "   ./sustainability-analyzer/test-pipeline.sh"
echo ""
echo "🎯 Quick Start Guide:"
echo "   cat sustainability-analyzer/PIPELINE_QUICKSTART.md"
echo ""

echo "🚀 Ready to Set Up Azure DevOps Pipeline!"
echo "========================================="
echo ""
echo "👉 Next Steps:"
echo "   1. Open Azure DevOps in your browser"
echo "   2. Follow METHOD 1 instructions above"
echo "   3. Create and run your first pipeline"
echo "   4. Review the sustainability analysis results"
echo ""
echo "✨ Your code is ready - just create the pipeline! 🌱"