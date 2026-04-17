import discord
from discord.ext import commands
from collections import defaultdict

delmsg = defaultdict(list)

class S(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return

        delmsg[message.channel.id].append({
            "author": str(message.author),
            "msg": message.content,
            "time": message.created_at
        })

    @commands.command()
    async def s(self, ctx):
        channel_snipes = delmsg.get(ctx.channel.id)

        if not channel_snipes:
            await ctx.send("nothing to snipe")
            return

        last = channel_snipes[-1]

        embed = discord.Embed(description=last["msg"] or "*[no text content]*", timestamp=last["time"], color=discord.Color.dark_blue())
        embed.set_author(name=last["author"])
        embed.set_footer(text=f"{len(channel_snipes)} sniped message(s) in this channel")

        await ctx.send(embed=embed)

    @commands.command()
    async def cs(self, ctx):

        if ctx.channel.id in delmsg:
            del delmsg[ctx.channel.id]
            embed = discord.Embed(color=discord.Color.dark_blue())
            embed.add_field(name="", value="cleared snipes for this channel", inline=False)
            await ctx.send(embed=embed)
        else:
            embedd = discord.Embed(color=discord.Color.dark_blue())
            embedd.add_field(name="", value="no snipes to clear", inline=False)
            await ctx.send(embed=embedd)

async def setup(bot):
    await bot.add_cog(S(bot))