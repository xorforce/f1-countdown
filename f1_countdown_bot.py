#!/usr/bin/env python3.13
"""
F1 Race Countdown Bot
Version 3.4

Automated script to post daily F1 race countdown tweets at 3:00 PM IST.
"""

import os
import sys
import logging
import configparser
from datetime import datetime, timedelta
from typing import Optional, Tuple

import pandas as pd
import pytz
import tweepy
import fastf1 as ff1
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('f1_countdown_bot.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class F1CountdownBot:
    """F1 Race Countdown Bot for automated Twitter posting."""

    def __init__(self, config_file: str = 'config.ini', debug_mode: bool = False):
        """Initialize the F1 Countdown Bot."""
        self.debug_mode = debug_mode
        self.config = self._load_config(config_file, debug_mode)

        # Only setup Twitter API if not in debug mode
        if not self.debug_mode:
            self.twitter_api = self._setup_twitter_api()
        else:
            self.twitter_api = None
            print("🔧 DEBUG MODE: Twitter authentication skipped")

        self.timezone = pytz.timezone(
            self.config.get('settings', 'timezone', fallback='Asia/Kolkata')
        )
        self.cache_location = self.config.get('settings', 'cache_location', fallback='./cache/')
        self.tweet_time = self.config.get('settings', 'tweet_time', fallback='15:00')

        # Initialize FastF1 cache
        self._setup_fastf1_cache()

        # Fibonacci retry state
        self._fibonacci_index = 0
        self._last_successful_fetch = None

        mode_info = " (DEBUG MODE)" if self.debug_mode else ""
        logger.info(f"F1 Countdown Bot initialized successfully{mode_info}")

    def _load_config(self, config_file: str, debug_mode: bool = False) -> configparser.ConfigParser:
        """Load configuration from file."""
        if not os.path.exists(config_file):
            logger.error(
                f"Config file {config_file} not found. Please create it based on config.ini.template"
            )
            sys.exit(1)

        config = configparser.ConfigParser()
        config.read(config_file)

        # Validate required sections - Twitter section is now optional as we use env vars
        required_sections = ['settings']

        for section in required_sections:
            if not config.has_section(section):
                logger.error(
                    f"Missing required section '{section}' in config file"
                )
                sys.exit(1)

        logger.info(
            "Configuration loaded successfully (Twitter credentials from environment variables)"
        )
        return config

    def _setup_twitter_api(self) -> tweepy.API:
        """Set up Twitter API connection using environment variables."""
        try:
            # Get Twitter API credentials from environment variables
            consumer_key = os.getenv('TWITTER_CONSUMER_KEY')
            consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET')
            access_token = os.getenv('TWITTER_ACCESS_TOKEN')
            access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

            # Check if all required environment variables are set
            if not all([consumer_key, consumer_secret, access_token, access_token_secret]):
                missing_vars = []
                if not consumer_key:
                    missing_vars.append('TWITTER_CONSUMER_KEY')
                if not consumer_secret:
                    missing_vars.append('TWITTER_CONSUMER_SECRET')
                if not access_token:
                    missing_vars.append('TWITTER_ACCESS_TOKEN')
                if not access_token_secret:
                    missing_vars.append('TWITTER_ACCESS_TOKEN_SECRET')

                logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
                logger.error("Please set these variables in your .env file or environment")
                sys.exit(1)

            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)

            api = tweepy.API(auth, wait_on_rate_limit=True)

            # Verify credentials
            api.verify_credentials()
            logger.info(
                "Twitter API authenticated successfully using environment variables"
            )
            return api

        except Exception as e:
            logger.critical(f"Failed to authenticate with Twitter API: {e}")
            sys.exit(1)

    def _setup_fastf1_cache(self):
        """Set up FastF1 cache directory."""
        if not os.path.exists(self.cache_location):
            os.makedirs(self.cache_location)
            logger.info(f"Created cache directory: {self.cache_location}")

        ff1.Cache.enable_cache(self.cache_location)
        logger.info(f"FastF1 cache enabled at: {self.cache_location}")

    def _fibonacci(self, n: int) -> int:
        """Generate Fibonacci number for retry delays."""
        if n <= 1:
            return 1
        a, b = 1, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b

    def _get_race_schedule(self, year: int) -> Optional[pd.DataFrame]:
        """Fetch F1 race schedule for a given year."""
        try:
            schedule_df = ff1.get_event_schedule(year)
            if schedule_df.empty:
                logger.warning(f"No F1 schedule available for year {year}")
                return None

            # Filter for Grand Prix events (EventFormat = 'conventional')
            races_df = schedule_df[schedule_df['EventFormat'] == 'conventional'].copy()

            if races_df.empty:
                logger.warning(f"No Grand Prix races found for year {year}")
                return None

            # Convert EventDate to datetime if it's not already
            if not pd.api.types.is_datetime64_any_dtype(races_df['EventDate']):
                races_df['EventDate'] = pd.to_datetime(races_df['EventDate'])

            logger.info(f"Successfully fetched {len(races_df)} races for year {year}")
            return races_df

        except Exception as e:
            logger.error(f"Failed to fetch F1 schedule for year {year}: {e}")
            return None

    def _find_next_and_last_races(
        self, current_year: int
    ) -> Tuple[Optional[pd.Series], Optional[pd.Series], int]:
        """Find next upcoming race and last completed race."""
        today = datetime.now(self.timezone).date()

        # Try current year first
        races_df = self._get_race_schedule(current_year)
        if races_df is None:
            return None, None, current_year

        # Convert EventDate to date for comparison
        races_df['EventDate_date'] = races_df['EventDate'].dt.date

        # Find upcoming races (today or later)
        upcoming_races = races_df[races_df['EventDate_date'] >= today]

        if not upcoming_races.empty:
            # Found upcoming race in current year
            next_race = upcoming_races.iloc[0]

            # Find last completed race
            completed_races = races_df[races_df['EventDate_date'] < today]
            last_race = completed_races.iloc[-1] if not completed_races.empty else None

            return next_race, last_race, current_year

        # No upcoming races in current year, try next year
        logger.info(f"No upcoming races in {current_year}, checking {current_year + 1}")
        next_year_races = self._get_race_schedule(current_year + 1)

        if next_year_races is None:
            return None, None, current_year + 1

        # Convert EventDate to date for comparison
        next_year_races['EventDate_date'] = next_year_races['EventDate'].dt.date

        # First race of next year
        next_race = next_year_races.iloc[0]

        # Last race of current year
        last_race = races_df.iloc[-1] if not races_df.empty else None

        return next_race, last_race, current_year + 1

    def _calculate_progress(self, next_race: pd.Series, last_race: Optional[pd.Series]) -> float:
        """Calculate race progress percentage based on days remaining."""
        today = datetime.now(self.timezone).date()

        if last_race is None:
            # If no last race, assume 0% progress (100% race left)
            return 0.0

        next_race_date = next_race['EventDate'].date()
        last_race_date = last_race['EventDate'].date()

        # Calculate total days between races
        total_days = (next_race_date - last_race_date).days

        # Calculate days remaining until next race
        days_remaining = (next_race_date - today).days

        # Handle edge cases
        if total_days <= 0:
            return 100.0  # Today is race day or past it

        if days_remaining <= 0:
            return 100.0  # Today is race day or past it

        if days_remaining > total_days:
            return 0.0  # Before last race (shouldn't happen)

        # Calculate percentage of time remaining
        race_left_percentage = (days_remaining / total_days) * 100

        # Clamp between 0 and 100
        return max(0.0, min(100.0, race_left_percentage))

    def _generate_progress_bar(self, race_left_percentage: float) -> str:
        """Generate ASCII progress bar."""
        total_chars = 15
        # Calculate progress made (elapsed time since last race)
        progress_made_percentage = 100 - race_left_percentage
        filled_chars = int((progress_made_percentage / 100) * total_chars)
        empty_chars = total_chars - filled_chars

        # Use ▓ for filled (progress made/time elapsed) and ░ for empty (time remaining)
        progress_bar = '▓' * filled_chars + '░' * empty_chars

        return progress_bar

    def _compose_tweet(self, next_race: pd.Series, race_left_percentage: float) -> str:
        """Compose tweet content."""
        race_name = next_race['EventName']
        progress_bar = self._generate_progress_bar(race_left_percentage)

        # Calculate progress made percentage to match the progress bar visual
        progress_made_percentage = 100 - race_left_percentage

        tweet = f"""F1 Race Countdown: {race_name}
{progress_bar} {progress_made_percentage:.2f}%
#F1 #Formula1 #Countdown"""

        return tweet

    def _compose_waiting_tweet(self, year: int) -> str:
        """Compose tweet for waiting for next season's calendar."""
        return f"The {year} F1 season has concluded! Waiting for the {year + 1} calendar to be announced. #F1"

    def _post_tweet(self, tweet_content: str, race_info: dict = None) -> bool:
        """Post tweet to Twitter."""
        # Always print the tweet content to console for debugging
        print("\n" + "="*60)
        print("TWEET CONTENT:")
        print("="*60)
        print(tweet_content)
        print("="*60)
        print(f"Tweet length: {len(tweet_content)} characters")
        print("="*60 + "\n")

        # In debug mode, just simulate posting
        if self.debug_mode:
            logger.info(f"DEBUG: Would post tweet: {tweet_content[:50]}...")
            print("🔧 DEBUG MODE: Tweet not actually posted to Twitter")

            # Send success notification even in debug mode to test
            self._send_success_notification(tweet_content, race_info)
            return True

        # Normal mode: actually post to Twitter
        try:
            self.twitter_api.update_status(tweet_content)
            logger.info(f"Successfully posted tweet: {tweet_content[:50]}...")
            print("✅ Tweet posted successfully to Twitter!")

            # Send success notification to Discord
            self._send_success_notification(tweet_content, race_info)

            return True
        except Exception as e:
            logger.error(f"Failed to post tweet: {e}")
            print(f"❌ Failed to post tweet to Twitter: {e}")
            return False

    def _send_discord_notification(self, title: str, message: str, error_type: str = "ERROR") -> bool:
        """Send error notification to Discord webhook."""
        discord_webhook_url = os.getenv('DISCORD_WEBHOOK_URL')

        if not discord_webhook_url:
            logger.warning("Discord webhook URL not configured - skipping Discord notification")
            return False

        try:
            current_time = datetime.now(self.timezone).strftime('%Y-%m-%d %H:%M:%S %Z')

            # Create Discord embed
            embed = {
                "title": f"🚨 F1 Countdown Bot - {title}",
                "description": message,
                "color": 15158332,  # Red color
                "fields": [
                    {
                        "name": "Error Type",
                        "value": error_type,
                        "inline": True
                    },
                    {
                        "name": "Timestamp",
                        "value": current_time,
                        "inline": True
                    }
                ],
                "footer": {
                    "text": "F1 Countdown Bot Error Alert"
                }
            }

            payload = {
                "content": f"@here F1 Bot encountered an error!",
                "embeds": [embed]
            }

            response = requests.post(discord_webhook_url, json=payload, timeout=10)

            if response.status_code == 204:
                logger.info("Discord notification sent successfully")
                print("📢 Discord notification sent successfully!")
                return True
            else:
                logger.error(f"Failed to send Discord notification: {response.status_code}")
                print(f"❌ Failed to send Discord notification: {response.status_code}")
                return False

        except Exception as e:
            logger.error(f"Error sending Discord notification: {e}")
            print(f"❌ Error sending Discord notification: {e}")
            return False

    def _send_success_notification(self, tweet_content: str, race_info: dict = None) -> bool:
        """Send successful tweet notification to Discord webhook."""
        discord_success_webhook_url = os.getenv('DISCORD_SUCCESS_WEBHOOK_URL')

        if not discord_success_webhook_url:
            logger.info("Discord success webhook URL not configured - skipping success notification")
            return False

        try:
            current_time = datetime.now(self.timezone).strftime('%Y-%m-%d %H:%M:%S %Z')

            # Create Discord embed for success
            embed = {
                "title": "✅ F1 Countdown Bot - Tweet Posted Successfully",
                "description": f"**Tweet Content:**\n```\n{tweet_content}\n```",
                "color": 5763719,  # Green color
                "fields": [
                    {
                        "name": "Status",
                        "value": "SUCCESS",
                        "inline": True
                    },
                    {
                        "name": "Timestamp",
                        "value": current_time,
                        "inline": True
                    }
                ],
                "footer": {
                    "text": "F1 Countdown Bot Success Alert"
                }
            }

            # Add race information if provided
            if race_info:
                embed["fields"].extend([
                    {
                        "name": "Next Race",
                        "value": race_info.get("next_race", "Unknown"),
                        "inline": True
                    },
                    {
                        "name": "Progress Made",
                        "value": f"{race_info.get('progress_made', 0):.2f}%",
                        "inline": True
                    },
                    {
                        "name": "Days Left",
                        "value": f"{race_info.get('race_left', 0):.2f}%",
                        "inline": True
                    }
                ])

            payload = {
                "content": "🏁 F1 Bot posted a new countdown tweet!",
                "embeds": [embed]
            }

            response = requests.post(discord_success_webhook_url, json=payload, timeout=10)

            if response.status_code == 204:
                logger.info("Discord success notification sent successfully")
                print("📢 Discord success notification sent!")
                return True
            else:
                logger.error(f"Failed to send Discord success notification: {response.status_code}")
                print(f"❌ Failed to send Discord success notification: {response.status_code}")
                return False

        except Exception as e:
            logger.error(f"Error sending Discord success notification: {e}")
            print(f"❌ Error sending Discord success notification: {e}")
            return False

    def daily_tweet_generation(self):
        """Main function to generate and post daily tweet."""
        logger.info("Starting daily tweet generation")

        # Print start message
        current_time = datetime.now(self.timezone).strftime('%Y-%m-%d %H:%M:%S %Z')
        print(f"\n🚀 DAILY TWEET GENERATION STARTED at {current_time}")
        print("-" * 60)

        try:
            current_year = datetime.now(self.timezone).year

            # Find next race and last race
            next_race, last_race, _ = self._find_next_and_last_races(current_year)

            if next_race is None:
                # No race data available
                logger.warning("No race data available, posting waiting tweet")
                print(f"\n🏁 F1 COUNTDOWN DEBUG INFO:")
                print(f"No upcoming races found for {current_year}")
                print("Posting waiting tweet for next season...")

                waiting_tweet = self._compose_waiting_tweet(current_year)
                self._post_tweet(waiting_tweet, {
                    "next_race": f"Waiting for {current_year + 1} season",
                    "progress_made": 0,
                    "race_left": 0
                })

                # Reset Fibonacci index on successful data fetch (even if no races)
                self._fibonacci_index = 0
                self._last_successful_fetch = datetime.now(self.timezone)
                return

            # Calculate progress
            race_left_percentage = self._calculate_progress(next_race, last_race)

            # Print debug information
            print(f"\n🏁 F1 COUNTDOWN DEBUG INFO:")
            print(f"Next Race: {next_race['EventName']}")
            print(f"Next Race Date: {next_race['EventDate'].date()}")
            if last_race is not None:
                print(f"Last Race: {last_race['EventName']}")
                print(f"Last Race Date: {last_race['EventDate'].date()}")
            else:
                print("Last Race: None (start of season)")
            print(f"Progress: {100 - race_left_percentage:.2f}%")
            print(f"Race Left: {race_left_percentage:.2f}%")

            # Compose and post tweet
            tweet_content = self._compose_tweet(next_race, race_left_percentage)

            if self._post_tweet(tweet_content, {
                "next_race": next_race['EventName'],
                "progress_made": 100 - race_left_percentage,
                "race_left": race_left_percentage
            }):
                # Reset Fibonacci index on successful operation
                self._fibonacci_index = 0
                self._last_successful_fetch = datetime.now(self.timezone)

                logger.info(f"Race: {next_race['EventName']}, Progress: {100 - race_left_percentage:.2f}%, "
                          f"Race Left: {race_left_percentage:.2f}%")

        except Exception as e:
            logger.error(f"Error in daily tweet generation: {e}")
            print(f"❌ Error in daily tweet generation: {e}")

            # Send Discord notification about the error
            self._send_discord_notification(
                title="Daily Tweet Generation Failed",
                message=f"The F1 countdown bot encountered an error during tweet generation:\n\n`{str(e)}`",
                error_type="TWEET_GENERATION_ERROR"
            )

            self._handle_fetch_failure()

    def _handle_fetch_failure(self):
        """Handle data fetch failure with Fibonacci retry."""
        self._fibonacci_index += 1
        retry_delay_minutes = self._fibonacci(self._fibonacci_index)

        logger.warning(f"Data fetch failed. Retrying in {retry_delay_minutes} minutes "
                      f"(Fibonacci index: {self._fibonacci_index})")

        # Print retry information
        retry_time = datetime.now(self.timezone) + timedelta(minutes=retry_delay_minutes)
        print(f"⏰ Data fetch failed. Retrying in {retry_delay_minutes} minutes at {retry_time.strftime('%H:%M')}")
        print(f"   Fibonacci retry sequence: attempt #{self._fibonacci_index}")

        # SCHEDULING DISABLED FOR PYTHONANYWHERE CRON - Uncomment below for self-managed scheduling
        # Schedule retry
        # schedule.every().day.at(retry_time.strftime('%H:%M')).do(self.daily_tweet_generation).tag('retry')

        # Clear previous retry jobs to avoid accumulation
        # schedule.clear('retry')
        # schedule.every().day.at(retry_time.strftime('%H:%M')).do(self.daily_tweet_generation).tag('retry')

    def run(self):
        """Main execution loop."""
        logger.info("F1 Countdown Bot starting...")

        # SCHEDULING DISABLED FOR PYTHONANYWHERE CRON - Uncomment below for self-managed scheduling
        # Schedule daily tweet
        # schedule.every().day.at(self.tweet_time).do(self.daily_tweet_generation).tag('daily')

        # logger.info(f"Scheduled daily tweet at {self.tweet_time} {self.timezone}")

        # Print startup information
        print("\n🏁 F1 COUNTDOWN BOT STARTING")
        print("="*50)
        print(f"Daily tweet time: {self.tweet_time} {self.timezone}")
        print(f"Cache location: {self.cache_location}")
        print(f"Current time: {datetime.now(self.timezone).strftime('%Y-%m-%d %H:%M:%S %Z')}")
        print("="*50)
        print("Note: Scheduling disabled - using external cron job")
        print("Running once and exiting...")

        # Run once instead of continuously for cron job execution
        self.daily_tweet_generation()

        # CONTINUOUS LOOP DISABLED FOR PYTHONANYWHERE CRON - Uncomment below for self-managed scheduling
        # print("Bot is running... Press Ctrl+C to stop")
        # print("Checking for scheduled tweets every minute...")

        # Run continuously
        # while True:
        #     try:
        #         schedule.run_pending()
        #         time.sleep(60)  # Check every minute
        #     except KeyboardInterrupt:
        #         logger.info("Bot stopped by user")
        #         print("\n👋 Bot stopped by user")
        #         break
        #     except Exception as e:
        #         logger.error(f"Unexpected error in main loop: {e}")
        #         print(f"❌ Unexpected error: {e}")
        #         time.sleep(60)  # Continue after error


