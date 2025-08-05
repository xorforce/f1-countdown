#!/usr/bin/env python3
"""
Script to help with git-filter-repo to remove sensitive data.
This script identifies all the sensitive patterns that need to be removed.
"""

import re

# All the sensitive patterns we found
SENSITIVE_PATTERNS = [
    ***REMOVED***
    r'6fkqzIOINvOvkAnYOgdSeQePd',
    r'Oru2Y8hKx0zERCz1o8KMfI9e6MlywBtBEKZrWnYFkIIefXiXm5',
    r'1945769838070337536-43EDh8RLsDp511SFLCTkisQQZBNNFt',
    r'Opn8VWOY2gvt92Y05Uu1o9ZTyjyA3T0llZhoofnGmeFSP',
    
    ***REMOVED***
    r'1393343102642684005',
    r'WJ4VLmQJlwKgV4gEFygYSDIMf-GdIJqsA5O4OhzPbpwrOoYC4alyMHTx-3H3_LPc0T_7',
    r'1393347157171507350',
    r'2hSms-MqF2_yzpnNhEbFJbFse6JP2-TpsTV0h0ywDGgAjUwaXa9iiwTVzroBQ_WgF4zC',
    
    ***REMOVED***
    r'1945769838070337536',
    r'43EDh8RLsDp511SFLCTkisQQZBNNFt',
]

def create_filter_repo_commands():
    """Create the git-filter-repo commands to remove sensitive data."""
    
    print("🔍 Creating git-filter-repo commands to remove sensitive data...")
    print()
    
    # Create the main filter command
    filter_command = "git filter-repo --force"
    
    # Add pattern replacements for each sensitive pattern
    for i, pattern in enumerate(SENSITIVE_PATTERNS):
        filter_command += f' --replace-text <(echo "{pattern}=[REMOVED]")'
    
    print("📋 Use this command to remove sensitive data:")
    print("=" * 80)
    print(filter_command)
    print("=" * 80)
    print()
    
    print("⚠️  WARNING: This will rewrite your entire Git history!")
    print("⚠️  Make sure you have a backup before proceeding.")
    print("⚠️  All collaborators will need to re-clone the repository.")
    print()
    
    print("📝 Alternative approach - Remove specific files from history:")
    print("=" * 80)
    print("git filter-repo --force --path config.ini --invert-paths")
    print("git filter-repo --force --path .env --invert-paths")
    print("git filter-repo --force --path f1_countdown_bot.log --invert-paths")
    print("=" * 80)

if __name__ == "__main__":
    create_filter_repo_commands() 