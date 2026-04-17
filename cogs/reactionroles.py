import discord
from discord.ext import commands
from discord import ui
from collections import defaultdict
import asyncio

delmsg = defaultdict(list)

class ReactionRolesView(ui.LayoutView):
    def __init__(self, bot_avatar_url: str) -> None:
        super().__init__()

        container = ui.Container(
            ui.Section(
                ui.TextDisplay("### selfless help"),
                ui.TextDisplay("` {} = optional, < > = required `"),
                accessory=ui.Thumbnail(media=bot_avatar_url)
            ),
            ui.Separator(),

            ui.TextDisplay("**reactionrole command usage**"),
            ui.TextDisplay("**,rr create** `<reaction> <role> <channelid>`"),

            accent_color=discord.Color.dark_blue()
        )

        self.add_item(container)

class ReactionRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reactionrolemsg = {}

    @commands.group(invoke_without_command=True, aliases=["rr"])
    async def reactionroles(self, ctx):
        
        await ctx.send(view=ReactionRolesView(bot_avatar_url=self.bot.user.avatar.url))

    @reactionroles.command()
    async def create(self, ctx, reaction: str = None, role: discord.Role = None, channelid: int = None):

        channel = ctx.guild.get_channel(channelid)

        if not ctx.author.guild_permissions.manage_roles:
            
            declinede = discord.Embed(title="", color=discord.Color.dark_blue())
            declinede.add_field(name="", value=f"missing guild permissions: manage roles")

            declined = await ctx.send(embed=declinede)

            await asyncio.sleep(3)

            await declined.delete()
            await ctx.message.delete()
            return

        if reaction is None:
            
            await ctx.send("no reaction")
            await ctx.send(view=ReactionRolesView(bot_avatar_url=self.bot.user.avatar.url))
            return
        
        if role is None:

            await ctx.send("no role")
            await ctx.send(view=ReactionRolesView(bot_avatar_url=self.bot.user.avatar.url))
            return
        
        if channel is None:

            await ctx.send("no channel")
            await ctx.send(view=ReactionRolesView(bot_avatar_url=self.bot.user.avatar.url))
            return
        
        chan = ctx.guild.get_channel(channel.id)

        embed = discord.Embed(title="selfless reaction roles",color=discord.Color.dark_blue())
        embed.add_field(name="", value=f"react to claim role {role.mention}", inline=False)

        msg = await chan.send(embed=embed)

        await msg.add_reaction(reaction)

        self.reactionrolemsg[msg.id] = {
            "roleid": role.id,
            "emoji": str(reaction)
        }

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):

        if user.bot:
            return
        
        msgid = reaction.message.id

        if msgid not in self.reactionrolemsg:
            return
        
        data = self.reactionrolemsg[msgid]

        if str(reaction.emoji) != data["emoji"]:
            return
        
        g = reaction.message.guild
        r = g.get_role(data["roleid"])

        if r:
            m = g.get_member(user.id)
            await m.add_roles(r)

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):

            msgid = reaction.message.id

            if msgid not in self.reactionrolemsg:
                return
            
            data = self.reactionrolemsg[msgid]

            if str(reaction.emoji) != data["emoji"]:
                return
            
            g = reaction.message.guild
            r = g.get_role(data["roleid"])

            if r:
                m = g.get_member(user.id)
                await m.remove_roles(r)

async def setup(bot):
    await bot.add_cog(ReactionRoles(bot))