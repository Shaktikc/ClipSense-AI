import os
from moviepy import VideoFileClip, CompositeVideoClip, concatenate_videoclips
import numpy as np
from typing import List, Dict


def preview_intro_clip(
    saved_video_paths: List[str], summary_map_to_transcript: any, video_ids: List[str]
):
    """
    Loads videos, extracts subclips, and previews them.
    """
    videos: Dict[str, VideoFileClip] = {}  # Store videos with their IDs as keys
    clips: List[VideoFileClip] = []  # Store subclips to be merged

    for video_path in saved_video_paths:
        video_name = os.path.splitext(os.path.basename(video_path))[0]
        try:
            video = VideoFileClip(video_path)
            videos[video_name] = video
            print(f"Loaded video: {video_name}")
        except Exception as e:
            print(f"Error loading video {video_name}: {str(e)}")

    try:
        # Process only matching video IDs from summary map
        for key, value in summary_map_to_transcript.items():
            if value:
                video_id = value[0]["video_id"]
                # Only process if video ID exists in loaded videos
                if video_id in videos:
                    start = value[0]["start"]
                    end = value[0]["start"] + value[0]["duration"]
                    video_duration = videos[video_id].duration
                    # Clamp end time to video duration
                    if end > video_duration:
                        end = video_duration
                    print(
                        f"Processing clip for {video_id} - Start: {start}, End: {end}"
                    )
                    clip = videos[video_id].subclipped(start, end)
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
