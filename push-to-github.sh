#!/bin/bash

echo "📤 Pushing Sustainability Tracker to GitHub..."

# Check if github remote exists
if ! git remote | grep -q "^github$"; then
    echo "❌ GitHub remote not found. Please run ./setup-github.sh first"
    exit 1
fi

# Make sure we're on main branch
echo "🌿 Switching to main branch..."
git checkout main 2>/dev/null || git checkout -b main

# Add any uncommitted changes
echo "📝 Adding any uncommitted files..."
git add .

# Check if there are changes to commit
if ! git diff --staged --quiet; then
    echo "💾 Committing latest changes..."
    git commit -m "📦 Final update before GitHub migration

- All sustainability analysis components ready
- GitHub Actions workflows configured  
- Azure DevOps pipeline available as backup
- Ready for production deployment"
fi

# Push to GitHub
echo "🚀 Pushing to GitHub..."
git push github main

echo ""
echo "✅ Successfully pushed to GitHub!"
echo ""
echo "🎯 Your GitHub Actions are now available at:"
echo "   https://github.com/$(git remote get-url github | sed 's|https://github.com/||' | sed 's|\.git||')/actions"
echo ""
echo "🔥 Next steps:"
echo "1. Visit your repository on GitHub"
echo "2. Go to the 'Actions' tab"
echo "3. Click 'I understand my workflows, go ahead and enable them'"
echo "4. Trigger your first run by making a small change and pushing"
echo ""
echo "📊 Available workflows:"
echo "   • Full Sustainability Analysis (comprehensive reporting)"
echo "   • Simple Sustainability Check (quick validation)"