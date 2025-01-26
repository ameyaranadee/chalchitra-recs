import os
from openai import OpenAI
from pydub import AudioSegment
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

yt_video = open("rohan_joshi.mp4", "rb")
audio_file = AudioSegment.from_file(yt_video, format="mp4")

# PyDub handles time in milliseconds
chunk_size = 24 * 1024 * 1024  # 24MB in bytes
chunk_duration = (chunk_size / (audio_file.frame_rate * audio_file.frame_width * audio_file.channels)) * 1000  # in milliseconds

chunks = [audio_file[i:i + chunk_duration] for i in range(0, len(audio_file), chunk_duration)]

for i, chunk in enumerate(chunks):
    chunk.export(f"chunk_{i}.mp3", format="mp3")
    transcription = client.audio.transcriptions.create(
        model="whisper-1", 
        file=chunk
    )
    print(transcription.text)
    with open('rohan_joshi_transcript.txt', 'a') as file:
        file.write(transcription.text)