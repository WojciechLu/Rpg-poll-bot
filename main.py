from prettytable import PrettyTable as pt
import asyncio
import os
import nextcord
from nextcord.ext import commands
from nextcord import Client, Intents, Interaction, SlashOption
import logging
import sqlite3
from typing import Optional
import discord
from dotenv import load_dotenv
from Helpers.helper import Helper
import datetime

# consts
if load_dotenv():
    TOKEN = os.getenv('TOKEN')
else:
    TOKEN = os.environ["TOKEN"]


# logger
logger = logging.getLogger('nextcord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(
    filename='nextcord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# intents

intents = Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.messages = True
intents.reactions = True

# bot
bot = commands.Bot(command_prefix="$",
                   description="Opis bota, moze dziala", intents=intents)

# stale do testowanie - potem dodac do bazy danych
messages = []

print("Run bot")

# bot events

@bot.event
async def on_ready():
    global messages
    print(f'We have logged in as {bot.user}')

# bot commands

@bot.slash_command(guild_ids=[1030024780314845234, 693775903532253254, 870607350946463795])
async def ping(ctx):
    await ctx.send("Pong")

@bot.slash_command(guild_ids=[1030024780314845234, 693775903532253254, 870607350946463795])
async def members(interaction: Interaction, person: str, description: str):
    names = [x.name for x in ctx.guild.members]
    await ctx.send(names)

@bot.slash_command(guild_ids=[1030024780314845234, 693775903532253254, 870607350946463795])
async def create_rpg_poll(interaction: Interaction, rpg_system: Optional[str]):
    """Create Rpg poll for next week

    Parameters
    ----------
    interaction: Interaction
        The interaction object
    ranking_name: Optional[str]
        Type ranking name or leave blank if there is only 1 ranking in your server!
    """
    if rpg_system is None:
        rpg_system = "DnD"
    some_url = "https://fallendeity.github.io/discord.py-masterclass/"
    embed = discord.Embed(
        title="Title",
        description="Description",
        url=some_url,
        color=discord.Color.random(),
        timestamp=datetime.datetime.utcnow()
    )
    embed.add_field(name="Field name", value="Color sets that <")
    embed.add_field(name="Field name", value="Color should be an integer or discord.Colour object")
    embed.add_field(name="Field name", value="You can't set image width/height")
    embed.add_field(name="Non-inline field name", value="The number of inline fields that can shown on the same row is limited to 3", inline=False)
    embed.set_author(name="Author", url=some_url,
                     icon_url="https://cdn.discordapp.com/attachments/1112418314581442650/1124820259384332319/fd0daad3d291ea1d.png")
    embed.set_image(url="https://cdn.discordapp.com/attachments/1028706344158634084/1124822236801544324/ea14e81636cb2f1c.png")
    embed.set_thumbnail(url="https://media.discordapp.net/attachments/1112418314581442650/1124819948317986926/db28bfb9bfcdd1f6.png")
    embed.set_footer(text="Footer", icon_url="https://cdn.discordapp.com/attachments/1112418314581442650/1124820375587528797/dc4b182a87ecee3d.png")
    await interaction.response.send_message(embed=embed)

    

bot.run(TOKEN)
