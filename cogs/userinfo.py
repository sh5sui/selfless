import discord
from discord.ext import commands
import time

class Userinfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def userinfo(self, ctx, target: discord.Member = None):

        if target is None:
            target = ctx.author

        embed = discord.Embed(color=discord.Color.dark_blue())

        embed.set_author(name="selfless", icon_url=self.bot.user.avatar.url)

        embed.set_thumbnail(url=target.avatar.url)

        embed.add_field(name="user", value=target.name, inline=False)
        embed.add_field(name="user id", value=target.id, inline=False)
        embed.add_field(name="creation time", value=target.created_at, inline=False)
        embed.add_field(name="joined time", value=target.joined_at, inline=False)
        embed.add_field(name="roles", value=" ".join([r.mention for r in target.roles[1:]]), inline=False)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Userinfo(bot))