# F1 Race Countdown Bot 🏁

An automated Python bot that posts daily Formula 1 race countdown tweets with visual progress bars. The bot tracks the time between F1 races and posts daily updates showing the progress towards the next race.

## About the Project

This bot automatically posts tweets at 3:00 PM IST daily, displaying:
- **Race Progress**: Percentage completion between races
- **Visual Progress Bars**: ASCII art showing countdown progress
- **Race Information**: Current and next race details
- **Smart Season Handling**: Automatically transitions between seasons

The bot uses official F1 data from the FastF1 library and includes robust error handling with Fibonacci retry intervals for data fetch failures.

## Security

This repository is designed with security in mind:
- ✅ **No hardcoded credentials** - All API keys are stored in environment variables
- ✅ **Template-based configuration** - Users must provide their own credentials
- ✅ **Secure .gitignore** - Prevents accidental commit of sensitive files
- ✅ **Interactive setup** - Prompts users to input their own webhook URLs

**Important**: Never commit your `.env` file or `config.ini` file to version control. These files contain sensitive API credentials.

## Features

- 🏎️ **Daily Automated Tweets** at 3:00 PM IST
- 📊 **Visual Progress Tracking** with ASCII progress bars
- 🔄 **Off-Season Handling** with automatic season transitions
- 🛡️ **Robust Error Handling** with smart retry mechanisms
- 🔔 **Discord Notifications** for success/error alerts
- 🧪 **Debug Mode** for testing without posting tweets

## Quick Start

### Prerequisites

- Python 3.13+
- Twitter Developer Account
- Discord Server (optional, for notifications)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/F1-script.git
   cd F1-script
   ```

2. **Set up virtual environment**
   ```bash
   python3.13 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure the bot**
   ```bash
   cp config.ini.template config.ini
   cp env_example.txt .env
   ```

4. **Set up Twitter API credentials**
   - Go to [Twitter Developer Portal](https://developer.twitter.com/)
   - Create a new app and generate API keys
   - Edit `.env` file with your credentials:
     ```env
     TWITTER_CONSUMER_KEY=your_consumer_key_here
     TWITTER_CONSUMER_SECRET=your_consumer_secret_here
     TWITTER_ACCESS_TOKEN=your_access_token_here
     TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret_here
     ```

5. **Set up Discord webhooks (optional)**
   - Create webhooks in your Discord server
   - Add to `.env` file:
     ```env
     DISCORD_WEBHOOK_URL=your_webhook_url_here
     DISCORD_SUCCESS_WEBHOOK_URL=your_success_webhook_url_here
     ```

6. **Test the setup**
   ```bash
   python verify_setup.py
   python f1_countdown_bot.py --debug
   ```

## Usage

### Running Modes

| Command | Purpose | Posts Tweet |
|---------|---------|-------------|
| `python f1_countdown_bot.py --debug` | Test mode (no tweets) | ❌ |
| `python f1_countdown_bot.py --test` | Single tweet test | ✅ |
| `python f1_countdown_bot.py` | Production mode | ✅ |

### Example Tweet Output

```
F1 Race Countdown: Monaco Grand Prix
52.00% to go!
▓▓▓▓▓▓▓▓░░░░░░░ 52.00%
#F1 #Formula1 #Countdown
```

## Configuration

Edit `config.ini` to customize:

```ini
[settings]
tweet_time = 15:00          # 24-hour format
timezone = Asia/Kolkata     # Your timezone
cache_location = ./cache/   # Cache directory

[logging]
log_level = INFO
log_file = f1_countdown_bot.log
```

## Deployment

### PythonAnywhere (Recommended)

1. Upload files to PythonAnywhere
2. Set up virtual environment and install dependencies
3. Create `.env` file with your credentials
4. Set up scheduled task to run daily at your desired time

### Docker

```dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "f1_countdown_bot.py"]
```

### Cron Job (Linux/macOS)

```bash
# Add to crontab -e
0 15 * * * cd /path/to/F1-script && source venv/bin/activate && python f1_countdown_bot.py
```

## Troubleshooting

### Common Issues

- **Import errors**: Run `pip install -r requirements.txt`
- **Authentication failed**: Check `.env` file credentials
- **No race data**: Check internet connection
- **Discord not working**: Run `python test_discord.py`

### Debug Mode

Run in debug mode to see detailed output:
```bash
python f1_countdown_bot.py --debug
```

## File Structure

```
F1-script/
├── f1_countdown_bot.py      # Main bot script
├── config.ini.template      # Configuration template
├── env_example.txt          # Environment variables example
├── verify_setup.py          # Setup verification
├── test_discord.py          # Discord webhook test
├── requirements.txt         # Python dependencies
├── README.md               # This file
└── cache/                  # FastF1 cache directory
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
3. Run in debug mode for detailed output
4. Open an issue on the repository

---

**Note**: This bot requires constant internet connection and should be run on a reliable server for uninterrupted operation.