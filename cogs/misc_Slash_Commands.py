import discord
from discord.ext import commands
from discord import app_commands


class Question(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Slash Cogs Loaded")

    @commands.command()
    @commands.is_owner()
    async def sync(self, ctx) -> None:
        fmt = await ctx.bot.tree.sync(guild=ctx.guild)
        await ctx.send(f"synced{len(fmt)} commands.")

    # Pings the Discord Bot (ms)
    @app_commands.command(name="ping", description="Ping Slash")
    async def ping(self, interactions: discord.Interaction):
        await interactions.response.send_message(f'Pong! {round(self.client.latency * 1000)}ms')

    # panda command sends a Gif of a Panda
    @app_commands.command(name="panda", description="maybe the panda loves you :)")
    async def panda(self, ctx: discord.Interaction):
        await ctx.response.send_message("https://media.giphy.com/media/N6funLtVsHW0g/giphy.gif")

    # Hippo Command sends a Gif of a Hippo
    @app_commands.command(name="hippo", description="maybe the hippo loves you :)")
    async def hippo(self, ctx: discord.Interaction):
        await ctx.response.send_message(
            "https://giphy.com/gifs/FZHO7QURk1pH1zdVex")






async def setup(client):
    client.remove_command("help")
    await client.add_cog(Question(client), guilds=[discord.Object(id="1041205088657616898")])
