import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional

class BanCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="ban", description="Bans a user from the server.")
    @app_commands.describe(
        member="The user to ban",
        reason="The reason for the ban"
    )
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx: commands.Context, member: discord.Member, *, reason: Optional[str] = "No reason provided"):
        if member == ctx.author:
            await ctx.send("You cannot ban yourself.", ephemeral=True)
            return

        if ctx.author != ctx.guild.owner and member.top_role >= ctx.author.top_role:
            await ctx.send("You cannot ban this user as they have a higher or equal role.", ephemeral=True)
            return
        
        try:
            await member.ban(reason=reason)
            embed = discord.Embed(title="Ban", colour=0xdd2e44)
            embed.add_field(name="User", value=f"{member.mention} ({member.id})", inline=False)
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.set_footer(text=f"Moderator: {ctx.author.name}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"Failed to ban user: {e}", ephemeral=True)

    @commands.hybrid_command(name="unban", description="Unbans a user from the server.")
    @app_commands.describe(
        user="The user to unban (use their ID or Name#Tag)",
        reason="The reason for the unban"
    )
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx: commands.Context, user: discord.User, *, reason: Optional[str] = "No reason provided"):
        try:
            await ctx.guild.unban(user, reason=reason)
            embed = discord.Embed(title="Unban", colour=0x78b159)
            embed.add_field(name="User", value=f"{user.mention} ({user.id})", inline=False)
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.set_footer(text=f"Moderator: {ctx.author.name}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
            await ctx.send(embed=embed)
        except discord.NotFound:
            await ctx.send(f"User {user.name} is not banned.", ephemeral=True)
        except Exception as e:
            await ctx.send(f"Failed to unban user: {e}", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(BanCog(bot))