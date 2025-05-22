import os
from moviepy import VideoFileClip, CompositeVideoClip, concatenate_videoclips
import numpy as np
from typing import List, Dict


def mergedVideo_for_user_query(
    saved_video_paths: List[str], user_query_match: dict, video_ids: List[str]
):
    """
    Loads videos, extracts subclips based on transcript matches, and merges them.
    """
    videos: Dict[str, VideoFileClip] = {}  # Store videos with their IDs as keys
    clips: List[VideoFileClip] = []  # Store subclips to be merged

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
        # Process each transcript segment
        for segment in user_query_match.get("transcript", []):
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
                    clip = videos[video_id].subclip(start, end)
                    clips.append(clip)

        # Merge clips if any were created
        if clips:
            final_video = concatenate_videoclips(clips)
            final_video.write_videofile("merged.mp4")
            print("Successfully created merged.mp4")

    finally:
        # Clean up
        for video in videos.values():
            video.close()
