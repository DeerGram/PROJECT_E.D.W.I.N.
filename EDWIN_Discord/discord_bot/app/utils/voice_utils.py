import os
import openai
from google.cloud import speech_v1p1beta1 as speech
from google.cloud import texttospeech_v1 as texttospeech
from google.cloud import translate_v2 as translate
import youtube_dl
from pydub import AudioSegment

openai.api_key = api_keys[user_id]["OPENAI_API_KEY"]

def api_keys_valid(user_id):
    if user_id not in api_keys:
        return False

    user_keys = api_keys[user_id]

    for key, value in user_keys.items():
        if value == 'your-key-here' or not value.strip():
            return False

    return True

def extract_audio_from_video(video_url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
        'outtmpl': 'temp_audio.%(ext)s',
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    audio = AudioSegment.from_wav("temp_audio.wav")
    audio.export("audio_for_transcription.wav", format="wav")

def transcribe_audio_with_diarization(user_id, audio_file):
    client = speech.SpeechClient()

    with open(audio_file, 'rb') as audio:
        audio_content = audio.read()

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
        enable_speaker_diarization=True,
        diarization_speaker_count=2,
    )

    audio = speech.RecognitionAudio(content=audio_content)

    response = client.recognize(config=config, audio=audio)

    return response

def translate_text(transcription_response, target_language):
    translator = Translator()
    full_text = ""
    for result in transcription_response.results:
        for word_info in result.alternatives[0].words:
            word = word_info.word
            full_text += f"{word} "

    translated_text = translator.translate(full_text, dest=target_language).text
    return translated_text

def synthesize_audio(text, voice_id):
    client = texttospeech.TextToSpeechClient()
    input_text = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name=voice_id,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
    )

    response = client.synthesize_speech(
        request={"input": input_text, "voice": voice, "audio_config": audio_config}
    )

    return response.audio_content