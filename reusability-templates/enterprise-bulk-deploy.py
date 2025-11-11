#!/usr/bin/env python3
"""
🏢 Enterprise Bulk Sustainability Pipeline Deployment
Deploy sustainability analysis across entire GitHub organizations

Usage:
    python3 enterprise-bulk-deploy.py your-org --template enterprise --workers 5
    python3 enterprise-bulk-deploy.py startup-co --template mixed --workers 10
"""

import subprocess
import json
import sys
import os
import argparse
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import requests

class EnterpriseDeployer:
    def __init__(self, organization, template_type="enterprise", dry_run=False):
        self.org = organization
        self.template = template_type
        self.dry_run = dry_run
        self.deployed = []
        self.failed = []
        self.skipped = []
        self.start_time = time.time()
        
        # Template repository settings
        self.template_repo = "cog-meenss/sustainability-tracker"
        self.deploy_script_url = f"https://raw.githubusercontent.com/{self.template_repo}/main/reusability-templates/deploy-sustainability.sh"
        
    def get_repositories(self, include_private=True, include_archived=False):
        """Get all repositories in the organization"""
        try:
            cmd = ["gh", "repo", "list", self.org, "--json", "name,primaryLanguage,isPrivate,isArchived,updatedAt", "--limit", "1000"]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            repos = json.loads(result.stdout)
            
            # Filter repositories
            filtered_repos = []
            for repo in repos:
                # Skip archived unless explicitly included
                if repo.get('isArchived', False) and not include_archived:
                    continue
                    
                # Skip private unless explicitly included  
                if repo.get('isPrivate', False) and not include_private:
                    continue
                    
                filtered_repos.append(repo)
            
            return filtered_repos
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to get repositories: {e}")
            return []
    
    def detect_project_type(self, repo_info):
        """Map GitHub language to our project types"""
        primary_language = repo_info.get('primaryLanguage')
        
        language_map = {
            'Python': 'python',
            'JavaScript': 'javascript',
            'TypeScript': 'javascript',
            'Java': 'java',
            'Go': 'go',
            'C#': 'dotnet',
            'PHP': 'php',
            'Ruby': 'ruby',
            'Rust': 'rust',
            'C++': 'cpp',
            'C': 'c'
        }
        
        detected_type = language_map.get(primary_language, 'mixed')
        
        # Override with template type if specified
        if self.template != 'auto':
            return self.template
            
        return detected_type
    
    def check_existing_sustainability_pipeline(self, repo_name):
        """Check if repository already has sustainability pipeline"""
        try:
            # Check for existing workflow
            cmd = ["gh", "api", f"repos/{self.org}/{repo_name}/contents/.github/workflows/sustainability.yml"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False
    
    def deploy_to_repository(self, repo_info):
        """Deploy sustainability pipeline to a single repository"""
        repo_name = repo_info['name']
        project_type = self.detect_project_type(repo_info)
        
        print(f"🚀 [{repo_name}] Starting deployment (type: {project_type})...")
        
        # Check if already deployed
        if self.check_existing_sustainability_pipeline(repo_name):
            print(f"⚠️  [{repo_name}] Already has sustainability pipeline - skipping")
            self.skipped.append(repo_name)
            return
        
        if self.dry_run:
            print(f"🔍 [DRY RUN] Would deploy {project_type} template to {repo_name}")
            self.deployed.append(repo_name)
            return
        
        temp_dir = f"temp-{repo_name}-{int(time.time())}"
        
        try:
            # Clone repository
            print(f"📥 [{repo_name}] Cloning repository...")
            subprocess.run(["gh", "repo", "clone", f"{self.org}/{repo_name}", temp_dir], 
                         check=True, capture_output=True, cwd="/tmp")
            
            repo_path = f"/tmp/{temp_dir}"
            
            # Download deployment script
            print(f"📦 [{repo_name}] Downloading deployment script...")
            script_path = f"{repo_path}/deploy-sustainability.sh"
            response = requests.get(self.deploy_script_url)
            response.raise_for_status()
            
            with open(script_path, 'w') as f:
                f.write(response.text)
            os.chmod(script_path, 0o755)
            
            # Run deployment script
            print(f"⚙️  [{repo_name}] Running sustainability deployment...")
            deploy_cmd = ["./deploy-sustainability.sh", project_type, repo_name]
            result = subprocess.run(deploy_cmd, cwd=repo_path, check=True, 
                                  capture_output=True, text=True)
            
            # Commit changes
            print(f"💾 [{repo_name}] Committing changes...")
            subprocess.run(["git", "add", "."], cwd=repo_path, check=True)
            
            commit_msg = f"🌱 Add sustainability pipeline ({project_type} template)\n\n- Automated deployment via enterprise bulk script\n- Template: {project_type}\n- Deployed: {datetime.now().isoformat()}"
            
            subprocess.run(["git", "commit", "-m", commit_msg], 
                         cwd=repo_path, check=True)
            
            # Push changes
            print(f"🚀 [{repo_name}] Pushing changes...")
            subprocess.run(["git", "push"], cwd=repo_path, check=True)
            
            # Configure repository settings
            print(f"⚙️  [{repo_name}] Configuring repository settings...")
            self.configure_repository_settings(repo_name)
            
            # Cleanup
            subprocess.run(["rm", "-rf", repo_path], check=True)
            
            self.deployed.append(repo_name)
            print(f"✅ [{repo_name}] Deployment completed successfully!")
            
        except Exception as e:
            error_msg = str(e)
            # Try to get more specific error from subprocess
            if hasattr(e, 'stderr') and e.stderr:
                error_msg = e.stderr.decode() if isinstance(e.stderr, bytes) else str(e.stderr)
            
            self.failed.append((repo_name, error_msg))
            print(f"❌ [{repo_name}] Deployment failed: {error_msg}")
            
            # Cleanup on failure
            try:
                subprocess.run(["rm", "-rf", f"/tmp/{temp_dir}"], check=False)
            except:
                pass
    
    def configure_repository_settings(self, repo_name):
        """Configure repository settings for sustainability pipeline"""
        try:
            # Enable GitHub Pages (source: GitHub Actions)
            pages_config = {
                "source": {
                    "branch": "gh-pages",
                    "path": "/"
                }
            }
            
            subprocess.run([
                "gh", "api", f"repos/{self.org}/{repo_name}/pages", 
                "-X", "POST", "--field", f"source={json.dumps(pages_config['source'])}"
            ], check=False, capture_output=True)  # Don't fail if pages already exists
            
            # Enable vulnerability alerts
            subprocess.run([
                "gh", "api", f"repos/{self.org}/{repo_name}/vulnerability-alerts",
                "-X", "PUT"
            ], check=False, capture_output=True)
            
            # Enable dependency graph
            subprocess.run([
                "gh", "api", f"repos/{self.org}/{repo_name}",
                "-X", "PATCH", 
                "-f", "has_vulnerability_alerts=true",
                "-f", "has_automated_security_fixes=true"
            ], check=False, capture_output=True)
            
            print(f"⚙️  [{repo_name}] Repository settings configured")
            
        except subprocess.CalledProcessError as e:
            print(f"⚠️  [{repo_name}] Could not configure all settings: {e}")
    
    def bulk_deploy(self, max_workers=5, include_private=True, include_archived=False):
        """Deploy to all repositories in parallel"""
        print(f"🔍 Discovering repositories in {self.org}...")
        repos = self.get_repositories(include_private, include_archived)
        
        if not repos:
            print("❌ No repositories found or access denied")
            return
            
        print(f"📊 Found {len(repos)} repositories in {self.org}")
        
        if self.dry_run:
            print(f"🔍 DRY RUN MODE - No changes will be made")
        
        print(f"🚀 Starting bulk deployment with {max_workers} parallel workers...")
        print(f"📝 Template: {self.template}")
        print("")
        
        # Deploy in parallel
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all jobs
            future_to_repo = {
                executor.submit(self.deploy_to_repository, repo): repo['name'] 
                for repo in repos
            }
            
            # Process completed jobs
            for future in as_completed(future_to_repo):
                repo_name = future_to_repo[future]
                try:
                    future.result()
                except Exception as exc:
                    print(f"❌ [{repo_name}] Exception during deployment: {exc}")
        
        # Generate summary report
        self.generate_summary_report()
    
    def generate_summary_report(self):
        """Generate and display deployment summary"""
        total_time = time.time() - self.start_time
        total_repos = len(self.deployed) + len(self.failed) + len(self.skipped)
        
        print(f"\n" + "="*60)
        print(f"🏢 ENTERPRISE DEPLOYMENT SUMMARY")
        print(f"="*60)
        print(f"⏱️  Total time: {total_time:.1f} seconds")
        print(f"📊 Total repositories: {total_repos}")
        print(f"✅ Successfully deployed: {len(self.deployed)}")
        print(f"❌ Failed deployments: {len(self.failed)}")
        print(f"⚠️  Skipped (already deployed): {len(self.skipped)}")
        print(f"📈 Success rate: {(len(self.deployed)/total_repos*100):.1f}%" if total_repos > 0 else "N/A")
        
        if self.deployed:
            print(f"\n✅ SUCCESSFUL DEPLOYMENTS ({len(self.deployed)}):")
            for i, repo in enumerate(self.deployed, 1):
                dashboard_url = f"https://{self.org.lower()}.github.io/{repo}/"
                print(f"   {i:2d}. {repo}")
                print(f"       🌐 Dashboard: {dashboard_url}")
                
        if self.skipped:
            print(f"\n⚠️  SKIPPED REPOSITORIES ({len(self.skipped)}):")
            for i, repo in enumerate(self.skipped, 1):
                print(f"   {i:2d}. {repo} (already has sustainability pipeline)")
                
        if self.failed:
            print(f"\n❌ FAILED DEPLOYMENTS ({len(self.failed)}):")
            for i, (repo, error) in enumerate(self.failed, 1):
                print(f"   {i:2d}. {repo}")
                print(f"       Error: {error[:100]}{'...' if len(error) > 100 else ''}")
        
        # Next steps
        print(f"\n🎯 NEXT STEPS:")
        if self.deployed:
            print(f"   1. Visit repository GitHub Pages to view sustainability dashboards")
            print(f"   2. Review initial analysis results and adjust thresholds if needed")
            print(f"   3. Set up organization-wide Slack notifications (optional)")
            print(f"   4. Schedule regular sustainability reviews with development teams")
            
        print(f"\n🌐 Organization Dashboard:")
        print(f"   Generate with: python3 generate-org-dashboard.py --org {self.org}")
        print(f"\n🌱 Happy sustainable coding!")

def verify_prerequisites():
    """Verify required tools are installed and authenticated"""
    # Check GitHub CLI
    try:
        subprocess.run(["gh", "auth", "status"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ GitHub CLI not authenticated. Please run: gh auth login")
        sys.exit(1)
    
    # Check git
    try:
        subprocess.run(["git", "--version"], check=True, capture_output=True)
    except FileNotFoundError:
        print("❌ Git not found. Please install git.")
        sys.exit(1)
    
    # Check python requests module
    try:
        import requests
    except ImportError:
        print("❌ Python requests module not found. Please run: pip install requests")
        sys.exit(1)
    
    print("✅ Prerequisites verified")

def main():
    parser = argparse.ArgumentParser(
        description='Deploy sustainability pipeline across GitHub organization',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Deploy enterprise template to all repositories
    python3 enterprise-bulk-deploy.py your-company --template enterprise
    
    # Deploy with auto-detection and 10 parallel workers
    python3 enterprise-bulk-deploy.py startup-co --template auto --workers 10
    
    # Dry run to see what would be deployed
    python3 enterprise-bulk-deploy.py test-org --dry-run
    
    # Deploy only to public repositories
    python3 enterprise-bulk-deploy.py open-source-org --no-private
        """
    )
    
    parser.add_argument('organization', help='GitHub organization name')
    parser.add_argument('--template', default='enterprise', 
                       choices=['auto', 'python', 'javascript', 'enterprise', 'mixed', 'microservice', 'library'],
                       help='Template type to deploy (auto = detect from language)')
    parser.add_argument('--workers', type=int, default=5, 
                       help='Number of parallel deployment workers (default: 5)')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be deployed without making changes')
    parser.add_argument('--no-private', action='store_true',
                       help='Exclude private repositories')
    parser.add_argument('--include-archived', action='store_true',
                       help='Include archived repositories')
    
    args = parser.parse_args()
    
    print("🏢 Enterprise Sustainability Pipeline Bulk Deployment")
    print("="*55)
    
    # Verify prerequisites
    verify_prerequisites()
    
    # Confirm deployment
    if not args.dry_run:
        response = input(f"\n⚠️  This will deploy sustainability pipelines to ALL repositories in '{args.organization}'.\nContinue? (y/N): ")
        if response.lower() not in ['y', 'yes']:
            print("❌ Deployment cancelled")
            sys.exit(0)
    
    # Initialize deployer
    deployer = EnterpriseDeployer(
        organization=args.organization,
        template_type=args.template,
        dry_run=args.dry_run
    )
    
    # Run bulk deployment
    deployer.bulk_deploy(
        max_workers=args.workers,
        include_private=not args.no_private,
        include_archived=args.include_archived
    )

if __name__ == "__main__":
    main()