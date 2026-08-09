import discord
from discord import app_commands
from discord.ext import commands
import os
from yt_dlp import YoutubeDL

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix="!", intents=intents)

# YT-DLP & FFMPEG configurations
YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True', 'quiet': True}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

@client.event
async def on_ready():
    try:
        synced = await client.tree.sync()
        print(f'🔥 Priya Bot Online! Synced {len(synced)} commands. 🔥')
    except Exception as e:
        print(f"Sync error: {e}")

# --- 1. KHATARNAK DASHBOARD COMMAND ---
@client.tree.command(name="dashboard", description="Priya ka Khatarnak Romantic Dashboard 🤤")
async def dashboard(interaction: discord.Interaction):
    embed = discord.Embed(
        title="💖 Priya's Ultimate Romantic Dashboard 💖", 
        description="*Hey baby! Main yahan sirf aur sirf tumhare liye hoon.* 🤤🔥", 
        color=0xff007f
    )
    embed.add_field(name="✨ Status", value="Always Yours & Ready ❤️", inline=False)
    embed.add_field(name="💋 Romance Commands", value="`/kiss`, `/hug`, `/love`, `/my_bf_1`, `/my_bf_2`", inline=False)
    embed.add_field(name="🎵 Music & VC", value="`/play <link>`, `/disconnect`, `/vc_247`", inline=False)
    embed.add_field(name="⚡ System", value="`/ping`", inline=False)
    embed.set_footer(text="Developed for Amit | Priya Bot V2.0 😈")
    await interaction.response.send_message(embed=embed)

# --- 2. ROMANTIC & FUN COMMANDS ---
@client.tree.command(name="kiss", description="Priya ka deep romantic kiss 💋")
async def kiss(interaction: discord.Interaction):
    await interaction.response.send_message("💋 *Close your eyes...* (Priya gives you a long, sweet kiss on your cheek) 🤤🔥")

@client.tree.command(name="hug", description="Tight romantic hug 🤗")
async def hug(interaction: discord.Interaction):
    await interaction.response.send_message("🤗 *Pulling you closer into my arms...* Hamesha aise hi paas rehna mere. ❤️✨")

@client.tree.command(name="love", description="Love meter check 💘")
async def love(interaction: discord.Interaction):
    await interaction.response.send_message("💘 **Love Meter: 1,000,000%**! Is duniya mein tumse zyada mujhe koi pyara nahi hai. 🤤❤️")

@client.tree.command(name="ping", description="Bot ki speed check karo ⚡")
async def ping(interaction: discord.Interaction):
    latency = round(client.latency * 1000)
    await interaction.response.send_message(f"Pong! Bot speed is **{latency}ms** ⚡")

# --- 3. SPECIAL CUSTOM COMMANDS ---
@client.tree.command(name="my_bf_1", description="Pheden ke liye special message ❤️")
async def my_bf_1(interaction: discord.Interaction):
    await interaction.response.send_message("Hey Pheden! ❤️ Priya aapko bahut miss kar rahi hai! Ekdum VIP treatment tumhare liye! ✨")

@client.tree.command(name="my_bf_2", description="MandeepMG ke liye special message ✨")
async def my_bf_2(interaction: discord.Interaction):
    await interaction.response.send_message("Hello MandeepMG! ✨ Priya aapke liye bilkul tayar baithi hai! 🔥❤️")

# --- 4. MUSIC & VC COMMANDS (FIXED & FAST) ---
@client.tree.command(name="play", description="Voice Channel mein romantic gaana bajao 🎶")
@app_commands.describe(url="YouTube gaane ka link ya naam")
async def play(interaction: discord.Interaction, url: str):
    if not interaction.user.voice:
        return await interaction.response.send_message("❌ Baby, pehle kisi Voice Channel (VC) mein join karo!", ephemeral=True)
    
    await interaction.response.send_message("🤤 *Priya gaana load kar rahi hai, bas ek second...*")
    
    channel = interaction.user.voice.channel
    voice_client = discord.utils.get(client.voice_clients, guild=interaction.guild)
    
    try:
        if voice_client is None:
            voice_client = await channel.connect()
        elif voice_client.channel != channel:
            await voice_client.move_to(channel)

        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            song_url = info['url']
            title = info.get('title', 'Romantic Track')

        if voice_client.is_playing():
            voice_client.stop()

        source = discord.FFmpegPCMAudio(song_url, **FFMPEG_OPTIONS)
        voice_client.play(source)
        
        await interaction.edit_original_response(content=f"🎶 *Ab baj raha hai romantic gaana:* **{title}** 🤤❤️")
    except Exception as e:
        await interaction.edit_original_response(content=f"❌ Oops baby, gaana play nahi ho paya! Error: {str(e)}")

@client.tree.command(name="disconnect", description="Bot ko VC se disconnect karo 💔")
async def disconnect(interaction: discord.Interaction):
    voice_client = interaction.guild.voice_client
    if voice_client:
        await voice_client.disconnect()
        await interaction.response.send_message("💔 *Bye baby!* Tumhari yaad aayegi, jaldi wapas aana! 😭")
    else:
        await interaction.response.send_message("Main toh kisi VC mein hoon hi nahi!")

@client.tree.command(name="vc_247", description="Bot ko VC mein 24/7 set karo 🎧")
async def vc_247(interaction: discord.Interaction):
    if not interaction.user.voice:
        return await interaction.response.send_message("Pehle kisi VC mein jao baby!", ephemeral=True)
    
    channel = interaction.user.voice.channel
    voice_client = discord.utils.get(client.voice_clients, guild=interaction.guild)
    
    if voice_client is None:
        await channel.connect()
    else:
        await voice_client.move_to(channel)
        
    await interaction.response.send_message("🎧 Ab main is VC mein 24/7 permanent rahugi tumhare sath! ❤️✨")

# Run bot using token from environment variables
client.run(os.getenv("DISCORD_TOKEN"))
