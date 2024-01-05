import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime
import pymongo


class VoiceChannelNotifications(commands.Cog):
    def __init__(self, client):
        self.bot = client
        self.log_channel = None
        self.mongo_client = pymongo.MongoClient("mongodb+srv://Asicc:q31vCgHan67vo1ut@discordbotdatabse.66op6h9.mongodb.net/?retryWrites=true&w=majority")
        self.db = self.mongo_client["discordBotDatabse"]
        self.voice_logs_collection = self.db["voice_logs"]

    @commands.Cog.listener()
    async def on_ready(self):
        print("Socials Buttons is ready")

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

    @app_commands.command(name="set-voice-log-channel",
                          description="Set the log channel for voice channel notifications")
    @commands.has_permissions(administrator=True)
    async def set_log_channel(self, ctx: discord.Interaction, channel: discord.TextChannel):
        self.log_channel = channel
        await self.voice_logs_collection.delete_many({})  # Clear the existing logs when setting a new channel
        await self.voice_logs_collection.insert_one({"channel_id": str(channel.id)})

        await ctx.response.send_message(f"Log channel set to {channel.mention} for voice channel notifications.")

    @app_commands.command(name="reset-voice-log-channel",
                          description="Reset the log channel for voice channel notifications")
    @commands.has_permissions(administrator=True)
    async def reset_log_channel(self, ctx: discord.Interaction):
        stored_channel = await self.voice_logs_collection.find_one()
        if stored_channel:
            stored_channel_id = int(stored_channel["channel_id"])
            stored_channel_obj = ctx.guild.get_channel(stored_channel_id)
            if stored_channel_obj:
                self.log_channel = stored_channel_obj
                await ctx.response.send_message(
                    f"Log channel reset to {self.log_channel.mention} for voice channel notifications.")
            else:
                await ctx.response.send_message("Stored log channel not found. Please set a new log channel.")
        else:
            await ctx.response.send_message("No log channel stored. Please set a log channel.")


async def setup(client):
    await client.add_cog(VoiceChannelNotifications(client),guilds=[discord.Object(id="1041205088657616898")])
