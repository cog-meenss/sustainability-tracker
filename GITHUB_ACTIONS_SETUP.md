# 🚀 GitHub Actions Setup Guide

## 🎯 Why GitHub Actions?

- ✅ **Free Tier**: 2,000 minutes/month for private repos, unlimited for public repos
- ✅ **No Setup Required**: Works immediately without grants or approvals
- ✅ **Rich Ecosystem**: Thousands of pre-built actions
- ✅ **Integrated**: Built into GitHub with great UI/UX
- ✅ **Powerful**: Matrix builds, environments, secrets management

## 📋 Setup Steps

### Option 1: Create New GitHub Repository

1. **Go to GitHub**: https://github.com/new
2. **Repository Name**: `sustainability-tracker` 
3. **Description**: `Code sustainability analysis and business data tracker`
4. **Visibility**: Choose Public (unlimited CI/CD) or Private (2000 min/month)
5. **Initialize**: ✅ Add README, .gitignore (Node.js), License (MIT)
6. **Create Repository**

### Option 2: Mirror from Azure DevOps

```bash
# Clone your Azure DevOps repo
git clone https://159645@dev.azure.com/159645/Alpha/_git/Alpha alpha-mirror
cd alpha-mirror

# Add GitHub as new origin (replace USERNAME with your GitHub username)
git remote add github https://github.com/USERNAME/sustainability-tracker.git

# Push to GitHub
git push github main
```

### Option 3: Dual Setup (Recommended)

Keep both Azure DevOps and GitHub, sync when needed:

```bash
# Add GitHub as additional remote
git remote add github https://github.com/USERNAME/sustainability-tracker.git

# Push current state to GitHub  
git push github main

# Future syncing
git push origin main      # Push to Azure DevOps
git push github main      # Push to GitHub
```

## 🔧 Activating GitHub Actions

1. **Navigate** to your GitHub repository
2. **Go to Actions tab** (https://github.com/USERNAME/sustainability-tracker/actions)
3. **GitHub will auto-detect** the workflows in `.github/workflows/`
4. **Click "I understand my workflows"** to enable Actions
5. **Workflows will run automatically** on next push

## 📊 Available Workflows

### 1. Full Sustainability Analysis (`sustainability-analysis.yml`)
- **Triggers**: Push to main/develop, PRs, weekly schedule, manual
- **Features**: 
  - Comprehensive file analysis
  - Interactive HTML dashboard with Chart.js
  - Quality gates with configurable thresholds
  - PR comments with results
  - Artifact publishing (30-day retention)
  - Job summaries in GitHub UI

### 2. Simple Check (`simple-sustainability.yml`)  
- **Triggers**: Push to main, manual
- **Features**:
  - Quick file counting and basic scoring
  - Minimal resource usage
  - Fast execution (< 1 minute)

## 🎯 GitHub Actions Benefits

### Rich Integration
- **PR Comments**: Automatic analysis results on pull requests
- **Job Summaries**: Rich markdown summaries in the Actions UI
- **Artifacts**: Download reports, dashboards, and raw data
- **Status Checks**: Integration with branch protection rules

### Advanced Features  
- **Matrix Builds**: Test multiple Node.js/Python versions
- **Environments**: Staging, production deployments
- **Secrets**: Secure API keys and tokens
- **Scheduled Runs**: Automatic weekly/monthly analysis

### Monitoring & Notifications
- **Email Notifications**: On workflow failures
- **Slack/Teams Integration**: Custom webhook notifications
- **Status Badges**: Show build status in README
- **Insights**: Detailed workflow analytics

## 🚀 Next Steps

1. **Create GitHub Repository** using one of the options above
2. **Push the workflows** (already committed to your local repo)
3. **Enable GitHub Actions** in repository settings
4. **Trigger first run** by pushing code or manual trigger
5. **Review results** in Actions tab and download artifacts

## 💡 Pro Tips

- **Public Repositories**: Get unlimited GitHub Actions minutes
- **Marketplace**: Browse 10,000+ pre-built actions
- **Starter Workflows**: GitHub provides templates for common scenarios
- **Self-Hosted Runners**: Use your own infrastructure for private needs

## 🔗 Useful Links

- **GitHub Actions Docs**: https://docs.github.com/en/actions
- **Marketplace**: https://github.com/marketplace/actions
- **Pricing**: https://github.com/pricing
- **Status**: https://www.githubstatus.com/

---

**Ready to migrate to GitHub Actions?** Choose your setup method above and enjoy unlimited sustainability analysis! 🌱