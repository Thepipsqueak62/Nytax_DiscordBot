import discord
from discord import app_commands
from discord.ext import commands


class MessageLogger(commands.Cog):
    def __init__(self, client):
        self.bot = client
        self.log_channel = None

    @commands.Cog.listener()
    async def on_ready(self):
        print("Message Logger is ready")

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if self.log_channel:
            embed = discord.Embed(title="Message Deleted", color=discord.Color.red())
            embed.add_field(name="Author", value=message.author.mention, inline=False)
            embed.add_field(name="Channel", value=message.channel.mention, inline=False)
            embed.add_field(name="Content", value=message.content, inline=False)
            await self.log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if self.log_channel and before.content != after.content:
            embed = discord.Embed(title="Message Edited", color=discord.Color.orange())
            embed.add_field(name="Author", value=before.author.mention, inline=False)
            embed.add_field(name="Channel", value=before.channel.mention, inline=False)
            embed.add_field(name="Before", value=before.content, inline=False)
            embed.add_field(name="After", value=after.content, inline=False)
            await self.log_channel.send(embed=embed)

    @app_commands.command(name="set-message-logger", description="sets the log channel for message logging")
    @commands.has_permissions(administrator=True)
    async def set_log_channel(self, ctx, channel_name: discord.TextChannel):
        guild = ctx.guild
        self.log_channel = discord.utils.get(guild.channels, name=channel_name.name)
        if self.log_channel:
            await ctx.response.send_message(f"Message log channel set to {channel_name.mention}.")
        else:
            await ctx.response.send_message(f"Channel {channel_name.mention} not found.")

    @app_commands.command(name="reset-message-logger", description="Reset the log channel for message logging")
    @commands.has_permissions(administrator=True)
    async def reset_log_channel(self, ctx):
        self.log_channel = None
        await ctx.send("Message log channel reset.")


async def setup(client):
    await client.add_cog(MessageLogger(client), guilds=[discord.Object(id="1041205088657616898")])
