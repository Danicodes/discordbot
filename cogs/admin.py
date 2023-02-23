import os
import discord
from discord.ext import commands

class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Admin cog loaded")

    @commands.command(name='load')
    async def load_cog(self, ctx, cog):
        if not cog:
            await ctx.send("Missing name of cog to load")
            return

        try:
            if (os.path.exists(f'cogs/{cog}.py')):
                print(f"loading {cog}...")
                await self.bot.load_extension(f'cogs.{cog}') # Sub-cogs must be dot separated like python imports
                await ctx.send(f"loaded {cog}")
        except Exception as e:
            await ctx.send(f"Error loading cog {cog}")
            print(e)
            raise(e)
        return 
            
    @commands.command(name='unload')
    async def unload_cog(self, ctx, cog):
        if not cog:
            await ctx.send("Missing name of cog to unload")
            return

        try: 
            print(f"unloading {cog}")
            await self.bot.unload_extension(f"cogs.{cog}")
            await ctx.send(f"unloaded {cog}")
        except Exception as e:
            await ctx.send(f"Error unloading cog {cog}")
            print(e)
            raise(e)
        return

    @commands.command(name='reload')
    async def reload_cog(self, ctx, cog):
        if not cog:
            await ctx.send("Missing name of cog to reload")
            return
            
        try:
            print(f"reloading {cog}")
            await self.bot.reload_extension(f"cogs.{cog}")
            await ctx.send(f"reloaded {cog}")
        except Exception as e:
            await ctx.send(f"Error reloading cog {cog}")
            print(e)
            raise(e)
        return
 
async def setup(bot):
    await bot.add_cog(AdminCog(bot))

async def teardown(bot):
    await bot.remove_cog("admin")