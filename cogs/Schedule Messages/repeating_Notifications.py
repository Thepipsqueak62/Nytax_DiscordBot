import pytz
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.combining import AndTrigger

from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from discord import Embed


class AurorianCR(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.scheduler = AsyncIOScheduler(timezone=pytz.timezone('US/Eastern'))
        self.scheduler.start()
        firstAurorianCR = AndTrigger([CronTrigger(hour=13, minute=10, day_of_week='mon,tue,wed,thu,fri,sat,sun', timezone=pytz.timezone('US/Eastern'))])
        secondAurorianCR = AndTrigger([CronTrigger(hour=17, minute=10, day_of_week='mon,tue,wed,thu,fri,sat,sun', timezone=pytz.timezone('US/Eastern'))])
        thirdAurorianCR = AndTrigger([CronTrigger(hour=21, minute=10, day_of_week='mon,tue,wed,thu,fri,sat,sun', timezone=pytz.timezone('US/Eastern'))])

        self.scheduler.add_job(self.send_message, firstAurorianCR)
        self.scheduler.add_job(self.send_message, secondAurorianCR)
        self.scheduler.add_job(self.send_message, thirdAurorianCR)

    async def send_message(self):
        channel = self.client.get_channel(1105751148356456500)  # replace with your channel ID
        embed = Embed(title="Crimson Rift **Auroria**", description="**Spawns in 10 Minutes**", color=0xff0000)
        embed.set_image(url="http://archeage.mablog.eu/wp-content/uploads/2018/09/ScreenShot0126.jpg")
        embed.set_thumbnail(
            url="https://1000logos.net/wp-content/uploads/2020/09/ArcheAge-logo.png")

        self.client.loop.create_task(channel.send(embed=embed))

    @commands.Cog.listener()
    async def on_ready(self):
        print("Grimghast Rift Timer Loaded")
        self.scheduler.start()


async def setup(client):
    await client.add_cog(AurorianCR(client))
