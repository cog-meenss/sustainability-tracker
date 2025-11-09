# How to View Visual Reports in GitHub Actions

## **Step 1: Trigger Your First Analysis**

### Option A: Manual Trigger (Recommended for First Run)
1. **Go to**: https://github.com/cog-meenss/sustainability-tracker/actions
2. **Click**: "Sustainability Analysis" workflow (left sidebar)
3. **Click**: "Run workflow" button (blue button on the right)
4. **Select**: "Branch: main" 
5. **Click**: "Run workflow" (green button)

### Option B: Automatic Trigger
```bash
# Make a small change and push to trigger analysis
echo "# Test trigger" >> test-trigger.md
git add test-trigger.md
git commit -m "🧪 Trigger sustainability analysis"
git push github main
```

## **Step 2: View Real-Time Execution**

After triggering, you'll see:
- ⏳ **Yellow dot**: Workflow is running
- **Green checkmark**: Workflow completed successfully 
- **Red X**: Workflow failed (check logs)

**Click on the workflow run** to see detailed execution.

## **Step 3: Access Visual Reports**

### A. Job Summary (GitHub UI Integration)
1. **Click** on the completed workflow run
2. **Scroll down** to see the **Job Summary** section
3. **View**:
 - Overall sustainability score
 - Detailed metrics table
 - Quality gate status
 - File analysis breakdown
 - Key recommendations

### B. Interactive Dashboard (Downloadable)
1. **Scroll down** to **"Artifacts"** section
2. **Click**: "sustainability-dashboard" 
3. **Download** the ZIP file
4. **Extract** and open `dashboard.html` in your browser
5. **View**: Interactive Chart.js radar charts and visualizations

### C. Detailed Reports (Downloadable)
1. **Click**: "sustainability-reports" artifact
2. **Download** and extract ZIP file
3. **Files included**:
 - `analysis.json` - Complete raw data
 - `dashboard.html` - Interactive visual dashboard
 - `summary.txt` - Text-based summary

## **Visual Report Features**

### Interactive Dashboard Includes:
- **Radar Chart**: Multi-dimensional sustainability metrics
- **Score Cards**: Color-coded performance indicators
- **File Breakdown**: Analysis by file type and count
- **Recommendations List**: Actionable improvement suggestions
- 🎨 **Professional Styling**: Responsive design with gradients and animations

### Job Summary Shows:
- **Overall Score**: X/100 with visual status
- **Metrics Table**: Energy, Resource, Carbon scores
- **Quality Gate**: Pass/Fail with threshold
- **Project Stats**: File counts by type
- **Top 3 Recommendations**: Key improvement areas

## **Step 4: Understanding the Analysis**

### Sustainability Scores:
- **90-100**: **Excellent** (Green)
- **75-89**: **Good** (Yellow) 
- **60-74**: **Needs Attention** (Orange)
- **<60**: **Poor** (Red)

### Key Metrics:
- **Energy Efficiency**: Code patterns that minimize computational overhead
- **Resource Utilization**: Memory and storage optimization
- **Carbon Footprint**: Environmental impact (lower is better)
- **Overall Score**: Weighted combination of all metrics

## **Step 5: Acting on Recommendations**

Common recommendations include:
- **Optimize JavaScript/TypeScript** files for better energy efficiency
- **Review Python code** for resource optimization
- **Implement code splitting** for large applications
- **Apply sustainable coding practices** across the project

## **Pro Tips for Best Results**

### 1. Enable GitHub Pages (Optional)
```bash
# Create a simple index.html that redirects to latest dashboard
echo '<meta http-equiv="refresh" content="0; url=./dashboard.html">' > docs/index.html
git add docs/index.html
git commit -m "Add GitHub Pages redirect"
git push github main
```

Then enable GitHub Pages in repository settings → Pages → Deploy from branch → `/docs`

### 2. Add Status Badges to README
Your README already includes status badges that will show:
- ![Sustainability Analysis](https://github.com/cog-meenss/sustainability-tracker/workflows/%20Sustainability%20Analysis/badge.svg)

### 3. Set Up Notifications
In repository settings → Notifications, enable:
- **Actions**: Get notified when workflows complete
- **Pull requests**: Automatic analysis comments

## 🔗 **Quick Access Links**

- **Actions Dashboard**: https://github.com/cog-meenss/sustainability-tracker/actions
- **Latest Run**: https://github.com/cog-meenss/sustainability-tracker/actions/workflows/sustainability-analysis.yml
- **Repository Settings**: https://github.com/cog-meenss/sustainability-tracker/settings

## **Next Steps**

1. **Trigger your first run** using Option A above
2. **Download the dashboard** from artifacts
3. **Review recommendations** and implement improvements
4. **Make changes** and watch scores improve over time
5. **Set up regular monitoring** with weekly scheduled runs

---

**Ready to see your first sustainability report?** Follow Step 1 above to trigger the analysis! 