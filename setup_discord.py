#!/usr/bin/env python3.13
"""
Helper script to set up Discord webhook URLs in .env file.
This script sets up the webhooks with the provided URLs.
"""

import os
from pathlib import Path

***REMOVED***
ERROR_WEBHOOK_URL = (
    "https://discord.com/api/webhooks/1393343102642684005/"
    "WJ4VLmQJlwKgV4gEFygYSDIMf-GdIJqsA5O4OhzPbpwrOoYC4alyMHTx-3H3_LPc0T_7"
)
SUCCESS_WEBHOOK_URL = (
    "https://discord.com/api/webhooks/1393347157171507350/"
    "2hSms-MqF2_yzpnNhEbFJbFse6JP2-TpsTV0h0ywDGgAjUwaXa9iiwTVzroBQ_WgF4zC"
)

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

    for line in lines:
        if line.startswith('DISCORD_WEBHOOK_URL='):
            new_lines.append(f'DISCORD_WEBHOOK_URL={ERROR_WEBHOOK_URL}')
            discord_webhook_set = True
            print("✅ Updated DISCORD_WEBHOOK_URL for error notifications")
        elif line.startswith('DISCORD_SUCCESS_WEBHOOK_URL='):
            new_lines.append(f'DISCORD_SUCCESS_WEBHOOK_URL={SUCCESS_WEBHOOK_URL}')
            discord_success_webhook_set = True
            print("✅ Updated DISCORD_SUCCESS_WEBHOOK_URL for success notifications")
        else:
            new_lines.append(line)

    # Add webhook URLs if they weren't found
    if not discord_webhook_set:
        new_lines.append(f'DISCORD_WEBHOOK_URL={ERROR_WEBHOOK_URL}')
        print("✅ Added DISCORD_WEBHOOK_URL for error notifications")

    if not discord_success_webhook_set:
        new_lines.append(f'DISCORD_SUCCESS_WEBHOOK_URL={SUCCESS_WEBHOOK_URL}')
        print("✅ Added DISCORD_SUCCESS_WEBHOOK_URL for success notifications")

    # Write back to .env file
    with open(env_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))

    print(f"\n🎉 Discord webhooks configured in {env_file}")
    print("\nConfigured webhooks:")
    print("  • Error notifications → Incoming Failures channel")
    print("  • Success notifications → Incoming Tweets channel")

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
