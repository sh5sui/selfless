import discord
from discord.ext import commands
from discord import ui
import asyncio
import sqlite3

def stes(syntax: str, example: str):
    return f"```ansi\n\u001b[2;34mSyntax: {syntax}\nExample: {example}\u001b[0m\n```"

class AntiRaidView(ui.LayoutView):
    def __init__(self, bot_avatar_url: str) -> None:
        super().__init__()

        container = ui.Container(
            ui.Section(
                ui.TextDisplay("### selfless help"),
                ui.TextDisplay("` {} = optional, < > = required `"),
                accessory=ui.Thumbnail(media=bot_avatar_url)
            ),
            ui.Separator(),

            ui.TextDisplay("**antiraid command usage**"),
            ui.TextDisplay("**,antiraid setup** `null`"),
            ui.TextDisplay("**,antiraid view** `null`"),
            ui.TextDisplay("**,antiraid (state)** `<enable/disable>`"),
            ui.TextDisplay("**,antiraid** `<flag>`"),

            accent_color=discord.Color.dark_blue()
        )

        self.add_item(container)


conn = sqlite3.connect("selfless.db")

cursor = conn.cursor()

class Antiraid(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def antiraid(self, ctx):

        await ctx.send(view=AntiRaidView(bot_avatar_url=self.bot.user.avatar.url))

    @antiraid.command()
    async def setup(self, ctx):

        if not ctx.author.guild_permissions.administrator:
            
            declinede = discord.Embed(title="", color=discord.Color.dark_blue())
            declinede.add_field(name="", value=f"missing guild permissions: administrator")

            declined = await ctx.send

            await asyncio.sleep(3)

            await declined.delete()
            await ctx.message.delete()
            return
        
        cursor.execute("SELECT guildid FROM guildid WHERE guildid = ?", (ctx.guild.id,))
        existing = cursor.fetchone()

        if existing:
            embed = discord.Embed(title="", color=discord.Color.dark_blue())
            embed.set_author(name="selfless", icon_url=self.bot.user.avatar.url)
            embed.add_field(name="", value="antiraid is already setup in this server, use ,antiraid modify to change any settings you have in place", inline=False)
            return
        
        cursor.execute("INSERT INTO guildid (guildid) VALUES (?)", (ctx.guild.id,))
        conn.commit()

    @antiraid.command()
    async def view(self, ctx):


        if not ctx.author.guild_permissions.administrator:
            
            declinede = discord.Embed(title="", color=discord.Color.dark_blue())
            declinede.add_field(name="", value=f"missing guild permissions: administrator")

            declined = await ctx.send

            await asyncio.sleep(3)

            await declined.delete()
            await ctx.message.delete()
            return
        
        pass

conn.close()

async def setup(bot):
    await bot.add_cog(Antiraid(bot))