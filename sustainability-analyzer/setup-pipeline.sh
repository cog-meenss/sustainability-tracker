#!/bin/bash
# 🚀 Azure DevOps Pipeline Setup Script
# Automates the setup of sustainability analysis pipeline

echo "🌱 Azure DevOps Pipeline Setup"
echo "=============================="
echo ""

# Configuration
REPO_NAME="${1:-sustainability-tracker}"
PROJECT_NAME="${2:-SustainabilityAnalysis}"
BRANCH_NAME="${3:-main}"

echo "📋 Configuration:"
echo "  Repository: $REPO_NAME"
echo "  Project: $PROJECT_NAME"  
echo "  Branch: $BRANCH_NAME"
echo ""

# Step 1: Prepare Repository
echo "📂 Step 1: Preparing Repository"
echo "------------------------------"

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "🔄 Initializing git repository..."
    git init
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository detected"
fi

# Check if azure-pipelines.yml exists
if [ ! -f "azure-pipelines.yml" ]; then
    echo "📝 Creating azure-pipelines.yml symlink..."
    ln -sf sustainability-analyzer/pipeline/azure-pipelines.yml azure-pipelines.yml
    echo "✅ Pipeline configuration linked"
else
    echo "✅ Pipeline configuration exists"
fi

# Step 2: Commit Files
echo ""
echo "📤 Step 2: Committing Files"
echo "--------------------------"

# Add sustainability analyzer files
echo "📁 Adding sustainability analyzer files..."
git add sustainability-analyzer/
git add azure-pipelines.yml

# Check for changes
if git diff --staged --quiet; then
    echo "✅ No changes to commit (already up to date)"
else
    echo "💾 Committing sustainability analysis setup..."
    git commit -m "🌱 Add sustainability analysis pipeline

- Azure DevOps pipeline configuration
- Sustainability analyzer with multi-language support
- Interactive dashboard generation
- Quality gates and reporting
- Pipeline testing scripts

Includes:
- Core analyzer for sustainability metrics
- Visual dashboard with Chart.js integration  
- Advanced data tables with filtering/export
- Executive summary reporting
- Azure DevOps native integration"
    echo "✅ Changes committed"
fi

# Step 3: Pipeline Commands
echo ""
echo "🚀 Step 3: Azure DevOps Setup Commands"
echo "-------------------------------------"

cat << 'EOF'
# Commands to run in Azure DevOps CLI or portal:

## 1. Create Pipeline (Azure CLI)
az pipelines create \
  --name "Sustainability-Analysis" \
  --description "Automated code sustainability evaluation" \
  --repository $REPO_NAME \
  --branch main \
  --yaml-path azure-pipelines.yml

## 2. Set Pipeline Variables
az pipelines variable create \
  --pipeline-name "Sustainability-Analysis" \
  --name sustainabilityThreshold \
  --value 75

az pipelines variable create \
  --pipeline-name "Sustainability-Analysis" \
  --name reportFormat \
  --value "all"

## 3. Create Variable Group (Optional)
az pipelines variable-group create \
  --name "sustainability-analysis-config" \
  --variables sustainabilityThreshold=75 reportFormat=all

## 4. Run Pipeline
az pipelines run --name "Sustainability-Analysis"

EOF

# Step 4: Manual Setup Instructions
echo ""
echo "🖥️  Step 4: Manual Setup (Azure DevOps Portal)"
echo "---------------------------------------------"

cat << EOF
## Portal Setup Steps:

### 1. Create Pipeline
   • Go to Pipelines → New Pipeline
   • Select your repository
   • Choose "Existing Azure Pipelines YAML file"
   • Select: azure-pipelines.yml
   • Click Run

### 2. Configure Variables
   • Pipeline → Edit → Variables
   • Add: sustainabilityThreshold = 75
   • Add: reportFormat = all
   • Add: TeamsWebhookUrl = <your-webhook> (optional)

### 3. Set Permissions
   • Ensure pipeline has artifact publish permissions
   • Enable PR triggers if desired
   • Configure branch policies

### 4. Test Pipeline
   • Trigger manual run
   • Check artifacts are published
   • Verify quality gates work
   • Review build summary

EOF

# Step 5: Verification
echo ""
echo "✅ Step 5: Verification Checklist"
echo "--------------------------------"

echo "After pipeline setup, verify:"
echo "  □ Pipeline runs successfully"
echo "  □ Sustainability reports generated"
echo "  □ Quality gates evaluate correctly"  
echo "  □ Artifacts published to build"
echo "  □ Build summary shows metrics"
echo "  □ Notifications work (if configured)"
echo ""

# Step 6: Next Steps
echo "🎯 Step 6: Next Steps"
echo "-------------------"

cat << EOF
## Recommended Next Actions:

### 1. Baseline Establishment
   • Run pipeline on main branch
   • Document initial scores
   • Set improvement targets

### 2. Integration Setup  
   • Enable PR triggers
   • Add to required checks
   • Configure notifications

### 3. Monitoring Dashboard
   • Set up Azure Analytics
   • Track score trends
   • Monitor threshold compliance

### 4. Team Training
   • Share sustainability metrics guide
   • Review report interpretation
   • Establish improvement process

EOF

# Final output
echo ""
echo "🎉 Setup Complete!"
echo "================="
echo ""
echo "🚀 Ready to run sustainability analysis in Azure DevOps!"
echo ""
echo "📋 Quick Commands:"
echo "  • Test locally: ./sustainability-analyzer/test-pipeline.sh"
echo "  • View config: cat azure-pipelines.yml"
echo "  • Check status: git status"
echo ""
echo "📖 Documentation:"
echo "  • Setup Guide: sustainability-analyzer/PIPELINE_SETUP.md"
echo "  • Test Results: sustainability-analyzer/pipeline-test-output/"
echo ""
echo "✨ Happy sustainable coding!"