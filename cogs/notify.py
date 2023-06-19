import os,sys
import discord
from discord.ext import commands
from datetime import timedelta
import asyncio
import discord.utils
from random import random


class Notify(commands.Cog):
    """ Notifications cog"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def notify(self, ctx, channel_name="testing", time=10):
        channel = discord.utils.get(ctx.guild.channels, name=channel_name)
        channel_id = channel.id
        channel = self.bot.get_channel(channel_id)
        random_notification = None
        await ctx.send(f"{channel.mention} Heyyy")
        
        return


async def setup(bot):
    await bot.add_cog(Notify(bot))

async def teardown(bot):
    await bot.remove_cog("notify")
