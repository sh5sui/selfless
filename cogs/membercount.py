import discord
from discord.ext import commands
import time

class Membercount(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def membercount(self, ctx):

        embed = discord.Embed(title="", color=discord.Color.dark_blue())
        embed.add_field(name="", value=f"Member count for server {ctx.guild.name} is {ctx.guild.member_count}")

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Membercount(bot))