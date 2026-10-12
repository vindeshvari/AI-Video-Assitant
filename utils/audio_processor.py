import os
import yt_dlp

def download_youtube_audio(youtube_url: str, output_path: str = "downloads") -> str:
    """
    Downloads audio from a YouTube URL using yt-dlp with client impersonation 
    to bypass cloud data center 403 Forbidden restrictions.
    """
    os.makedirs(output_path, exist_ok=True)
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_path, '%(id)s.%(ext)s'),
        'impersonate': 'chrome',
        'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
        'no_warnings': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=True)
        filename = ydl.prepare_filename(info)
        base, _ = os.path.splitext(filename)
        audio_file = f"{base}.mp3"
        return audio_file