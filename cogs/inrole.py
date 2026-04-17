import discord
from discord.ext import commands
import time
import asyncio

class Inrole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def inrole(self, ctx, role: discord.Role = None):

        if not ctx.author.guild_permissions.manage_roles:
            
            declinede = discord.Embed(title="", color=discord.Color.dark_blue())
            declinede.add_field(name="", value=f"missing guild permissions: manage roles")

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
        
        perms = [perm.replace("_", " ").title() for perm, value in role.permissions if value]
        value = "\n".join(perms) or "none"
        
        embed = discord.Embed(title="", color=discord.Color.dark_blue())
        embed.add_field(name=f"Details about role {role}", value="", inline=False)
        embed.add_field(name="name", value=f"{role.name}", inline=False)
        embed.add_field(name="id", value=f"{role.id}", inline=False)
        embed.add_field(name="members", value="\n".join(m.mention for m in role.members), inline=False)
        embed.add_field(name="permissions", value=value[:1024], inline=False)
        embed.add_field(name="created at", value=f"{role.created_at}", inline=False)
        embed.add_field(name="icon", value=f"{role.icon}", inline=False)
        embed.add_field(name="position", value=f"{role.position}", inline=False)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Inrole(bot))