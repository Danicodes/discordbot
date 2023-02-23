import asyncio
import yt_dlp
import discord
from discord.ext import commands

# Must have installed the discord with voice options to be able to join a voice channel (pip install -U discord.py[voice])
# Must also have ffmpeg installed in the running environment (e.g. sudo apt install ffmpeg)

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn',
}

class VoiceCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_client = None
 
    async def from_url(self, url: str, loop=None, stream=False) -> discord.FFmpegPCMAudio:
        loop = loop if loop else asyncio.get_event_loop()    
        ytdl = yt_dlp.YoutubeDL(ytdl_format_options)
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            data = data['entries'][0]

        filename = data.get('url') if stream  else ytdl.prepare_filename(data)
        return discord.FFmpegPCMAudio(filename, **ffmpeg_options)
        
    async def connect(self, channel: discord.VoiceChannel) -> None: 
        self.voice_client = await channel.connect()
        return

    async def disconnect(self) -> None:
        await self.voice_client.disconnect()
        self.voice_client = None
        return

    @commands.command(name="join_general")
    async def join_general(self, ctx: commands.Context) -> None:
        for voice_channel in ctx.guild.voice_channels:
            if voice_channel.name.lower() == "general":
                await self.connect(voice_channel)
                await ctx.send("Joined General voice")
                return 
        return
    
    @commands.command(name="join")
    async def join_voice(self, ctx: commands.Context, channel_name: str) -> None:
        if not channel_name:
            await ctx.send("Please specify a channel to join")

        async with ctx.typing():
            for voice_channel in ctx.guild.voice_channels:
                if voice_channel.name.lower() == channel_name.lower():
                    await self.connect(voice_channel)
                    await ctx.send(f"Joined {channel_name}")
                    return
            await ctx.send(f"Couldn't find channel with the name {channel_name}")
        return

    @commands.command(name="stream")
    async def stream(self, ctx: commands.Context, url: str, stream:bool = False) -> None:
        if not self.voice_client:
            await ctx.send("Not in voice channel! Add me to voice to start streaming music")
            return
        
        if not url:
            await ctx.send("Please provide a url")
            return

        async with ctx.typing():
            player = await self.from_url(url, loop=self.bot.loop, stream=stream)
            self.voice_client.play(player, after=lambda e: print(f"Player error: {e}") if e else None)
            await ctx.send("Playing url", mention_author=True)
        return 

    @commands.command()
    async def is_connected(self, ctx: commands.Context) -> None:
        await ctx.send(f"Connected to {ctx.message.channel.name} ({ctx.message.channel.type})")
    
    @commands.command(name="leave")
    async def leave(self, ctx) -> None:
        await self.disconnect()
        await ctx.send("Disconnected from voice")
     
    @commands.command(name="elevator")
    async def play_song(self, ctx) -> None:
        """ Play a local audio file called elevator.mp3 """

        await ctx.send("Playing elevator music")
        self.voice_client.play(discord.FFmpegPCMAudio('./assets/elevator.mp3'))
        return

    @commands.command(name="nightride")
    async def play_nightride(self, ctx) -> None:
        """ Play music from a stream url"""

        async with ctx.typing(): # Sends a typing indicator in the channel while the client attempts to play the stream
            self.voice_client.play(discord.FFmpegPCMAudio("https://stream.nightride.fm/nightride.m4a"))
        
        await ctx.send("Streaming from nightride fm")

    @commands.command(name="is_playing")
    async def is_playing(self, ctx) -> None:
        await ctx.send(self.voice_client.is_playing())
        return

    @commands.command(name="pause")
    async def pause(self, ctx) -> None:
        self.voice_client.pause()
        return

    @commands.command(name="play")
    async def play(self, ctx) -> None:
        self.voice_client.play()
        return 

    async def get_voice_channel(self, guild_id) -> None:
        general_channel = discord.utils.get(guild_id, "General")
        return general_channel

async def setup(bot):
    await bot.add_cog(VoiceCog(bot))

async def teardown(bot):
    #Ensure that the client stops before disconnect
    voice = await bot.get_cog("voice")
    if voice.voice_client:
        await voice.disconnect()
    
    await bot.remove_cog("voice")