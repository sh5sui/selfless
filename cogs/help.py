import discord
from discord import ui
from discord.ext import commands

class HelpView(ui.LayoutView):
    def __init__(self, bot_avatar_url: str) -> None:
        super().__init__()

        container = ui.Container(
            ui.Section(
                ui.TextDisplay("### selfless"),
                ui.TextDisplay("` {} = optional, < > = required `"),
                accessory=ui.Thumbnail(media=bot_avatar_url)
            ),

            ui.Separator(),

            ui.TextDisplay("**utilities**"),
            ui.TextDisplay("**help** — shows this menu"),
            ui.TextDisplay("**ping** — displays the latency of the bot"),
            ui.Separator(),

            ui.TextDisplay("**server**"),
            ui.TextDisplay("**membercount** — displays the membercount of the server"),
            ui.TextDisplay("**serverinfo** — displays info about the server"),
            ui.Separator(),

            ui.TextDisplay("**anti raid**"),
            ui.Separator(),

            ui.TextDisplay("**messages**"),
            ui.TextDisplay("**purge** `<amount>` — deletes a certain amount of messages in a channel"),
            ui.TextDisplay("**s** — snipe the last deleted message"),
            ui.TextDisplay("**cs** - clear the snipes for the channel"),
            ui.Separator(),

            ui.TextDisplay("**members**"),
            ui.TextDisplay("**userinfo** `{target}` — shows the information for a specified user `requires manage messages`"),
            ui.Separator(),

            ui.TextDisplay("**lastfm**"),
            ui.TextDisplay("**fm setup** `<user>` - links your lastfm account to the bot"),
            ui.TextDisplay("**fm unlink** `<user>` - unlinks your lastfm account to the bot"),
            ui.TextDisplay("**fm** - shows your currently or last played track"),
            ui.TextDisplay("**fm help** - shows all the lastfm commands"),
            ui.Separator(),

            ui.TextDisplay("**staff**"),
            ui.TextDisplay("**ban** `<target> {reason}` — bans a member `requires ban members`"),
            ui.TextDisplay("**rr create** `<reaction> <role> <channel>` — creates a reactionrole message for the specified role in a specified channel `requires manage roles`"),
            ui.TextDisplay("**unban** `<userid> {reason}` — unbans a member `requires ban members`"),
            ui.TextDisplay("**kick** `<target> {reason}` — kicks a member `requires kick members`"),
            ui.TextDisplay("**mute** `<target> {reason}` — mutes a member `requires moderate members`"),
            ui.TextDisplay("**unmute** `<target> {reason}` — unmutes a member `requires moderate members`"),
            ui.TextDisplay("**role** `<target> <role>` — gives a member a role `requires manage roles`"),
            ui.TextDisplay("**roleall** `<role>` — gives all members in the server that role `requires manage roles`"),
            ui.Separator(),

            ui.TextDisplay("-# page 1/1 • selfless help"),

            ui.Separator(),

            accent_color=discord.Color.dark_blue(),

        )

        self.add_item(container)


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):

        await ctx.send(view=HelpView(bot_avatar_url=self.bot.user.avatar.url))

async def setup(bot):
    await bot.add_cog(Help(bot))