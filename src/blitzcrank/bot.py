import discord
import os
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv
import logging

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")
CLIENT_ID = os.getenv("DISCORD_CLIENT_ID")


logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready() -> None:
    print("We have logged in as {0.user}".format(bot))


# @bot.event
# async def on_message(message):
#     if message.author == bot.user:
#         return

#     return

def fetch_role_by_name(name: str) -> discord.Role:
    return get(member.server.roles, name=name)

@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f"Hi {member.name}, please head to #rules and type !agree to become a member.")

@bot.command()
@commands.has_role("admin")
async def kisses(ctx: commands.Context) -> None:
    response = "Muah muah muah"
    await ctx.send(response)

@bot.command(name="mentor")
async def mentor(ctx: commands.Context) -> None:
    member = ctx.message.author
    role = get(member.guild.roles, name='Mentor')
    await member.add_roles(role, reason="user requested")

@bot.command(name="agree")
async def member(ctx: commands.Context) -> None:
    member = ctx.message.author
    role = get(member.guild.roles, name='Member')
    await member.add_roles(role, reason="user accepted rules")

@bot.command(name="oauth2")
@commands.has_role("Admin")
async def oauth2_url(ctx: commands.Context) -> str:
    await ctx.send(discord.utils.oauth_url(CLIENT_ID))


bot.run(TOKEN)
