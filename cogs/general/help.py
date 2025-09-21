import discord
from discord.ext import commands
from discord import app_commands, Interaction

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="help")
    async def help_command(self, ctx):
        """Shows the list of commands"""
        embed = discord.Embed(
            title="List of commands",
            description="**Command prefix - !**\nhelp - Shows the list of commands",
            colour=0x26a269
        )

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(General(bot))