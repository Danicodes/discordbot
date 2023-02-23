from datetime import timedelta
import discord
from discord.ext import commands

class SafetyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.blacklist = ['cake']

    async def _timeout(self, user: discord.Member, time:int=10):
        """Internal command to timeout a user"""
        time = timedelta(seconds=time) 
        await user.timeout(time)
        return

    @commands.command()
    async def purge(self, ctx):
        """Delete the last messages from the channel (defaults to deleting 100)"""
        await ctx.channel.purge(check=lambda message: message is not None)
        return
        
    @commands.command()
    async def timeout(self, ctx, time=10):
        """Command to time a user out for a number of seconds (default = 10)"""
        await ctx.send(f"Timing user out!")
        await self._timeout(ctx.author, time=time)
        return

    @commands.has_any_role('admin', 'chatbot')
    @commands.command(name="add_blacklisted_term")
    async def add_blacklisted_term(self, ctx, term=None):
        """Command to add a new blacklisted term"""
        if not term:
            await ctx.send("Need to specify a term to add")
            return

        await ctx.send("Adding to blacklisted terms")
        self.blacklist.append(term)
        return

    @commands.Cog.listener()
    async def on_message(self, message) -> None:
        """On message listener to handle usage of any blacklisted words"""
        if any(map(lambda word: word in message.content, self.blacklist)) and message.author.name.lower() != 'chatbot':
            # User entered blacklisted word
            await message.channel.send(f"{message.author.name} used a blacklisted word; timeout for 5 minutes (10 seconds so we're not here all day)")
            await self._timeout(message.author)
        return
    

async def setup(bot):
    await bot.add_cog(SafetyCog(bot))

async def teardown(bot):
    await bot.remove_cog("safety")