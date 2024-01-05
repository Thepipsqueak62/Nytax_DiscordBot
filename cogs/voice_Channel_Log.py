import discord
from discord.ext import commands
from datetime import datetime


class VoiceChannelNotifications(commands.Cog):
    def __init__(self, client):
        self.bot = client
        self.log_channel = None

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        guild = member.guild
        if self.log_channel:
            timestamp_formatted = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")  # Format timestamp as desired
            if before.channel is None and after.channel:  # User joined a voice channel
                embed = discord.Embed(title="User Joined Voice Channel", color=discord.Color.green())
                embed.add_field(name="Username", value=member.mention, inline=False)
                embed.add_field(name="Channel", value=after.channel.name, inline=False)
                embed.add_field(name="Timestamp", value=timestamp_formatted, inline=False)
                await self.log_channel.send(embed=embed)
            elif before.channel and after.channel is None:  # User left a voice channel
                embed = discord.Embed(title="User Left Voice Channel", color=discord.Color.red())
                embed.add_field(name="Username", value=member.mention, inline=False)
                embed.add_field(name="Channel", value=before.channel.name, inline=False)
                embed.add_field(name="Timestamp", value=timestamp_formatted, inline=False)
                await self.log_channel.send(embed=embed)

    @commands.command(name="set-voice-log-channel", description="Set the log channel for voice channel notifications")
    @commands.has_permissions(administrator=True)
    async def set_log_channel(self, ctx: commands.Context, channel: discord.TextChannel):
        self.log_channel = channel
        await ctx.send(f"Log channel set to {channel.mention} for voice channel notifications.")

    @commands.command(name="reset-voice-log-channel", description="Reset the log channel for voice channel notifications")
    @commands.has_permissions(administrator=True)
    async def reset_log_channel(self, ctx: commands.Context):
        self.log_channel = None
        await ctx.send("Log channel for voice channel notifications reset.")


async def setup(client):
    await client.add_cog(VoiceChannelNotifications(client))
