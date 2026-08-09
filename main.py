import discord
from discord import app_commands
from discord.ext import commands
import os
from yt_dlp import YoutubeDL

# Bot setup with intents
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix="!", intents=intents)

# YT-DLP options for music streaming
YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

@client.event
async def on_ready():
    print(f'Bot Online as {client.user}!')
    try:
        synced = await client.tree.sync()
        print(f'Synced {len(synced)} slash commands.')
    except Exception as e:
        print(e)

# 1. Kiss Command
@client.tree.command(name="kiss", description="Priya ka sweet kiss 😘")
async def kiss(interaction: discord.Interaction):
    await interaction.response.send_message("Muuah! 😘 Sirf aapke liye! ✨")

# 2. Hug Command
@client.tree.command(name="hug", description="Priya ka hug 🤗")
async def hug(interaction: discord.Interaction):
    await interaction.response.send_message("Awww, idhar aao! 🤗 Ek tight hug! ❤️")

# 3. Love Command
@client.tree.command(name="love", description="Love check karo ❤️")
async def love(interaction: discord.Interaction):
    await interaction.response.send_message("Pyar ka score 100% hai! ❤️🥰")

# 4. Ping Command
@client.tree.command(name="ping", description="Bot ki speed ⚡")
async def ping(interaction: discord.Interaction):
    latency = round(client.latency * 1000)
    await interaction.response.send_message(f"Pong! {latency}ms ⚡")

# 5. My BF 1 (Pheden)
@client.tree.command(name="my_bf_1", description="Pheden ke liye special message ❤️")
async def my_bf_1(interaction: discord.Interaction):
    await interaction.response.send_message("Hey Pheden! ❤️ Priya aapko bahut miss kar rahi hai! ✨")

# 6. My BF 2 (MandeepMG)
@client.tree.command(name="my_bf_2", description="MandeepMG ke liye special message ✨")
async def my_bf_2(interaction: discord.Interaction):
    await interaction.response.send_message("Hello MandeepMG! ✨ Priya aapke liye hazir hai! ❤️")

# 7. Play Music Command (VC Join & Play)
@client.tree.command(name="play", description="Gaana play karo 🎶")
@app_commands.describe(url="YouTube ka link ya gaane ka naam")
async def play(interaction: discord.Interaction, url: str):
    if not interaction.user.voice:
        return await interaction.response.send_message("Pehle kisi Voice Channel (VC) mein join karo My BF! 🎶", ephemeral=True)

    voice_channel = interaction.user.voice.channel
    
    if interaction.guild.voice_client is not None:
        await interaction.guild.voice_client.move_to(voice_channel)
    else:
        await voice_channel.connect()

    await interaction.response.defer()

    server = interaction.guild
    voice_client = server.voice_client

    try:
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            if 'entries' in info:
                info = info['entries'][0]
            song_url = info['url']
            title = info.get('title', 'Audio')

        if voice_client.is_playing():
            voice_client.stop()

        source = discord.FFmpegPCMAudio(song_url, **FFMPEG_OPTIONS)
        voice_client.play(source)

        await interaction.followup.send(f"🎵 Play ho raha hai: **{title}**")
    except Exception as e:
        print(f"Music Error: {e}")
        await interaction.followup.send("❌ Gaana play karne mein error aa gaya!")

client.run(os.getenv("DISCORD_TOKEN"))
