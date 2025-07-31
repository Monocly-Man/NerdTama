# The Finals weapon data bot, by Monocly Man
# Created 30th of March 2025 in python version 3.12.1 (I can't be bothered to update)
# Last edited 24th June 2025
# TODO
    # Change to actively maintained env package
    # Migrate to slash command structure
    # Maybe rework weapons.json into separate files for each weapon?
    # Use pyplot and graph damage falloff??? Maybe can compare with other weapons?


import os
import json
import discord
import datetime
from dotenv import load_dotenv      # Using deprecated module cause this is a fork from an older project
from discord.ext import commands
from random import choice, sample

import alias
import equipment
import maps

# Variables
__version__ = str("0.3.1")
__gamever__ = str("7.6.0")
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


def random_loadout():
    spec = choice(equipment.CLASSES)

    if spec in equipment.CLASSES[0:3]:
        wep = choice(equipment.WEP_L)
        gad = sample(equipment.GAD_L, 3)

    elif spec in equipment.CLASSES[3:6]:
        wep = choice(equipment.WEP_M)
        gad = sample(equipment.GAD_M, 3)

    else:
        wep = choice(equipment.WEP_H)
        gad = sample(equipment.GAD_H, 3)

    return spec, wep, gad[0], gad[1], gad[2]


# Main
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

help_command = commands.DefaultHelpCommand(no_category="Commands")

bot = commands.Bot(
    command_prefix='t! ',
    help_command=help_command,
    intents=intents
)


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord! Running version {__version__}\n'
          f'{bot.user.name} is currently in {len(bot.guilds)} server/s:'
          )
    for guild in bot.guilds:
        print(guild.name)
    print('----------------------------------------')


@bot.command(name="get", help="Usage: t! get [weaponname]\n"
                              "Acquires the data of the named weapon. Aliases accepted.")
async def cmd_get(ctx):
    # Hacky fix to truncate the miliseconds and nanoseconds from datetime.now
    print(f"[{str(datetime.datetime.now())[0:19]}] cmd_get called by {ctx.author} in {ctx.guild}")
    user_message = ctx.message.content
    user_message = user_message.replace("t! get ", "")

    alias_result = search_alias(user_message.lower())

    if alias_result == 1:
        await ctx.send("Weapon not found.")
        return
    else:
        weapon = get_weapon(alias_result)
        response = weapon_embed(weapon)

    await ctx.send(embed=response)#, delete_after=20)


@bot.command(name="recoil", help="Usage: t! recoil [weaponname]\n"
                                 "Acquires the recoil pattern of the named weapon. Aliases accepted."
                                 "Recoil patterns taken at approximately 10 metres away.")
async def cmd_recoil(ctx):
    print(f"[{str(datetime.datetime.now())[0:19]}] cmd_recoil called by {ctx.author} in {ctx.guild}")
    user_message = ctx.message.content
    user_message = user_message.replace("t! recoil ", "")

    alias_result = search_alias(user_message.lower())

    if alias_result == 1:
        response = "Weapon not found."
    else:
        response = get_weapon(alias_result)['Recoil']

    await ctx.send(response)#, delete_after=20)


@bot.command(name="loadout", help="Usage: t! loadout\n"
                                  "Generates a random loadout.")
async def cmd_loadout(ctx):
    print(f"[{str(datetime.datetime.now())[0:19]}] cmd_loadout called by {ctx.author} in {ctx.guild}")
    spec, wep, gad0, gad1, gad2 = random_loadout()
    await ctx.send(f"{spec}, {wep} | {gad0}, {gad1}, {gad2}")


@bot.command(name="map", help="Usage: t! map\n"
                              "Randomly selects a map.")
async def cmd_map(ctx):
    print(f"[{str(datetime.datetime.now())[0:19]}] cmd_map called by {ctx.author} in {ctx.guild}")
    map = choice(maps.MAPS)
    await ctx.send(f"{map}")


@bot.command(name="version", help="Gets the current bot version and game version the bot is updated for.")
async def cmd_version(ctx):
    await ctx.channel.send(f"Running {bot.user.name} version {__version__}\n"
                           f"Updated for game version {__gamever__}\n")
    return

@bot.event
async def on_command_error(ctx, error):
    print(f"[{str(datetime.datetime.now())[0:19]}] invalid command by {ctx.author} in {ctx.guild}")
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("?")

# Runs bot
bot.run(TOKEN)
