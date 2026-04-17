import discord
from discord.ext import commands
from discord import ui
import asyncio
import sqlite3
import time

conn = sqlite3.connect("selfless.db")

cursor = conn.cursor()

def stes(syntax: str, example: str):
    return f"```ansi\n\u001b[2;34mSyntax: {syntax}\nExample: {example}\u001b[0m\n```"

class VoiceMasterView(ui.LayoutView):
    def __init__(self, bot_avatar_url: str) -> None:
        super().__init__()

        container = ui.Container(
            ui.Section(
                ui.TextDisplay("### selfless help"),
                ui.TextDisplay("` {} = optional, < > = required `"),
                accessory=ui.Thumbnail(media=bot_avatar_url)
            ),
            ui.Separator(),

            ui.TextDisplay("**voicemaster command usage**"),
            ui.TextDisplay("**,vc join** `null`"),
            ui.TextDisplay("**,vc lock** `null`"),
            ui.TextDisplay("**,vc unlock** `null`"),
            ui.TextDisplay("**,vc permit** `<target>`"),
            ui.TextDisplay("**,vc kick** `<target>`"),
            ui.TextDisplay("**,vc rename** `<name>`"),

            accent_color=discord.Color.dark_blue()
        )

        self.add_item(container)

class Voicemaster(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, aliases=["vc"])
    async def voicemaster(self, ctx):
        
        await ctx.send(view=VoiceMasterView(bot_avatar_url=self.bot.user.avatar.url))

    @voicemaster.command()
    async def setup(self, ctx):

        embed = discord.Embed(title="", color=discord.Color.dark_blue())
        embed.add_field(name="", value="setting up voicemaster...", inline=False)

        init = await ctx.send(embed=embed)

        start = time.monotonic()

        cate = await ctx.guild.create_category(name="voice channels")

        await ctx.guild.create_voice_channel(name="Join to create", category=cate)

        end = time.monotonic()

        final = f"{end - start:.2f}s"

        embede = discord.Embed(title="", color=discord.Color.dark_blue())
        embede.add_field(name="", value=f"voicemaster setup time took: {final}", inline=False)
        embede.add_field(name="", value=f"if you don't like the category name (voice channels) you can rename it or make a new one just make sure (Join to create) vc is still in the category or Join to create won't work")

        await init.edit(embed=embede)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):

        channel = after.channel

        if channel and channel.name == "Join to create":
            cate = discord.utils.get(member.guild.voice_channels, name="Join to create")
            if not cate:
                return
            categ = cate.category
            vc = await member.guild.create_voice_channel(name=f"{member.name}'s channel", category=categ)
            await member.move_to(vc)
            cursor.execute("INSERT INTO voice_channels VALUES (?, ?)", (vc.id, member.id))
            conn.commit()
            
        if before.channel:
            cursor.execute("SELECT owner_id FROM voice_channels WHERE channel_id = ?", (before.channel.id,))
            row = cursor.fetchone()
            if row and len(before.channel.members) == 0:
                await before.channel.delete()
                cursor.execute("DELETE FROM voice_channels WHERE channel_id = ?", (before.channel.id,))
                conn.commit()

    @voicemaster.command()
    async def claim(self, ctx):

        if not ctx.author.voice:
            await ctx.send("your not in a voice channel")
            return
        
        channel = ctx.author.voice.channel

        cursor.execute("SELECT owner_id FROM voice_channels WHERE channel_id = ?", (channel.id,))
        row = cursor.fetchone()

        if not row:
            await ctx.send("channel not registered")
            return

        ownerpresent = any(m.id == row[0] for m in channel.members)

        if ctx.author.id == row[0]:
            await ctx.send("can't claim your own channel")
            return

        if not ownerpresent:
            cursor.execute("DELETE FROM voice_channels WHERE channel_id = ?", (channel.id,))
            cursor.execute("INSERT INTO voice_channels (channel_id, owner_id) VALUES (?, ?)", (channel.id, ctx.author.id))
            conn.commit()
            await ctx.send(f"{ctx.author.mention} is now the owner of {channel.mention}")
        else:
            await ctx.send("owner hasn't left the call")
            return

    @voicemaster.command()
    async def join(self, ctx):

        if ctx.author.voice:
            cha = ctx.author.voice.channel
            await cha.connect()
            await ctx.guild.me.edit(deafen=True)
        else:
            embed = discord.Embed(color=discord.Color.dark_blue())
            embed.add_field(name="", value="your either not in a voice chat or im not able to join", inline=False)
            await ctx.send(embed=embed)
            return
        
    @voicemaster.command()
    async def unlock(self, ctx):

        if not ctx.author.voice:
            await ctx.send("your not in a voice channel")
            return
        
        channel = ctx.author.voice.channel

        cursor.execute("SELECT owner_id FROM voice_channels WHERE channel_id = ?", (channel.id,))
        row = cursor.fetchone()

        if not row or row[0] != ctx.author.id:
            await ctx.send("You don't own this channel.")
            return
        
        await channel.set_permissions(ctx.guild.default_role, connect=True)
        await ctx.send(f"{channel.mention} unlocked")        
        
    @voicemaster.command()
    async def lock(self, ctx):

        if not ctx.author.voice:
            await ctx.send("your not in a voice channel")
            return
        
        channel = ctx.author.voice.channel

        cursor.execute("SELECT owner_id FROM voice_channels WHERE channel_id = ?", (channel.id,))
        row = cursor.fetchone()

        if not row or row[0] != ctx.author.id:
            await ctx.send("You don't own this channel.")
            return
        
        await channel.set_permissions(ctx.guild.default_role, connect=False)
        await ctx.send(f"{channel.mention} locked")

    @voicemaster.command()
    async def permit(self, ctx, target: discord.Member = None):

        if target is None:
            
            await ctx.send(view=VoiceMasterView(bot_avatar_url=self.bot.user.avatar.url))
            return

        if not ctx.author.voice:
            await ctx.send("your not in a voice channel")
            return
        
        channel = ctx.author.voice.channel

        cursor.execute("SELECT owner_id FROM voice_channels WHERE channel_id = ?", (channel.id,))
        row = cursor.fetchone()

        if not row or row[0] != ctx.author.id:
            await ctx.send("You don't own this channel.")
            return
        
        await channel.set_permissions(target, connect=True)
        await ctx.send(f"{target} permitted to join {channel.mention}")

    @voicemaster.command()
    async def kick(self, ctx, target: discord.Member = None):

        if target is None:
            
            await ctx.send(view=VoiceMasterView(bot_avatar_url=self.bot.user.avatar.url))
            return

        if not ctx.author.voice:
            await ctx.send("your not in a voice channel")
            return
        
        channel = ctx.author.voice.channel

        cursor.execute("SELECT owner_id FROM voice_channels WHERE channel_id = ?", (channel.id,))
        row = cursor.fetchone()

        if not row or row[0] != ctx.author.id:
            await ctx.send("You don't own this channel.")
            return
        
        await channel.set_permissions(target, connect=False)
        await target.move_to(None)
        await ctx.send(f"{target} blocked from joining {channel.mention}")

    @voicemaster.command()
    async def rename(self, ctx, *, name: str = None):

        if name is None:
            
            await ctx.send(view=VoiceMasterView(bot_avatar_url=self.bot.user.avatar.url))
            return

        if not ctx.author.voice:
            await ctx.send("your not in a voice channel")
            return
        
        channel = ctx.author.voice.channel

        cursor.execute("SELECT owner_id FROM voice_channels WHERE channel_id = ?", (channel.id,))
        row = cursor.fetchone()

        if not row or row[0] != ctx.author.id:
            await ctx.send("You don't own this channel.")
            return
        
        await channel.edit(name=name)
        await ctx.send(f"{channel.mention} renamed to {name}")

async def setup(bot):
    await bot.add_cog(Voicemaster(bot))