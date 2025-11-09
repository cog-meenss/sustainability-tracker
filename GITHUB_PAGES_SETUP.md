# GitHub Pages Configuration for Sustainability Reports

This repository is configured to automatically publish sustainability analysis reports to GitHub Pages.

## 🌐 Live Dashboard Access

**Direct URL:** `https://USERNAME.github.io/REPO-NAME/`

### What's Published

**Automatic Updates:**
- 📊 **Interactive HTML Dashboard** - Latest sustainability analysis with real-time metrics
- 📋 **JSON Data Reports** - Raw analysis data for programmatic access  
- 🎯 **Navigation Index** - Easy access to all generated reports
- 📈 **Statistics Summary** - Key metrics and scores overview

### Setup Instructions

**1. Enable GitHub Pages**
- Go to Repository Settings → Pages
- Source: "GitHub Actions" 
- Branch: Leave as default (managed by workflow)

**2. Verify Deployment**
- Check Actions tab after next commit
- Look for "Deploy to GitHub Pages" step
- URL will be: `https://[username].github.io/[repo-name]/`

**3. Access Reports**
- Main dashboard: `https://[username].github.io/[repo-name]/`
- Direct report: `https://[username].github.io/[repo-name]/sustainability-report-{commit}-{timestamp}.html`

### Features

**Live Dashboard:**
- 🎨 Professional interface with navigation
- 📊 Real-time sustainability metrics
- 🌱 Green coding analysis with file-specific issues
- 💡 Actionable recommendations with energy impact
- 📈 Interactive charts and progress indicators
- 🔄 Auto-refresh controls for runtime updates

**No Download Required:**
- ✅ View reports directly in browser
- ✅ Share links with team members
- ✅ Bookmark for quick access
- ✅ Mobile-responsive design

### Automatic Updates

Reports are automatically published on every commit to `main` branch:
1. Workflow runs sustainability analysis
2. Generates HTML dashboard and JSON data
3. Creates navigation index page
4. Deploys to GitHub Pages
5. Updates live dashboard with latest metrics

### Security

- Reports contain only code analysis metrics
- No sensitive data or credentials exposed
- Public visibility matches repository visibility
- Can be made private by changing repository settings

---

**Next Steps:**
1. Enable GitHub Pages in repository settings
2. Make a commit to trigger workflow
3. Access live dashboard at your GitHub Pages URL
4. Share the link with your team! 🌱✨