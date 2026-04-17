import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio
import sqlite3

load_dotenv()

token = os.getenv("token")

bot = commands.Bot(command_prefix=",", intents=discord.Intents.all(), help_command=None)

cmds = os.listdir("cogs")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

    await bot.change_presence(activity=discord.Streaming(name="selfless on top", url="https://www.twitch.tv/placeholder"))

    conn = sqlite3.connect("selfless.db")

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS guildid (
            guildid INTEGER PRIMARY KEY,
            logsid INTEGER NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lastfm (
            userid INTEGER PRIMARY KEY,
            username TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS voice_channels (
            channel_id INTEGER PRIMARY KEY,
            owner_id INTEGER NOT NULL
        )
    """)

    conn.commit()
    conn.close()

async def main():
    async with bot:
        for i in cmds:
            if i.endswith(".py"):
                await bot.load_extension(f"cogs.{i[:-3]}")
        await bot.start(token)

asyncio.run(main())