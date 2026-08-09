import discord
from discord import app_commands
from discord.ext import commands
import os
from yt_dlp import YoutubeDL

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix="!", intents=intents)

# Music Options
YDL_OPTIONS = {'format': 'bestaudio', 'quiet': True}
FFMPEG_OPTIONS = {'options': '-vn'}

@client.event
async def on_ready():
    await client.tree.sync()
    print(f'🔥 Priya is ready to rule the server! 🔥')

# --- KHATARNAK EMBED DASHBOARD ---
@client.tree.command(name="dashboard", description="Priya ka Khatarnak Dashboard 🤤")
async def dashboard(interaction: discord.Interaction):
    embed = discord.Embed(title="💖 Priya's Romantic Dashboard 💖", description="*Hey baby! Main yahan sirf tumhare liye hoon.* 🤤", color=0xff007f)
    embed.add_field(name="✨ Status", value="Always Yours ❤️", inline=False)
    embed.add_field(name="💋 Special Commands", value="/kiss, /hug, /love, /my_bf_1, /my_bf_2", inline=False)
    embed.add_field(name="🎵 Music", value="/play <link>, /disconnect", inline=False)
    embed.set_footer(text="Developed by Amit | Priya Bot V1.0 😈")
    await interaction.response.send_message(embed=embed)

# --- ROMANTIC COMMANDS ---
@client.tree.command(name="kiss", description="Priya ka deep kiss 💋")
async def kiss(interaction: discord.Interaction):
    await interaction.response.send_message("💋 *Close your eyes...* (Priya gives you a long, romantic kiss) 🤤🔥")

@client.tree.command(name="hug", description="Tight romantic hug 🤗")
async def hug(interaction: discord.Interaction):
    await interaction.response.send_message("🤗 *Pulling you closer...* Hamesha aise hi raho mere saath. ❤️✨")

@client.tree.command(name="love", description="Love meter check 💘")
async def love(interaction: discord.Interaction):
    await interaction.response.send_message("💘 **Love Meter: 1,000,000%**! Tumse zyada mujhe koi nahi janta. 🤤❤️")

# --- MUSIC & VC ---
@client.tree.command(name="play", description="Romantic gaane bajao 🎶")
async def play(interaction: discord.Interaction, url: str):
    if not interaction.user.voice:
        return await interaction.response.send_message("❌ Baby, VC join karo pehle!")
    
    channel = interaction.user.voice.channel
    voice_client = await channel.connect() if not interaction.guild.voice_client else interaction.guild.voice_client
    
    await interaction.response.defer()
    with YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)
        url_link = info['url']
        source = discord.FFmpegPCMAudio(url_link, **FFMPEG_OPTIONS)
        voice_client.play(source)
        await interaction.followup.send(f"🎶 *Playing your romantic track:* **{info['title']}** 🤤❤️")

@client.tree.command(name="disconnect", description="Goodbye for now 💔")
async def disconnect(interaction: discord.Interaction):
    if interaction.guild.voice_client:
        await interaction.guild.voice_client.disconnect()
        await interaction.response.send_message("💔 *Bye baby!* Tumhari yaad aayegi. 😭")

client.run(os.getenv("DISCORD_TOKEN"))
