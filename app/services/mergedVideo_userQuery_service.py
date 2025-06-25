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
        transcript_segments = match_obj.get("transcript", [])[:3]  # Will take up to 3 segments
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

            # Get video resolution using ffprobe
            probe_cmd = [
                ffmpeg_path.replace('ffmpeg', 'ffprobe'),
                '-v', 'error',
                '-select_streams', 'v:0',
                '-show_entries', 'stream=height',
                '-of', 'default=noprint_wrappers=1:nokey=1',
                matching_video
            ]
            try:
                result = subprocess.run(probe_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
                video_height = int(result.stdout.strip())
            except Exception as e:
                print(f"Could not determine video resolution, defaulting to no scaling: {e}")
                video_height = None

            drawtext_filter = f"drawtext=fontfile='{escaped_font}':text='{channel_text}':fontsize=34:fontcolor=white:x=w-tw-10:y=h-th-10"
            if video_height == 720:
                scale_filter = "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2"
                vf_filter = f"{drawtext_filter},{scale_filter}"
            elif video_height == 1080:
                vf_filter = drawtext_filter  # No scaling for 1080p
            else:
                vf_filter = drawtext_filter  # No scaling for other resolutions

            cmd = [
                ffmpeg_path, "-y",
                "-ss", str(start),
                "-t", str(duration),
                "-i", matching_video,
                "-vf", vf_filter,
                "-c:v", "libx264",     # CPU encoder
                "-preset", "medium",    # Higher quality preset
                "-crf", "23",        # Lower CRF for higher quality (range 0-51, lower is better)
                "-c:a", "aac",
                "-ar", "44100",      # Higher audio sample rate
                "-ac", "2",
                "-b:a", "128k",      # Higher audio bitrate
                "-pix_fmt", "yuv420p",
                "-r", "30",
                "-profile:v", "high",  # High profile for better quality
                "-level", "4.2",      # Compatibility level
                "-movflags", "+faststart",  # Web playback optimization
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
            "-c:v", "libx264",     # CPU encoder
            "-preset", "medium",    # Higher quality preset
            "-crf", "18",        # Lower CRF for higher quality
            "-c:a", "aac",
            "-ar", "44100",      # Higher audio sample rate
            "-ac", "2",
            "-b:a", "128k",      # Higher audio bitrate
            "-profile:v", "high", # High profile for better quality
            "-level", "4.2",     # Compatibility level
            "-movflags", "+faststart",  # Web playback optimization
            output_final
        ]
        try:
            subprocess.run(concat_cmd, check=True)
            print("✅ Successfully created merged.mp4")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error concatenating clips: {e}")
            print("Command used:", " ".join(concat_cmd))