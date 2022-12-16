import discord
import datetime
import DiscordUtils
import asyncio
from discord.ext import commands

music = DiscordUtils.Music()

class Music(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def leave(self, ctx):
        invc = ctx.author.voice
        botinvc = ctx.guild.me.voice
        if not botinvc:
            await ctx.send(f"{ctx.author.mention}, I'm not in a VC!")
            return
        if not invc:
            await ctx.send(f'{ctx.author.mention}, You are not in a VC!')
            return
        else:
            await ctx.guild.voice_client.disconnect() 
            await ctx.send("Left the VC!")

    @commands.command()
    async def play(self, ctx, *, url):
        invc = ctx.author.voice
        botinvc = ctx.guild.me.voice
        if not invc:
            await ctx.send(f'{ctx.author.mention}, You are not in a VC!')
            return
        if invc:
            if not botinvc:
                await ctx.author.voice.channel.connect()
                player = music.get_player(guild_id=ctx.guild.id)
                if not player:
                    player =  music.create_player(ctx, ffmpeg_error_betterfix=True)
                if not ctx.voice_client.is_playing():
                    await player.queue(url, search=True)
                    song = await player.play()
                    await ctx.send(f'Now Playing: `{song.name}`')
            
            if botinvc:
                player = music.get_player(guild_id=ctx.guild.id)
                if not player:
                    player =  music.create_player(ctx, ffmpeg_error_betterfix=True)
                if not ctx.voice_client.is_playing():
                    await player.queue(url, search=True)
                    song = await player.play()
                    await ctx.send(f'Now Playing: `{song.name}`')
                else:
                    song = await player.queue(url, search=True)
                    embed=discord.Embed(title='Song Added to Queue!', description=f'**{song.name}** added!', color=0x00FFFF)
                    embed.timestamp = datetime.datetime.utcnow()
                    embed.set_footer(text=f'Added by {ctx.author}')
                    await ctx.send(embed=embed)
        await asyncio.sleep(300)
        if not ctx.voice_client.is_playing():
            await ctx.guild.voice_client.disconnect() 
            await ctx.send("Left the VC due to inactivity!")
        else:
            pass

    @commands.command()
    async def pause(self, ctx):
        invc = ctx.author.voice
        botinvc = ctx.guild.me.voice
        if not botinvc:
            await ctx.send(f"{ctx.author.mention}, I'm not in a VC!")
            return
        if not invc:
            await ctx.send(f'{ctx.author.mention}, You are not in a VC!')
            return
        player = music.get_player(guild_id=ctx.guild.id)
        song = await player.pause()
        await ctx.send(f"Paused `{song.name}`!")
        await asyncio.sleep(300)
        if not ctx.voice_client.is_playing():
            await ctx.guild.voice_client.disconnect() 
            await ctx.send("Left the VC due to inactivity!")
        else:
            pass

    @commands.command()
    async def resume(self, ctx):
        invc = ctx.author.voice
        botinvc = ctx.guild.me.voice
        if not botinvc:
            await ctx.send(f"{ctx.author.mention}, I'm not in a VC!")
            return
        if not invc:
            await ctx.send(f'{ctx.author.mention}, You are not in a VC!')
            return
        player = music.get_player(guild_id=ctx.guild.id)
        song = await player.resume()
        await ctx.send(f"Resumed `{song.name}`!")
        await asyncio.sleep(300)
        if not ctx.voice_client.is_playing():
            await ctx.guild.voice_client.disconnect() 
            await ctx.send("Left the VC due to inactivity!")
        else:
            pass

    @commands.command()
    async def skip(self, ctx):
        invc = ctx.author.voice
        botinvc = ctx.guild.me.voice
        if not botinvc:
            await ctx.send(f"{ctx.author.mention}, I'm not in a VC!")
            return
        if not invc:
            await ctx.send(f'{ctx.author.mention}, You are not in a VC!')
            return
        player = music.get_player(guild_id=ctx.guild.id)
        try:
            await player.skip()
            await asyncio.sleep(1)
            song = player.now_playing()
            await ctx.send(f"Skipped! Now Playing `{song.name}`!")
        except:
            await ctx.send(f"There is nothing in the queue!")
            return
        await asyncio.sleep(300)
        if not ctx.voice_client.is_playing():
            await ctx.guild.voice_client.disconnect() 
            await ctx.send("Left the VC due to inactivity!")
        else:
            pass

    @commands.command()
    async def stop(self, ctx):
        invc = ctx.author.voice
        botinvc = ctx.guild.me.voice
        if not botinvc:
            await ctx.send(f"{ctx.author.mention}, I'm not in a VC!")
            return
        if not invc:
            await ctx.send(f'{ctx.author.mention}, You are not in a VC!')
            return
        player = music.get_player(guild_id=ctx.guild.id)
        await player.stop()
        await ctx.send("Music Stopped!")
        await asyncio.sleep(300)
        if not ctx.voice_client.is_playing():
            await ctx.guild.voice_client.disconnect() 
            await ctx.send("Left the VC due to inactivity!")
        else:
            pass

    @commands.command()
    async def loop(self, ctx):
        invc = ctx.author.voice
        botinvc = ctx.guild.me.voice
        player = music.get_player(guild_id=ctx.guild.id)
        if not botinvc:
            await ctx.send(f"{ctx.author.mention}, I'm not in a VC!")
            return
        if not invc:
            await ctx.send(f'{ctx.author.mention}, You are not in a VC!')
            return
        player = music.get_player(guild_id=ctx.guild.id)
        song = await player.toggle_song_loop()
        if song.is_looping:
            await ctx.send(f"`{song.name}` is now looping!")
        else:
            await ctx.send(f"`{song.name}` is not looping anymore!")
        await asyncio.sleep(300)
        if not ctx.voice_client.is_playing():
            await ctx.guild.voice_client.disconnect() 
            await ctx.send("Left the VC due to inactivity!")
        else:
            pass

    @commands.command()
    async def remove(self, ctx, song):
        player = music.get_player(guild_id=ctx.guild.id)
        song = await player.remove_from_queue(int(song))
        await ctx.send(f"Removed `{song.name}`` from the queue.")
        await asyncio.sleep(180)
        if not ctx.voice_client.is_playing():
            await ctx.guild.voice_client.disconnect() 
            await ctx.send("Left the VC due to inactivity!")
        else:
            pass

    @commands.command()
    async def playing(self, ctx):
        invc = ctx.author.voice
        botinvc = ctx.guild.me.voice
        player = music.get_player(guild_id=ctx.guild.id)
        song = player.now_playing()
        if not botinvc:
            await ctx.send(f"{ctx.author.mention}, I'm not in a VC!")
            return
        if not invc:
            await ctx.send(f'{ctx.author.mention}, You are not in a VC!')
            return
        await ctx.send(f'Currently playing: `{song.name}`')
        

    @commands.command()
    async def queue(self, ctx):
        invc = ctx.author.voice
        botinvc = ctx.guild.me.voice
        player = music.get_player(guild_id=ctx.guild.id)
        if not botinvc:
            await ctx.send(f"{ctx.author.mention}, I'm not in a VC!")
            return
        if not invc:
            await ctx.send(f'{ctx.author.mention}, You are not in a VC!')
            return
        nextline = " \n"
        player = music.get_player(guild_id=ctx.guild.id)
        queue = {nextline.join([song.name for song in player.current_queue()])}
        embed=discord.Embed(title=f'Current Queue for {ctx.guild.name}', description=f'{queue}', color=0x00FFFF)
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)
        await asyncio.sleep(180)
        if not ctx.voice_client.is_playing():
            await ctx.guild.voice_client.disconnect() 
            await ctx.send("Left the VC due to inactivity!")
        else:
            pass

def setup(client):
  client.add_cog(Music(client))