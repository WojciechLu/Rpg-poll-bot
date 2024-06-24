from prettytable import PrettyTable as pt
import asyncio
import os
import nextcord
from nextcord.ext import commands
from nextcord import Client, Intents, Interaction, SlashOption, Embed, Color, Role, AllowedMentions
import logging
import sqlite3
from typing import Optional
from dotenv import load_dotenv
from Helpers.helper import Helper
from Helpers.poll import Poll, PollMedia, PollAnswer
from Helpers.datetimeHelper import next_weekday, translate_weekday, get_next_week_range_format
import datetime
import requests
import json
from datetime import timedelta, date

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
async def ping(interaction: Interaction):
    await interaction.response.send_message("Pong")

@bot.slash_command(guild_ids=[1030024780314845234, 693775903532253254, 870607350946463795])
async def find_date_message_type(interaction: Interaction, role: Role, rpg_system: Optional[str]):
    """Create Rpg poll for next week

    Parameters
    ----------
    interaction: Interaction
        The interaction object
    role: Role
        Role for pinging interested members
    ranking_name: Optional[str]
        Type ranking name or leave blank if there is only 1 ranking in your server!
    """

    message = await interaction.response.send_message(f'<@&{role.id}>', delete_after=True, allowed_mentions=nextcord.AllowedMentions(roles=True))
    emoji=["🔴","🟠","🟡","🟢","🔵"]
    todayDate = datetime.date.today()
    nextMonady = next_weekday(todayDate, 0)

    if rpg_system is None:
        rpg_system = "DnD"

    embed = nextcord.Embed(
        title=f'Wybór dnia na tydzień {get_next_week_range_format(todayDate)}',
        color=nextcord.Color.random(),
        timestamp=datetime.datetime.now()
    )
    embed.add_field(name="", value=f'{role.mention} pora na wybór dnia na kolejny tydzień! Gramy w **{rpg_system}**.')
    for x in range(len(emoji)):
        day = nextMonady + timedelta(days=x)
        embed.add_field(name="", value=f"**{day.strftime("%d.%m")}** {translate_weekday(day.weekday())} - {emoji[x]}", inline=False)
    
    emoji.append("😔")
    embed.add_field(name="", value=f"Skip ten tydzień - {emoji[-1]}", inline=False)
    if(interaction.response.is_done()):
        await interaction.followup.send(embed=embed)
        message: nextcord.Message
        async for message in interaction.channel.history():
            if not message.embeds:
                continue
            if message.embeds[0].title == embed.title and message.embeds[0].colour == embed.colour:
                for x in emoji:
                    await message.add_reaction(x)
                break
        else:
            return

@bot.slash_command(guild_ids=[1030024780314845234, 693775903532253254, 870607350946463795])
async def find_date_poll_type(interaction: Interaction, role: Role, rpg_system: str, weekend: Optional[bool]):
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

    if weekend is None:
        weekend = False
    todayDate = datetime.date.today()

    message = await interaction.response.send_message(f'{role.mention} pora na wybór dnia na kolejny tydzień **{get_next_week_range_format(todayDate)}**! Gramy w **{rpg_system}**.', allowed_mentions=nextcord.AllowedMentions(roles=True))
    nextMonady = next_weekday(todayDate, 0)
    
    emoji=["🔴","🟠","🟡","🟢","🔵"]
    if weekend:
        emoji.append("🟣")
        emoji.append("⚪")

    question = PollMedia(f'Jaki termin Ci pasuje?')
    aswersList = []
    for x in range(len(emoji)):
        day = nextMonady + timedelta(days=x)
        aswersList.append(PollAnswer(PollMedia(f"{translate_weekday(day.weekday())} ({day.strftime("%d.%m")})", emoji[x])))
    aswersList.append(PollAnswer(PollMedia(f"Skip ten tydzień", "😔")))

    poll = Poll(question, aswersList, 7 * 24, True)

    channelId = interaction.channel_id
    body = {"poll": json.loads(poll.toJSON())}
    headers = {'Authorization': f'Bot {TOKEN}'}

    resp = requests.post(f'https://discord.com/api/v10/channels/{channelId}/messages', json=body, headers=headers)

bot.run(TOKEN)
