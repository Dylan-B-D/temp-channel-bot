# Discord Bot

A simple Discord bot with various functionalities including temporary channels and message auto-deletion.

## Features

- **!settempchannel**: Create temporary channels where messages get automatically deleted after a specified time.
- **!clear**: Manually delete all messages in a temporary channel.
- **!setcleartime [minutes]**: Adjust the auto-deletion time for messages in a temporary channel.
- **!info**: View temporary channels in server, and the clear time for the channels.
- **!removetempchannel**: Removes a temp channel from being a temp channel.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Dylan-B-D/temp-channel-bot
   ```
2. Rename `config-example.ini` to `config.ini`
3. Add your bot token to config.ini
4. Make sure you have Python installe
5. Run the following in Command Prompt/terminal
   ```bash
   pip install discord configparser
   ```
6. Run `python bot.py`

