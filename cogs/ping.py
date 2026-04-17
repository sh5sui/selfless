import discord
from discord.ext import commands
import time

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        start = time.monotonic()
        init = await ctx.send("pong")
        end = time.monotonic()

        initime = round(self.bot.latency * 1000)

        editinit = round((end - start) * 1000)

        embed = discord.Embed(title="", color=discord.Color.dark_blue())

        embed.add_field(name="", value=f"{initime}ms (edit: {editinit}ms)")

        await init.edit(content="", embed=embed)

async def setup(bot):
    await bot.add_cog(Ping(bot))