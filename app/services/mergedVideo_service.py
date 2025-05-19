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
    # video = VideoFileClip(saved_video_paths)
    # clip1 = video.subclipped(0, 5)
    # clip2 = video.subclipped(9, 14)
    # clip3 = video.subclipped(330, 350)
    # clip4 = video.subclipped(80, 90)

    # quick_compo = concatenate_videoclips([clip2, clip3])

    # quick_compo.write_videofile("merged.mp4")

    # print("summary_map_to_transcript", summary_map_to_transcript)

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
