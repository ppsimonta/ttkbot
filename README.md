# Discord Bot for Warzone Meta Information

This Discord bot provides users with up-to-date information about the top 20 long-range weapons in Call of Duty: Warzone, based on their Time-to-Kill (TTK). It uses Selenium to scrape data from the website.

---

## Features

- Fetches and displays the top 20 long-range weapons with their respective TTK values.
- Simple commands for ease of use.
- Implements cooldowns to prevent spamming.

---

## Prerequisites

Ensure you have the following:

- **Discord Developer Token**  
  Create a bot application on the [Discord Developer Portal](https://discord.com/developers/applications) and copy the bot token.  
  Replace the `TOKEN` variable in the script with your bot's token:
  ```python
  TOKEN = 'your-discord-bot-token'
