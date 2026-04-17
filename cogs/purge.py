import discord
from discord.ext import commands
import time
import asyncio

class Purge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def purge(self, ctx, amount: int):

        if not ctx.author.guild_permissions.manage_messages:
            
            declinede = discord.Embed(title="", color=discord.Color.dark_blue())
            declinede.add_field(name="", value=f"missing guild permissions: manage messages")

            declined = await ctx.send

            await asyncio.sleep(3)

            await declined.delete()
            await ctx.message.delete()
            return

        start = time.monotonic()

        deleted = await ctx.channel.purge(limit=amount + 1)

        end = time.monotonic()

        embed = discord.Embed(title="", color=discord.Color.dark_blue())

        timer = round((end - start) * 1000)

        count = len(deleted) - 1

        embed.add_field(name="", value=f"successfully purged {count} messages, took {timer}ms")

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Purge(bot))