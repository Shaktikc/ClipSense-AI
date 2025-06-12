from fastapi import APIRouter, HTTPException, APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from app.models.schemas import (
    VideoRequest,
    VideoSummaryResponse,
    TranscriptResult,
    ErrorResult,
)
from app.services.video_summerizer_service import VideoSummerizerService
from app.services.mergedVideo_userQuery_service import mergedVideo_userQuery_service
import json
import demjson3
import re
from typing import List
import tempfile
import shutil
import os

router = APIRouter()
video_summary_service = VideoSummerizerService()


@router.post("/summaries/youtube/", response_model=VideoSummaryResponse)
def get_youtube_videos_summary(
    video_ids: List[str] = Form(...),
    video_files: List[UploadFile] = File(...),  # Changed to List[UploadFile]
):
    results = []
    errors = []
    all_transcripts = []
    print("video_ids", video_ids)

    # Collect all transcripts
    for video_id in video_ids:
        result = video_summary_service.get_transcript(video_id)
        print("result", result)
        if result is None:  # Handle case when get_transcript returns None
            raise HTTPException(
                status_code=400,
                detail=f"Failed to get transcript for video ID: {video_id}"
            )
            
        transcript = result
        if transcript:
            transcript_string = json.dumps(
                {"video_id": video_id, "transcript": transcript}
            )
            all_transcripts.append(transcript_string)
            results.append(
                TranscriptResult(
                    video_id=video_id, transcript=transcript, status="success"
                )
            )
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Error getting transcript for video ID {video_id}: {result.error}"
            )

    # print(all_transcripts)

    # For each video_id, run transcript_related_to_user_query separately
    user_query_match_transcript_objs = []
    for video_id in video_ids:
        # Find the transcript for this video_id
        transcript_json = next(
            (json.loads(t) for t in all_transcripts if json.loads(t)["video_id"] == video_id),
            None,
        )
        if transcript_json:
            user_query_match_transcript = video_summary_service.transcript_related_to_user_query(
                "Should I  buy samsung S25 Edge?", [json.dumps(transcript_json)]
            )
            cleaned_transcript = re.sub(
                r"[`\u2018\u2019\u201c\u201d]", "", user_query_match_transcript
            )
            user_query_match_transcript_obj = demjson3.decode(cleaned_transcript)
            user_query_match_transcript_objs.append(user_query_match_transcript_obj)
        else:
            user_query_match_transcript_objs.append({"video_id": video_id, "error": "Transcript not found"})
    print("user_query_match_transcript_objs", user_query_match_transcript_objs)
    saved_video_paths = []

    if all_transcripts:
        # Process each uploaded video file
        for video_file in video_files:
            original_filename = video_file.filename
            temp_dir = os.path.join(os.getcwd(), "temp")
            os.makedirs(temp_dir, exist_ok=True)
            tmp_path = os.path.join(temp_dir, original_filename)

            with open(tmp_path, "wb") as tmp:
                shutil.copyfileobj(video_file.file, tmp)
            saved_video_paths.append(tmp_path)

        # Pass all video paths at once
        mergedVideo_userQuery_service(
            saved_video_paths,  # Now passing list of paths
            user_query_match_transcript_objs,
            video_ids,
        )

    return JSONResponse(
        content=VideoSummaryResponse(
            results=results,
            errors=errors,
            transcript_related_to_user_query=user_query_match_transcript_objs,
        ).model_dump(),
        status_code=200 if results else 500,
    )
