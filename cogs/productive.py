import random
import functools
from datetime import timedelta

from discord.ext import commands

class ProductiveCog(commands.Cog):
    """ Productive commands cog """
    def __init__(self, bot):
        self.bot = bot 

    @commands.command()
    async def pomodoro(self, ctx, time=15): 
        """Command to time yourself out from the server for a specified time"""
        await ctx.send(f"{ctx.author.name} needs time to concentrate, enjoy a {time} second timeout")
        await ctx.author.timeout(timedelta(seconds=time))
        return

    @commands.has_any_role('oncall', 'admin')
    @commands.command(name="incident")
    async def start_incident(self, ctx, *details):
        """Open a new incident channel"""
        incident_name = details[0] if details and len(details) > 0 else None
        if not incident_name:
            incident_name = random.randint(1,100)
        incident_description = " ".join(details[1:]) if len(details) > 1 else None
        
        channel_name = f"incident_{incident_name}"
        incident_channel = await ctx.guild.create_text_channel(channel_name, reason=incident_description)
        await ctx.send(f"Created {incident_channel}")
        return
    
    @commands.command(name="monitor")
    async def monitor_event(self, ctx, event_name=None):
        """Request event monitoring for some event_name"""
        incident_channels = list(filter(lambda channel: channel.name.startswith('incident_'), ctx.guild.channels))
        newest_incident = functools.reduce(lambda inc1, inc2: inc1 if inc1.created_at == max(inc1.created_at, inc2.created_at) else inc2, incident_channels)

        from utils.important_data import monitor_event
        
        #Create a webhook
        incident_webhook = await newest_incident.create_webhook(name=f"{newest_incident.name}_hook")
        await monitor_event(incident_webhook.url, event_name)
        return

    def is_incident_channel():
        """Decorator so that we don't accidentally delete a needed channel"""
        def predicate(ctx):
            return ctx.channel.name.startswith('incident_')
        return commands.check(predicate)

    @commands.command()
    @is_incident_channel()
    async def resolve(self, ctx):
        """Resolve incident by deleting channel"""
        await ctx.send("Archiving channel")
        await ctx.channel.delete()
        return


async def setup(bot):
    await bot.add_cog(ProductiveCog(bot))

async def teardown(bot):
    await bot.remove_cog("productive")