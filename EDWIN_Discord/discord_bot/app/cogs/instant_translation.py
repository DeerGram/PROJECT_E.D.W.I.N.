import discord
import numpy as np
import pydub
from discord.ext import commands
from utils.voice_utils import (
    transcribe_audio,
    translate_text,
    synthesize_audio,
)

# define function to transcribe audio using OpenAI Whisper API
def transcribe_audio_whisper(user_id, audio_data):
    openai.api_key = api_keys[user_id]["OPENAI_API_KEY"]
    
    model_engine = "davinci"
    response = openai.File.create(
        file=audio_data.tobytes(),
        purpose="transcription",
    )
    job_id = response["id"]

    # Poll for job completion
    while True:
        job = openai.File.retrieve(job_id)
        if job["status"] == "done":
            break
        time.sleep(1)

    transcript = job["plaintext"]
    return transcript

class InstantTranslation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def instant_translate(self, ctx, target_language: str):
        # Check if user is in a voice channel
        if not ctx.author.voice:
            await ctx.send("You need to be in a voice channel to use this command.")
            return

        # Get the user's voice channel and connect to it
        voice_channel = ctx.author.voice.channel
        voice_client = await voice_channel.connect()

        # Start listening for user's audio input
        def check_author(author):
            def inner_check(message):
                return message.author == author and message.content != ""

            return inner_check

        try:
            await ctx.send("Please start speaking.")
            user_audio_message = await self.bot.wait_for("message", timeout=10.0, check=check_author(ctx.author))
        except:
            await ctx.send("Timeout. Please try again.")
            return

        # Configure the audio stream
        voice_client.listen(discord.reader.ConditionalFilter(discord.reader.AudioReader()))

        # Get the user's audio data
        def get_audio_data(data):
            # convert data to numpy array
            samples = np.frombuffer(data, dtype=np.int16)
            # convert numpy array to bytes
            audio_bytes = samples.tobytes()
            return audio_bytes

        audio_data = b""
        while not voice_client.is_playing():
            audio_data += await self.bot.loop.run_in_executor(None, get_audio_data, await voice_client.receive())

        # Call Whisper API for transcription
        transcript = transcribe_audio_whisper(audio_data)

        # Translate the transcribed text
        translated_text = translate_text(transcript, target_language)

        # Synthesize the translated text into audio
        audio_url = synthesize_audio(translated_text, "your_google_cloud_voice_id")

        # Play the synthesized audio in the voice channel
        audio_source = discord.FFmpegPCMAudio(audio_url)
        voice_client.play(audio_source)
        while voice_client.is_playing():
            await asyncio.sleep(1)
        voice_client.stop()

        # Disconnect from the voice channel
        await voice_client.disconnect()

        response_message = "Instant translation completed, and disconnected from voice channel."
        await ctx.send(response_message)

def setup(bot):
    bot.add_cog(InstantTranslation(bot))