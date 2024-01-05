import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import has_permissions


class Utility(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Utility Cog Loaded")

    @app_commands.command(name="edit-channel-name", description="Edit a channel's name", )
    async def edit_channel_name(self, interactions: discord.Interaction, channel: discord.VoiceChannel, name: str):
        await channel.edit(name=name)
        await interactions.response.send_message(f"Channel name changed to {name}")

    @app_commands.command(name='clear', description='Deletes a Set Amount of Messages')
    @commands.has_permissions(manage_messages=True)  # Adjust permissions as needed
    async def delete_message(self, interaction: discord.Interaction, amount: int):
        try:
            channel = interaction.channel
            if amount < 1:
                await interaction.response.send_message("Please provide a positive number.", ephemeral=True)
                return
            if amount > 100:
                await interaction.response.send_message("You cannot delete more than 100 messages at a time.",
                                                        ephemeral=True)
                return

            await interaction.response.defer(ephemeral=True)
            deleted_messages = await channel.purge(limit=amount)
            await interaction.followup.send(f"✅ Successfully deleted {len(deleted_messages)} messages")
        except commands.MissingPermissions:
            await interaction.response.send_message("You don't have the required permissions to manage messages.",
                                                    ephemeral=True)

    @app_commands.command(name='massdelete', description='Delete all messages in the chat')
    @commands.has_permissions(manage_messages=True)  # Adjust permissions as needed
    async def mass_delete_messages(self, interaction):
        try:
            channel = interaction.channel
            await interaction.response.defer(ephemeral=True)

            deleted_message_count = 0
            async for message in channel.history(limit=None):
                await message.delete()
                deleted_message_count += 1

            response_message = f"Successfully deleted {deleted_message_count} messages."
            await interaction.followup.send(response_message)
        except commands.MissingPermissions:
            await interaction.response.send_message("You don't have the required permissions to manage messages.",
                                                    ephemeral=True)

    @commands.command()
    @has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f"User {member} has benn banned")

    @ban.error
    async def ban_error(self, ctx, error):
        embed = discord.Embed(
            title="Permissions Error",
            description="You Don't Have Permissions to Use that ",
            colour=discord.Colour.green()
        )
        embed.set_footer(text="© Asicc.co")
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def dm(self, ctx, *, message=None):
        await ctx.message.delete()
        if message is not None:
            members = ctx.guild.members
            for member in members:
                try:
                    await member.send(message)
                except discord.Forbidden:
                    print(f"Failed to send message to {member.display_name}. User has DMs disabled or blocked the bot.")
                except Exception as e:
                    print(f"An error occurred while sending a message to {member.display_name}: {e}")
        else:
            await ctx.send("Please provide a message!")

    @dm.error
    async def dm_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="Permissions Error",
                description="You Don't Have Permissions to Use That Command",
                colour=discord.Colour.red()
            )
            await ctx.send(embed=embed)


async def setup(client):
    await client.add_cog(Utility(client), guilds=[discord.Object(id="1041205088657616898")])
