from discord.ext import commands

class GenCog(commands.Cog):
    """ General commands cog """
    def __init__(self, bot):
        self.bot = bot 

    # On ready called before bot starts; won't be printed if loaded after bot starts
    @commands.Cog.listener() 
    async def on_ready(self):
        print("General cog loaded")

    @commands.command()
    async def hello(self, ctx):
        print("Hi! :)")
        #await ctx.send("Hello")
    
    @commands.command()
    async def tts(self, ctx, *args):
        if len(args) == 0:
            await ctx.send("Provide a message to send")
            return 
            
        message = " ".join(args)
        await ctx.send(message, tts=True)
        return

async def setup(bot):
    # Because I've organized the commands into a class we need to specify the setup
    # i.e. we instantiate the class and pass it along to the bot
    await bot.add_cog(GenCog(bot))

async def teardown(bot):
    await bot.remove_cog("general")