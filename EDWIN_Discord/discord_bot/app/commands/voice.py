import os
import asyncio
from discord.ext import commands
from discord import FFmpegPCMAudio

class VoiceCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='join')
    async def join(self, ctx):
        channel = ctx.author.voice.channel
        await channel.connect()

    @commands.command(name='leave')
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()

    @commands.command(name='translate')
    async def translate(self, ctx, audio_file, api_preference='google'):
        transcript = await self.bot.transcribe_audio(audio_file)
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": transcript},
        ]
        response = await self.bot.generate_gpt_response(messages)

        if api_preference.lower() == 'azure':
            raise NotImplementedError("Azure TTS support is not implemented yet.")
        else:
            voice_id = "2235c634-e4db-4ad6-aa15-066fb69b1c8f" # Replace with desired voice ID
            voice_style_id = "b9a0ebf3-b259-4b98-975c-a847678f9faf" # Replace with desired voice style ID
            audio_url = await self.bot.text_to_speech_descript(response, voice_id, voice_style_id)

        await ctx.send(response)

        # Download audio file
        audio_path = os.path.join('temp', 'response.mp3')
        with open(audio_path, 'wb') as f:
            f.write(requests.get(audio_url).content)

        # Play audio in the voice channel
        audio_source = FFmpegPCMAudio(audio_path)
        ctx.voice_client.play(audio_source)

        # Delete the temporary audio file
        os.remove(audio_path)

def setup(bot):
    bot.add_cog(VoiceCommands(bot))
