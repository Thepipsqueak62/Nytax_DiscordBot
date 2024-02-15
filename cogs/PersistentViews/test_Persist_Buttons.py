import discord
from discord.ext import commands
from discord import ui


class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def d(self, ctx):
        embed = discord.Embed(title="Welcome to NHF", description="Please Select the Role for you")
        await ctx.send(embed=embed, view=RolesView())


class RolesView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    # This is the persistent B
    @discord.ui.button(label="Valorant", custom_id="Role 1", style=discord.ButtonStyle.blurple)
    async def button1(self, interaction, button):
        role_id = 1181242831298379818
        user = interaction.user
        role = interaction.guild.get_role(role_id)
        if role:
            if role in user.roles:
                await user.remove_roles(role)
                await interaction.response.send_message("You have removed a role!", ephemeral=True)
            else:
                await user.add_roles(role)
                await interaction.response.send_message("You have added a role!", ephemeral=True)
        else:
            await interaction.response.send_message("Role not found.", ephemeral=True)

    @discord.ui.button(label="Black Desert", custom_id="Role 2", style=discord.ButtonStyle.blurple)
    async def button2(self, interaction, button):
        role_id = 1181242900462452787
        user = interaction.user
        role = interaction.guild.get_role(role_id)
        if role:
            if role in user.roles:
                await user.remove_roles(role)
                await interaction.response.send_message("You have removed a role!", ephemeral=True)
            else:
                await user.add_roles(role)
                await interaction.response.send_message("You have added a role!", ephemeral=True)
        else:
            await interaction.response.send_message("Role not found.", ephemeral=True)


async def setup(client):
    await client.add_cog(Roles(client))
