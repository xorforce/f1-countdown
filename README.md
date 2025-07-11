# F1 Race Countdown Bot

An automated Python script that posts daily F1 race countdown tweets at 3:00 PM IST, showing the progress between races with ASCII progress bars.

## Features

- **Daily Automated Tweets**: Posts at 3:00 PM IST daily
- **Race Progress Tracking**: Shows percentage progress between races
- **ASCII Progress Bars**: Visual representation using ▓ and ░ characters
- **Off-Season Handling**: Automatically transitions to next season
- **Robust Error Handling**: Fibonacci retry intervals for data fetch failures
- **FastF1 Integration**: Uses official F1 data from the FastF1 library

## Requirements

- Python 3.13+
- Twitter Developer Account with API keys
- Internet connection for F1 data fetching

## Installation & Setup

### 1. Project Setup
```bash
# Clone or download the project
git clone <repository-url>
cd F1-script

# Create virtual environment
python3.13 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**Note**: The bot uses `curl_cffi` for Discord webhook requests to bypass Cloudflare protection.

### 2. Configuration Files
```bash
# Create configuration files
cp config.ini.template config.ini
touch .env
```

### 3. Twitter API Setup
1. **Create Twitter Developer Account**:
   - Go to https://developer.twitter.com/
   - Apply for a developer account and create a new app
   - Generate Consumer Key, Consumer Secret, Access Token, Access Token Secret
   - Set app permissions to "Read and Write"

2. **Add credentials to .env file**:
   ```env
   TWITTER_CONSUMER_KEY=your_consumer_key_here
   TWITTER_CONSUMER_SECRET=your_consumer_secret_here
   TWITTER_ACCESS_TOKEN=your_access_token_here
   TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret_here
   ```

### 4. Discord Webhook Setup (Optional)
For notifications when the bot posts tweets or encounters errors:

1. **Create Discord Webhooks**:
   - Go to your Discord server → Right-click channel → Edit Channel
   - Go to Integrations → Webhooks → Create New Webhook
   - Copy webhook URL(s)

2. **Add to .env file**:
   ```env
   # For error notifications
   DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN
   
   # For success notifications (optional)
   DISCORD_SUCCESS_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR_SUCCESS_WEBHOOK_ID/YOUR_SUCCESS_WEBHOOK_TOKEN
   ```

### 5. Verify Setup
```bash
# Complete setup verification
python verify_setup.py

# Test Discord webhooks (if configured)
python test_discord.py

# Test bot in debug mode (no tweets posted)
python f1_countdown_bot.py --debug
```

## Usage

### Running Modes

| Command | Purpose | Authentication | Posts Tweet |
|---------|---------|---------------|------------|
| `python verify_setup.py` | Complete setup verification | ❌ No | ❌ No |
| `python f1_countdown_bot.py --debug` | Testing/debugging | ❌ No | ❌ No |
| `python f1_countdown_bot.py --test` | Single tweet test | ✅ Yes | ✅ Yes |
| `python f1_countdown_bot.py` | Production (cron) | ✅ Yes | ✅ Yes |
| `python f1_countdown_bot.py --schedule` | Self-managed | ✅ Yes | ✅ Yes |

### Development Workflow
```bash
# 1. Always test in debug mode first
python f1_countdown_bot.py --debug

# 2. Test with single tweet if needed
python f1_countdown_bot.py --test

# 3. Deploy to production
python f1_countdown_bot.py
```

## Configuration Options

Edit `config.ini` to customize:

- **Tweet Time**: Change `tweet_time` (24-hour format)
- **Timezone**: Modify `timezone` (default: Asia/Kolkata)
- **Cache Location**: Update `cache_location` path
- **Logging**: Adjust `log_level` and `log_file`

## Tweet Format

```
F1 Race Countdown: {RaceName}
{RaceLeftPercentage:.2f}% to go!
{ProgressBar} {RaceLeftPercentage:.2f}%
#F1 #Formula1 #Countdown
```

**Example**:
```
F1 Race Countdown: Monaco Grand Prix
52.00% to go!
▓▓▓▓▓▓▓▓░░░░░░░ 52.00%
#F1 #Formula1 #Countdown
```

## Deployment

### PythonAnywhere (Recommended)

1. **Upload Project**: Upload all files to PythonAnywhere

2. **Set Up Environment**:
   ```bash
   # In PythonAnywhere console
   cd /home/yourusername/F1-script
   python3.10 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   
   # Create .env file with your credentials
   nano .env
   ```

3. **Test Installation**:
   ```bash
   python3.10 f1_countdown_bot.py --debug
   python3.10 test_discord.py
   ```

4. **Set Up Scheduled Task**:
   - Go to PythonAnywhere Dashboard → Tasks → Scheduled Tasks
   - Command: `cd /home/yourusername/F1-script && source venv/bin/activate && python f1_countdown_bot.py`
   - Schedule: Daily at desired time (e.g., 15:00 for 3 PM IST)

### Docker
```dockerfile
FROM python:3.13-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "f1_countdown_bot.py"]
```

### systemd (Linux)
```ini
[Unit]
Description=F1 Race Countdown Bot
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/F1-script
ExecStart=/usr/bin/python3 /path/to/F1-script/f1_countdown_bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

