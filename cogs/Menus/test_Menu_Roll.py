import discord
from discord.ext import commands
import pymongo


class DatabaseCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.mongo_client = pymongo.MongoClient("mongodb+srv://Asicc:q31vCgHan67vo1ut@discordbotdatabse.66op6h9.mongodb.net/?retryWrites=true&w=majority")
        self.database = self.mongo_client["discordBotDatabse"]
        self.collection = self.database["discordbot"]

    @commands.command()
    async def user(self, ctx):
        user_id = ctx.author.id

        # Check if the user ID is already in the database
        if self.collection.find_one({"user_id": user_id}):
            await ctx.send("User ID already stored.")
        else:
            # Insert the user ID into the database
            self.collection.insert_one({"user_id": user_id})
            await ctx.send("User ID stored successfully.")


async def setup(client):
    await client.add_cog(DatabaseCog(client))
