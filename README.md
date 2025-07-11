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

## Installation

1. **Clone or download the project**:
   ```bash
   git clone <repository-url>
   cd F1-script
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   
   **Note**: The bot uses `curl_cffi` for Discord webhook requests to bypass Cloudflare protection. This provides better reliability when sending notifications to Discord.

3. **Set up configuration**:
   ```bash
   cp config.ini.template config.ini
   ```

4. **Configure API credentials using environment variables**:
   Create a `.env` file in the project root:
   ```bash
   # Create .env file
   touch .env
   ```
   
   Add your Twitter API credentials to the `.env` file:
   ```env
   TWITTER_CONSUMER_KEY=your_consumer_key_here
   TWITTER_CONSUMER_SECRET=your_consumer_secret_here
   TWITTER_ACCESS_TOKEN=your_access_token_here
   TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret_here
   
   # Optional: Discord webhooks for notifications
   DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN
   DISCORD_SUCCESS_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR_SUCCESS_WEBHOOK_ID/YOUR_SUCCESS_WEBHOOK_TOKEN
   ```

   **Note**: The `.env` file should be kept private and not committed to version control.

## Twitter API Setup

1. **Create a Twitter Developer Account**:
   - Go to https://developer.twitter.com/
   - Apply for a developer account
   - Create a new app

2. **Generate API Keys**:
   - Consumer Key and Consumer Secret
   - Access Token and Access Token Secret

3. **Set Permissions**:
   - Ensure your app has "Read and Write" permissions

## Discord Webhook Setup (Optional)

To receive notifications when the bot posts tweets or encounters errors:

1. **Create Discord Webhooks**:
   - Go to your Discord server
   - Right-click on a channel → Edit Channel
   - Go to Integrations → Webhooks
   - Create New Webhook(s) - you can use separate channels for successes and errors
   - Copy the webhook URL(s)

2. **Add to Environment Variables**:
   - Add webhook URLs to your `.env` file:
   ```env
   # For error notifications (failures, crashes, etc.)
   DISCORD_WEBHOOK_URL=your_error_webhook_url_here
   
   # For success notifications (successful tweets)
   DISCORD_SUCCESS_WEBHOOK_URL=your_success_webhook_url_here
   ```
   - Both are optional - bot will work without them
   - You can use the same webhook URL for both if desired

3. **Notification Types**:
   - **Error Notifications**: When bot fails, crashes, or encounters issues
   - **Success Notifications**: When tweets are posted successfully with race info
   - Includes detailed information, timestamps, and tweet content
   - Helps with monitoring and remote debugging on PythonAnywhere

4. **Quick Setup (Using Provided Webhooks)**:
   ```bash
   python setup_discord.py
   ```
   This will automatically configure the Discord webhooks with the provided URLs and test them.

5. **Test Discord Integration**:
   ```bash
   python test_discord.py
   ```
   This will test both webhooks and send sample messages to verify they're working.

## Usage

### 🚀 Complete Setup Guide for New Machine

#### Prerequisites
- Python 3.13 or higher installed
- Git installed (optional, for cloning)
- Twitter Developer Account with API credentials
- Discord server with webhook permissions (optional)

#### Step 1: Download and Setup Project
```bash
# Option A: Clone from repository
git clone <repository-url>
cd F1-script

# Option B: Download and extract ZIP
# Download ZIP, extract, and navigate to F1-script folder
cd F1-script
```

#### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python3.13 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
# venv\Scripts\activate

# Verify virtual environment is active (should show (venv) in prompt)
which python  # Should show path with venv
```

#### Step 3: Install Dependencies
```bash
# Make sure virtual environment is active
pip install -r requirements.txt

# Verify installation
pip list | grep -E "(tweepy|pandas|fastf1|requests|python-dotenv)"
```

#### Step 4: Create Configuration Files
```bash
# Create config file from template
cp config.ini.template config.ini

# Create environment variables file
touch .env

# Verify files exist
ls -la config.ini .env
```

#### Step 5: Set Up Twitter API Credentials
1. **Get Twitter API Keys**:
   - Go to https://developer.twitter.com/
   - Create developer account if needed
   - Create a new app
   - Generate Consumer Key, Consumer Secret, Access Token, Access Token Secret
   - Ensure app has "Read and Write" permissions

