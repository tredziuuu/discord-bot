import discord
from discord.ext import commands
import json
import os

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

FILE = "/tmp/rep.json"

if not os.path.exists(FILE):
    with open(FILE, "w") as f:
        json.dump({"count": 0}, f)

with open(FILE, "r") as f:
    data = json.load(f)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="+", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot zalogowany jako {bot.user}")

# COOLDOWN: 1 użycie co 60 sekund na kanał
@commands.cooldown(1, 60, commands.BucketType.channel)
@bot.command()
async def rep(ctx, user: discord.Member = None):
    data["count"] += 1

    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

    channel = ctx.guild.get_channel(CHANNEL_ID)
    if channel:
        try:
            await channel.edit(name=f"✅𝐋𝐄𝐆𝐈𝐓𝐊𝐈-{data['count']}")
        except discord.HTTPException:
            await ctx.send("⚠️ Discord chwilowo blokuje zmianę nazwy kanału. Spróbuj za chwilę.")

    await ctx.send(f"Rep dodany! Aktualny licznik: **{data['count']}**")

# Obsługa spamu
@rep.error
async def rep_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"⏳ Zwolnij! Możesz użyć komendy ponownie za **{round(error.retry_after)}s**.")

bot.run(TOKEN)

