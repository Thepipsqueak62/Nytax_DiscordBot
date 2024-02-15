import discord
from discord.ext import commands
from discord import app_commands
import Paginator

H1 = discord.Embed(title="Command List", description="List of  Usable Prefix(!) and SlashCommands")
welcome = discord.Embed(title="Nytaks",
                        description="Hello My Name is Kijin i'm a Python Developer \n"
                                    "Nytax is General Purpose Bot Better than Mee6 :)s"
                                    ,
                        color=0x115599)
welcome.add_field(name="What now?", value="Use the Previous, Next Buttons to Navigate ")
H1.add_field(name="Help Command", value="use /help for a list of commands ")

embeds = [
    welcome.set_image(url=""),
    H1.set_thumbnail(
        url=""),
]


class HelpCommand(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Slash Cogs Loaded")

    # Bot help Command
    @app_commands.command(name="help", description="help command")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def help(self, ctx):
        PreviousButton = discord.ui.Button(style=discord.ButtonStyle.blurple, label="Previous")
        NextButton = discord.ui.Button(style=discord.ButtonStyle.blurple, label="Next")
        InitialPage = 0
        timeout = 100  # Seconds to timeout. Default is 60
        ephemeral = True  # Defaults t
        await Paginator.Simple(
            PreviousButton=PreviousButton,
            NextButton=NextButton,
            InitialPage=InitialPage,
            timeout=timeout, ephemeral=ephemeral).start(ctx, pages=embeds, )


async def setup(client):
    client.remove_command("help")
    await client.add_cog(HelpCommand(client), guilds=[discord.Object(id="1041205088657616898")])
