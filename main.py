import discord
from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager  
import time


TOKEN = 'asdasd'


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

#ar
def fetch_ar_info():
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
async def ar_meta(ctx):
    try:
        ar_meta_message = fetch_ar_info()
        await ctx.send(ar_meta_message)
    except Exception as e:
        await ctx.send("Tapahtui virhe: " + str(e))


@ar_meta.error
async def ar_meta_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"Voit lähettää viestin minuutin välein. Yritä uudelleen {round(error.retry_after, 2)} sekunnin kuluttua.")


@bot.command()
async def coms(ctx):
    help_message = """
**Tässä ovat käytettävissä olevat komennot:**
1. `!ar_meta` - Long range meta top20.
2. `!smg_meta` - Smg meta top20.
3. `!sniper_meta` - Sniper tiedot.
"""
    await ctx.send(help_message)


@bot.event
async def on_ready():
    print(f'{bot.user} on valmiina!')  


#smg
def fetch_smg_info():
    chrome_service = Service(ChromeDriverManager().install())
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    driver.get('https://wzstats.gg/warzone/meta/close-range-meta')

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'table'))
    )

    name_part_elements_smg = driver.find_elements(By.CLASS_NAME, "name-part")
    ttk_part_elements_smg = driver.find_elements(By.CLASS_NAME, "table-stats-display-container")

    ttk_smg = []
    weapons_smg = []

    for element in name_part_elements_smg:
        weapons_smg.append(element.text)

    for i in range(0, len(ttk_part_elements_smg), 4):
        ttk_smg.append(ttk_part_elements_smg[i].text)

    combined = list(zip(weapons_smg, ttk_smg))
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
async def smg_meta(ctx):
    try:
        smg_meta_message = fetch_smg_info()
        await ctx.send(smg_meta_message)
    except Exception as e:
        await ctx.send("Tapahtui virhe: " + str(e))

@smg_meta.error
async def smg_meta_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"Voit lähettää viestin minuutin välein. Yritä uudelleen {round(error.retry_after, 2)} sekunnin kuluttua.")

#sniper
def fetch_sniper_info():
    chrome_service = Service(ChromeDriverManager().install())
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    driver.get('https://wzstats.gg/warzone/meta/sniper-meta')

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'table'))
    )

    sn_name_part_elements = driver.find_elements(By.CLASS_NAME, "name-part")
    sn_info_part_elements = driver.find_elements(By.CLASS_NAME, "table-stats-display-container")

    sn_info = []
    sn_weapons = []

    for element in sn_name_part_elements:
        sn_weapons.append(element.text)

    for element in sn_info_part_elements:
        sn_info.append(element.text)

    info_chunks = [sn_info[i:i + 4] for i in range(0, len(sn_info), 4)]

    info_fields = ["One shot(m)", "ADS(ms)", "BV(ms)", "Mobility"]

    combined = []
    for weapon, info in zip(sn_weapons, info_chunks):
        named_info = dict(zip(info_fields, info))
        combined.append((weapon, named_info))

    message = ""
    for index, (weapon, info) in enumerate(combined, 1):
        info_message = ", ".join([f"{key}: {value}" for key, value in info.items()])
        message += f"{index}. {weapon}, {info_message}\n"

    driver.quit()

    return message

@bot.command()
@commands.cooldown(1, 60, commands.BucketType.user)
async def sniper_meta(ctx):
    try:
        sniper_meta_message = fetch_sniper_info()
        await ctx.send(sniper_meta_message)
    except Exception as e:
        await ctx.send("Tapahtui virhe: " + str(e))

@sniper_meta.error
async def sniper_meta_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"Voit lähettää viestin minuutin välein. Yritä uudelleen {round(error.retry_after, 2)} sekunnin kuluttua.")

# AR OSAT
def fetch_ar_parts():
    chrome_service = Service(ChromeDriverManager().install())
    chrome_options = Options()
    
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    driver.get('https://wzstats.gg/warzone-2/guns/long-range/ar')

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'content-container-article'))
    )

    scroll_nb = 20
    page_height = driver.execute_script("return document.body.scrollHeight")
    scrolls = round(page_height / scroll_nb)

    for x in range(scroll_nb):
        driver.execute_script(f"window.scrollBy(0, {scrolls})")
        time.sleep(1)

    gun_name_elements = driver.find_elements(By.CLASS_NAME, "article-card-header")
    
     # Extract and print the names of the guns
    gun_names = [element.text for element in gun_name_elements]
    print(gun_names)
    
    driver.quit()



# Lisää testauslohko
if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "test":
        try:
            print("Fetching AR info for testing...")
            result = fetch_ar_parts()
            print(result)
        except Exception as e:
            print("Tapahtui virhe:", e)
    else:
        bot.run(TOKEN)

