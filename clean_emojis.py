#!/usr/bin/env python3
"""
Clean up emoji icons from sustainability analyzer files
"""

import re
from pathlib import Path

def clean_emojis_from_file(file_path):
    """Remove emoji icons from a file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Common emoji patterns to remove
    emoji_patterns = [
        r'🌱\s*',  # plant
        r'📊\s*',  # bar chart  
        r'✅\s*',  # check mark
        r'❌\s*',  # cross mark
        r'🔧\s*',  # wrench
        r'🎯\s*',  # target
        r'💡\s*',  # light bulb
        r'🚀\s*',  # rocket
        r'📄\s*',  # document
        r'🎉\s*',  # party
        r'⚠️\s*',  # warning
        r'📈\s*',  # trending up
        r'🔍\s*',  # magnifying glass
        r'📁\s*',  # folder
        r'💾\s*',  # floppy disk
        r'⚡\s*',  # lightning
        r'🔥\s*',  # fire
        r'🐍\s*',  # snake
        r'📦\s*',  # package
        r'📢\s*',  # megaphone
        r'🚨\s*',  # alarm
        r'🌍\s*',  # globe
        r'♻️\s*',  # recycling
        r'⏱️\s*',  # timer
        r'🌿\s*',  # herb
    ]
    
    original_content = content
    
    for pattern in emoji_patterns:
        content = re.sub(pattern, '', content)
    
    # Clean up double spaces that might result from emoji removal
    content = re.sub(r'  +', ' ', content)
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Cleaned emojis from: {file_path}")
        return True
    return False

def main():
    """Clean up emojis from all sustainability analyzer files"""
    project_root = Path('/Users/159645/Meena/Projects/vibe-coding/Tracker')
    
    # Files to clean (excluding frontend/backend)
    files_to_clean = [
        '.github/workflows/sustainability-analysis.yml',
        'sustainability-analyzer/README.md',
        'sustainability-analyzer/analyzer/sustainability_analyzer.py',
        'sustainability-analyzer/reports/html_generator.py',
        'sustainability-analyzer/reports/azure_publisher.py',
        'HOW_TO_VIEW_REPORTS.md',
        'DEPENDENCY_FIX_SUMMARY.md',
        'GITHUB_ACTIONS_SETUP.md',
        'CLEANUP_SUMMARY.md',
        'azure-pipelines.yml',
        'docs/README.md'
    ]
    
    cleaned_count = 0
    
    for file_path in files_to_clean:
        full_path = project_root / file_path
        if full_path.exists():
            if clean_emojis_from_file(full_path):
                cleaned_count += 1
        else:
            print(f"File not found: {full_path}")
    
    print(f"\nCleaned {cleaned_count} files")

if __name__ == "__main__":
    main()