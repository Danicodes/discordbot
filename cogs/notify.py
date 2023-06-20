import os,sys
import discord
from discord.ext import commands
from datetime import timedelta, datetime
import asyncio
import discord.utils
from random import random
import json 
import pytz
from pytz import timezone

class Notify(commands.Cog):
    """ Notifications cog"""
    def __init__(self, bot):
        self.bot = bot

    def datetime_to_timedelta(datestring):
        est = timezone('EST')

        datestr = datetime.strptime(datestring, "%Y-%m-%d %H:M")
        datestr.replace(tzinfo=est)

        myutc = datestr.astimezone(pytz.utc)
        delta = myutc - datetime.now(tz=pytz.utc)

        delta


        

    @commands.command()
    async def notify(self, ctx, channel_name="testing", time=10):
        channel = discord.utils.get(ctx.guild.channels, name=channel_name)
        channel_id = channel.id
        channel = self.bot.get_channel(channel_id)

        with open("../assets/schedule.json", "r") as schedule:
            _schedule = json.load(schedule)

            for key, message in _schedule.items():

                
        random_notification = None
        await ctx.send(f"{channel.mention} Heyyy")
        
        return


async def setup(bot):
    await bot.add_cog(Notify(bot))

async def teardown(bot):
    await bot.remove_cog("notify")
