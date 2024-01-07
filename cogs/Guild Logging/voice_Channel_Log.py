import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime
import pymongo


class VoiceChannelLog(commands.Cog):
    def __init__(self, client):
        self.bot = client
        self.log_channel = None
        self.mongo_client = pymongo.MongoClient("mongodb+srv://Asicc:q31vCgHan67vo1ut@discordbotdatabse.66op6h9.mongodb.net/?retryWrites=true&w=majority")
        self.db = self.mongo_client["discordBotDatabse"]
        self.voice_logs_collection = self.db["voice_logs_channel"]

    @commands.Cog.listener()
    async def on_ready(self):
        print("Voice Channel Log is ready")

        # Load the log channel from the database
        guild_id = str(self.bot.guilds[0].id)  # Change this line if the bot is in multiple guilds
        self.log_channel = await self.get_log_channel(guild_id)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if self.log_channel:
            timestamp_formatted = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")

            if before.channel is None and after.channel:  # User joined a voice channel
                await self.log_join(member, after.channel, timestamp_formatted)
            elif before.channel and after.channel is None:  # User left a voice channel
                await self.log_leave(member, before.channel, timestamp_formatted)
            elif before.channel and after.channel and before.channel != after.channel:  # User moved to a different voice channel
                await self.log_move(member, before.channel, after.channel, timestamp_formatted)
            elif not after.channel:  # User timed out or got disconnected
                await self.log_timeout(member, before.channel, timestamp_formatted)

    async def log_join(self, member, channel, timestamp):
        embed = discord.Embed(title="User Joined Voice Channel", color=discord.Color.green())
        embed.add_field(name="Username", value=member.mention, inline=False)
        embed.add_field(name="Channel", value=channel.name, inline=False)
        embed.add_field(name="Timestamp", value=timestamp, inline=False)
        await self.log_channel.send(embed=embed)

    async def log_leave(self, member, channel, timestamp):
        embed = discord.Embed(title="User Left Voice Channel", color=discord.Color.red())
        embed.add_field(name="Username", value=member.mention, inline=False)
        embed.add_field(name="Channel", value=channel.name, inline=False)
        embed.add_field(name="Timestamp", value=timestamp, inline=False)
        await self.log_channel.send(embed=embed)

    async def log_move(self, member, before_channel, after_channel, timestamp):
        embed = discord.Embed(title="User Moved Voice Channels", color=discord.Color.blue())
        embed.add_field(name="Username", value=member.mention, inline=False)
        embed.add_field(name="Before Channel", value=before_channel.name, inline=False)
        embed.add_field(name="After Channel", value=after_channel.name, inline=False)
        embed.add_field(name="Timestamp", value=timestamp, inline=False)
        await self.log_channel.send(embed=embed)

    async def log_timeout(self, member, channel, timestamp):
        embed = discord.Embed(title="User Timed Out or Disconnected", color=discord.Color.orange())
        embed.add_field(name="Username", value=member.mention, inline=False)
        embed.add_field(name="Channel", value=channel.name, inline=False)
        embed.add_field(name="Timestamp", value=timestamp, inline=False)
        await self.log_channel.send(embed=embed)

    @app_commands.command(name="setup-voice-log", description="Setup the voice channel logging")
    @commands.has_permissions(administrator=True)
    async def setup_voice_log(self, ctx: discord.Interaction, channel_name: discord.TextChannel):
        guild = ctx.guild
        self.log_channel = channel_name
        guild_id = str(guild.id)
        channel_id = str(channel_name.id)

        # Store the channel information in the database
        self.voice_logs_collection.update_one(
            {"_id": guild_id},
            {"$set": {"log_channel_id": channel_id}},
            upsert=True
        )

        await ctx.response.send_message(f"Voice channel log setup in {channel_name.mention}.")

    @app_commands.command(name="reset-voice-log", description="Reset the voice channel logging")
    @commands.has_permissions(administrator=True)
    async def reset_voice_log(self, ctx: discord.Interaction):
        guild_id = str(ctx.guild.id)

        # Remove the channel information from the database
        self.voice_logs_collection.update_one(
            {"_id": guild_id},
            {"$unset": {"log_channel_id": ""}}
        )

        self.log_channel = None
        await ctx.response.send_message("Voice channel log reset.")

    async def get_log_channel(self, guild_id):
        result = self.voice_logs_collection.find_one({"_id": str(guild_id)})
        if result and "log_channel_id" in result:
            return self.bot.get_channel(int(result["log_channel_id"]))
        return None


async def setup(client):
    await client.add_cog(VoiceChannelLog(client), guilds=[discord.Object(id="1041205088657616898")])
