# 🔧 GitHub Pages Troubleshooting Guide

## Current Issue
GitHub Pages URL https://cog-meenss.github.io/sustainability-tracker/ is not accessible even though:
- ✅ Repository exists: https://github.com/cog-meenss/sustainability-tracker
- ✅ Workflow has Pages deployment configured
- ✅ Proper permissions are set

## Quick Fixes

### 1. Enable GitHub Pages in Repository Settings
1. Go to: https://github.com/cog-meenss/sustainability-tracker/settings/pages
2. Under "Source" section:
   - Select **"GitHub Actions"** (not "Deploy from branch")
   - This allows the workflow to deploy Pages automatically

### 2. Check Workflow Permissions
Ensure the workflow has proper permissions (already configured in workflow file):
```yaml
permissions:
  contents: write
  pages: write
  id-token: write
  actions: read
  deployments: write
```

### 3. Trigger Manual Deployment
If Pages still doesn't work, trigger the workflow manually:

1. Go to: https://github.com/cog-meenss/sustainability-tracker/actions/workflows/sustainability-auto-report.yml
2. Click **"Run workflow"** 
3. Select branch: `main`
4. Click **"Run workflow"** button

### 4. Check Pages Deployment Status
Monitor deployment at:
- Actions tab: https://github.com/cog-meenss/sustainability-tracker/actions
- Pages tab: https://github.com/cog-meenss/sustainability-tracker/deployments

### 5. Alternative: Manual Pages Setup

If automated deployment fails, you can set up Pages manually:

```bash
# Create a gh-pages branch with reports
git checkout --orphan gh-pages
git rm -rf .
cp sustainability-reports/*.html ./
cp sustainability-reports/*.json ./
git add .
git commit -m "🌐 Setup GitHub Pages with sustainability reports"
git push origin gh-pages
```

Then in repository settings, select "Deploy from branch" and choose `gh-pages`.

## Expected URLs After Fix
- **Main Dashboard:** https://cog-meenss.github.io/sustainability-tracker/
- **Direct Report:** https://cog-meenss.github.io/sustainability-tracker/sustainability-report-[commit]-[timestamp].html

## Verification Steps
1. Check if Pages is enabled: Repository Settings → Pages
2. Verify workflow runs successfully: Actions tab
3. Confirm deployment: Deployments/Environments tab
4. Test URL: https://cog-meenss.github.io/sustainability-tracker/

## Common Issues
- **Pages not enabled:** Go to repository settings and enable GitHub Pages
- **Wrong source:** Should be "GitHub Actions", not "Deploy from branch"
- **Permissions:** Ensure workflow has `pages: write` permission
- **Branch protection:** Make sure `main` branch allows Actions to run

## Quick Test
Run this command locally to verify reports exist:
```bash
ls sustainability-reports/*.html
```

If reports exist locally but Pages doesn't work, the issue is GitHub Pages configuration, not report generation.