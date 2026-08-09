import discord
from discord import app_commands
from discord.ext import commands
import os
from yt_dlp import YoutubeDL

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix="!", intents=intents)

# YT-DLP & FFMPEG configurations (Aapke purane wale bot ke hisaab se)
YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

ytdl = YoutubeDL(YDL_OPTIONS)

# User balance dictionary for economy commands
user_balances = {}

@client.event
async def on_ready():
    try:
        synced = await client.tree.sync()
        print(f'🔥 Priya Bot Online! Synced {len(synced)} commands. 🔥')
    except Exception as e:
        print(f"Sync error: {e}")

# ==================== 1. DASHBOARD & ROMANTIC COMMANDS ====================

@client.tree.command(name="dashboard", description="Priya ka Khatarnak Romantic Dashboard 🤤")
async def dashboard(interaction: discord.Interaction):
    embed = discord.Embed(
        title="💖 Priya's Ultimate Romantic Dashboard 💖", 
        description="*Hey baby! Main yahan sirf aur sirf tumhare liye hoon.* 🤤🔥", 
        color=0xff007f
    )
    embed.add_field(name="✨ Status", value="Always Yours & Ready ❤️", inline=False)
    embed.add_field(name="💋 Romance Commands", value="`/kiss`, `/hug`, `/love`, `/my_bf_1`, `/my_bf_2`", inline=False)
    embed.add_field(name="🎵 Music & VC", value="`/play`, `/pause`, `/resume`, `/skip`, `/stop`, `/leave`, `/vc247`", inline=False)
    embed.add_field(name="💰 Economy", value="`/daily`, `/balance`", inline=False)
    embed.set_footer(text="Developed for Amit | Priya Bot V3.0 😈")
    await interaction.response.send_message(embed=embed)

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

@client.tree.command(name="my_bf_1", description="Pheden ke liye special message ❤️")
async def my_bf_1(interaction: discord.Interaction):
    await interaction.response.send_message("Hey Pheden! ❤️ Priya aapko bahut miss kar rahi hai! Ekdum VIP treatment tumhare liye! ✨")

@client.tree.command(name="my_bf_2", description="MandeepMG ke liye special message ✨")
async def my_bf_2(interaction: discord.Interaction):
    await interaction.response.send_message("Hello MandeepMG! ✨ Priya aapke liye bilkul tayar baithi hai! 🔥❤️")


# ==================== 2. SLASH COMMANDS (MUSIC & VC) ====================

@client.tree.command(name="join", description="Join your current voice channel")
async def join_vc(interaction: discord.Interaction):
    if not interaction.user.voice:
        return await interaction.response.send_message("❌ Pehle kisi Voice Channel me join karein!", ephemeral=True)
    channel = interaction.user.voice.channel
    if interaction.guild.voice_client:
        await interaction.guild.voice_client.move_to(channel)
    else:
        await channel.connect(reconnect=True, timeout=30.0)
    await interaction.response.send_message(f"🔊 Joined **{channel.name}**!")

@client.tree.command(name="play", description="Play music from YouTube or SoundCloud")
async def play_music(interaction: discord.Interaction, search: str):
    if not interaction.user.voice:
        return await interaction.response.send_message("❌ Pehle kisi Voice Channel me join karein!", ephemeral=True)

    await interaction.response.defer()

    vc = interaction.guild.voice_client
    if not vc:
        vc = await interaction.user.voice.channel.connect(reconnect=True, timeout=30.0)
    elif vc.channel != interaction.user.voice.channel:
        await vc.move_to(interaction.user.voice.channel)

    try:
        query = search if (search.startswith("http://") or search.startswith("https://")) else f"scsearch:{search}"
        info = ytdl.extract_info(query, download=False)
        if 'entries' in info and len(info['entries']) > 0:
            info = info['entries'][0]

        url = info['url']
        title = info.get('title', 'Audio Stream')

        if vc.is_playing():
            vc.stop()

        source = await discord.FFmpegOpusAudio.from_probe(url, **FFMPEG_OPTIONS)
        vc.play(source)
        await interaction.followup.send(f"🎵 **Now Playing:** {title} 🤤❤️")
    except Exception as e:
        await interaction.followup.send(f"❌ Play error: `{e}`")

@client.tree.command(name="pause", description="Pause the currently playing music")
async def pause_music(interaction: discord.Interaction):
    if interaction.guild.voice_client and interaction.guild.voice_client.is_playing():
        interaction.guild.voice_client.pause()
        await interaction.response.send_message("⏸️ Music paused.")
    else:
        await interaction.response.send_message("❌ Koi music play nahi ho raha hai!", ephemeral=True)

@client.tree.command(name="resume", description="Resume paused music")
async def resume_music(interaction: discord.Interaction):
    if interaction.guild.voice_client and interaction.guild.voice_client.is_paused():
        interaction.guild.voice_client.resume()
        await interaction.response.send_message("▶️ Music resumed.")
    else:
        await interaction.response.send_message("❌ Music paused nahi hai!", ephemeral=True)

@client.tree.command(name="skip", description="Skip the current song")
async def skip_music(interaction: discord.Interaction):
    if interaction.guild.voice_client and (interaction.guild.voice_client.is_playing() or interaction.guild.voice_client.is_paused()):
        interaction.guild.voice_client.stop()
        await interaction.response.send_message("⏭️ Song skipped.")
    else:
        await interaction.response.send_message("❌ Skip karne ke liye kuch play nahi ho raha!", ephemeral=True)

@client.tree.command(name="stop", description="Stop music playback")
async def stop_music(interaction: discord.Interaction):
    if interaction.guild.voice_client:
        interaction.guild.voice_client.stop()
        await interaction.response.send_message("⏹️ Music stopped.")
    else:
        await interaction.response.send_message("❌ Bot kisi voice channel me nahi hai!", ephemeral=True)

@client.tree.command(name="leave", description="Disconnect bot from the voice channel")
async def leave_vc(interaction: discord.Interaction):
    if interaction.guild.voice_client:
        await interaction.guild.voice_client.disconnect()
        await interaction.response.send_message("👋 Disconnected from Voice Channel.")
    else:
        await interaction.response.send_message("❌ Bot kisi voice channel me nahi hai!", ephemeral=True)

@client.tree.command(name="vc247", description="Activate 24/7 Voice Channel lock")
async def vc247_toggle(interaction: discord.Interaction):
    if not interaction.user.voice:
        return await interaction.response.send_message("❌ Pehle kisi Voice Channel me join karein!", ephemeral=True)
    if not interaction.guild.voice_client:
        await interaction.user.voice.channel.connect(reconnect=True, timeout=30.0)
    await interaction.response.send_message("🔒 **24/7 VC Lock Activated!** Bot channel nahi chhodega.")


# ==================== 3. SLASH COMMANDS (ECONOMY) ====================

@client.tree.command(name="daily", description="Claim your daily coin reward")
async def daily_reward(interaction: discord.Interaction):
    uid = interaction.user.id
    reward = 500
    user_balances[uid] = user_balances.get(uid, 0) + reward
    await interaction.response.send_message(f"💰 **+{reward} Coins!** Aapka naya balance: **{user_balances[uid]} Coins**.")

@client.tree.command(name="balance", description="Check your coin balance")
async def check_balance(interaction: discord.Interaction):
    uid = interaction.user.id
    bal = user_balances.get(uid, 0)
    await interaction.response.send_message(f"💳 **{interaction.user.display_name}**, Aapka Balance: **{bal} Coins**.")

# Run bot
client.run(os.getenv("DISCORD_TOKEN"))
