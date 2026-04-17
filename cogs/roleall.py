import discord
from discord.ext import commands
from collections import defaultdict
import asyncio
import time

class Roleall(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def roleall(self, ctx, role: discord.Role = None):

        if not ctx.author.guild_permissions.administrator:
            
            declinede = discord.Embed(title="", color=discord.Color.dark_blue())
            declinede.add_field(name="", value=f"missing guild permissions: administrator")

            declined = await ctx.send(embed=declinede)

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
        
        embedd = discord.Embed(color=discord.Color.dark_blue())
        embedd.add_field(name="", value=f"adding {role} to all applicable members")

        init = await ctx.send(embed=embedd)
        
        start = time.monotonic()
        
        count = 0
        async for member in ctx.guild.fetch_members(limit=None):
            if role not in member.roles:
                await member.add_roles(role)
                count+=1

        end = time.monotonic()

        embed = discord.Embed(color=discord.Color.dark_blue())
        embed.add_field(name="", value=f"sucessfully added role {role} to {count} members", inline=False)
        embed.add_field(name="", value=f"time taken: {end - start:2.f}s", inline=False)

        await init.edit(embed=embed)

async def setup(bot):
    await bot.add_cog(Roleall(bot))