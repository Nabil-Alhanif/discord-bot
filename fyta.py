from asyncio import sleep
import discord
from discord.ext import commands
from discord.opus import Encoder
from discord.utils import get
from googletrans import Translator
from gtts import gTTS
import io
import shlex
import subprocess

class FFmpegPCMAudioMan(discord.AudioSource):
    def __init__(self, source, *, executable='ffmpeg', pipe=False, stderr=None, before_options=None, options=None):
        stdin = None if not pipe else source
        args = [executable]
        if isinstance(before_options, str):
            args.extend(shlex.split(before_options))
        args.append('-i')
        args.append('-' if pipe else source)
        args.extend(('-f', 's16le', '-ar', '48000', '-ac', '2', '-loglevel', 'warning'))
        if isinstance(options, str):
            args.extend(shlex.split(options))
        args.append('pipe:1')
        self._process = None
        try:
            self._process = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=stderr)
            self._stdout = io.BytesIO(
                self._process.communicate(input=stdin)[0]
            )
        except FileNotFoundError:
            raise discord.ClientException(executable + ' was not found.') from None
        except subprocess.SubprocessError as exc:
            raise discord.ClientException('Popen failed: {0.__class__.__name__}: {0}'.format(exc)) from exc
    def read(self):
        ret = self._stdout.read(Encoder.FRAME_SIZE)
        if len(ret) != Encoder.FRAME_SIZE:
            return b''
        return ret
    def cleanup(self):
        proc = self._process
        if proc is None:
            return
        proc.kill()
        if proc.poll() is None:
            proc.communicate()

        self._process = None

bot = commands.Bot(command_prefix='~', case_insensitive=True)

token = open('token.txt').read()

all_can_speak = False

def is_connected(ctx):
    voice_client = get(ctx.bot.voice_clients, guild=ctx.guild)
    return voice_client and voice_client.is_connected()

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.event
async def on_voice_state_update(member, before, after):
    if member == bot.user:
        try:
            if member.voice.mute:
                await member.edit(mute=False)
        except:
            pass

@bot.command(name='hello', description='Greet the user!', case_insensitive=True)
async def hello(ctx):
    creator = await bot.is_owner(ctx.message.author)
    if not creator:
        await ctx.send(f'hello {ctx.author.name}!')
    else:
        await ctx.send('Hello Creator')

@bot.command(name='allspeak', case_insensitive=True)
async def allspeak(ctx, *args):
    global all_can_speak

    silent = False

    for i in args:
        silent |= (i == 'silent')

    creator = await bot.is_owner(ctx.message.author)

    if creator:
        await ctx.send("Alright creator, from now on everyone can send speak command!")
        all_can_speak = True
        if not silent:
            await speak(ctx, 'Halo semuanya, sekarang kalian semua bisa ngirim perintah speak', hapus=False)
    else:
        await ctx.send("You are not my creator, thus I'm in no obligation to follow your order!")

@bot.command(name='ispeak', case_insensitive=True)
async def ispeak(ctx, *args):
    global all_can_speak

    silent = False

    for i in args:
        silent |= (i == 'silent')

    creator = await bot.is_owner(ctx.message.author)

    if creator:
        await ctx.send("Alright creator, from now on you're the only one who can send speak command!")
        all_can_speak = False
        if not silent:
            await speak(ctx, 'Halo semuanya, maaf ya, tapi sekarang tinggal kreator ku doang yang bisa ngirim perintah speak', hapus=False)
    else:
        await ctx.send("You are not my creator, thus I'm in no obligation to follow your order!")

@bot.command(name='join', case_insensitive=True)
async def join(ctx):
    message = ctx.message
    
    creator = await bot.is_owner(message.author)
    
    if not creator:
        await ctx.send("You are not my creator, thus I'm in no obligation to follow your order!")
        return

    author_voice_state = message.author.voice
    if author_voice_state is None:
        await message.channel.send("I'm sorry creator, but you must connected to a voice channel before I can assist you any further.")
    else:
        if is_connected(ctx):
            await message.channel.send("Creator, I'm already connected to the voice channel. If you think this is a mistake, please consult the logfile")
        else:
            await message.channel.send("Alright creator, I'm joining the voice channel now...")
            await message.author.voice.channel.connect()

@bot.command(name='speak', case_insensitive=True)
async def speak(ctx, *args, hapus=True):
    message = " ".join(args)
    await bacot(ctx, 'id', message, hapus=hapus)

@bot.command(name='bacot', case_insensitive=True)
async def bacot(ctx, country_code, *args, hapus=True):
    global all_can_speak

    creator = await bot.is_owner(ctx.message.author)
    sambung = "berkata"

    comment_voice_state = ctx.message.author.voice

    if not creator and not all_can_speak:
        return

    if comment_voice_state is None and not creator:
        await ctx.send("You must be connected to a voice channel before you can use speak command!")
        return
    
    message = " ".join(args)

    translator = Translator()
    try:
        sambung2 = translator.translate(sambung, dest=country_code)
        sambung = sambung2.text
    except:
        message = country_code + ' ' + message

    if not creator:
        message = str(ctx.message.author) + " " + str(sambung) + " " + message
    print(message)

    tts = gTTS(text=message, lang='id')
    try:
        tts2 = gTTS(text=message, lang=country_code)
        tts = tts2
    except:
        pass
    mp3_fp = io.BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    
    if hapus:
        await ctx.message.delete()
    
    file = FFmpegPCMAudioMan(mp3_fp.read(), pipe=True)
    if not is_connected(ctx):
        voice_channel = ctx.message.author.voice.channel
        await voice_channel.connect()

    voice_client = get(ctx.bot.voice_clients, guild=ctx.guild)
    voice_client.play(file)

@bot.command(name='leave', case_insensitive=True)
async def leave(ctx):
    global all_can_speak
    creator = await bot.is_owner(ctx.message.author)

    if not creator:
        await ctx.send("You are not my creator, thus I'm in no obligation to follow your order!")
        return
    else:
        if is_connected(ctx):
            await ctx.send("Alright creator, I'm disconnecting now. It is my pleasure to assist you...")
            await ctx.voice_client.disconnect()
            all_can_speak = False
        else:
            await ctx.send("Creator, I'm currently not connected to any voice channel. If you think this is a mistake, please consult the logfile")

if __name__ == "__main__":
    bot.run(token)
