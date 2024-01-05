import discord
from discord.ext import commands
import pymongo


class Economy(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.mongo_client = pymongo.MongoClient("mongodb+srv://Asicc:q31vCgHan67vo1ut@discordbotdatabse.66op6h9.mongodb.net/?retryWrites=true&w=majority")
        self.db = self.mongo_client["discordBotDatabse"]
        self.balances_collection = self.db["balances"]

    @commands.Cog.listener()
    async def on_ready(self):
        print("Economy Cog Loaded")

    async def get_balance(self, user_id):
        user_data = self.balances_collection.find_one({"user_id": user_id})
        return user_data.get("balance", 0) if user_data else 0

    async def update_balance(self, user_id, amount):
        user_data = self.balances_collection.find_one({"user_id": user_id})

        if not user_data:
            self.balances_collection.insert_one({"user_id": user_id, "balance": amount})
        else:
            self.balances_collection.update_one({"user_id": user_id}, {"$inc": {"balance": amount}})

    @commands.command()
    async def balance(self, ctx):
        user_id = ctx.author.id
        user_balance = await self.get_balance(user_id)

        # Format the balance using commas
        formatted_balance = "{:,}".format(user_balance)

        # Create an embed with a coin emoji
        embed = discord.Embed(
            title=f"{ctx.author.display_name}'s Balance",
            description=f"You have {formatted_balance} coins 💰",
            color=discord.Color.gold()  # You can customize the color
        )

        await ctx.send(embed=embed)

    @commands.command()
    async def userbalance(self, ctx, target_user: discord.Member = None):
        try:
            target_user = target_user or ctx.author
            user_id = target_user.id
            user_balance = await self.get_balance(user_id)

            # Format the user balance using commas
            formatted_user_balance = "{:,}".format(user_balance)

            # Create an embed with a coin emoji
            embed = discord.Embed(
                title=f"{target_user.display_name}'s Balance",
                description=f"They have {formatted_user_balance} coins 💰",
                color=discord.Color.gold()  # You can customize the color
            )

            await ctx.send(embed=embed)

        except Exception as e:
            # Handle exceptions and send an error message
            error_message = f"An error occurred: {e}"
            await ctx.send(error_message)

    @commands.command()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 1, commands.BucketType.user)  # 1-second cooldown per user
    async def boost(self, ctx, target_user: discord.Member, amount: int):
        user_id = target_user.id
        await self.update_balance(user_id, amount)
        updated_balance = await self.get_balance(user_id)

        # Format the updated balance using commas
        formatted_amount = "{:,}".format(amount)
        formatted_updated_balance = "{:,}".format(updated_balance)

        # Create an embed with a coin emoji
        embed = discord.Embed(
            title=f"You gave {formatted_amount} coins to {target_user.display_name}!",
            description=f"Their new balance: {formatted_updated_balance} coins 💰",
            color=discord.Color.gold()  # You can customize the color
        )

        await ctx.send(embed=embed)

    @boost.error
    async def boost_error(self, ctx, error):
        embed = discord.Embed(
            title="Boost Command Error",
            color=discord.Color.red()  # You can customize the color
        )

        if isinstance(error, commands.CheckFailure):
            embed.description = "You don't have the required permissions to use this command."
        elif isinstance(error, commands.MissingRequiredArgument):
            embed.description = "Please provide the amount and the target user."
        elif isinstance(error, commands.BadArgument):
            embed.description = "Invalid amount. Please provide a valid integer."
        elif isinstance(error, commands.CommandOnCooldown):
            embed.description = f"This command is on cooldown. Please try again in {error.retry_after:.2f} seconds."
        else:
            embed.description = f"An error occurred: {error}"

        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 1, commands.BucketType.user)  # 1-second cooldown per user
    async def remove(self, ctx, target_user: discord.Member, amount: int):
        user_id = target_user.id
        current_balance = await self.get_balance(user_id)

        # Check if the user has sufficient balance
        if current_balance < amount:
            await ctx.send(f"{target_user.display_name} doesn't have enough coins to remove.")
            return

        # Update balance by subtracting the specified amount
        await self.update_balance(user_id, -amount)
        updated_balance = await self.get_balance(user_id)

        # Create an embed with a coin emoji
        embed = discord.Embed(
            title=f"You removed {amount} coins from {target_user.display_name}!",
            description=f"Their new balance: {updated_balance} coins 💰",
            color=discord.Color.gold()  # You can customize the color
        )

        await ctx.send(embed=embed)

    @remove.error
    async def remove_coins_error(self, ctx, error):
        embed = discord.Embed(
            title="Remove Coins Command Error",
            color=discord.Color.red()  # You can customize the color
        )

        if isinstance(error, commands.CheckFailure):
            embed.description = "You don't have the required permissions to use this command."
        elif isinstance(error, commands.MissingRequiredArgument):
            embed.description = "Please provide the amount and the target user."
        elif isinstance(error, commands.BadArgument):
            embed.description = "Invalid amount. Please provide a valid integer."
        elif isinstance(error, commands.CommandOnCooldown):
            embed.description = f"This command is on cooldown. Please try again in {error.retry_after:.2f} seconds."
        else:
            embed.description = f"An error occurred: {error}"

        await ctx.send(embed=embed)


async def setup(client):
    client.remove_command("help")
    await client.add_cog(Economy(client))
