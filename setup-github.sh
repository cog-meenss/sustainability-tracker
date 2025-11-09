#!/bin/bash

echo "🚀 Setting up GitHub repository for Sustainability Tracker..."

# Get GitHub username
read -p "Enter your GitHub username: " GITHUB_USERNAME

if [ -z "$GITHUB_USERNAME" ]; then
    echo "❌ GitHub username is required"
    exit 1
fi

echo "📝 Setting up repository: $GITHUB_USERNAME/sustainability-tracker"

# Add GitHub remote
echo "🔗 Adding GitHub remote..."
git remote add github https://github.com/$GITHUB_USERNAME/sustainability-tracker.git

# Show remotes
echo "📋 Current remotes:"
git remote -v

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 Next steps:"
echo "1. Make sure you created the GitHub repository: https://github.com/$GITHUB_USERNAME/sustainability-tracker"
echo "2. Run: ./push-to-github.sh"
echo ""
echo "📊 After pushing, your GitHub Actions will be available at:"
echo "   https://github.com/$GITHUB_USERNAME/sustainability-tracker/actions"