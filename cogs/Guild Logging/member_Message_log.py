import discord
from discord import app_commands
from discord.ext import commands
import pymongo

import discord
from discord import app_commands
from discord.ext import commands
import pymongo

class MessageLogger(commands.Cog):
    def __init__(self, client, mongo_uri, database_name):
        self.bot = client
        self.mongo_uri = mongo_uri
        self.database_name = database_name
        self.log_channel_id = None

        # Connect to MongoDB
        self.mongo_client = pymongo.MongoClient(self.mongo_uri)
        self.database = self.mongo_client[self.database_name]

        # Load the log channel ID from MongoDB
        self.load_log_channel_id()

    def load_log_channel_id(self):
        collection_name = "member_message_log_channel"  # Updated collection name
        config_collection = self.database[collection_name]
        document = config_collection.find_one({"_id": "log_channel_id"})
        if document:
            self.log_channel_id = document.get("value")

    def save_log_channel_id(self):
        collection_name = "member_message_log_channel"  # Updated collection name
        config_collection = self.database[collection_name]
        config_collection.update_one(
            {"_id": "log_channel_id"},
            {"$set": {"value": self.log_channel_id}},
            upsert=True
        )

    @commands.Cog.listener()
    async def on_ready(self):
        print("Message Logger is ready")

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if self.log_channel_id:
            embed = discord.Embed(title="Message Deleted", color=discord.Color.red())
            embed.add_field(name="Author", value=message.author.mention, inline=False)
            embed.add_field(name="Channel", value=message.channel.mention, inline=False)
            embed.add_field(name="Content", value=message.content, inline=False)
            await self.bot.get_channel(int(self.log_channel_id)).send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if self.log_channel_id and before.content != after.content:
            embed = discord.Embed(title="Message Edited", color=discord.Color.orange())
            embed.add_field(name="Author", value=before.author.mention, inline=False)
            embed.add_field(name="Channel", value=before.channel.mention, inline=False)
            embed.add_field(name="Before", value=before.content, inline=False)
            embed.add_field(name="After", value=after.content, inline=False)
            await self.bot.get_channel(int(self.log_channel_id)).send(embed=embed)

    @app_commands.command(name="set-message-logger", description="Sets the log channel for message logging")
    @commands.has_permissions(administrator=True)
    async def set_log_channel(self, ctx: discord.Interaction, channel_name: discord.TextChannel):
        guild = ctx.guild
        log_channel = discord.utils.get(guild.channels, name=channel_name.name)

        if log_channel:
            self.log_channel_id = str(log_channel.id)
            self.save_log_channel_id()
            await ctx.response.send_message(f"Message log channel set to {channel_name.mention}.")
        else:
            await ctx.response.send_message(f"Channel {channel_name.mention} not found.")

    @app_commands.command(name="reset-message-logger", description="Resets the log channel for message logging")
    @commands.has_permissions(administrator=True)
    async def reset_log_channel(self, ctx: discord.Interaction):
        self.log_channel_id = None
        self.save_log_channel_id()
        await ctx.response.send_message("Message log channel reset.")

async def setup(client):
    mongo_uri = "mongodb+srv://Asicc:q31vCgHan67vo1ut@discordbotdatabse.66op6h9.mongodb.net/?retryWrites=true&w=majority"
    database_name = "discordBotDatabse"

    # Create a 'member_message_log_channel' collection in the database if it doesn't exist
    mongo_client = pymongo.MongoClient(mongo_uri)
    database = mongo_client[database_name]
    collection_name = "member_message_log_channel"  # Updated collection name
    config_collection = database[collection_name]
    config_collection.create_index("value", unique=True)

    await client.add_cog(MessageLogger(client, mongo_uri, database_name),
                         guilds=[discord.Object(id="1041205088657616898")])
