import discord
from discord.ext import commands
import time
import asyncio

class Kick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def kick(self, ctx, target: discord.Member = None, reason: str = None):

        if not ctx.author.guild_permissions.kick_members:
            
            declinede = discord.Embed(title="", color=discord.Color.dark_blue())
            declinede.add_field(name="", value=f"missing guild permissions: kick members")

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
        
        if target.top_role > ctx.author.top_role:
            await ctx.send("cannot kick someone with a higher role than you")
            return
        
        if target.guild_permissions.administrator:
            await ctx.send("cannot kick administrators")
            return


        if reason is None:
            reason = "no reason specified"

        await target.kick(reason=reason)

        embed = discord.Embed(title="", color=discord.Color.dark_blue())

        embed.add_field(name="", value=f"{target} kicked by {ctx.author} for {reason}")

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Kick(bot))