2. **Add credentials to .env file**:
   ```bash
   # Edit .env file (use nano, vim, or any text editor)
   nano .env
   ```
   
   Add these lines to `.env`:
   ```env
   TWITTER_CONSUMER_KEY=your_actual_consumer_key_here
   TWITTER_CONSUMER_SECRET=your_actual_consumer_secret_here
   TWITTER_ACCESS_TOKEN=your_actual_access_token_here
   TWITTER_ACCESS_TOKEN_SECRET=your_actual_access_token_secret_here
   ```

#### Step 6: Set Up Discord Webhooks (Optional but Recommended)
1. **Create Discord Webhooks**:
   - Go to your Discord server
   - Right-click on a channel (e.g., #bot-alerts) → Edit Channel
   - Go to Integrations → Webhooks → Create New Webhook
   - Copy the webhook URL
   - Optionally create a second webhook for success notifications in another channel

2. **Add Discord URLs to .env**:
   ```bash
   # Edit .env file again
   nano .env
   ```
   
   Add these lines to `.env`:
   ```env
   # For error notifications (bot failures, crashes)
   DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN
   
   # For success notifications (successful tweets) - optional
   DISCORD_SUCCESS_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR_SUCCESS_WEBHOOK_ID/YOUR_SUCCESS_WEBHOOK_TOKEN
   ```

3. **Complete .env file should look like**:
   ```env
   TWITTER_CONSUMER_KEY=your_actual_consumer_key_here
   TWITTER_CONSUMER_SECRET=your_actual_consumer_secret_here
   TWITTER_ACCESS_TOKEN=your_actual_access_token_here
   TWITTER_ACCESS_TOKEN_SECRET=your_actual_access_token_secret_here
   DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN
   DISCORD_SUCCESS_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR_SUCCESS_WEBHOOK_ID/YOUR_SUCCESS_WEBHOOK_TOKEN
   ```

#### Step 7: Test Your Setup
```bash
# Make sure virtual environment is active
source venv/bin/activate  # If not already active

# Test 1: Complete setup verification (recommended)
python verify_setup.py

# Test 2: Test Discord webhooks only (if configured)
python test_discord.py

# Test 3: Test bot in debug mode (no tweets posted, but Discord notifications sent)
python f1_countdown_bot.py --debug

# Test 4: Test with actual tweet posting (optional)
python f1_countdown_bot.py --test
```

**Alternative manual verification**:
```bash
# Manual check of environment variables
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
print('Twitter Consumer Key:', '✅ Set' if os.getenv('TWITTER_CONSUMER_KEY') else '❌ Missing')
print('Twitter Consumer Secret:', '✅ Set' if os.getenv('TWITTER_CONSUMER_SECRET') else '❌ Missing')
print('Twitter Access Token:', '✅ Set' if os.getenv('TWITTER_ACCESS_TOKEN') else '❌ Missing')
print('Twitter Access Token Secret:', '✅ Set' if os.getenv('TWITTER_ACCESS_TOKEN_SECRET') else '❌ Missing')
print('Discord Error Webhook:', '✅ Set' if os.getenv('DISCORD_WEBHOOK_URL') else '⚠️ Not set')
print('Discord Success Webhook:', '✅ Set' if os.getenv('DISCORD_SUCCESS_WEBHOOK_URL') else '⚠️ Not set')
"
```

#### Step 8: Verify Everything Works
After running the debug test, you should see:
- Console output showing race information
- Tweet content displayed (but not posted to Twitter)
- Discord success notification sent (if webhook configured)
- No errors in the output

#### Step 9: Deploy to Production (PythonAnywhere)
1. **Upload files to PythonAnywhere**:
   - Use Files tab to upload all project files
   - Or use git clone in PythonAnywhere console

2. **Set up virtual environment on PythonAnywhere**:
   ```bash
   # In PythonAnywhere console
   cd /home/yourusername/F1-script
   python3.10 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Create .env file on PythonAnywhere**:
   ```bash
   # In PythonAnywhere console
   nano .env
   # Copy your credentials from local .env file
   ```

4. **Test on PythonAnywhere**:
   ```bash
   # Test in debug mode
   python3.10 f1_countdown_bot.py --debug
   
   # Test Discord notifications
   python3.10 test_discord.py
   ```

5. **Set up scheduled task**:
   - Go to PythonAnywhere Dashboard → Tasks → Scheduled Tasks
   - Create new task:
     - Command: `cd /home/yourusername/F1-script && source venv/bin/activate && python f1_countdown_bot.py`
     - Schedule: Daily at desired time (e.g., 15:00 for 3 PM IST)

#### Common Issues and Solutions

1. **"Module not found" errors**:
   ```bash
   # Make sure virtual environment is active
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Twitter authentication failed**:
   - Check all 4 Twitter credentials in .env
   - Ensure app has "Read and Write" permissions
   - Verify no extra spaces in .env file

3. **Discord notifications not working**:
   - **First**: Ensure Discord webhook URLs are set in .env file
   - Check webhook URLs in .env file
   - Run `python test_discord.py` to verify
   - Ensure webhooks are from correct Discord server
   - Debug mode requires Discord URLs to be set for notifications to work

4. **"No race data" errors**:
   - Check internet connection
   - Try again later (FastF1 servers might be updating)

5. **Virtual environment issues**:
   ```bash
   # Delete and recreate virtual environment
   rm -rf venv
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

### Quick Commands Reference

```bash
# Daily development workflow
source venv/bin/activate
python verify_setup.py               # Verify complete setup
python f1_countdown_bot.py --debug    # Test and debug
python f1_countdown_bot.py --test     # Single tweet test
python f1_countdown_bot.py            # Production run

# Maintenance commands
python test_discord.py               # Test Discord webhooks
tail -20 f1_countdown_bot.log        # View recent logs
pip install --upgrade -r requirements.txt  # Update dependencies
```

### Running Modes

#### Debug Mode (Recommended for Testing)
```bash
python f1_countdown_bot.py --debug
```
**What it does:**
- Skips Twitter authentication
- Shows all debug information
- Displays tweet content without posting
- Perfect for testing configuration and data fetching

**Use when:**
- First time setup
- Testing changes
- Debugging issues
- Verifying race data

#### Test Mode (Single Tweet)
```bash
python f1_countdown_bot.py --test
```
**What it does:**
- Authenticates with Twitter
- Generates and posts ONE tweet immediately
- Shows debug information
- Exits after posting

**Use when:**
- Testing live Twitter integration
- Verifying tweet format
- Manual tweet posting
- Validating credentials

#### Production Mode (Cron Job)
```bash
python f1_countdown_bot.py
```
**What it does:**
- Authenticates with Twitter
- Generates and posts tweet
- Runs once and exits
- Designed for cron job execution

**Use when:**
- Running via scheduled tasks
- PythonAnywhere scheduled tasks
- Automated daily execution

#### Schedule Mode (Self-Managed)
```bash
python f1_countdown_bot.py --schedule
```
**What it does:**
- Runs continuously with internal scheduling
- Posts tweets at configured time
- Includes retry logic
- For self-managed deployments

**Use when:**
- Running on your own server
- Want built-in scheduling
- Need Fibonacci retry logic

### Development Workflow

#### Making Changes
```bash
# 1. Always test in debug mode first
python f1_countdown_bot.py --debug

# 2. Test with single tweet if needed
python f1_countdown_bot.py --test

# 3. Deploy to production/cron job
python f1_countdown_bot.py
```

#### Testing Different Scenarios
```bash
# Test during F1 season
python f1_countdown_bot.py --debug

# Test during off-season
# (Bot should handle gracefully and post waiting message)

# Test error handling
# (Temporarily break something to test Discord notifications)
```

### PythonAnywhere Deployment

#### Step-by-Step PythonAnywhere Setup

1. **Upload Files**
   ```bash
   # Upload all files to your PythonAnywhere account
   # You can use the Files tab or git clone
   ```

2. **Set Up Virtual Environment**
   ```bash
   # In PythonAnywhere console
   cd /home/yourusername/F1-script
   python3.10 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**
   ```bash
   # Create .env file in your project directory
   nano .env
   # Add your Twitter API credentials and Discord webhook
   ```

4. **Test Installation**
   ```bash
   # Test discord webhook
   python3.10 test_discord.py
   
   # Test bot functionality
   python3.10 f1_countdown_bot.py --debug
   
   # Test actual tweet posting
   python3.10 f1_countdown_bot.py --test
   ```

5. **Set Up Scheduled Task**
   - Go to PythonAnywhere Dashboard
   - Navigate to "Tasks" → "Scheduled Tasks"
   - Create new task:
     ```bash
     # Command:
     cd /home/yourusername/F1-script && source venv/bin/activate && python f1_countdown_bot.py
     
     # Schedule: Daily at your preferred time
     # Hour: 15 (for 3 PM IST)
     # Minute: 0
     ```

6. **Monitor and Maintain**
   ```bash
   # Check logs
   cat /home/yourusername/F1-script/f1_countdown_bot.log
   
   # Manual test run
   cd /home/yourusername/F1-script && source venv/bin/activate && python f1_countdown_bot.py --debug
   ```

### Local Development Setup

#### Daily Development Routine
```bash
# 1. Activate virtual environment
source venv/bin/activate

# 2. Test current state
python f1_countdown_bot.py --debug

# 3. Make changes to code

# 4. Test changes
python f1_countdown_bot.py --debug

# 5. Test with actual posting (if needed)
python f1_countdown_bot.py --test
```

#### Testing Different Race Scenarios
```bash
# During race weekend
python f1_countdown_bot.py --debug
# Should show very low percentage (close to 0% or 100%)

# Mid-season between races
python f1_countdown_bot.py --debug
# Should show moderate percentage

# Off-season
python f1_countdown_bot.py --debug
# Should show waiting message for next season
```

### Monitoring and Maintenance

#### Regular Checks
```bash
# Check if bot is working correctly
python f1_countdown_bot.py --debug

# View recent logs
tail -50 f1_countdown_bot.log

# Test Discord notifications
python test_discord.py
```

#### Troubleshooting Commands
```bash
# Check Python environment
python --version
pip list

# Check configuration
cat config.ini

# Check environment variables (don't print sensitive values)
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('Twitter key set:', bool(os.getenv('TWITTER_CONSUMER_KEY'))); print('Discord set:', bool(os.getenv('DISCORD_WEBHOOK_URL')))"

# Test internet connectivity and F1 data access
python -c "import fastf1; print('FastF1 working')"

# Manual Twitter API test
python -c "
import os
import tweepy
from dotenv import load_dotenv
load_dotenv()
auth = tweepy.OAuthHandler(os.getenv('TWITTER_CONSUMER_KEY'), os.getenv('TWITTER_CONSUMER_SECRET'))
auth.set_access_token(os.getenv('TWITTER_ACCESS_TOKEN'), os.getenv('TWITTER_ACCESS_TOKEN_SECRET'))
api = tweepy.API(auth)
api.verify_credentials()
print('Twitter API working')
"
```

### Environment Variable Management

#### Creating Your .env File
```bash
# Method 1: Copy from example
cp env_example.txt .env
# Then edit .env with your actual credentials

# Method 2: Create manually
cat > .env << 'EOF'
TWITTER_CONSUMER_KEY=your_actual_consumer_key
TWITTER_CONSUMER_SECRET=your_actual_consumer_secret
TWITTER_ACCESS_TOKEN=your_actual_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_actual_access_token_secret
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN
DISCORD_SUCCESS_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR_SUCCESS_WEBHOOK_ID/YOUR_SUCCESS_WEBHOOK_TOKEN
EOF
```

#### Validating Environment Variables
```bash
# Check if all required variables are set
python -c "
import os
from dotenv import load_dotenv
load_dotenv()

required = ['TWITTER_CONSUMER_KEY', 'TWITTER_CONSUMER_SECRET', 'TWITTER_ACCESS_TOKEN', 'TWITTER_ACCESS_TOKEN_SECRET']
optional = ['DISCORD_WEBHOOK_URL', 'DISCORD_SUCCESS_WEBHOOK_URL']

print('Required Variables:')
for var in required:
    value = os.getenv(var)
    status = '✅ Set' if value else '❌ Missing'
    print(f'  {var}: {status}')

print('\\nOptional Variables:')
for var in optional:
    value = os.getenv(var)
    status = '✅ Set' if value else '⚠️  Not set'
    print(f'  {var}: {status}')
"
```

#### Security Best Practices
```bash
# Ensure .env file has proper permissions
chmod 600 .env

# Verify .env is in .gitignore
grep -q "^\.env$" .gitignore && echo "✅ .env is gitignored" || echo "❌ Add .env to .gitignore"

# Never commit .env file
git status --ignored  # Should show .env as ignored
```

### Common Workflows

#### First Time Setup
```bash
git clone <repo> && cd F1-script
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp config.ini.template config.ini
# Add credentials to .env file
python test_discord.py
python f1_countdown_bot.py --debug
python f1_countdown_bot.py --test
```

#### Deploy to PythonAnywhere
```bash
# Upload files, set up venv, add .env
python3.10 test_discord.py
python3.10 f1_countdown_bot.py --debug
python3.10 f1_countdown_bot.py --test
# Set up scheduled task
```

#### Regular Maintenance
```bash
source venv/bin/activate
python f1_countdown_bot.py --debug  # Check current status
tail -20 f1_countdown_bot.log        # Check recent activity
python test_discord.py              # Test notifications
```

#### Debugging Issues
```bash
python f1_countdown_bot.py --debug  # First step
cat f1_countdown_bot.log | grep ERROR  # Check for errors
python test_discord.py              # Test Discord
# Check Discord for error notifications
# Check PythonAnywhere task logs
```

#### Updating Dependencies
```bash
# Activate virtual environment
source venv/bin/activate

# Update all packages
pip install --upgrade -r requirements.txt

# Test after updates
python f1_countdown_bot.py --debug
python test_discord.py
```

#### Backup and Recovery
```bash
# Backup important files
tar -czf f1-bot-backup.tar.gz \
  f1_countdown_bot.py \
  config.ini \
  .env \
  requirements.txt \
  README.md

# Restore from backup
tar -xzf f1-bot-backup.tar.gz

# Verify after restore
python f1_countdown_bot.py --debug
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

## Progress Calculation

- **Progress** = Days elapsed since last race / Total days between races
- **Race Left** = 100% - Progress
- **Race Day** = 100% progress (0% race left)

## Error Handling

- **Data Fetch Failures**: Fibonacci retry intervals (1, 1, 2, 3, 5, 8... minutes)
- **Twitter API Issues**: Logged but doesn't trigger data retry
- **Off-Season**: Automatically posts waiting message if next year's calendar unavailable

## Logging

All activities are logged to:
- Console output
- `f1_countdown_bot.log` file

Log levels: INFO, WARNING, ERROR, CRITICAL

## Debug Console Output

The bot now includes comprehensive console output for debugging:

### Debug Information Displayed:
- **Startup Info**: Tweet time, cache location, current time
- **Race Data**: Next race, last race, dates
- **Progress Calculation**: Percentage calculations and race left
- **Tweet Content**: Full tweet with length and ASCII progress bar
- **Error Handling**: Detailed error messages and retry information

### Sample Debug Output:
```
🏁 F1 COUNTDOWN DEBUG INFO:
Next Race: Hungarian Grand Prix
Next Race Date: 2025-08-03
Last Race: British Grand Prix
Last Race Date: 2025-07-06
Progress: 17.86%
Race Left: 82.14%

============================================================
TWEET CONTENT:
============================================================
F1 Race Countdown: Hungarian Grand Prix
82.14% to go!
▓▓▓▓▓▓▓▓▓▓▓▓░░░ 82.14%
#F1 #Formula1 #Countdown
============================================================
Tweet length: 101 characters
============================================================
```

## File Structure

```
F1-script/
├── f1_countdown_bot.py      # Main script
├── config.ini               # Configuration file (create from template)
├── config.ini.template      # Configuration template
├── .env                     # Environment variables (create this file)
├── env_example.txt          # Example environment variables
├── test_discord.py          # Discord webhook test script
├── setup_discord.py         # Discord webhook setup helper
├── verify_setup.py          # Complete setup verification script
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── cache/                  # FastF1 cache directory
└── f1_countdown_bot.log    # Log file (created when running)
```

## Troubleshooting

### Common Issues

1. **Import Errors**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Authentication Failed**:
   - Check Twitter API credentials in `.env` file
   - Ensure all four environment variables are set correctly
   - Verify app permissions (Read and Write)

3. **No Race Data**:
   - Check internet connection
   - FastF1 may be updating data - wait and retry

4. **Permission Denied**:
   - Ensure write permissions for cache directory
   - Check log file permissions

5. **Discord Notifications Not Working**:
   - Check that `DISCORD_WEBHOOK_URL` and/or `DISCORD_SUCCESS_WEBHOOK_URL` are set in `.env` file
   - Verify webhook URLs are correct and accessible
   - Run `python test_discord.py` to test both webhooks
   - **Cloudflare Protection**: If you see "Access denied" errors from Discord, the bot uses `curl_cffi` to bypass Cloudflare protection. Make sure `curl_cffi>=0.7.0` is installed.
   - Test webhooks manually with a simple HTTP POST request

### Debug Mode

For detailed debugging, you can:

1. **Run in debug mode** (recommended):
   ```bash
   python f1_countdown_bot.py --debug
   ```

2. **Modify logging level** in `config.ini`:
   ```ini
   [logging]
   log_level = DEBUG
   ```

3. **Console output**: All runs now show detailed debug information automatically

## Running in Production

### Using PythonAnywhere (Recommended)

1. **Upload your project** to PythonAnywhere
2. **Set up environment variables**:
   - Go to your PythonAnywhere dashboard
   - Navigate to "Tasks" → "Scheduled Tasks"
   - Create a `.env` file in your project directory with your Twitter API credentials
   - The bot will automatically load these on startup

3. **Set up a daily task**:
   ```bash
   # Example: Run daily at 3:00 PM IST (9:30 AM UTC)
   python3.10 /home/yourusername/F1-script/f1_countdown_bot.py
   ```

4. **Test the setup**:
   ```bash
   # Run in debug mode first
   python3.10 /home/yourusername/F1-script/f1_countdown_bot.py --debug
   ```

### Using systemd (Linux)

1. Create a service file:
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

2. Enable and start:
   ```bash
   sudo systemctl enable f1-countdown-bot
   sudo systemctl start f1-countdown-bot
   ```

### Using Docker

```dockerfile
FROM python:3.13-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "f1_countdown_bot.py"]
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source. Please ensure compliance with Twitter's API terms of service and FastF1's usage guidelines.

