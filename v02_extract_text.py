import os
from openai import OpenAI
from moviepy.editor import VideoFileClip
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

# Load the video file
video = VideoFileClip("rohan_joshi.mp4")
audio = video.audio

# Define chunk size in bytes and calculate chunk duration in seconds
chunk_size = 24 * 1024 * 1024  # 24MB in bytes
bitrate = audio.fps * audio.nchannels * 16  # Assuming 16-bit audio
chunk_duration = chunk_size / (bitrate / 8)  # in seconds

# Split audio into chunks
chunks = [audio.subclip(i, min(i + chunk_duration, audio.duration)) for i in range(0, int(audio.duration), int(chunk_duration))]

for i, chunk in enumerate(chunks):
    chunk_filename = f"chunk_{i}.mp3"
    chunk.write_audiofile(chunk_filename, codec="mp3")
    with open(chunk_filename, "rb") as chunk_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1", 
            file=chunk_file
        )
    print(transcription.text)
    with open('rohan_joshi_moviepy_transcript.txt', 'a') as file:
        file.write(transcription.text)