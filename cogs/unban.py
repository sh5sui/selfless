import discord
from discord.ext import commands
import time
import asyncio

class Unban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def unban(self, ctx, targetid: str = None, reason: str = None):

        if not ctx.author.guild_permissions.ban_members:
            
            declinede = discord.Embed(title="", color=discord.Color.dark_blue())
            declinede.add_field(name="", value=f"missing guild permissions: ban members")

            declined = await ctx.send(embed=declinede)

            await asyncio.sleep(3)

            await declined.delete()
            await ctx.message.delete()
            return
        
        if targetid is None:
            
            declinedem = discord.Embed(title="", color=discord.Color.dark_blue())
            declinedem.add_field(name="", value=f"must specify an id")

            declined = await ctx.send(embed=declinedem)

            await asyncio.sleep(3)

            await declined.delete()
            await ctx.message.delete()
            return

        if reason is None:
            reason = "no reason specified"

        await targetid.unban(reason=reason)

        embed = discord.Embed(title="", color=discord.Color.dark_blue())

        embed.add_field(name="", value=f"{targetid} unbanned by {ctx.author} for {reason}")

        ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Unban(bot))