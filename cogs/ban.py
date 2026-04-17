import discord
from discord.ext import commands
import time
import asyncio

class Ban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ban(self, ctx, target: discord.Member = None, reason: str = None):

        if not ctx.author.guild_permissions.ban_members:
            
            declinede = discord.Embed(title="", color=discord.Color.dark_blue())
            declinede.add_field(name="", value=f"missing guild permissions: ban members")

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
        
        if target is ctx.author:
            await ctx.send("can't ban yourself")
            return
        
        if target.top_role > ctx.author.top_role:
            await ctx.send("cannot ban someone with a higher role than you")
            return

        if reason is None:
            reason = "no reason specified"

        await target.ban(reason=reason)

        embed = discord.Embed(title="", color=discord.Color.dark_blue())

        embed.add_field(name="", value=f"{target} banned by {ctx.author} for {reason}")

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Ban(bot))
