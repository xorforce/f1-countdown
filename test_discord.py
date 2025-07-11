#!/usr/bin/env python3.13
"""
Test script to verify Discord webhook functionality.
Run this to test if your Discord webhooks are working before using the main bot.
"""

import os
from datetime import datetime

from curl_cffi import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_discord_webhook(webhook_url, webhook_type):
    """Test Discord webhook functionality."""
    if not webhook_url:
        print(f"❌ DISCORD_{webhook_type.upper()}_WEBHOOK_URL not found in environment variables")
        print("Please add it to your .env file")
        return False

    try:
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')

        # Create test embed based on webhook type
        if webhook_type == "ERROR":
            embed = {
                "title": "🧪 F1 Countdown Bot - Error Webhook Test",
                "description": (
                    "This is a test message to verify Discord error webhook "
                    "integration is working correctly."
                ),
                "color": 15158332,  # Red color
                "fields": [
                    {
                        "name": "Test Type",
                        "value": "ERROR_WEBHOOK_TEST",
                        "inline": True
                    },
                    {
                        "name": "Timestamp",
                        "value": current_time,
                        "inline": True
                    }
                ],
                "footer": {
                    "text": "F1 Countdown Bot Error Webhook Test"
                }
            }
            content = "🧪 Discord error webhook test from F1 Countdown Bot"
        else:
            embed = {
                "title": "✅ F1 Countdown Bot - Success Webhook Test",
                "description": (
                    "This is a test message to verify Discord success webhook "
                    "integration is working correctly.\n\n"
                    "**Sample Tweet:**\n```\nF1 Race Countdown: Hungarian Grand Prix\n"
                    "▓▓░░░░░░░░░░░░░ 17.86%\n#F1 #Formula1 #Countdown\n```"
                ),
                "color": 5763719,  # Green color
                "fields": [
                    {
                        "name": "Test Type",
                        "value": "SUCCESS_WEBHOOK_TEST",
                        "inline": True
                    },
                    {
                        "name": "Timestamp",
                        "value": current_time,
                        "inline": True
                    },
                    {
                        "name": "Next Race",
                        "value": "Hungarian Grand Prix",
                        "inline": True
                    },
                    {
                        "name": "Progress Made",
                        "value": "17.86%",
                        "inline": True
                    },
                    {
                        "name": "Days Left",
                        "value": "82.14%",
                        "inline": True
                    }
                ],
                "footer": {
                    "text": "F1 Countdown Bot Success Webhook Test"
                }
            }
            content = "🧪 Discord success webhook test from F1 Countdown Bot"

        payload = {
            "content": content,
            "embeds": [embed]
        }

        print(f"🔄 Sending test message to Discord {webhook_type} webhook...")
        response = requests.post(webhook_url, json=payload, timeout=10)

        if response.status_code == 204:
            print(f"✅ Discord {webhook_type} webhook test successful!")
            print(f"📢 Check your Discord channel for the {webhook_type.lower()} test message")
            return True
        else:
            print(f"❌ Discord {webhook_type} webhook test failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False

    except Exception as e:
        print(f"❌ Error testing Discord {webhook_type} webhook: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testing Discord Webhook Integration")
    print("=" * 50)

    # Test error webhook
    error_webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    success_webhook_url = os.getenv('DISCORD_SUCCESS_WEBHOOK_URL')

    results = []

    print("\n🔴 Testing Error Webhook:")
    print("-" * 30)
    ERROR_SUCCESS = test_discord_webhook(error_webhook_url, "ERROR")
    results.append(("Error Webhook", ERROR_SUCCESS))

    print("\n🟢 Testing Success Webhook:")
    print("-" * 30)
    SUCCESS_SUCCESS = test_discord_webhook(success_webhook_url, "SUCCESS")
    results.append(("Success Webhook", SUCCESS_SUCCESS))

    print("\n" + "=" * 50)
    print("📋 RESULTS SUMMARY:")
    print("=" * 50)

    ALL_SUCCESSFUL = True
    for webhook_name, success in results:
        STATUS = "✅ Working" if success else "❌ Failed"
        print(f"{webhook_name}: {STATUS}")
        if not success:
            ALL_SUCCESSFUL = False

    if ALL_SUCCESSFUL:
        print("\n🎉 All Discord webhooks are working correctly!")
        print("You can now use the F1 Countdown Bot with Discord notifications")
    else:
        print("\n💥 Some Discord webhooks failed!")
        print("Please check your webhook URLs in the .env file")
        print("\nNote: Both webhooks are optional. The bot will work even if some fail.")
