import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import Button, View


class TicketSystemButton(Button):
    def __init__(self, ticket_channel, ticket_author):
        super().__init__(style=discord.ButtonStyle.red, label="Close Ticket")
        self.ticket_channel = ticket_channel
        self.ticket_author = ticket_author

    @commands.has_permissions(manage_messages=True)
    async def callback(self, interaction: discord.Interaction):
        await self.ticket_channel.delete()
        await self.ticket_author.send(
            "Your ticket has been closed. If you have any further questions, feel free to ask.")


class TicketSystemView(View):
    def __init__(self, ticket_channel, ticket_author):
        super().__init__()
        self.ticket_channel = ticket_channel
        self.ticket_author = ticket_author

        close_button = TicketSystemButton(ticket_channel, ticket_author)
        self.add_item(close_button)


class TicketSystemCog(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.ticket_category_id = 1192349729166741544  # Replace with the category ID where you want to create tickets
        self.ticket_channel_id = 1192349861148893225  # Replace with the channel ID where you want to send ticket messages
        self.ticket_limit = 3  # Maximum number of tickets per user



    @commands.Cog.listener()
    async def on_ready(self):
        print("TicketSystemCog is ready")

    @app_commands.command(name="ticket", description="Create a ticket")
    async def create_ticket(self, interactions: discord.Interaction):
        guild = interactions.guild
        user = interactions.user
        ticket_category = discord.utils.get(guild.categories, id=self.ticket_category_id)
        ticket_channel = discord.utils.get(guild.channels, id=self.ticket_channel_id)

        if not ticket_category or not ticket_channel:
            await interactions.response.send_message(
                "Ticket category or channel not found. Please make sure the IDs are correct.", ephemeral=True
            )
            return

        # Check ticket limit for the user
        user_tickets = 0
        for channel in guild.channels:
            if isinstance(channel, discord.TextChannel) and channel.name.startswith("ticket-"):
                if channel.topic == str(user.id):
                    user_tickets += 1

        if user_tickets >= self.ticket_limit:
            await interactions.response.send_message(
                f"You have reached the maximum ticket limit of {self.ticket_limit}. "
                "Please close some of your existing tickets before creating a new one.",
                ephemeral=True,
            )
            return

        # Create a new ticket channel
        channel_name = f"ticket-{user.id}"
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True),
        }
        ticket_channel = await ticket_category.create_text_channel(channel_name, overwrites=overwrites)
        await ticket_channel.edit(topic=str(user.id))  # Set the topic of the ticket channel to the user ID

        # Create an embed for the ticket message
        embed = discord.Embed(
            title="Ticket Created",
            description=f"Ticket created by {user.mention}",
            color=discord.Color.blue(),
        )

        # Send a message in the ticket channel
        ticket_message = await ticket_channel.send(embed=embed, view=TicketSystemView(ticket_channel, user))

        # Send a reply in the command channel
        await interactions.response.send_message(
            f"Ticket created successfully! Your",ephemeral=True,)


async def setup(client):
    await client.add_cog(TicketSystemCog(client), guilds=[discord.Object(id="1041205088657616898")])
