import discord
import os
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")

bot = commands.Bot(command_prefix="!")


@bot.event
async def on_ready():
    print("We have logged in as {0.user}".format(bot))


# @bot.event
# async def on_message(message):
#     if message.author == bot.user:
#         return

#     return

roles = [
]


@bot.event
async def on_member_join(member):
    pass
    # await member.create_dm()
    # await member.dm_channel.send(f"Hi {member.name}, welcome to my Discord server!")
    # role = get(member.server.roles, name='Member')
    # member = member or bot.message.author
    # await member.add_roles(role, reason="given on join")

@bot.command()
@commands.has_role("admin")
async def kisses(ctx):
    response = "Muah muah muah"
    await ctx.send(response)

@bot.command(name="mentor")
@commands.has_role("mentor")
async def mentor(ctx: commands.Context):
    member = ctx.message.author
    role = get(member.guild.roles, name='Mentor')
    await member.add_roles(role, reason="user requested")

@bot.command(name="agree")
async def member(ctx: commands.Context):
    print("Making member")
    member = ctx.message.author
    role = get(member.guild.roles, name='Member')
    await member.add_roles(role, reason="user accepted rules")



bot.run(TOKEN)
