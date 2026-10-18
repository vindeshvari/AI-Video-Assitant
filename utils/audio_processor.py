import yt_dlp
from pydub import AudioSegment
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError
import os

DOWNLOAD_DIR = 'downloades'
os.makedirs(DOWNLOAD_DIR,exist_ok = True)


def download_youtube_audio(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
        'extractor_args': {
            'youtube': {
                'player_client': ['mweb', 'android']
            }
        },
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'no_warnings': True,
        'quiet': True,
    }

    try:
        os.makedirs("downloads", exist_ok=True)
        output_template = os.path.join("downloads", "%(title)s.%(ext)s")
        ydl_opts['outtmpl'] = output_template

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            base, _ = os.path.splitext(filename)
            wav_path = base + ".wav"
            return wav_path
            
    except DownloadError as e:
        raise RuntimeError(
            "YouTube blocks direct media downloads from cloud hosting servers (Streamlit Cloud IP restriction). "
            "To use this app with YouTube links, please run the project locally on your computer where your residential IP is allowed."
        )



def convert_to_wav(input_path: str) -> str:
    """Convert any audio/video file to WAV format using pydub."""
    output_path = os.path.splitext(input_path)[0] + "_converted.wav"
    audio = AudioSegment.from_file(input_path)
    audio = audio.set_channels(1).set_frame_rate(16000) #16khz
    audio.export(output_path, format="wav")
    return output_path



def chunk_audio(wav_path : str , chunk_minutes : int = 10) -> list:
    audio = AudioSegment.from_wav(wav_path)
    chunk_ms = chunk_minutes * 60 * 1000 

    chunks = []

    for i, start in enumerate(range(0,len(audio),chunk_ms)):
        chunk = audio[start : start + chunk_ms]
        chunk_path = f"{wav_path}_chunk_{i}.wav"
        chunk.export(chunk_path , format = "wav")

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

