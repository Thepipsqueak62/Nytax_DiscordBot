import discord
from discord.ext import commands


class BadWordsFilter(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.banned_words = ["badword1", "badword2"]  # Add your list of banned words here
        self.warning_threshold = 3  # Number of warnings before taking action

        # You may want to have a separate collection for warnings in MongoDB if you're using it
        self.user_warnings = {}

    async def check_for_bad_words(self, message):
        content_lower = message.content.lower()
        for word in self.banned_words:
            if word in content_lower:
                return True
        return False

    @commands.Cog.listener()
    async def on_ready(self):
        print("Chat Filter Cog")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if await self.check_for_bad_words(message):
            user_id = str(message.author.id)
            warnings = self.user_warnings.get(user_id, 0)
            warnings += 1
            self.user_warnings[user_id] = warnings

            await message.channel.send(
                f"{message.author.mention}, please refrain from using inappropriate language. Warning #{warnings}")

            if warnings >= self.warning_threshold:
                # Take action, e.g., mute, kick, or any other moderation action
                # You can add your own logic here based on your moderation requirements
                await message.author.send("You have reached the warning threshold. Further actions may be taken.")

        else:
            await self.client.process_commands(message)


async def setup(client):
    await client.add_cog(BadWordsFilter(client))
