import discord
from discord.ext import commands
from discord import ui


class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def d(self, ctx):
        embed = discord.Embed(title="Role Selection Form", description="Press to add/remove a role.")
        await ctx.send(embed=embed, view=RolesView())


class RolesView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
# This is the persistent But
    @discord.ui.button(label="Role 1", custom_id="Role 1", style=discord.ButtonStyle.secondary)
    async def button1(self, interaction, button):
        role_id = 1127874025692082186
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
