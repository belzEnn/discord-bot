import discord
from discord.ext import commands

class HelpSelect(discord.ui.Select):
    def __init__(self, author: discord.User):
        options = [
            discord.SelectOption(label="General", value="General", description="General commands"),
            discord.SelectOption(label="Moderation", value="Moderation", description="Moderation commands")
        ]
        super().__init__(placeholder="Choose a category...", min_values=1, max_values=1, options=options)
        self.author = author

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.author.id:
            await interaction.response.send_message("You can't use this menu.", ephemeral=True)
            return

        if self.values[0] == "General":
            embed = discord.Embed(
                title="General commands",
                description="`help` - shows the list of commands",
                colour=0x26a269
            )
            await interaction.response.edit_message(embed=embed, view=self.view)
        if self.values[0] == "Moderation":
            embed = discord.Embed(
                title="Moderation commands",
                description="`ban <member> <reason>` - Ban user\n`unban <member> <reason>` - Unban user\n`mute <member> <duration>` - Mute user\n`unmute <member> <reason>` - Unmute user\n\n-# To use these commands, you must have administrator privileges.",
                colour=0x26a269
            )
            await interaction.response.edit_message(embed=embed, view=self.view)


class HelpView(discord.ui.View):
    def __init__(self, author: discord.User):
        super().__init__(timeout=60)
        self.add_item(HelpSelect(author))

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="help")
    async def help_command(self, ctx):
        embed = discord.Embed(
            title="List of commands",
            description="**General**\n`help`\n\n**Moderation**\n`ban`, `unban`, `mute`, `unmute`",
            colour=0x26a269
        )
        view = HelpView(ctx.author)
        await ctx.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(General(bot))