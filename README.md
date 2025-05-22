# NerdTama
## Disclaimer: I am aware this is running on very obsolete code, however I have no short-term plans to migrate it to discord.ext 2.0.
I may migrate it in the future, however I'm currently busy with uni and can't really be bothered to migrate it over.

A Discord bot for THE FINALS. Currently running version 0.2.5, using Python 3.12. <br>
Requires the following python libraries: os, json, dotenv (deprecated, planned to be replaced), discord.ext (not migrated to 2.0) <br>
Heavily based off of my previous BolboBot project, which in turn was based on the [old Tekken 7 frame bot](https://github.com/BKNR/mokujin) by BKNR.
Please send all feedback/ideas to monocly_man on Discord, I don't check GitHub very often.

Weapon data acquired from [Zafferman's master sheet](https://docs.google.com/spreadsheets/d/1Ud7Rdl3AgMw9mmfDwW2LtDMnzZQ9IIhnqSE4ivsaMTs/edit?gid=2136619021#gid=2136619021), and the official patchnotes.

To use type "t! [COMMANDNAME] [WEAPONNAME]" in a Discord chat e.g. s! get akm <br>

## To install and run your own instance of NerdTama
- Download the files and extract to any particular location
- Install the dependencies listed above
- Create a Discord bot using the Discord Applications portal
- Create a file in the NerdTama folder called '.env'
- Inside the .env you should only have 2 lines:
>\# .env<br>
>DISCORD_TOKEN=[YOUR TOKEN HERE]
- Run main.py to connect to discord

## The files
main.py - The main body of the program. <br>
alias.py - A giant dictionary. Used to check for weapon aliases so the user can type common alises or shortened names. <br>
weapons.json - Contains a weapon data.
