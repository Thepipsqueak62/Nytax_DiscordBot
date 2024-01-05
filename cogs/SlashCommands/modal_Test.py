import discord
from discord.ext import commands
from discord import app_commands, ui


class MyModal(ui.Modal, title="hello world"):
    name = ui.TextInput(label="Please Enter Name",
                          placeholder="John Doe",
                          custom_id="nameField",
                          style=discord.TextStyle.short)
    age = ui.TextInput(label="Please Enter Age",
                       placeholder="18+",
                       custom_id="ageField",
                       style=discord.TextStyle.short)
    about = ui.TextInput(label="Tell me about Yourself",
                         placeholder="im gay",
                         custom_id="aboutField",
                         style=discord.TextStyle.long)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Hello **{self.name}** You are **{self.age}** years old and **{self.about}"
                                                f"about yourself")


class modal_Test(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Slash Cogs Loaded")

    # Pings the Discord Bot (ms)

    @app_commands.command(name="modal", description="Ping Slash")
    async def modal(self, interaction: discord.Interaction):
        await interaction.response.send_modal(MyModal())


async def setup(client):
    client.remove_command("help")
    await client.add_cog(modal_Test(client), guilds=[discord.Object(id="1041205088657616898")])
