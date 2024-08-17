import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
import pyautoreload

bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("Bot ready!")
    try:
        synced_commands = await bot.tree.sync()
        print(f"Synced {len(synced_commands)} commands.")
    except Exception as e:
        print("an error with syncing application commands has occoured: ", e)

load_dotenv()
TOKEN = os.getenv("TOKEN")

async def load():
    for filename in os.listdir("./Cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"Cogs.{filename[:-3]}")

async def main():
    async with bot:
        await load()
        await bot.start(TOKEN)

asyncio.run(main())