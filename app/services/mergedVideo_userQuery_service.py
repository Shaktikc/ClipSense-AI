import os
import subprocess
from typing import List, Dict
import yt_dlp
import tempfile
import uuid
import sys
import re


def deduplicate_segments(segments: List[dict]) -> List[dict]:
    """Remove duplicate and overlapping segments"""
    if not segments:
        return []
    
    # Sort segments by video_id and start time
    sorted_segments = sorted(segments, key=lambda x: (x['video_id'], x['start']))
    deduplicated = []
    
    for segment in sorted_segments:
        # Skip if this segment overlaps with the previous one
        if deduplicated and segment['video_id'] == deduplicated[-1]['video_id']:
            prev_end = deduplicated[-1]['start'] + deduplicated[-1]['duration']
            curr_start = segment['start']
            
            # If there's overlap, skip this segment
            if curr_start < prev_end:
                continue
        
        deduplicated.append(segment)
    
    return deduplicated


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

    # Collect all segments first and deduplicate them
    all_segments = []
    for match_obj in user_query_match:
        transcript_segments = match_obj.get("transcript", [])
        all_segments.extend(transcript_segments)
    
    # Deduplicate segments before processing
    deduplicated_segments = deduplicate_segments(all_segments)
    print(f"Found {len(all_segments)} segments, reduced to {len(deduplicated_segments)} after deduplication")

    for segment in deduplicated_segments:
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

        # FFmpeg command with improved segment handling
        cmd = [
            ffmpeg_path, "-y",
            "-ss", str(start),
            "-t", str(duration),
            "-i", matching_video,            "-vf", f"drawtext=fontfile='{escaped_font}':text='{channel_text}':fontsize=24:fontcolor=white:x=w-tw-10:y=h-th-10",
            # CPU encoding settings
            "-c:v", "libx264",     # CPU encoder
            "-preset", "medium",    # Balanced preset for CPU
            "-crf", "23",          # Quality level
            "-b:v", "5M",          # Maximum bitrate
            "-force_key_frames", f"expr:gte(t,n_forced*{duration})", # Force keyframe at start
            "-g", "30",             # Keyframe interval
            "-keyint_min", "30",    # Minimum keyframe interval
            "-strict", "experimental",
            "-c:a", "aac",
            "-ar", "44100",
            "-ac", "2",
            "-b:a", "192k",         # Increased audio bitrate
            "-pix_fmt", "yuv420p",
            "-r", "30",
            "-vsync", "1",          # Ensure frame timing consistency
            "-async", "1",          # Audio sync
            output_path
        ]

        try:
            subprocess.run(cmd, check=True)
            clips_paths.append(output_path)
        except subprocess.CalledProcessError as e:
            print(f"Error processing clip from {matching_video}: {e}")
            print("Command used:", " ".join(cmd))

    if clips_paths:
        # Create a temporary filter file for complex concatenation
        filter_file = os.path.join(temp_dir, "filter.txt")
        with open(filter_file, "w") as f:
            for i, clip_path in enumerate(clips_paths):
                f.write(f"[{i}:v]setpts=PTS-STARTPTS[v{i}];\n")
                f.write(f"[{i}:a]asetpts=PTS-STARTPTS[a{i}];\n")
            
            # Write the concat line
            v_inputs = "".join(f"[v{i}]" for i in range(len(clips_paths)))
            a_inputs = "".join(f"[a{i}]" for i in range(len(clips_paths)))
            f.write(f"{v_inputs}concat=n={len(clips_paths)}:v=1:a=0[vout];\n")
            f.write(f"{a_inputs}concat=n={len(clips_paths)}:v=0:a=1[aout]")

        # Build input arguments for each clip
        input_args = []
        for clip_path in clips_paths:
            input_args.extend(["-i", clip_path])

        output_final = "merged.mp4"
        # Final concatenation with complex filter
        concat_cmd = [
            ffmpeg_path, "-y",
            *input_args,
            "-filter_complex_script", filter_file,
            "-map", "[vout]",
            "-map", "[aout]",
            # Use CPU encoding for final output for better stability
            "-c:v", "libx264",     # CPU encoder
            "-preset", "medium",    # Balanced preset
            "-crf", "23",          # Quality level
            "-g", "30",            # Keyframe interval
            "-keyint_min", "30",   # Minimum keyframe interval
            "-bf", "2",            # Maximum 2 B-frames
            "-c:a", "aac",
            "-ar", "44100",
            "-ac", "2",
            "-b:a", "192k",        # Consistent audio bitrate
            "-movflags", "+faststart",  # Enable fast start for web playback
            "-vsync", "1",         # Ensure frame timing consistency
            "-async", "1",         # Audio sync
            output_final
        ]
        try:
            subprocess.run(concat_cmd, check=True)
            print("✅ Successfully created merged.mp4")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error concatenating clips: {e}")
            print("Command used:", " ".join(concat_cmd))
