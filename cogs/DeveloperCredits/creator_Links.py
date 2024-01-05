from discord.ui import Button
import discord
from discord.ext import commands


class testbutton(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Socials Buttons is ready")

    # Developer Links
    @commands.command()
    @commands.is_owner()
    async def dev_links(self, ctx):
        embed = discord.Embed(
            title="Trashdarkrunner",
            description="Feel Free to follow my Socials",
            colour=discord.Colour.blue()
        )
        embed.set_image(
            url='https://1000logos.net/wp-content/uploads/2020/09/ArcheAge-logo.png')

        embed.set_thumbnail(url="https://1000logos.net/wp-content/uploads/2020/09/ArcheAge-logo.png")
        embed.set_footer(text="© Asicc.co",
                         icon_url="https://styles.redditmedia.com/t5_qwcgo/styles/communityIcon_ar51amnh0qn51.png")
        view = SimpleView()

        view.add_item(github)
        view.add_item(replit)
        await ctx.send(embed=embed, view=view, delete_after=60)


class SimpleView(discord.ui.View):
    @discord.ui.button(label="Socials", style=discord.ButtonStyle.success)
    async def playerNation(self, interaction: discord.Interaction):
        await interaction.response.send_message("Please click the Link Buttons to follow them to my socials",
                                                ephemeral=True, )


github = Button(label="Github", url="https://github.com/Moonsight91", style=discord.ButtonStyle.green,
                emoji="🍻")
replit = Button(label="Replit", url="https://replit.com/@llTrashdrunnerl", style=discord.ButtonStyle.green,
                emoji="🍻")


async def setup(client):
    await client.add_cog(testbutton(client))