## Troubleshooting

### Quick Fixes

| Problem | Solution |
|---------|----------|
| Import errors | `pip install -r requirements.txt` |
| Authentication failed | Check `.env` file credentials |
| No race data | Check internet, try again later |
| Discord not working | Run `python test_discord.py` |
| Permission denied | Check cache directory permissions |

### Common Issues

1. **Setup Issues**: Run `python verify_setup.py` first

2. **Twitter API Issues**:
   - Verify all four environment variables are set
   - Ensure app has "Read and Write" permissions
   - Check for typos in `.env` file

3. **Discord Notifications**:
   - Verify webhook URLs in `.env` file
   - Test with `python test_discord.py`
   - Bot uses `curl_cffi` to bypass Cloudflare protection

4. **Virtual Environment Issues**:
   ```bash
   # Recreate virtual environment
   rm -rf venv
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

### Debug Information

Run in debug mode to see detailed output:
```bash
python f1_countdown_bot.py --debug
```

Sample debug output:
```
🏁 F1 COUNTDOWN DEBUG INFO:
Next Race: Hungarian Grand Prix
Progress: 17.86%
Race Left: 82.14%

TWEET CONTENT:
F1 Race Countdown: Hungarian Grand Prix
82.14% to go!
▓▓▓▓▓▓▓▓▓▓▓▓░░░ 82.14%
#F1 #Formula1 #Countdown
```

## Monitoring

### Regular Checks
```bash
# Check bot status
python f1_countdown_bot.py --debug

# View logs
tail -50 f1_countdown_bot.log

# Test Discord notifications
python test_discord.py
```

### Environment Validation
```bash
# Check environment variables
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
required = ['TWITTER_CONSUMER_KEY', 'TWITTER_CONSUMER_SECRET', 'TWITTER_ACCESS_TOKEN', 'TWITTER_ACCESS_TOKEN_SECRET']
for var in required:
    print(f'{var}: {\"✅ Set\" if os.getenv(var) else \"❌ Missing\"}')"
```

## Error Handling

- **Data Fetch Failures**: Fibonacci retry intervals (1, 1, 2, 3, 5, 8... minutes)
- **Twitter API Issues**: Logged but doesn't trigger data retry
- **Off-Season**: Automatically posts waiting message if next year's calendar unavailable

## Progress Calculation

- **Progress** = Days elapsed since last race / Total days between races
- **Race Left** = 100% - Progress
- **Race Day** = 100% progress (0% race left)

## File Structure

```
F1-script/
├── f1_countdown_bot.py      # Main script
├── config.ini               # Configuration file
├── config.ini.template      # Configuration template
├── .env                     # Environment variables
├── env_example.txt          # Example environment variables
├── test_discord.py          # Discord webhook test
├── setup_discord.py         # Discord webhook setup
├── verify_setup.py          # Setup verification
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── cache/                  # FastF1 cache directory
└── f1_countdown_bot.log    # Log file
```

## Quick Start

```bash
# Complete setup
git clone <repo> && cd F1-script
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp config.ini.template config.ini

# Add credentials to .env file
touch .env
# Edit .env with your Twitter API keys and Discord webhook

# Test setup
python verify_setup.py
python f1_countdown_bot.py --debug
python f1_countdown_bot.py --test
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source. Please ensure compliance with Twitter's API terms of service and FastF1's usage guidelines.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review log files for errors
3. Run in debug mode to see detailed output
4. Open an issue on the repository

---

**Note**: This bot requires constant internet connection and should be run on a reliable server for uninterrupted operation. 