#!/usr/bin/env python3
"""
🧪 Test script to verify sustainability analyzer dependencies work correctly
"""

import sys
import importlib
import subprocess

def test_dependency(package_name, import_name=None):
    """Test if a package can be imported successfully"""
    if import_name is None:
        import_name = package_name
    
    try:
        module = importlib.import_module(import_name)
        version = getattr(module, '__version__', 'unknown')
        print(f"✅ {package_name}: {version}")
        return True
    except ImportError as e:
        print(f"❌ {package_name}: {e}")
        return False

def main():
    print("🌱 Testing Sustainability Analyzer Dependencies")
    print("=" * 50)
    
    # Core dependencies from requirements.txt
    dependencies = [
        ('pyyaml', 'yaml'),
        ('requests', 'requests'),
        ('jinja2', 'jinja2'),
        ('matplotlib', 'matplotlib'),
        ('seaborn', 'seaborn'),
        ('plotly', 'plotly'),
        ('pandas', 'pandas'),
        ('numpy', 'numpy'),
        ('gitpython', 'git'),
        ('chardet', 'chardet'),
        ('toml', 'toml'),
        ('colorama', 'colorama'),
        ('psutil', 'psutil'),
    ]
    
    print(f"Python Version: {sys.version}")
    print("-" * 50)
    
    success_count = 0
    for package, import_name in dependencies:
        if test_dependency(package, import_name):
            success_count += 1
    
    print("-" * 50)
    print(f"✅ {success_count}/{len(dependencies)} dependencies working")
    
    if success_count == len(dependencies):
        print("🎉 All dependencies are working correctly!")
        return 0
    else:
        print("⚠️  Some dependencies are missing. Install with:")
        print("pip install -r sustainability-analyzer/requirements.txt")
        return 1

if __name__ == "__main__":
    sys.exit(main())