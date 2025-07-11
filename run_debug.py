#!/usr/bin/env python3.13
"""Debug script for F1 Countdown Bot."""

from f1_countdown_bot import F1CountdownBot

if __name__ == "__main__":
    bot = F1CountdownBot(debug_mode=True)
    bot.daily_tweet_generation()
