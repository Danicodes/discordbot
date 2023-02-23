from discord.ext import commands
from utils import nlg

class SentienceCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
   
    @commands.Cog.listener()
    async def on_message(self, message):
        # Does this THEN the bot's on message
        if message.mentions and 'chatbot' in map(lambda x: x.name, message.mentions):
            await message.channel.send(f"You rang, {message.author.mention}?")

        if message.content == "hello":
            await message.channel.send(f"Hello, {message.author.mention}")

    @commands.command(name="question")
    async def question(self, ctx, *args):
        input_text = " ".join(args)
        if len(args) > 0:
            output = nlg.respond(input_text)
            await ctx.send(output)
        return

    @commands.command(name="anything")
    async def say_anything(self, ctx):
        output = nlg.say_anything()
        await ctx.send(output)
        return

        
async def setup(bot):
    await bot.add_cog(SentienceCog(bot))

async def teardown(bot):
    await bot.remove_cog("sentience")