Project E.D.W.I.N. (Empowering Digital Worlds with Intelligent Narration) is a cutting-edge SAAS solution designed to streamline content localization for medium to large YouTube channels, social media creators, and e-learning platforms. E.D.W.I.N. leverages advanced AI-driven voice-overs and translations to make video content globally accessible and adaptable.

You can use the /voice command to generate text-to-speech audio dubs and obtain transcriptions for video content in your desired language. The bot can process both video URLs and SRT files. Follow the guidelines below to interact with the bot:

1️⃣ To use the /voice command with a video URL:
Type /voice url [video_url] and replace [video_url] with the actual URL of the video you'd like to transcribe and generate audio dubs for.

2️⃣ To use the /voice command with an SRT file:
Type /voice srt and attach the SRT file you'd like to generate audio dubs for.

🌐 Translation:
If you'd like to translate the transcription before generating audio dubs, add the translate keyword followed by the target language code (e.g., en, es, fr) to the command.
For example: /voice url [video_url] translate fr

🎚️ Process:
The bot will perform the following steps:
- Extract the video URL or SRT file.
- Transcribe the video using the Whisper API.
- (Optional) Correct transcription errors using GPT-3.5 Turbo (GPT-4 optional for demanding video scipts).
- (Optional) Translate the transcription.
- Generate text-to-speech audio dubs using Azure or Descript API.
    If translated add following steps:
    - Use the timings of the subtitle lines to calculate the correct duration of each spoken audio clip
    - Perform a second pass to with the adjusted speed to match the.
- Once the audio dubs are generated, the bot will provide a link to download or listen to them, as well as the transcribed and translated text output. You can review the text and make any additional edits if necessary.

Please note that the transcription, translation, and audio generation process may take some time depending on the size and duration of the video. Your patience is appreciated!

Happy dubbing! 🎧