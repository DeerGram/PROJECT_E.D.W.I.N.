import os
import discord
import cogs.chatbot
import cogs.voice
import cogs.instant_translation
from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = "!"

client = discord.Client()

api_keys = {}

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} is connected to the following guilds:")
    for guild in bot.guilds:
        print(f"{guild.name}(id: {guild.id})")

@bot.command()
async def set_api_keys(ctx, openai_key: str, descript_key: str, google_key: str):
    user_id = ctx.author.id
    api_keys[user_id] = {
        "OPENAI_API_KEY": openai_key,
        "DESCRIPT_API_KEY": descript_key,
        "GOOGLE_APPLICATION_CREDENTIALS": google_key
    }
    await ctx.send("API keys have been set successfully.")

bot.load_extension("cogs.chatbot")
bot.load_extension("cogs.voice")
bot.load_extension("cogs.instant_translation")

bot.run(TOKEN)