def main():
    """Main entry point."""
    try:
        if len(sys.argv) > 1 and sys.argv[1] == '--test':
            # Test mode: run once immediately
            print("🧪 Running in TEST MODE (single tweet generation)")
            bot = F1CountdownBot()
            bot.daily_tweet_generation()
        elif len(sys.argv) > 1 and sys.argv[1] == '--debug':
            # Debug mode: run once immediately with extra output, skip Twitter auth
            print("🔍 Running in DEBUG MODE (single tweet generation with extra output)")
            bot = F1CountdownBot(debug_mode=True)
            bot.daily_tweet_generation()
        elif len(sys.argv) > 1 and sys.argv[1] == '--schedule':
            # Schedule mode: run continuously with self-managed scheduling (for migration)
            print("🚀 Running in SCHEDULE MODE (continuous operation with self-managed scheduling)")
            bot = F1CountdownBot()
            # Note: You'll need to uncomment the scheduling code in run() method for this to work
            bot.run()
        else:
            # Default mode: run once for cron job execution
            print("🚀 Running in CRON MODE (single tweet generation for external scheduling)")
            bot = F1CountdownBot()
            bot.daily_tweet_generation()

    except Exception as e:
        # Handle any unhandled exceptions
        logger.critical(f"Critical error in main execution: {e}")
        print(f"💥 Critical error in main execution: {e}")

        # Try to send Discord notification (if possible)
        try:
            # Create a temporary bot instance just for sending the notification
            discord_webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
            if discord_webhook_url:
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')

                embed = {
                    "title": "💥 F1 Countdown Bot - Critical Error",
                    "description": f"The F1 countdown bot encountered a critical error and crashed:\n\n`{str(e)}`",
                    "color": 10038562,  # Dark red color
                    "fields": [
                        {
                            "name": "Error Type",
                            "value": "CRITICAL_ERROR",
                            "inline": True
                        },
                        {
                            "name": "Timestamp",
                            "value": current_time,
                            "inline": True
                        }
                    ],
                    "footer": {
                        "text": "F1 Countdown Bot Critical Error Alert"
                    }
                }

                payload = {
                    "content": f"@here F1 Bot crashed with critical error!",
                    "embeds": [embed]
                }

                response = requests.post(discord_webhook_url, json=payload, timeout=10)
                if response.status_code == 204:
                    print("📢 Discord notification sent for critical error")
                else:
                    print(f"❌ Failed to send Discord notification: {response.status_code}")
        except Exception as discord_error:
            print(f"❌ Could not send Discord notification: {discord_error}")

        # Exit with error code
        sys.exit(1)


if __name__ == "__main__":
    main()
