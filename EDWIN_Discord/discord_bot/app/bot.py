import openai
from discord.ext import commands

class EDWINBot(commands.Bot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        openai.api_key = self.openai_api_key

    async def transcribe_audio(self, audio_file):
        with open(audio_file, "rb") as file:
            transcript = openai.Audio.transcribe("whisper-1", file)
        return transcript["text"]

    async def generate_gpt_response(self, messages):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        return response.choices[0].message.content

    async def text_to_speech_descript(self, text, voice_id, voice_style_id):
        payload = {
            "text": text,
            "voice_id": voice_id,
            "voice_style_id": voice_style_id
        }
        headers = {
            "Authorization": f"Bearer {os.getenv('DESCRIPT_API_KEY')}",
            "Content-Type": "application/json"
        }
        response = requests.post("https://api.descript.com/v1/audio/generate", json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["url"]
