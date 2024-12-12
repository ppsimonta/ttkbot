# Warzone Meta Discord Bot

This Discord bot helps players find the best weapon loadouts and attachments for **Call of Duty: Warzone** based on the current meta.

The bot fetches tier and weapon data from [Warzone Loadout](https://warzoneloadout.games/warzone-meta/), allowing users to select tiers and weapons, and then view the recommended attachments (meta) for those weapons.

## Features

- **Tier Selection**: Users can choose a tier, and then pick a weapon from that tier.
- **Gun Selection**: After selecting a tier, the bot will show all available guns in that tier. The user can then select a gun.
- **Meta Information**: After selecting a gun, the bot will fetch the recommended attachments (meta) for that specific weapon.

## Setup and Installation

1. Clone this repository to your local machine.
2. Install the necessary dependencies:

   ```bash
   pip install requests beautifulsoup4 discord.py
