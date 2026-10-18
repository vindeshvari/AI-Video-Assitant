import os
import re
from youtube_transcript_api import YouTubeTranscriptApi

def extract_video_id(url):
    """Extracts the 11-character video ID from various YouTube URL formats."""
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'(?:embed\/)([0-9A-Za-z_-]{11})',
        r'(?:watch\?v=)([0-9A-Za-z_-]{11})'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return url if len(url) == 11 else None

def download_youtube_audio(url):
    """
    Fetches the transcript text directly using the updated youtube-transcript-api.
    """
    video_id = extract_video_id(url)
    if not video_id:
        raise ValueError("Invalid YouTube URL provided.")
    
    try:
        # Instantiate the API and fetch the transcript
        ytt_api = YouTubeTranscriptApi()
        fetched_transcript = ytt_api.fetch(video_id)
        
        # Convert fetched transcript items to text
        raw_data = fetched_transcript.to_raw_data()
        full_transcript = " ".join([item['text'] for item in raw_data])
        return full_transcript
    except Exception as e:
        raise RuntimeError(f"Could not fetch YouTube transcript: {e}")

def process_input(source):
    """
    Main entry point called by app.py.
    Checks if the source is a YouTube URL and retrieves its text transcript.
    """
    if "youtube.com" in source or "youtu.be" in source:
        return download_youtube_audio(source)
    else:
        raise NotImplementedError("Local file processing should remain handled by your existing upload logic.")