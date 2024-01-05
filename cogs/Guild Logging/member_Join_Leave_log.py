import discord
from discord import app_commands
from discord.ext import commands


class MemberNotifications(commands.Cog):
    def __init__(self, client):
        self.bot = client
        self.log_channel = None

    @commands.Cog.listener()
    async def on_ready(self):
        print("Socials Buttons is ready")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        embed = discord.Embed(
            title=f"Hello {member.name}! Welcome to {member.guild}",
            description="Please See the <#1080701975231995924> channel to Assign Your Roles",
            colour=discord.Colour.blue()
        )
        embed.add_field(name="Verification?", value="Please wait for verification DM Admins or Raid Callers")
        embed.set_image(url="https://archeage-download1.xlgames.com/web0/preview_en/res_1/images/zone/area/1.jpg")
        await member.send(embed=embed)

        embed2 = discord.Embed(
            title=f"Hello {member.name}! Welcome to {member.guild}",
            description="Please See the <#1080701975231995924> channel to Assign Your Roles",
            colour=discord.Colour.blue()
        )
        embed2.set_footer(text="© Asicc.co",
                          icon_url="https://c4.wallpaperflare.com/wallpaper/363/13/252/valorant-killjoy-valorant-digital-art-artwork-digital-hd-wallpaper-preview.jpg")

        await channel.send(embed=embed2)

    # Listens for an on Member Join
    @commands.Cog.listener()
    async def on_member_join(self, member):
        if self.log_channel:
            embed = discord.Embed(title="Member Joined", color=discord.Color.green())
            embed.add_field(name="Username", value=member.mention, inline=False)
            embed.add_field(name="Account ID", value=member.id, inline=False)
            embed.add_field(name="Account Created", value=member.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
            await self.log_channel.send(embed=embed)

    # Listens for a member Leaving the Server
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if self.log_channel:
            embed = discord.Embed(title="Member Left", color=discord.Color.red())
            embed.add_field(name="Username", value=member.mention, inline=False)
            embed.add_field(name="Account ID", value=member.id, inline=False)
            embed.add_field(name="Account Created", value=member.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
            await self.log_channel.send(embed=embed)

    # Sets the Log Channel
    @app_commands.command(name="set-join-leave-log", description="Setup Member Notification")
    @commands.has_permissions(administrator=True)
    async def set_log_channel(self, ctx: discord.Interaction, channel_name: discord.TextChannel):
        guild = ctx.guild
        self.log_channel = discord.utils.get(guild.channels, name=channel_name.name)
        if self.log_channel:
            await ctx.response.send_message(f"Log channel set to {channel_name.mention}.")
        else:
            await ctx.response.send_message(f"Channel {channel_name.mention} not found.")

    # Resets the log Channel
    @app_commands.command(name="reset-join-leave-log", description="Setup Member Notification Reset")
    @commands.has_permissions(administrator=True)
    async def set_log_channel_reset(self, ctx: discord.Interaction):
        self.log_channel = None
        await ctx.response.send_message("Log channel re.")


async def setup(client):
    await client.add_cog(MemberNotifications(client), guilds=[discord.Object(id="1041205088657616898")])
