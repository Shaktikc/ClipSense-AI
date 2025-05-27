import os
from moviepy import VideoFileClip, CompositeVideoClip, concatenate_videoclips, TextClip
import numpy as np
from typing import List, Dict
from pytube import YouTube

# Font path for TextClip
FONT_PATH = os.path.join(os.path.dirname(__file__), "..", "assets", "fonts", "OpenSans-Regular.ttf")

def mergedVideo_userQuery_service(
    saved_video_paths: List[str], user_query_match: list, video_ids: List[str]
):
    """
    Loads videos, extracts subclips based on transcript matches, and merges them.
    Now supports a list of transcript match objects (one per video).
    """
    videos: Dict[str, VideoFileClip] = {}  # Store videos with their IDs as keys
    clips: List[VideoFileClip] = []  # Store subclips to be merged
    channel_names = {}
    
    # Extract channel names for each video_id
    for video_id in video_ids:
        try:
            yt = YouTube(f"https://www.youtube.com/watch?v={video_id}")
            channel_names[video_id] = yt.author
        except Exception as e:
            channel_names[video_id] = "Unknown Source"

    # Load all videos first
    for video_path in saved_video_paths:
        video_name = os.path.splitext(os.path.basename(video_path))[0]
        try:
            video = VideoFileClip(video_path)
            videos[video_name] = video
            print(f"Loaded video: {video_name}")
        except Exception as e:
            print(f"Error loading video {video_name}: {str(e)}")

    try:
        # Iterate through each transcript match object (one per video)
        for match_obj in user_query_match:
            transcript_segments = match_obj.get("transcript", [])
            for segment in transcript_segments:
                video_id = segment["video_id"]
                # Only process if video ID exists in loaded videos
                if video_id in videos:
                    start = segment["start"]
                    duration = segment["duration"]
                    end = start + duration
                    video_duration = videos[video_id].duration

                    # Clamp end time to video duration
                    if end > video_duration:
                        end = video_duration

                    if start < end:  # Only process valid time ranges
                        print(
                            f"Processing clip for {video_id} - Start: {start}, End: {end}"
                        )
                        clip = videos[video_id].subclipped(start, end)  # Changed from subclipped to subclip
                        # Overlay channel name as text at the top left
                        channel_text = channel_names.get(video_id, "Unknown Source")
                        txt_clip = TextClip(
                            text=f"Source: {channel_text}",
                            font="C:/Windows/Fonts/arial.ttf",
                            font_size=30,
                            color="white",
                            bg_color="black",
                            method="caption",
                            size=(clip.w, None)  # Match video width, auto-height
                        ).with_position((10, 10)).with_duration(clip.duration)
                        
                        composite = CompositeVideoClip([clip, txt_clip])
                        clips.append(composite)

        # Merge clips if any were created
        if clips:
            final_video = concatenate_videoclips(clips)
            final_video.write_videofile("merged.mp4", fps=24)  # Added fps parameter
            print("Successfully created merged.mp4")

    finally:
        # Clean up
        for video in videos.values():
            video.close()
