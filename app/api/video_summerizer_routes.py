from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import json
import demjson3
import re
import os
import asyncio

from app.models.schemas import VideoSummaryResponse, TranscriptResult
from app.services.video_summerizer_service import VideoSummerizerService
from app.services.mergedVideo_userQuery_service import mergedVideo_userQuery_service
from app.services.downloadVideo_service import download_youtube_video, extract_video_id

router = APIRouter()
video_summary_service = VideoSummerizerService()


class YouTubeVideoRequest(BaseModel):
    urls: List[str]
    user_query: str


async def process_video(url: str, output_path: str):
    """
    Process a single video: download and get video ID
    """
    try:
        video_id = extract_video_id(url)
        video_path = download_youtube_video(url=url, output_path=output_path)
        return {
            "url": url,
            "video_id": video_id,
            "status": "success",
            "video_path": video_path,
        }
    except Exception as e:
        return {
            "url": url,
            "video_id": None,
            "status": "failed",
            "error": str(e),
            "video_path": None,
        }


@router.post("/summaries/youtube/")
async def get_youtube_videos_summary(request: YouTubeVideoRequest):
    """
    Download YouTube videos and generate summaries based on user query
    """
    try:
        # Create temporary directory for downloaded videos
        temp_dir = os.path.join(os.getcwd(), "temp")
        os.makedirs(temp_dir, exist_ok=True)

        # Download all videos concurrently
        download_tasks = [
            process_video(url, temp_dir) for url in request.urls
        ]
        download_results = await asyncio.gather(*download_tasks)

        # Filter successful downloads
        successful_downloads = [
            result for result in download_results 
            if result["status"] == "success"
        ]

        # Collect errors from failed downloads
        errors = [
            {"video_url": result["url"], "error": result["error"]}
            for result in download_results
            if result["status"] == "failed"
        ]

        if not successful_downloads:
            return JSONResponse(
                content=VideoSummaryResponse(
                    results=[],
                    errors=errors,
                    transcript_related_to_user_query=[]
                ).model_dump(),
                status_code=500
            )

        results = []
        all_transcripts = []

        # Process transcripts for successfully downloaded videos
        for download in successful_downloads:
            video_id = download["video_id"]
            transcript = video_summary_service.get_transcript(video_id)

            if transcript:
                transcript_string = json.dumps({
                    "video_id": video_id,
                    "transcript": transcript
                })
                all_transcripts.append(transcript_string)
                results.append(TranscriptResult(
                    video_id=video_id,
                    transcript=transcript,
                    status="success"
                ))
            else:
                errors.append({
                    "video_url": download["url"],
                    "error": f"Failed to get transcript for video ID: {video_id}"
                })

        # Process user query for each video
        user_query_match_transcript_objs = []
        for download in successful_downloads:
            video_id = download["video_id"]
            transcript_json = next(
                (json.loads(t) for t in all_transcripts if json.loads(t)["video_id"] == video_id),
                None
            )
            
            if transcript_json:
                user_query_match_transcript = video_summary_service.transcript_related_to_user_query(
                    request.user_query, [json.dumps(transcript_json)]
                )
                cleaned_transcript = re.sub(
                    r"[`\u2018\u2019\u201c\u201d]", "", user_query_match_transcript
                )
                user_query_match_transcript_obj = demjson3.decode(cleaned_transcript)
                if isinstance(user_query_match_transcript_obj, list):
                    user_query_match_transcript_obj.sort(key=lambda x: x.get('start', 0))
                user_query_match_transcript_objs.append(user_query_match_transcript_obj)

        # Process video merging if needed
        video_paths = [download["video_path"] for download in successful_downloads]
        video_ids = [download["video_id"] for download in successful_downloads]
        if video_paths:
            _ = mergedVideo_userQuery_service(
                video_paths,
                user_query_match_transcript_objs,
                video_ids
            )

        return JSONResponse(
            content=VideoSummaryResponse(
                results=results,
                errors=errors,
                transcript_related_to_user_query=user_query_match_transcript_objs
            ).model_dump(),
            status_code=200 if results else 500
        )

    except Exception as e:
        return JSONResponse(
            content=VideoSummaryResponse(
                results=[],
                errors=[{"error": str(e)}],
                transcript_related_to_user_query=[]
            ).model_dump(),
            status_code=500
        )
    finally:
        # Clean up downloaded videos
        try:
            for download in download_results:
                if download["video_path"] and os.path.exists(download["video_path"]):
                    os.remove(download["video_path"])
            if os.path.exists(temp_dir):
                os.rmdir(temp_dir)
        except Exception as e:
            print(f"Error cleaning up files: {str(e)}")
