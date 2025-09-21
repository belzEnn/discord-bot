import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv
# Import cogs
from cogs.general import help

load_dotenv()
TOKEN = os.getenv("TOKEN")

# Intents   
intents = discord.Intents.all()

# Command prefix
COMMAND_PREFIX = '!'
class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=COMMAND_PREFIX, intents=intents)
        # Remove default help command
        self.remove_command('help')

    async def setup_hook(self):
        # List of cogs to load
        cogs = [
            (help.General, "General")
        ]
    
        # Register cogs
        registered_cogs = set()
        for cog, name in cogs:
            if name not in registered_cogs:
                try:
                    if isinstance(cog, str):
                        await self.load_extension(cog)
                    else:
                        await self.add_cog(cog(self))
                    registered_cogs.add(name)
                    print(f"Loaded cog: {name}")
                except Exception as e:
                    print(f"Failed to load cog {name}: {e}")


bot = Bot()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        await bot.tree.sync()
    except Exception as e:
        print(f"Error syncing slash commands: {e}")

# Run the bot
if __name__ == "__main__":
    bot.run(TOKEN)