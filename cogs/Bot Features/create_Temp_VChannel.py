import asyncio
import discord
from discord.ext import commands

class TempChan(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Create Temporary channel Cog Loaded")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if after.channel and after.channel.name == "🟢 Create Temporary Channel":
            guild = member.guild
            category = after.channel.category
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(connect=True)
            }
            channel = await guild.create_voice_channel(
                f"{member.name}'s channel",
                category=category,
                user_limit=5,
                overwrites=overwrites
            )
            await member.move_to(channel)

            # Wait for 5 seconds
            await asyncio.sleep(5)

            # Check if the channel is still empty after 5 seconds
            if len(channel.members) == 0:
                await channel.delete()

    @commands.command()
    @commands.is_owner()
    async def tempchan(self, ctx):
        category = ctx.channel.category
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(connect=True)
        }
        channel = await ctx.guild.create_voice_channel(
            f"{ctx.author.name}'s channel",
            category=category,
            user_limit=5,
            overwrites=overwrites
        )
        await ctx.author.edit(voice_channel=channel)
        while True:
            await asyncio.sleep(60)  # wait for 60 seconds
            if len(channel.members) == 0:  # check if the channel is empty
                await channel.delete()  # delete the channel

    @commands.command()
    @commands.is_owner()
    async def delete_temp_voice(self, ctx):
        channel = ctx.author.voice.channel
        if channel.name.startswith(ctx.author.name):
            await channel.delete()
        else:
            await ctx.send("You can only delete a temporary channel that you created.")

async def setup(client):
    await client.add_cog(TempChan(client))
