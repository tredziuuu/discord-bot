import discord
from discord.ext import commands
import json
import os

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

# Plik zapisu w miejscu dozwolonym przez Railway
FILE = "/tmp/rep.json"

# Tworzymy plik jeśli nie istnieje
if not os.path.exists(FILE):
    with open(FILE, "w") as f:
        json.dump({"count": 0}, f)

# Wczytujemy dane
with open(FILE, "r") as f:
    data = json.load(f)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="+", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot zalogowany jako {bot.user}")

@bot.command()
async def rep(ctx, user: discord.Member = None):
    data["count"] += 1

    # zapis do pliku
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

    # zmiana nazwy kanału
    channel = ctx.guild.get_channel(CHANNEL_ID)
    if channel:
        await channel.edit(name=f"✅𝐋𝐄𝐆𝐈𝐓𝐊𝐈-{data['count']}")

    await ctx.send(f"Rep dodany! Aktualny licznik: **{data['count']}**")

bot.run(TOKEN)
