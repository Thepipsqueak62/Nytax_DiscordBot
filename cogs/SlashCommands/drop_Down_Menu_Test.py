import discord
from discord.ext import commands
from discord import app_commands

from discord.ui import Select, View, Button


class SelectMenu(discord.ui.View):
    options = [
        discord.SelectOption(label="Red", value="1", description="Gives the color red to user"),
        discord.SelectOption(label="Blue", value="2", description="Gives the color blue to user"),
        discord.SelectOption(label="Yellow", value="3", description="Gives the color yellow to user")
    ]

    @discord.ui.select(placeholder="Select Color", options=options)
    async def menu_callback(self, interaction: discord.Interaction, select):
        select.disabled = True
        user = interaction.user
        guild = interaction.guild
        selected_value = select.values[0]

        # Define your role IDs corresponding to the options
        role_ids = {
            '1': 1093956750274723971,  # Replace with your role ID for red
            '2': 1093956917954617476,  # Replace with your role ID for blue
            '3': 1093956937504264233  # Replace with your role ID for yellow
        }

        role_id = role_ids.get(selected_value)

        if role_id:
            role = guild.get_role(role_id)

            if role:
                # Check if the user already has the role
                if role in user.roles:
                    await interaction.response.send_message(content="You already have this color role.")
                else:
                    # Add the role to the user
                    await user.add_roles(role)
                    await interaction.response.send_message(content=f"Your color is now {role.name}.")
            else:
                await interaction.response.send_message(content="Error: Role not found.")
        else:
            await interaction.response.send_message(content="Error: Invalid selection.")


class RemoveButton(discord.ui.View):
    def __init__(self, role_id):
        super().__init__()
        self.role_id = role_id

    @discord.ui.button(label="Remove Color", style=discord.ButtonStyle.red)
    async def remove_button_callback(self, button: Button, interaction: discord.Interaction):
        user = interaction.user
        guild = interaction.guild
        role = guild.get_role(self.role_id)

        if role:
            # Check if the user has the role before removing it
            if role in user.roles:
                await user.remove_roles(role)
                await interaction.response.send_message(content=f"Color role {role.name} removed.")
            else:
                await interaction.response.send_message(content="You don't have this color role.")
        else:
            await interaction.response.send_message(content="Error: Role not found.")


class drop_Down(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Slash Cogs Loaded")

    @app_commands.command(name="setcolor", description="Select your role color of choice")
    async def selectcolor(self, interaction: discord.Interaction):
        view = SelectMenu()
        await interaction.response.send_message(content='Select your Role color', view=view)

        # Add the Remove Button
        role_ids = {
            '1': 1093957528330698913,  # Replace with your role ID for red
            '2': 1093957528330698913,  # Replace with your role ID for blue
            '3': 1093957528330698913   # Replace with your role ID for yellow
        }
        selected_value = view.children[0].values[0]
        role_id = role_ids.get(selected_value)

        if role_id:
            remove_view = RemoveButton(role_id)
            await interaction.followup.send(content="Use the button to remove your color role.", view=remove_view)


async def setup(client):
    client.remove_command("help")
    await client.add_cog(drop_Down(client), guilds=[discord.Object(id="1041205088657616898")])
