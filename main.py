import discord
from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager  


TOKEN = 'tipilleeikerrota'


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


def fetch_meta_info():
    chrome_service = Service(ChromeDriverManager().install())
    chrome_options = Options()
    chrome_options.add_argument("--headless")  

    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    driver.get('https://wzstats.gg/warzone/meta/long-range-meta')

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'table'))
    )

    name_part_elements = driver.find_elements(By.CLASS_NAME, "name-part")
    ttk_part_elements = driver.find_elements(By.CLASS_NAME, "table-stats-display-container")

    ttk = []
    weapons = []

    for element in name_part_elements:
        weapons.append(element.text)

    for i in range(0, len(ttk_part_elements), 4):
        ttk.append(ttk_part_elements[i].text)

    combined = list(zip(weapons, ttk))
    combined = [(weapon, float(ttk_value.replace(',', ''))) for weapon, ttk_value in combined]


    combined.sort(key=lambda x: x[1])


    top_20_combined = combined[:20] 


    message = ""
    for index, (weapon, ttk_value) in enumerate(top_20_combined, 1):
        message += f"{index}. Weapon: {weapon}, TTK: {ttk_value}\n"

    driver.quit()

    return message

@bot.command()
@commands.cooldown(1, 60, commands.BucketType.user)  
async def meta(ctx):
    try:
        meta_message = fetch_meta_info()
        await ctx.send(meta_message)
    except Exception as e:
        await ctx.send("Tapahtui virhe: " + str(e))


@meta.error
async def meta_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"Voit lähettää viestin minuutin välein. Yritä uudelleen {round(error.retry_after, 2)} sekunnin kuluttua.")


@bot.command()
async def commands(ctx):
    help_message = """
**Tässä ovat käytettävissä olevat komennot:**
1. `!meta` - Long range meta top20.
"""
    await ctx.send(help_message)


@bot.event
async def on_ready():
    print(f'{bot.user} on valmiina!')  

bot.run(TOKEN)
