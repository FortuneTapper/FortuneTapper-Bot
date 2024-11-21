import discord
from discord.ext import commands
import asyncio
import adapter.config as cfg

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    cfg.logger.info(f"{bot.user} is ready and commands are sync.")

async def load_extensions():
    await bot.load_extension("adapter.cogs.tap_cog")
    await bot.load_extension("adapter.cogs.character_cog")
    pass

async def main():
    await load_extensions()
    await bot.start(cfg.DISCORD_TOKEN)


asyncio.run(main())
