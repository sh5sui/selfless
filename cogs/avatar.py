import discord
from discord.ext import commands

class Avatar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def avatar(self, ctx, target: discord.Member = None):

        if target is None:
            target = ctx.author

        await ctx.send(target.avatar.url)

    @commands.command()
    async def av(self, ctx, target: discord.Member = None):

        if target is None:
            target = ctx.author

        await ctx.send(target.avatar.url)

    @commands.command()
    async def serveravatar(self, ctx, target: discord.Member = None):

        if target is None:
            target = ctx.author

        if target.guild_avatar is None:
            await ctx.send(target.avatar.url)
            return
        
        await ctx.send(target.guild_avatar.url)

    @commands.command()
    async def sav(self, ctx, target: discord.Member = None):

        if target is None:
            target = ctx.author

        if target.guild_avatar is None:
            await ctx.send(target.avatar.url)
            return

        await ctx.send(target.guild_avatar.url)

async def setup(bot):
    await bot.add_cog(Avatar(bot))