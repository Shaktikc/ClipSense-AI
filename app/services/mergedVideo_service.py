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
    # video = VideoFileClip(saved_video_paths)
    # clip1 = video.subclipped(0, 5)
    # clip2 = video.subclipped(9, 14)
    # clip3 = video.subclipped(330, 350)
    # clip4 = video.subclipped(80, 90)

    # quick_compo = concatenate_videoclips([clip2, clip3])

    # quick_compo.write_videofile("merged.mp4")

    # quick_compo.ipython_display(width=480)

    # print("summary_map_to_transcript", summary_map_to_transcript)

    for video_path in saved_video_paths:
        # Extract video name from path without extension
        video_name = os.path.splitext(os.path.basename(video_path))[0]
        try:
            video = VideoFileClip(video_path)
            videos[video_name] = video
            # print(f"Loaded video: {video_name}")
        except Exception as e:
            print(f"Error loading video {video_name}: {str(e)}")

    # Now you can access videos by their ID
    # Example: videos["FwOTs4UxQS4"] will give you that specific video's VideoFileClip
    print("Loaded videos:", videos)

    for key, value in summary_map_to_transcript.items():
        if value:  # Make sure the list is not empty
            start = value[0]["start"]
            end = value[0]["start"] + value[0]["duration"]
            video_id = value[0]["video_id"]
            print(
                f"start: {value[0]['start']}, end: {value[0]['start'] + value[0]['duration']}, video_id: {value[0]['video_id']}"
            )
    # try:
    #     # Process videos and create clips
    #     clips = []
    #     for video_name, video in videos.items():
    #         clip = video.subclip(0, 5)  # Example: first 5 seconds
    #         clips.append(clip)

    #     if clips:
    #         final_video = concatenate_videoclips(clips)
    #         final_video.write_videofile("merged.mp4")
    # finally:
    #     # Clean up - close all video files
    #     for video in videos.values():
    #         video.close()
