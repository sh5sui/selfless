import discord
from discord.ext import commands
import time
import asyncio
from datetime import timedelta, datetime

class Mute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def mute(self, ctx, target: discord.Member = None, time: str = None, *, reason: str = None):

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
        
        if time is None:
            await ctx.send("no time specified")
            return
        
        if target is ctx.author:
            await ctx.send("can't mute yourself")
            return

        if target.guild_permissions.administrator:
            await ctx.send("cannot mute administrators")
            return

        if target.top_role > ctx.author.top_role:
            await ctx.send("cannot mute someone with a higher role than you")
            return

        if reason is None:
            reason = "no reason specified"

        units = {"s": "seconds", "m": "minutes", "h": "hours", "d": "days"}
        unit = time[-1]
        amount = time[:-1]

        if unit not in units or not amount.isdigit():
            await ctx.send("enter a valid time such as 30s, 30m, 30h, 30d")
            return

        method = units[unit]

        await target.timeout(timedelta(**{method: int(amount)}), reason=reason)

        embed = discord.Embed(title="", color=discord.Color.dark_blue())

        embed.add_field(name="", value=f"{target} muted by {ctx.author} for {reason}")

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Mute(bot))