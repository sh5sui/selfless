import discord
from discord.ext import commands
from discord import ui
import requests
import sqlite3
import os
import urllib.parse

conn = sqlite3.connect("selfless.db")
cursor = conn.cursor()

class FmView(ui.LayoutView):
    def __init__(self, bot_avatar_url: str) -> None:
        super().__init__()

        container = ui.Container(
            ui.Section(
                ui.TextDisplay("### selfless help"),
                ui.TextDisplay("` {} = optional, < > = required `"),
                accessory=ui.Thumbnail(media=bot_avatar_url)
            ),
            ui.Separator(),

            ui.TextDisplay("**fm command usage**"),
            ui.TextDisplay("**,fm** `null`"),
            ui.TextDisplay("**,fm setup** `<user>`"),
            ui.TextDisplay("**,fm unlink** `null`"),
            ui.TextDisplay("**,fm help** `null`"),
            ui.TextDisplay("**,fm toptracks** `<target>`"),
            ui.TextDisplay("**,fm topartists** `<target>`"),

            accent_color=discord.Color.dark_blue()
        )

        self.add_item(container)

def get_playing(username):
        
        usernames = urllib.parse.quote(username.strip())

        url = "http://ws.audioscrobbler.com/2.0/"
        params = {
            "method": "user.getrecenttracks",
            "user": usernames,
            "api_key": os.getenv("fmapi"),
            "format": "json",
            "limit": 1
        }

        try:
            r = requests.get(url, params=params)
            r.raise_for_status()
            data = r.json()
        except requests.RequestException as e:
            print(f"request failed: {e}")
            return None

        tracks = data.get("recenttracks", {}).get("track", [])
        if not tracks:
            return None
        
        track = tracks[0]

        playing = "@attr" in track and track["@attr"].get("nowplaying") == "true"

        images = track.get("image", [])
        cover = next((img["#text"] for img in reversed(images) if img.get("#text")), None)

        artist = track["artist"]["#text"]
        name = track["name"]

        tir = requests.get(url=url, params={
            "method": "track.getInfo",
            "user": usernames,
            "artist": artist,
            "track": name,
            "api_key": os.getenv("fmapi"),
            "format": "json"
        })

        ti = tir.json().get("track", {})
        playcount = ti.get("userplaycount", 0)

        uir = requests.get(url=url, params={
            "method": "user.getInfo",
            "user": usernames,
            "api_key": os.getenv("fmapi"),
            "format": "json"
        })

        ui = uir.json().get("user", {})
        totalscrobbles = ui.get("playcount", 0)

        return{
            "artist": track["artist"]["#text"],
            "name": track["name"],
            "album": track.get("album", {}).get("#text", "unknown"),
            "now_playing": playing,
            "cover": cover,
            "playcount": playcount,
            "totalscrobbles": totalscrobbles
        }

class Fm(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def fm(self, ctx):

        cursor.execute("SELECT username FROM lastfm WHERE userid = ?", (ctx.author.id,))
        res = cursor.fetchone()
        lastfmuser = res[0] if res else None

        if lastfmuser is None:
            await ctx.send("use ,fm setup first")
            return
        
        data = get_playing(lastfmuser)

        if not data:
            await ctx.send("unable to fetch data")
            return

        embed = discord.Embed(color=discord.Color.dark_blue())
        embed.set_author(name=f"Last.fm: {lastfmuser}", icon_url=ctx.author.avatar.url)
        embed.set_thumbnail(url=data["cover"])
        embed.add_field(name="track", value=data["name"], inline=True)
        embed.add_field(name="artist", value=data["artist"], inline=False)
        embed.set_footer(text=f"Playcount: {data['playcount']} ∙ Total Scrobbles: {data['totalscrobbles']} ∙ Album: {data['album']}")

        await ctx.send(embed=embed)

    @fm.command()
    async def setup(self, ctx, user: str = None):

        data = get_playing(user)

        if data is None:
            await ctx.send("that user doesn't exist")
            return

        cursor.execute("SELECT username FROM lastfm WHERE userid = ?", (ctx.author.id,))
        res = cursor.fetchone()
        lastfmuser = res[0] if res else None

        if user is None:
            await ctx.send("you must provide a user")
            return

        if lastfmuser != None:
            await ctx.send("you already linked your account, if you want to unlink do ,fm unlink")
            return
        else:
            cursor.execute("INSERT INTO lastfm (userid, username) VALUES (?, ?)", (ctx.author.id, user,))
            conn.commit()
            await ctx.send(f"linked your lastfm to {user} you can now use all commands")

    @fm.command()
    async def help(self, ctx):

        await ctx.send(view=FmView(bot_avatar_url=self.bot.user.avatar.url))

    @fm.command()
    async def unlink(self, ctx):

        cursor.execute("SELECT username FROM lastfm WHERE userid = ?", (ctx.author.id,))
        res = cursor.fetchone()
        lastfmuser = res[0] if res else None

        if lastfmuser is None:
            await ctx.send("you don't have your account linked yet")
            return
        else:
            cursor.execute("DELETE FROM lastfm WHERE userid = ?", (ctx.author.id,))
            conn.commit()
            await ctx.send(f"deleted {lastfmuser} from your account")

    @fm.error
    async def fm_error(ctx, error):
        if isinstance(error, commands.errors.CommandNotFound):
            await ctx.send("unknown command, run ,fm help to see all available commands")
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"command on cooldown for {error.retry_after:.1f}s")

async def setup(bot):
    await bot.add_cog(Fm(bot))