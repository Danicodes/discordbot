import discord
from discord.ext import commands

class WelcomeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel and channel.name == "welcome":
            await channel.send(f"Welcome to the demo {member.mention}!")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.name != "chatbot":
            message = reaction.message
            if message.channel.name == 'welcome' and '🙂' not in message.reactions:
                await message.add_reaction('🙂')

    @commands.command(name="welcome")
    async def welcome_member(self, ctx, member=None):
        if not member:
            await ctx.send("Not sure who to welcome")
            return

        await ctx.send(f"{ctx.author.mention} welcomes {member}")
        return

    @commands.has_role('admin')
    @commands.command(name="invite")
    async def create_invite(self, ctx) -> None:
        """
        Create an invite link for the channel
        """        
        invite = await ctx.channel.create_invite(max_age=5000) #expires after 5000 seconds
        await ctx.send(invite.url)
        return
    
    
async def setup(bot):
    await bot.add_cog(WelcomeCog(bot))

async def teardown(bot):
    await bot.remove_cog("welcome")