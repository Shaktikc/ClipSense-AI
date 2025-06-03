import os
import subprocess
from typing import List, Dict
import yt_dlp
import tempfile
import uuid
import sys
import re


def get_ffmpeg_path():
    """Get the FFmpeg executable path"""
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, 'ffmpeg.exe')
    else:
        possible_paths = [
            "ffmpeg",
            r"C:\Program Files\ffmpeg\bin\ffmpeg.exe",
            r"C:\ffmpeg\bin\ffmpeg.exe",
            os.path.join(os.path.dirname(__file__), "..", "assets", "ffmpeg", "ffmpeg.exe")
        ]
        for path in possible_paths:
            if path == "ffmpeg":
                try:
                    subprocess.run([path, "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    return path
                except FileNotFoundError:
                    continue
            elif os.path.isfile(path):
                return path
        raise FileNotFoundError(
            "FFmpeg not found. Please install FFmpeg from https://ffmpeg.org/download.html "
            "and add it to your system PATH, or place ffmpeg.exe in one of the expected locations."
        )


def escape_ffmpeg_text(text: str) -> str:
    """Escape special characters for ffmpeg drawtext filter"""
    text = text.replace('\\', '\\\\')  # Escape backslashes
    text = text.replace(':', '\\:')    # Escape colons
    text = text.replace("'", "\\'")    # Escape single quotes
    return text


def mergedVideo_userQuery_service(
    saved_video_paths: List[str], user_query_match: list, video_ids: List[str]
):
    try:
        ffmpeg_path = get_ffmpeg_path()
    except FileNotFoundError as e:
        print(str(e))
        return

    temp_dir = tempfile.mkdtemp()
    clips_paths = []
    channel_names = {}
    arial_font = r"C:\Windows\Fonts\arial.ttf"

    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'force_generic_extractor': True,
        'no_warnings': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for video_id in video_ids:
            try:
                info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
                channel_names[video_id] = info.get('uploader', 'Unknown Source')
            except Exception as e:
                print(f"Error fetching channel for {video_id}: {e}")
                channel_names[video_id] = "Unknown Source"

    print("Channel names extracted:", channel_names)

    for match_obj in user_query_match:
        transcript_segments = match_obj.get("transcript", [])
        for segment in transcript_segments:
            video_id = segment["video_id"]
            start = segment["start"]
            duration = segment["duration"]

            matching_video = next((path for path in saved_video_paths if video_id in path), None)
            if not matching_video:
                continue

            output_path = os.path.join(temp_dir, f"{uuid.uuid4()}.mp4")
            raw_channel = channel_names.get(video_id, "Unknown Source")
            channel_text = escape_ffmpeg_text(f"Source: {raw_channel}")
            escaped_font = arial_font.replace("\\", "/")
            # Escape drive letter for FFmpeg (C:/... -> C\:/...)
            if len(escaped_font) > 1 and escaped_font[1] == ':':
                escaped_font = escaped_font[0] + '\\:' + escaped_font[2:]

            # FFmpeg command with NVIDIA GPU acceleration
            cmd = [
                ffmpeg_path, "-y",
                "-ss", str(start),
                "-t", str(duration),
                "-i", matching_video,
                "-vf", f"drawtext=fontfile='{escaped_font}':text='{channel_text}':fontsize=12:fontcolor=white:x=w-tw-10:y=h-th-10",
                # GPU encoding (NVIDIA)
                "-c:v", "h264_nvenc",  # Use NVIDIA encoder
                "-preset", "p1",        # Fast preset for NVENC
                "-rc:v", "vbr",        # Variable bitrate
                "-cq:v", "23",         # Quality level (similar to CRF)
                "-b:v", "5M",          # Maximum bitrate
                # CPU encoding (commented out)
                # "-c:v", "libx264",     # CPU encoder
                # "-preset", "ultrafast", # CPU preset
                # "-crf", "23",          # CPU quality level
                "-c:a", "aac",
                "-ar", "44100",
                "-ac", "2",
                "-b:a", "128k",
                "-pix_fmt", "yuv420p",
                "-r", "30",
                output_path
            ]

            try:
                subprocess.run(cmd, check=True)
                clips_paths.append(output_path)
            except subprocess.CalledProcessError as e:
                print(f"Error processing clip from {matching_video}: {e}")
                print("Command used:", " ".join(cmd))

    if clips_paths:
        concat_list = os.path.join(temp_dir, "inputs.txt")
        with open(concat_list, "w") as f:
            for clip_path in clips_paths:
                f.write(f"file '{clip_path}'\n")

        output_final = "merged.mp4"
        # Final concatenation with GPU acceleration
        concat_cmd = [
            ffmpeg_path, "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", concat_list,
            # GPU encoding (NVIDIA)
            "-c:v", "h264_nvenc",    # Use NVIDIA encoder
            "-preset", "p3",         # Higher quality preset for final output
            "-rc:v", "vbr",
            "-cq:v", "23",
            "-b:v", "8M",           # Higher bitrate for final output
            # CPU encoding (commented out)
            # "-c:v", "libx264",     # CPU encoder
            # "-preset", "medium",    # CPU preset
            # "-crf", "23",          # CPU quality level
            "-c:a", "aac",
            "-ar", "44100",
            "-ac", "2",
            "-b:a", "128k",
            output_final
        ]
        try:
            subprocess.run(concat_cmd, check=True)
            print("✅ Successfully created merged.mp4")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error concatenating clips: {e}")
            print("Command used:", " ".join(concat_cmd))
