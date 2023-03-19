import discord
from discord.ext import commands
import openai

openai.api_key = api_keys[user_id]["OPENAI_API_KEY"]

class Chatbot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.system_message = {"role": "system", "content": "Hello, I am E.D.W.I.N. Your helpful assistant. I can assist you with questions about the functionality of the bot and help you format SRT files correctly. What can I help you with today?"}

    @commands.command()
    async def chat(self, ctx, *, text: str):
        user_message = {"role": "user", "content": text}
        messages = [self.system_message, user_message]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
        )
        reply = response["choices"][0]["message"]["content"].strip()
        await ctx.send(reply)

def setup(bot):
    bot.add_cog(Chatbot(bot))