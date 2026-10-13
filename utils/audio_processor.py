import os
import tempfile
import yt_dlp
from pydub import AudioSegment

DOWNLOAD_DIR = 'downloades'
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def get_ydl_opts():
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
        }],
        'outtmpl': 'downloads/%(id)s.%(ext)s',
        'noplaylist': True,
        'socket_timeout': 30,
        'geo_bypass': True,
        'nocheckcertificate': True,
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'web'],
            }
        },
    }

    # Check if cookies are provided via environment variables (Render Secrets)
    cookies_content = os.getenv("YOUTUBE_COOKIES")
    if cookies_content:
        cookie_file = tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt")
        cookie_file.write(cookies_content)
        cookie_file.close()
        ydl_opts['cookiefile'] = cookie_file.name

    return ydl_opts

def download_youtube_audio(url: str) -> str:
    ydl_opts = get_ydl_opts()
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        # Handle extension replacements safely
        wav_path = os.path.splitext(filename)[0] + ".wav"
        if not os.path.exists(wav_path):
            # Fallback check if postprocessor named it differently
            wav_path = filename.replace(".webm", ".wav").replace(".m4a", ".wav").replace(".mp4", ".wav")
    return wav_path

def convert_to_wav(input_path: str) -> str:
    """Convert any audio/video file to WAV format using pydub."""
    output_path = os.path.splitext(input_path)[0] + "_converted.wav"
    audio = AudioSegment.from_file(input_path)
    audio = audio.set_channels(1).set_frame_rate(16000) # 16khz
    audio.export(output_path, format="wav")
    return output_path

def chunk_audio(wav_path: str, chunk_minutes: int = 10) -> list:
    audio = AudioSegment.from_wav(wav_path)
    chunk_ms = chunk_minutes * 60 * 1000 

    chunks = []

    for i, start in enumerate(range(0, len(audio), chunk_ms)):
        chunk = audio[start : start + chunk_ms]
        chunk_path = f"{wav_path}_chunk_{i}.wav"
        chunk.export(chunk_path, format="wav")
        chunks.append(chunk_path)
    
    return chunks

def process_input(source: str) -> list:
    if source.startswith("http://") or source.startswith("https://"):
        print("Detected YouTube URL. Downloading audio...")
        wav_path = download_youtube_audio(source)
    else:
        print("Detected local file. Converting to WAV...")
        wav_path = convert_to_wav(source)

    print("Chunking audio...")
    chunks = chunk_audio(wav_path)
    print(f"Audio ready — {len(chunks)} chunk(s) created.")
    return chunks