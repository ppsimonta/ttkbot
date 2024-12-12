import requests
from bs4 import BeautifulSoup
import discord
from discord.ext import commands


TOKEN = 'your token'


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

def get_tiers():
    tier_dict = {}
    url_dict = {}
    url = "https://warzoneloadout.games/warzone-meta/"

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    tier_section = soup.find_all('section', class_="new_mobile-tier-section")

    for section in tier_section:
        tier = section.find('h2', class_="new_tier-title")
        tier_name = tier.text
        names = section.find_all('h3', class_="new_weapon-name")
        labels = section.find_all('div', class_="loadoutlabelbo6")

        guns = []
        for index_name, name in enumerate(names):
            gun_name = name.text
            guns.append(gun_name)
            label = labels[index_name]
            styles = label.find_all("span", "new_weapon-playstylebo6")
            url_dict[gun_name] = styles[-1].text
        tier_dict[tier_name] = guns

    return tier_dict, url_dict

def get_meta(gun, url_dict):
    game = url_dict[gun]
    gun_url = gun.replace(" ", "-").replace(".", "-").lower()
    url = f"https://warzoneloadout.games/{game}/{gun_url}/"
    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')
    rows = soup.find('div', class_="attachments_weapondetailled")
    if rows is None:
        rows = soup.find('div', class_="attachments_container_loadouts")

    attachments = []
    for row in rows:
        try:
            label = row.find('span', class_='attachment_label_weapondetailled').text.strip(':')
            name = row.find('span', class_='attachment_name_weapondetailled').text
        except AttributeError:
            label = row.find('div', class_='detail-new-attachment__slot_loadouts').text.strip(':')
            name = row.find('div', class_='detail-new-attachment__name_loadouts').text
        attachments.append(f"{label}: {name}")

    return attachments



#botti hommat
tier_dict, url_dict = get_tiers()

user_state = {}

@bot.command()
async def meta(ctx):
    """Start the tier and gun selection process"""
    user_state[ctx.author.id] = {"step": "tier", "attempts": 0}
    tiers = "\n".join([f"{index + 1}: {tier}" for index, tier in enumerate(tier_dict.keys())])
    await ctx.send(f"Choose a tier by sending its number:\n{tiers}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    user_id = message.author.id
    if user_id in user_state:
        state = user_state[user_id]

        if state["step"] == "tier":
            try:
                tier_index = int(message.content) - 1
                tier_list = list(tier_dict.keys())

                if tier_index < 0 or tier_index >= len(tier_list):
                    state["attempts"] += 1
                    if state["attempts"] >= 2:
                        await message.channel.send("Loppu se spämmi.")
                        del user_state[user_id]
                        return

                    await message.channel.send("Invalid tier number. Please try again.")
                    return

                selected_tier = tier_list[tier_index]
                user_state[user_id]["tier"] = selected_tier
                user_state[user_id]["step"] = "gun"
                user_state[user_id]["attempts"] = 0

                guns = "\n".join([f"{index + 1}: {gun}" for index, gun in enumerate(tier_dict[selected_tier])])
                await message.channel.send(f"Now choose a gun by sending its number:\n{guns}")
            except ValueError:
                state["attempts"] += 1
                if state["attempts"] >= 2:
                    await message.channel.send("Loppu se spämmi.")
                    del user_state[user_id]
                    return
                await message.channel.send("Please send a valid number.")

        elif state["step"] == "gun":
            try:
                gun_index = int(message.content) - 1
                selected_tier = user_state[user_id]["tier"]
                guns_list = tier_dict[selected_tier]

                if gun_index < 0 or gun_index >= len(guns_list):
                    state["attempts"] += 1
                    if state["attempts"] >= 2:
                        await message.channel.send("Loppu se spämmi.")
                        del user_state[user_id]
                        return

                    await message.channel.send("Invalid gun number. Please try again.")
                    return

                selected_gun = guns_list[gun_index]
                user_state[user_id]["gun"] = selected_gun
                user_state[user_id]["step"] = None  # End the process
                user_state[user_id]["attempts"] = 0

                attachments = get_meta(selected_gun, url_dict)
                attachments_message = "\n".join(attachments)

                await message.channel.send(f"Meta for {selected_gun}:\n{attachments_message}")

                # Clear user state
                del user_state[user_id]
            except ValueError:
                state["attempts"] += 1
                if state["attempts"] >= 2:
                    await message.channel.send("Loppu se spämmi.")
                    del user_state[user_id]
                    return
                await message.channel.send("Please send a valid number.")

        return

    await bot.process_commands(message)

@bot.command()
async def coms(ctx):
    """List all available commands and explain the meta command"""
    commands_list = """
    **Available Commands:**
    1. `!meta` - Starts the tier and gun selection process for Warzone. 
       - First, you'll select a tier (e.g., 1, 2).
       - Then, you'll choose a gun within that tier (e.g., 1, 2).
       - After selecting the gun, the bot will provide the recommended attachments (meta) for that gun.
    """
    await ctx.send(commands_list)

bot.run(TOKEN)