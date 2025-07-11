#!/usr/bin/env python3.13
"""
Setup Verification Script for F1 Countdown Bot
Run this script to verify that all components are properly configured.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

def check_file_exists(file_path, description):
    """Check if a file exists."""
    if Path(file_path).exists():
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ {description}: {file_path} (NOT FOUND)")
        return False

def check_env_var(var_name, description, required=True):
    """Check if environment variable is set."""
    value = os.getenv(var_name)
    if value:
        print(f"✅ {description}: Set")
        return True
    else:
        status = "❌ Missing (REQUIRED)" if required else "⚠️ Not set (optional)"
        print(f"{status} {description}")
        return not required

def test_imports():
    """Test if all required packages can be imported."""
    print("\n📦 Testing Python Package Imports:")
    print("-" * 40)
    
    required_packages = [
        ('pandas', 'Pandas'),
        ('tweepy', 'Tweepy'),
        ('fastf1', 'FastF1'),
        ('requests', 'Requests'),
        ('dotenv', 'Python-dotenv'),
        ('pytz', 'Pytz'),
        ('schedule', 'Schedule'),
        ('numpy', 'NumPy')
    ]
    
    all_good = True
    for package, name in required_packages:
        try:
            __import__(package)
            print(f"✅ {name}: Available")
        except ImportError:
            print(f"❌ {name}: Not installed")
            all_good = False
    
    return all_good

def test_discord_webhook(webhook_url, webhook_type):
    """Test Discord webhook."""
    if not webhook_url:
        print(f"⚠️ Discord {webhook_type} webhook: Not configured")
        return False
    
    try:
        import requests
        
        # Simple test payload
        payload = {
            "content": f"🧪 Test message from F1 Bot setup verification ({webhook_type})",
            "embeds": [{
                "title": "Setup Verification Test",
                "description": f"This is a test message for the {webhook_type} webhook",
                "color": 5763719 if webhook_type == "success" else 15158332
            }]
        }
        
        response = requests.post(webhook_url, json=payload, timeout=10)
        
        if response.status_code == 204:
            print(f"✅ Discord {webhook_type} webhook: Working")
            return True
        else:
            print(f"❌ Discord {webhook_type} webhook: Failed ({response.status_code})")
            return False
            
    except Exception as e:
        print(f"❌ Discord {webhook_type} webhook: Error - {e}")
        return False

def main():
    """Main verification function."""
    print("🔍 F1 Countdown Bot - Setup Verification")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Check files
    print("\n📁 Checking Required Files:")
    print("-" * 30)
    files_ok = True
    files_ok &= check_file_exists("config.ini", "Configuration file")
    files_ok &= check_file_exists(".env", "Environment variables file")
    files_ok &= check_file_exists("requirements.txt", "Requirements file")
    files_ok &= check_file_exists("f1_countdown_bot.py", "Main bot script")
    
    # Check environment variables
    print("\n🔑 Checking Environment Variables:")
    print("-" * 35)
    env_ok = True
    env_ok &= check_env_var("TWITTER_CONSUMER_KEY", "Twitter Consumer Key", required=True)
    env_ok &= check_env_var("TWITTER_CONSUMER_SECRET", "Twitter Consumer Secret", required=True)
    env_ok &= check_env_var("TWITTER_ACCESS_TOKEN", "Twitter Access Token", required=True)
    env_ok &= check_env_var("TWITTER_ACCESS_TOKEN_SECRET", "Twitter Access Token Secret", required=True)
    
    discord_error_url = os.getenv("DISCORD_WEBHOOK_URL")
    discord_success_url = os.getenv("DISCORD_SUCCESS_WEBHOOK_URL")
    
    check_env_var("DISCORD_WEBHOOK_URL", "Discord Error Webhook", required=False)
    check_env_var("DISCORD_SUCCESS_WEBHOOK_URL", "Discord Success Webhook", required=False)
    
    # Test package imports
    imports_ok = test_imports()
    
    # Test Discord webhooks
    print("\n🔗 Testing Discord Webhooks:")
    print("-" * 30)
    discord_ok = True
    if discord_error_url:
        discord_ok &= test_discord_webhook(discord_error_url, "error")
    if discord_success_url:
        discord_ok &= test_discord_webhook(discord_success_url, "success")
    
    if not discord_error_url and not discord_success_url:
        print("⚠️ No Discord webhooks configured (optional)")
    
    # Final summary
    print("\n" + "=" * 50)
    print("📋 SETUP VERIFICATION SUMMARY")
    print("=" * 50)
    
    if files_ok:
        print("✅ Files: All required files found")
    else:
        print("❌ Files: Some files missing")
    
    if env_ok:
        print("✅ Twitter API: All credentials configured")
    else:
        print("❌ Twitter API: Missing credentials")
    
    if imports_ok:
        print("✅ Dependencies: All packages installed")
    else:
        print("❌ Dependencies: Some packages missing")
    
    if discord_error_url or discord_success_url:
        if discord_ok:
            print("✅ Discord: Webhooks working")
        else:
            print("❌ Discord: Webhook issues")
    else:
        print("⚠️ Discord: Not configured (optional)")
    
    print("\n🎯 NEXT STEPS:")
    print("-" * 15)
    
    if not files_ok:
        print("1. Create missing files (see README.md setup guide)")
    
    if not env_ok:
        print("2. Add Twitter API credentials to .env file")
    
    if not imports_ok:
        print("3. Install missing packages: pip install -r requirements.txt")
    
    if not discord_ok and (discord_error_url or discord_success_url):
        print("4. Fix Discord webhook configuration")
    
    if files_ok and env_ok and imports_ok:
        print("🎉 Setup looks good! Ready to test:")
        print("   python f1_countdown_bot.py --debug")
        print("   python test_discord.py")
        
        if not discord_error_url and not discord_success_url:
            print("\n💡 Consider adding Discord webhooks for notifications:")
            print("   - Add DISCORD_WEBHOOK_URL to .env file")
            print("   - Add DISCORD_SUCCESS_WEBHOOK_URL to .env file")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    main() 