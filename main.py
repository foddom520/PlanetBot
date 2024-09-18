import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
import logging

logging.basicConfig(level=logging.ERROR)

bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())

logger = logging.getLogger("bot")

@bot.event
async def on_connect():
    print("Bot connected to discord!")
    await sync_commands()

@bot.event
async def on_ready():
    print("Bot ready!")

async def sync_commands():
    try:
        synced_commands = await bot.tree.sync()
        print(f"Synced {len(synced_commands)} commands successfully!")
    except Exception as e:
        print(f"Error syncing application commands: {e}")

@bot.event
async def on_command_error(ctx, error):
    logger.error("Error in command %s: %s", ctx.command, error)
    await ctx.send(f"Error: {error}")

async def load_cogs():
    for filename in os.listdir("./Cogs"):
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"Cogs.{filename[:-3]}")
            except Exception as e:
                logger.error("Error loading cog %s: %s", filename, e)

async def main():
    async with bot:
        await load_cogs()
        await bot.start(os.getenv("TOKEN"))

if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())