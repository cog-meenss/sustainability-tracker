# 🌱 Sustainability Pipeline

This project uses an automated sustainability analysis pipeline to monitor and improve code quality, energy efficiency, and environmental impact.

## 📊 Dashboard

Visit [https://tracker.github.io/](https://tracker.github.io/) to view the sustainability dashboard.

## 🎯 Current Thresholds

- **Sustainability Score**: 60/100 (minimum)
- **Energy Efficiency**: 50/100 (minimum)
- **Code Quality**: 70/100 (target)
- **Security Score**: 75/100 (target)

## 🔧 Configuration

The pipeline is configured via `.sustainability/config.yml`. Key settings:

- **Project Type**: mixed
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
```bash
python3 sustainability_evaluator.py --path . --format both --output reports/
```

## 🔧 Customization

### Adjust Thresholds
Edit `.sustainability/config.yml` to modify score requirements:

```yaml
thresholds:
  sustainability_score: 70  # Increase for stricter requirements
```

### Exclude Files
Add patterns to `.sustainability/ignore`:

```
legacy/
vendor/
*.min.js
```

### Enable Notifications
Add `SLACK_WEBHOOK_URL` repository secret and set:

```yaml
notifications:
  slack: true
```

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
2. Check that the workflow has `pages: write` permissions
3. Verify the deployment step completed successfully

### Customize Analysis
1. Modify `.sustainability/config.yml` for project-specific settings
2. Add custom exclusion patterns in `.sustainability/ignore`
3. Adjust workflow triggers in `.github/workflows/sustainability.yml`

## 📞 Support

- 📖 [Full Documentation](https://github.com/cog-meenss/sustainability-tracker/blob/main/reusability-templates/cross-project-reusability-guide.md)
- 🐛 [Report Issues](https://github.com/cog-meenss/sustainability-tracker/issues)
- 💬 [Discussions](https://github.com/cog-meenss/sustainability-tracker/discussions)

---
*🌱 Powered by Reusable Sustainability Pipeline*
