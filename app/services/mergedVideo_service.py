from moviepy import VideoFileClip
import numpy as np


def preview_intro_clip(video_path: str, start: int = 1, end: int = 11, fps: int = 20):
    """
    Loads a video, extracts a subclip, and previews it.
    """
    video = VideoFileClip(video_path)
    intro_clip = video.subclipped(start, end)
    intro_clip.preview(fps=fps)


# Example usage:
# preview_intro_clip("./home/shakti/Downloads/AI Agents, Clearly Explained_1080p.mp4")
