import yt_dlp
import os
from pathlib import Path

def download_youtube_video(url: str, output_path: str = None) -> str:
    """
    Download a YouTube video using yt-dlp.
    
    Args:
        url (str): The URL of the YouTube video
        output_path (str, optional): The path where the video should be saved. 
                                   If not provided, saves in the current directory.
    
    Returns:
        str: Path to the downloaded video file
    
    Raises:
        Exception: If download fails
    """
    try:
        if output_path:
            # Create the output directory if it doesn't exist
            Path(output_path).mkdir(parents=True, exist_ok=True)
          # Configure yt-dlp options
        ydl_opts = {
            'format': 'bestvideo[height=1080][ext=mp4]+bestaudio[ext=m4a]/best[height=1080]/best',  # Prioritize 1080p MP4
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s') if output_path else '%(title)s.%(ext)s',
            'quiet': True,
            'no_warnings': True,
            'extract_audio': False,
            'merge_output_format': 'mp4'  # Ensure final output is MP4
        }
        
        # Create yt-dlp object with the options
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Download the video and get info
            info = ydl.extract_info(url, download=True)
            video_title = info['title']
            video_ext = info['ext']
            
            # Construct the full path of downloaded file
            video_path = os.path.join(output_path, f"{video_title}.{video_ext}") if output_path else f"{video_title}.{video_ext}"
            
            return video_path
            
    except Exception as e:
        raise Exception(f"Failed to download video: {str(e)}")