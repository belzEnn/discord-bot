import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv
# Import cogs
from cogs import general

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
        cogs = [general.General]
        
        # Register cogs
        registered_cogs = set()
        for cog in cogs:
            if cog.__name__ not in registered_cogs:
                try:
                    await self.add_cog(cog(self))
                    registered_cogs.add(cog.__name__)
                    print(f"Loaded cog: {cog.__name__}")
                except Exception as e:
                    print(f"Failed to load cog {cog.__name__}: {e}")


bot = Bot()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        await bot.tree.sync()
        print("Slash commands synced!")
    except Exception as e:
        print(f"Error syncing slash commands: {e}")
    
    print("Use !help or /help to see available commands")

# Run the bot
if __name__ == "__main__":
    bot.run(TOKEN)