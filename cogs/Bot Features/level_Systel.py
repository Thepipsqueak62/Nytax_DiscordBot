import discord
from discord.ext import commands
from discord import Embed
import pymongo

class Level_System(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.mongo_client = pymongo.MongoClient("mongodb+srv://Asicc:q31vCgHan67vo1ut@discordbotdatabse.66op6h9.mongodb.net/?retryWrites=true&w=majority")
        self.db = self.mongo_client["discordBotDatabse"]
        self.levels_collection = self.db["levels"]
        self.balances_collection = self.db["balances"]

    @commands.Cog.listener()
    async def on_ready(self):
        print("Level System Cog Loaded")

    async def calculate_xp_per_message(self, level):
        return 5 + 2.0 * (level - 1)

    async def get_user_level(self, user_id):
        user_data = self.levels_collection.find_one({"user_id": user_id})
        return user_data.get("level", 1) if user_data else 1

    async def get_user_xp(self, user_id):
        user_data = self.levels_collection.find_one({"user_id": user_id})
        return user_data.get("xp", 0) if user_data else 0

    async def update_xp_per_message(self, user_id, new_xp_per_message):
        self.levels_collection.update_one({"user_id": user_id}, {"$set": {"xp_per_message": new_xp_per_message}}, upsert=True)

    async def update_user_level(self, user_id, new_level):
        await self.update_xp_per_message(user_id, await self.calculate_xp_per_message(new_level))
        self.levels_collection.update_one({"user_id": user_id}, {"$set": {"level": new_level}}, upsert=True)

        # Add 500 coins when the user levels up
        await self.update_user_balance(user_id, 500)

    async def update_user_xp(self, user_id, xp_amount):
        current_xp = await self.get_user_xp(user_id)
        xp_per_message = await self.calculate_xp_per_message(await self.get_user_level(user_id))
        new_xp = max(current_xp + (xp_amount * xp_per_message), 0)  # Ensure new XP is not negative
        self.levels_collection.update_one({"user_id": user_id}, {"$set": {"xp": new_xp}}, upsert=True)

    async def check_level_up(self, user_id):
        xp = await self.get_user_xp(user_id)
        current_level = await self.get_user_level(user_id)
        xp_needed = 100 * (2 ** current_level)

        if xp >= xp_needed:
            new_level = current_level + 1
            xp_needed = 100 * (2 ** new_level)
            remaining_xp = xp - xp_needed
            await self.update_user_level(user_id, new_level)
            await self.update_user_xp(user_id, xp_amount=remaining_xp)

            # Send a DM to the user
            user = self.client.get_user(user_id)
            if user:
                await user.send(f"Congratulations! You've leveled up to Level {new_level}. "
                                f"You now need {xp_needed} XP to level up again.")

    async def update_user_balance(self, user_id, amount):
        user_data = self.balances_collection.find_one({"user_id": user_id})

        if not user_data:
            self.balances_collection.insert_one({"user_id": user_id, "balance": amount})
        else:
            self.balances_collection.update_one({"user_id": user_id}, {"$inc": {"balance": amount}})

    @commands.command()
    async def profile(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        level = await self.get_user_level(member.id)
        xp = await self.get_user_xp(member.id)
        xp_needed = 100 * (2 ** level) - (xp % (100 * (2 ** level)))
        xp_per_message = await self.calculate_xp_per_message(level)

        # Format numbers with 2 decimal places
        formatted_xp = "{:.2f}".format(xp)
        formatted_xp_needed = "{:.2f}".format(xp_needed)
        formatted_xp_per_message = "{:.2f}".format(xp_per_message)

        embed = Embed(
            title=f"{member.display_name}'s Profile",
            color=discord.Color.blue(),
            description=f"Level: {level}\nXP: {formatted_xp}\nXP Needed to Level Up: {formatted_xp_needed}\nXP Per Message: {formatted_xp_per_message}"
        )

        await ctx.send(embed=embed)

    @profile.error
    async def profile_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            await ctx.send("Member not found. Please provide a valid member.")
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"This command is on cooldown. Please try again in {error.retry_after:.2f} seconds.")
        else:
            # Handle other errors as needed
            await ctx.send(f"An error occurred: {error}")

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            await self.update_user_xp(message.author.id, xp_amount=1)
            await self.check_level_up(message.author.id)

async def setup(client):
    client.remove_command("help")
    await client.add_cog(Level_System(client))
