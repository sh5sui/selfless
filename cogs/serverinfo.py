import discord
from discord.ext import commands
import time

class Serverinfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def serverinfo(self, ctx):

        embed = discord.Embed(color=discord.Color.dark_blue())

        embed.set_author(name="selfless", icon_url=self.bot.user.avatar.url)

        embed.set_thumbnail(url=ctx.guild.icon.url)

        embed.add_field(name="server", value=ctx.guild.name, inline=False)
        embed.add_field(name="server id", value=ctx.guild.id, inline=False)
        embed.add_field(name="creation time", value=discord.utils.format_dt(ctx.guild.created_at, style="R"), inline=False)
        embed.add_field(name="roles", value=" ".join([r.mention for r in ctx.guild.roles[1:]]), inline=False)
        embed.add_field(name="member count", value=ctx.guild.member_count, inline=False)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Serverinfo(bot))