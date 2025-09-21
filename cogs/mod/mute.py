import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime, timedelta
from typing import Optional
import re

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def parse_time(self, time_str: str) -> float:
        """Convert time string to minutes"""
        time_dict = {"s": 1/60, "m": 1, "h": 60, "d": 1440}
        match = re.match(r"(\d+)([smhd])", time_str.lower())
        if not match:
            raise ValueError("Invalid time format. Use <number><s/m/h/d> (e.g. 30m, 1h, 1d)")
        number, unit = match.groups()
        return float(number) * time_dict[unit]

    @commands.hybrid_command(name="mute", description="Mute a user")
    @app_commands.describe(
        member="The user to mute",
        duration="Duration (e.g. 30s, 5m, 1h, 1d)",
        reason="Reason for mute"
    )
    @commands.has_permissions(moderate_members=True)
    async def mute(
        self, 
        ctx, 
        member: discord.Member,
        duration: str,
        reason: Optional[str] = "No reason provided"
    ):
        if member.top_role >= ctx.author.top_role:
            await ctx.send("You can't mute this user!", ephemeral=True)
            return

        try:
            duration_minutes = self.parse_time(duration)
            until_time = discord.utils.utcnow() + timedelta(minutes=duration_minutes)
            await member.timeout(until_time, reason=reason)
            
            # Create the embed with the new format
            embed = discord.Embed(title="Mute",
                                  colour=0xe66100)
            embed.add_field(name="User",
                            value=member.mention,
                            inline=False)
            embed.add_field(name="Duration",
                            value=duration,
                            inline=False)
            embed.add_field(name="Reason",
                            value=reason,
                            inline=False)
            embed.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
            
            await ctx.send(embed=embed)

        except ValueError as e:
            await ctx.send(str(e), ephemeral=True)
        except Exception as e:
            await ctx.send(f"Failed to mute user: {e}", ephemeral=True)

    @commands.hybrid_command(name="unmute", description="Unmute a user")
    @app_commands.describe(
        member="The user to unmute",
        reason="Reason for unmute"
    )
    @commands.has_permissions(moderate_members=True)
    async def unmute(
        self, 
        ctx, 
        member: discord.Member,
        reason: Optional[str] = "No reason provided"
    ):
        if member.top_role >= ctx.author.top_role:
            await ctx.send("You can't unmute this user!", ephemeral=True)
            return

        try:
            await member.timeout(None, reason=reason)
            
            embed = discord.Embed(title="Unmute",
                                  colour=0x26a269) # Green color
            embed.add_field(name="User",
                            value=member.mention,
                            inline=False)
            embed.add_field(name="Reason",
                            value=reason,
                            inline=False)
            embed.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
            
            await ctx.reply(embed=embed)

        except Exception as e:
            await ctx.send(f"Failed to unmute user: {e}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Moderation(bot))