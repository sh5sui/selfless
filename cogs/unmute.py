import discord
from discord.ext import commands
import time
import asyncio

class Unmute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def unmute(self, ctx, target: discord.Member = None):

        if not ctx.author.guild_permissions.moderate_members:
            
            declinede = discord.Embed(title="", color=discord.Color.dark_blue())
            declinede.add_field(name="", value=f"missing guild permissions: moderate members")

            declined = await ctx.send(embed=declinede)

            await asyncio.sleep(3)

            await declined.delete()
            await ctx.message.delete()
            return
        
        if target is None:
            
            declinedem = discord.Embed(title="", color=discord.Color.dark_blue())
            declinedem.add_field(name="", value=f"must specify a target")

            declined = await ctx.send(embed=declinedem)

            await asyncio.sleep(3)

            await declined.delete()
            await ctx.message.delete()
            return

        if not target.is_timed_out():
            await ctx.send(f"{target} is not muted")
            return

        await target.edit(timed_out_until=None)

        embed = discord.Embed(title="", color=discord.Color.dark_blue())

        embed.add_field(name="", value=f"{target} unmuted by {ctx.author}")

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Unmute(bot))