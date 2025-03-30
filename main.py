# The Finals weapon data bot, by Monocly Man
# Created 30th of March 2025 in python version 3.12.1 (I can't be bothered to update)
# Last edited 31st March 2025
# TODO
    # Change to actively maintained env package
    # Migrate to slash command structure
    # Maybe rework weapons.json into separate files for each weapon?
    # Get all recoil patterns (fml that's gonna take a while)
    # Use pyplot and graph damage falloff??? Maybe can compare with other weapons?


import os
import json
import discord
from dotenv import load_dotenv      # Using deprecated module cause this is a fork from an older project
from discord.ext import commands

import alias

# Variables
__version__ = str("0.2.3.3")
__gamever__ = str("6.1.0")
dirname = os.path.dirname(__file__)
imglink = str("https://mywikis-eu-wiki-media.s3.eu-central-2.wasabisys.com/thefinals/")


# Functions
def get_weapon(weapon_name):
    filepath = dirname + "/weapons.json"
    with open(filepath) as weapons_file:
        contents = weapons_file.read()
    weapons_json = json.loads(contents)

    weapon_details = list(filter(lambda x: (x['Weapon'].lower() == weapon_name), weapons_json))
    return weapon_details[0]


def weapon_embed(weapon):
    imgname = weapon['Weapon'].replace(" ", "_")

    embed = discord.Embed(title=weapon['Weapon'] + " - " + __gamever__, colour=0x1f3c80)
    if weapon['Weapon'] == "CB-01 Repeater":  # Wiki misspelled the image name
        embed.set_thumbnail(url="https://mywikis-eu-wiki-media.s3.eu-central-2.wasabisys.com/thefinals/CB-01_Reapeater_Rank_1.png")
    else:
        embed.set_thumbnail(url=imglink + imgname + "_Rank_1.png")

    for value in weapon:
        if value == "Weapon" or value == "Recoil":
            continue
        else:
            embed.add_field(name=value, value=weapon[value])

    return embed


def search_alias(weapon_name):
    weapon_alias = list(filter(lambda x: (weapon_name in x["alias"]), alias.WEAPON_NAMES))
    if weapon_alias:
        name = weapon_alias[0]["name"]
        return name
    else:
        return 1


# Main
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='s! ', intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord! Running version {__version__}\n'
          f'----------------------------------------'
          )


@bot.command(name="get", help="Acquires the data of the named weapon. Aliases accepted.")
async def cmd_get(ctx):
    user_message = ctx.message.content
    user_message = user_message.replace("s! get ", "")

    alias_result = search_alias(user_message.lower())

    if alias_result == 1:
        await ctx.send("Weapon not found.")
        return
    else:
        weapon = get_weapon(alias_result)
        response = weapon_embed(weapon)

    await ctx.send(embed=response)#, delete_after=20)


@bot.command(name="recoil", help="Acquires the recoil pattern of the named weapon. Aliases accepted.")
async def cmd_recoil(ctx):
    user_message = ctx.message.content
    user_message = user_message.replace("s! recoil ", "")

    alias_result = search_alias(user_message.lower())

    if alias_result == 1:
        response = "Weapon data not found."
    else:
        response = get_weapon(alias_result)['Recoil']

    await ctx.send(response)#, delete_after=20)

@bot.command(name="version", help="Gets the current bot version and game version the bot is updated for.")
async def cmd_version(ctx):
    await ctx.channel.send(f"Running ScottyBot version {__version__}\n"
                           f"Updated for game version {__gamever__}\n")
    return


# Runs bot
bot.run(TOKEN)
