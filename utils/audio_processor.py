import os
import yt_dlp
from yt_dlp.networking.impersonate import ImpersonateTarget

def download_youtube_audio(youtube_url: str, output_path: str = "downloads") -> str:
    """
    Downloads audio from a YouTube URL with cloud-safe fallbacks.
    """
    os.makedirs(output_path, exist_ok=True)
    
    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'outtmpl': os.path.join(output_path, '%(id)s.%(ext)s'),
        'impersonate': ImpersonateTarget('chrome'),
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=True)
            filename = ydl.prepare_filename(info)
            return filename
    except Exception as e:
        raise RuntimeError(
            "YouTube has blocked direct downloads from this cloud server's IP address (403 Forbidden). "
            "Please use the **Browse files** uploader in the sidebar to upload your audio/video file directly!"
        ) from e

def process_input(youtube_url: str = None, uploaded_file = None, output_path: str = "downloads") -> str:
    """
    Processes either a YouTube URL or an uploaded audio file and returns the local path to the audio file.
    """
    os.makedirs(output_path, exist_ok=True)
    
    if youtube_url:
        return download_youtube_audio(youtube_url, output_path)
    elif uploaded_file is not None:
        file_path = os.path.join(output_path, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return file_path
    else:
        raise ValueError("Either youtube_url or uploaded_file must be provided.")