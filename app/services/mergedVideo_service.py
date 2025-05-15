from moviepy import VideoFileClip, CompositeVideoClip, concatenate_videoclips
import numpy as np


def preview_intro_clip(video_path: str, summary_map_to_transcript: any):
    """
    Loads a video, extracts a subclip, and previews it.
    """
    video = VideoFileClip(video_path)
    # clip1 = video.subclipped(0, 5)
    # clip2 = video.subclipped(9, 14)
    # clip3 = video.subclipped(330, 350)
    # clip4 = video.subclipped(80, 90)

    # quick_compo = concatenate_videoclips([clip2, clip3])

    # quick_compo.write_videofile("merged.mp4")

    # quick_compo.ipython_display(width=480)

    # print("summary_map_to_transcript", summary_map_to_transcript)

    for key, value in summary_map_to_transcript.items():
        if value:  # Make sure the list is not empty

            print(f"start: {value[0]['start']}")

    # Extract the start and end times from the summary map


# Example usage:
# preview_intro_clip("./home/shakti/Downloads/AI Agents, Clearly Explained_1080p.mp4")
