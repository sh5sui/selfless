import discord
from discord.ext import commands
import time
import asyncio

class Role(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def role(self, ctx, target: discord.Member = None, role: discord.Role = None):

        if not ctx.author.guild_permissions.manage_roles:
            
            declinede = discord.Embed(title="", color=discord.Color.dark_blue())
            declinede.add_field(name="", value=f"missing guild permissions: manage roles")

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
        
        if role is None:

            declinedemb = discord.Embed(title="", color=discord.Color.dark_blue())
            declinedemb.add_field(name="", value=f"must specify a role")

            declined = await ctx.send(embed=declinedemb)

            await asyncio.sleep(3)

            await declined.delete()
            await ctx.message.delete()
            return
        
        if ctx.author.top_role < role:
            await ctx.send("cannot give someone a higher role than your top role")
            return

        await target.add_roles(role)

        embed = discord.Embed(title="", color=discord.Color.dark_blue())
        embed.add_field(name="", value=f"added role {role} to {target}", inline=False)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Role(bot))