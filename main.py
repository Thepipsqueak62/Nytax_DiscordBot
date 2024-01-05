import asyncio
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from cogs.test_Persist_Buttons import RolesView

load_dotenv()

intents = discord.Intents.all()


class bot_Index(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or("!"),
            owner_id=787565560677662720,
            intents=intents,
            case_insensitive=False,
            help_command=None
        )

    async def on_ready(self):
        print(f"{self.user} Has Logged In")
        await self.change_presence(
            activity=discord.Activity(type=discord.ActivityType.playing, name="type !help for a list of commands"),
            status=discord.Status.online
        )
        try:
            synced = await self.tree.sync(guild=discord.Object(id=1041205088657616898))
            print(f"{len(synced)} command(s)")
        except Exception as e:
            print(e)

    async def setup_hook(self):
        self.add_view(RolesView())

    async def load_cogs(self):
        for filename in os.listdir("cogs"):
            if filename.endswith(".py"):
                await self.load_extension(f"cogs.{filename[:-3]}")


if __name__ == "__main__":
    async def main():
        bot = bot_Index()
        await bot.load_cogs()
        await bot.start(os.getenv('DISCORD_API_TOKEN'))


    asyncio.run(main())
