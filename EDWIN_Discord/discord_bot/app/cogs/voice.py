import discord
from discord.ext import commands
from utils.voice_utils import process_voice_generation
import utils.voice_utils as voice_utils

class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def transcribe(self, ctx):
        user_id = ctx.author.id

        if not voice_utils.api_keys_valid(user_id):
            await ctx.send("Invalid API keys detected. Please input your credentials using the !set_api_keys command.")
            return

        audio_file_path = "path/to/audio_file.wav"
        transcription_response = voice_utils.transcribe_audio_with_diarization(user_id, audio_file_path)
        await ctx.send("Transcription completed. Check the console for the output.")

    @commands.command()
    async def voice(self, ctx, *, input_data):
        await ctx.send('Starting the voice generation process...')
        response_message = process_voice_generation(input_data)
        await ctx.send(response_message)

def setup(bot):
    bot.add_cog(Voice(bot))