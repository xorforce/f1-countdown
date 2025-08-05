#!/usr/bin/env python3.13
"""
Helper script to set up Discord webhook URLs in .env file.
This script prompts users to input their own Discord webhook URLs.
"""

import os
from pathlib import Path

def get_webhook_url(webhook_type: str) -> str:
    """Prompt user for webhook URL."""
    print(f"\n📝 {webhook_type} Webhook Setup:")
    print(f"1. Go to your Discord server")
    print(f"2. Right-click on a channel → Edit Channel")
    print(f"3. Go to Integrations → Webhooks")
    print(f"4. Create New Webhook or use existing one")
    print(f"5. Copy the webhook URL")
    
    while True:
        webhook_url = input(f"\nEnter your {webhook_type.lower()} webhook URL (or press Enter to skip): ").strip()
        
        if not webhook_url:
            print(f"⏭️  Skipping {webhook_type.lower()} webhook setup")
            return ""
        
        if webhook_url.startswith("https://discord.com/api/webhooks/"):
            return webhook_url
        else:
            print("❌ Invalid webhook URL format. Please enter a valid Discord webhook URL.")
            print("Example: https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN")

def setup_discord_webhooks():
    """Set up Discord webhook URLs in .env file."""
    env_file = Path(".env")

    # Read existing .env file if it exists
    env_content = ""
    if env_file.exists():
        with open(env_file, 'r', encoding='utf-8') as f:
            env_content = f.read()

    # Check if Discord webhook URLs are already set
    lines = env_content.split('\n')
    new_lines = []

    discord_webhook_set = False
    discord_success_webhook_set = False

    # Get webhook URLs from user
    error_webhook_url = get_webhook_url("Error")
    success_webhook_url = get_webhook_url("Success")

    for line in lines:
        if line.startswith('DISCORD_WEBHOOK_URL='):
            if error_webhook_url:
                new_lines.append(f'DISCORD_WEBHOOK_URL={error_webhook_url}')
                discord_webhook_set = True
                print("✅ Updated DISCORD_WEBHOOK_URL for error notifications")
            else:
                new_lines.append(line)  # Keep existing if user skipped
        elif line.startswith('DISCORD_SUCCESS_WEBHOOK_URL='):
            if success_webhook_url:
                new_lines.append(f'DISCORD_SUCCESS_WEBHOOK_URL={success_webhook_url}')
                discord_success_webhook_set = True
                print("✅ Updated DISCORD_SUCCESS_WEBHOOK_URL for success notifications")
            else:
                new_lines.append(line)  # Keep existing if user skipped
        else:
            new_lines.append(line)

    # Add webhook URLs if they weren't found and user provided them
    if not discord_webhook_set and error_webhook_url:
        new_lines.append(f'DISCORD_WEBHOOK_URL={error_webhook_url}')
        print("✅ Added DISCORD_WEBHOOK_URL for error notifications")

    if not discord_success_webhook_set and success_webhook_url:
        new_lines.append(f'DISCORD_SUCCESS_WEBHOOK_URL={success_webhook_url}')
        print("✅ Added DISCORD_SUCCESS_WEBHOOK_URL for success notifications")

    # Write back to .env file
    with open(env_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))

    print(f"\n🎉 Discord webhooks configured in {env_file}")
    
    if error_webhook_url or success_webhook_url:
        print("\nConfigured webhooks:")
        if error_webhook_url:
            print("  • Error notifications → Your Discord channel")
        if success_webhook_url:
            print("  • Success notifications → Your Discord channel")
    else:
        print("\nℹ️  No webhooks configured. Discord notifications will be disabled.")

    return True

def main():
    """Main entry point."""
    print("🚀 Setting up Discord Webhooks for F1 Countdown Bot")
    print("=" * 60)

    if not Path(".env").exists():
        print("❌ .env file not found!")
        print("Please create your .env file first with Twitter API credentials.")
        print("You can copy from env_example.txt and fill in your Twitter API keys.")
        return False

    try:
        setup_discord_webhooks()

        print("\n🧪 Testing Discord webhooks...")
        os.system("python test_discord.py")

        return True

    except Exception as e:
        print(f"❌ Error setting up Discord webhooks: {e}")
        return False

if __name__ == "__main__":
    main()
