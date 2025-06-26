import yt_dlp
import os
from pathlib import Path
from urllib.parse import urlparse, parse_qs

def extract_video_id(url: str) -> str:
    """
    Extract video ID from YouTube URL
    
    Args:
        url (str): YouTube URL
        
    Returns:
        str: Video ID
        
    Raises:
        ValueError: If video ID cannot be extracted
    """
    # Try parsing URL query parameters
    parsed_url = urlparse(url)
    
    # Check if it's a standard youtube.com URL
    if 'youtube.com' in parsed_url.netloc:
        query_params = parse_qs(parsed_url.query)
        if 'v' in query_params:
            return query_params['v'][0]
            
    # Check if it's a youtu.be URL
    elif 'youtu.be' in parsed_url.netloc:
        return parsed_url.path.lstrip('/')
        
    raise ValueError("Could not extract video ID from URL")

def get_default_download_path() -> str:
    """Get the default Windows Downloads folder path"""
    return os.path.join(os.path.expanduser("~"), "Downloads")

def download_youtube_video(url: str, output_path: str = None) -> str:
    """
    Download a YouTube video using yt-dlp. Retries up to 5 times if download fails.
    
    Args:
        url (str): The URL of the YouTube video
        output_path (str, optional): The path where the video should be saved. 
                                   If not provided, saves in the Windows Downloads folder.
    
    Returns:
        str: Path to the downloaded video file
    
    Raises:
        Exception: If download fails after 5 attempts
    """
    max_retries = 5
    last_exception = None
    for attempt in range(1, max_retries + 1):
        try:
            # Set default path to Windows Downloads folder if not provided
            if output_path is None:
                output_path = get_default_download_path()
            
            # Create the output directory if it doesn't exist
            Path(output_path).mkdir(parents=True, exist_ok=True)
            
            # Extract video ID for filename
            video_id = extract_video_id(url)
            
            # Configure yt-dlp options
            ydl_opts = {
                'format': 'bestvideo[height=1080][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height=720][ext=mp4]+bestaudio[ext=m4a]/best[height=1080]/best[height=720]/best',
                'outtmpl': os.path.join(output_path, f'{video_id}.%(ext)s'),
                'quiet': True,
                'no_warnings': True,
                'extract_audio': False,
                'merge_output_format': 'mp4'
            }
            
            # Create yt-dlp object with the options
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Download the video and get info
                info = ydl.extract_info(url, download=True)
                video_path = os.path.join(output_path, f"{video_id}.mp4")
                return video_path
        except Exception as e:
            last_exception = e
            if attempt < max_retries:
                continue  # Try again
            else:
                raise Exception(f"Failed to download video after {max_retries} attempts: {str(last_exception)}")