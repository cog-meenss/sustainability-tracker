#!/bin/bash
# 🚀 One-Command Sustainability Pipeline Setup
# Usage: ./deploy-sustainability.sh [project-type] [repository-name]

set -e

PROJECT_TYPE=${1:-"mixed"}
REPO_NAME=${2:-$(basename $(pwd))}
TEMPLATE_REPO="cog-meenss/sustainability-tracker"

echo "🌱 Setting up sustainability pipeline for $REPO_NAME ($PROJECT_TYPE project)"

# Create necessary directories
mkdir -p .github/workflows
mkdir -p .sustainability

# Download reusable workflow template
echo "📥 Downloading workflow template..."
curl -sSL "https://raw.githubusercontent.com/$TEMPLATE_REPO/main/reusability-templates/reusable-workflow-template.yml" \
  -o .github/workflows/reusable-sustainability.yml

# Create project-specific workflow that calls the reusable one
echo "⚙️ Creating project-specific workflow..."
cat > .github/workflows/sustainability.yml << EOF
name: 🌱 Sustainability Check

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 2 * * 1'  # Weekly on Monday 2 AM

jobs:
  sustainability:
    uses: ./.github/workflows/reusable-sustainability.yml
    with:
      project_type: '$PROJECT_TYPE'
      min_sustainability_score: 60
      analysis_depth: 'standard'
      enable_security_scan: true
      deploy_dashboard: true
    secrets:
      SLACK_WEBHOOK_URL: \${{ secrets.SLACK_WEBHOOK_URL }}
EOF

# Create project-specific configuration
echo "📝 Creating configuration file..."
cat > .sustainability/config.yml << EOF
# Sustainability Pipeline Configuration for $REPO_NAME
project:
  name: $REPO_NAME
  type: $PROJECT_TYPE
  
analysis:
  depth: standard
  focus_areas:
    - energy_efficiency
    - code_quality  
    - security
    - maintainability

thresholds:
  sustainability_score: 60
  energy_efficiency: 50
  code_quality: 70
  security_score: 75

reporting:
  format: both  # html, json, both
  dashboard: true
  trends: true
  pr_comments: true

quality_gates:
  block_on_fail: false
  require_improvement: true
  
notifications:
  slack: false  # Set to true and add SLACK_WEBHOOK_URL secret to enable
  pr_comments: true
EOF

# Create project-specific exclusions
echo "🚫 Creating exclusion patterns..."
cat > .sustainability/ignore << EOF
# Sustainability Analysis Exclusions
# Add patterns for files/directories to exclude from analysis

# Common exclusions
node_modules/
.venv/
venv/
__pycache__/
.git/
.pytest_cache/
coverage/
dist/
build/

# Project-specific exclusions (customize as needed)
# legacy/
# vendor/
# third_party/
EOF

# Download sustainability evaluator script
echo "📊 Downloading sustainability evaluator..."
curl -sSL "https://raw.githubusercontent.com/$TEMPLATE_REPO/main/sustainability_evaluator.py" \
  -o sustainability_evaluator.py
chmod +x sustainability_evaluator.py

# Create README for sustainability setup
echo "📚 Creating documentation..."
cat > SUSTAINABILITY.md << EOF
# 🌱 Sustainability Pipeline

This project uses an automated sustainability analysis pipeline to monitor and improve code quality, energy efficiency, and environmental impact.

## 📊 Dashboard

