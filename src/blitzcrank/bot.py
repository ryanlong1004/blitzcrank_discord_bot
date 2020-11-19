import discord
import os
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv
import logging
from blitzcrank.cogs.admin_utilities import AdminUtilities
from blitzcrank.cogs.permissions import Permissions

def main():
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
        logging.info("We have logged in as {0.user}".format(bot))


    # @bot.event
    # async def on_message(message):
    #     if message.author == bot.user:
    #         return

    #     return

    @bot.event
    async def on_member_join(member):
        await member.create_dm()
        await member.dm_channel.send(f"Hi {member.name}, please head to #rules and type !agree to become a member.")

    bot.add_cog(Permissions(bot))
    bot.add_cog(AdminUtilities(bot, CLIENT_ID))
    bot.run(TOKEN)

if __name__ == "__main__":
    main()