## Quick Start

```bash
# 1. Set up project
git clone <repo> && cd F1-script
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp config.ini.template config.ini

# 2. Add credentials to .env file
touch .env
# Edit .env with your Twitter API keys and Discord webhook (optional)

# 3. Test setup
python test_discord.py                    # Test Discord (optional)
python f1_countdown_bot.py --debug        # Test bot (no tweets)
python f1_countdown_bot.py --test         # Test with actual tweet

# 4. Deploy to PythonAnywhere
# Upload files, set up venv, create .env, set up scheduled task
```

## Command Reference

| Command | Purpose | Authentication | Posts Tweet |
|---------|---------|---------------|------------|
| `python verify_setup.py` | Complete setup verification | ❌ No | ❌ No |
| `python f1_countdown_bot.py --debug` | Testing/debugging | ❌ No | ❌ No |
| `python f1_countdown_bot.py --test` | Single tweet test | ✅ Yes | ✅ Yes |
| `python f1_countdown_bot.py` | Production (cron) | ✅ Yes | ✅ Yes |
| `python f1_countdown_bot.py --schedule` | Self-managed | ✅ Yes | ✅ Yes |
| `python test_discord.py` | Test Discord webhook | ❌ No | ❌ No |

## Quick Troubleshooting

| Problem | Quick Fix |
|---------|-----------|
| Any setup issues | Run `python verify_setup.py` first |
| Import errors | `pip install -r requirements.txt` |
| Authentication failed | Check `.env` file credentials |
| No race data | Check internet, try again later |
| Discord not working | Run `python test_discord.py` |
| Bot not posting | Run `python f1_countdown_bot.py --debug` first |

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review log files for errors
3. Run in debug mode to see detailed output
4. Open an issue on the repository

---

**Note**: This bot requires constant internet connection and should be run on a reliable server for uninterrupted operation. 