Visit [https://$(echo $REPO_NAME | tr '[:upper:]' '[:lower:]').github.io/](https://$(echo $REPO_NAME | tr '[:upper:]' '[:lower:]').github.io/) to view the sustainability dashboard.

## 🎯 Current Thresholds

- **Sustainability Score**: 60/100 (minimum)
- **Energy Efficiency**: 50/100 (minimum)
- **Code Quality**: 70/100 (target)
- **Security Score**: 75/100 (target)

## 🔧 Configuration

The pipeline is configured via \`.sustainability/config.yml\`. Key settings:

- **Project Type**: $PROJECT_TYPE
- **Analysis Depth**: Standard
- **Quality Gates**: Enabled (non-blocking)
- **Dashboard**: Auto-deployed to GitHub Pages

## 📈 How It Works

1. **Automated Triggers**: Runs on push to main/develop, PRs, and weekly schedule
2. **Multi-Dimensional Analysis**: Checks sustainability, security, performance, and dependencies  
3. **Quality Gates**: Enforces minimum sustainability standards
4. **Rich Reporting**: Generates interactive HTML dashboard and JSON reports
5. **PR Integration**: Adds detailed comments to pull requests with recommendations

## 🚀 Manual Execution

Run analysis locally:
\`\`\`bash
python3 sustainability_evaluator.py --path . --format both --output reports/
\`\`\`

## 🔧 Customization

### Adjust Thresholds
Edit \`.sustainability/config.yml\` to modify score requirements:

\`\`\`yaml
thresholds:
  sustainability_score: 70  # Increase for stricter requirements
\`\`\`

### Exclude Files
Add patterns to \`.sustainability/ignore\`:

\`\`\`
legacy/
vendor/
*.min.js
\`\`\`

### Enable Notifications
Add \`SLACK_WEBHOOK_URL\` repository secret and set:

\`\`\`yaml
notifications:
  slack: true
\`\`\`

## 📋 Quality Gates

The pipeline enforces these quality standards:

- ✅ **Sustainability Score** ≥ 60/100
- ✅ **No Critical Security Issues**
- ✅ **Code Quality** meets project standards
- ✅ **Performance** within acceptable limits

## 🛠️ Troubleshooting

### Pipeline Fails
1. Check the Actions tab for detailed logs
2. Review recommendations in the generated report
3. Address critical issues and re-run

### Dashboard Not Updating
1. Ensure GitHub Pages is enabled in repository settings
2. Check that the workflow has \`pages: write\` permissions
3. Verify the deployment step completed successfully

### Customize Analysis
1. Modify \`.sustainability/config.yml\` for project-specific settings
2. Add custom exclusion patterns in \`.sustainability/ignore\`
3. Adjust workflow triggers in \`.github/workflows/sustainability.yml\`

## 📞 Support

- 📖 [Full Documentation](https://github.com/$TEMPLATE_REPO/blob/main/reusability-templates/cross-project-reusability-guide.md)
- 🐛 [Report Issues](https://github.com/$TEMPLATE_REPO/issues)
- 💬 [Discussions](https://github.com/$TEMPLATE_REPO/discussions)

---
*🌱 Powered by Reusable Sustainability Pipeline*
EOF

# Create .gitignore entries for sustainability reports
if [ -f .gitignore ]; then
  if ! grep -q "sustainability-reports" .gitignore; then
    echo "" >> .gitignore
    echo "# Sustainability Reports" >> .gitignore
    echo "sustainability-reports/" >> .gitignore
  fi
else
  cat > .gitignore << EOF
# Sustainability Reports
sustainability-reports/
EOF
fi

# Set up GitHub Pages if repository exists
if command -v gh >/dev/null 2>&1; then
  echo "🌐 Configuring GitHub Pages..."
  gh api "repos/$(gh repo view --json owner,name -q '.owner.login + "/" + .name')" -X PATCH \
    -f has_pages=true 2>/dev/null || echo "⚠️  Could not auto-configure GitHub Pages (manual setup required)"
fi

echo ""
echo "✅ Sustainability pipeline setup complete!"
echo ""
echo "📋 Next Steps:"
echo "1. Commit and push the changes:"
echo "   git add ."
echo "   git commit -m '🌱 Add sustainability pipeline'"
echo "   git push"
echo ""
echo "2. Enable GitHub Pages in repository settings (if not auto-configured)"
echo "   - Go to Settings > Pages"  
echo "   - Select 'GitHub Actions' as source"
echo ""
echo "3. Optional: Add SLACK_WEBHOOK_URL secret for notifications"
echo ""
echo "4. View your dashboard after first run:"
echo "   https://$(echo $REPO_NAME | tr '[:upper:]' '[:lower:]').github.io/"
echo ""
echo "🌱 Happy sustainable coding!"