from fastapi import APIRouter, HTTPException, APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from app.models.schemas import (
    VideoRequest,
    VideoSummaryResponse,
    TranscriptResult,
    ErrorResult,
)
from app.services.video_summerizer_service import VideoSummerizerService
from app.services.mergedVideo_service import preview_intro_clip
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
    # video_files: List[UploadFile] = File(...),  # Changed to List[UploadFile]
):
    results = []
    errors = []
    all_transcripts = []

    # Collect all transcripts
    for video_id in video_ids:
        transcript, error = video_summary_service.get_transcript(video_id)
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
            errors.append(ErrorResult(video_id=video_id, error=error, status="error"))

    # print(all_transcripts)

    # Generate combined summary if we have any successful transcripts
    combined_summary = None
    combined_summary_obj = None
    transript_data = None
    # print("niceee", video_ids)
    if all_transcripts:
        user_query_match_transcript = video_summary_service.transcript_related_to_user_query("why i shouldnt buy iPhone 16?",all_transcripts)
        # summary_to_transcript_map = video_summary_service.summary_to_transcript_mapping(
        #     all_transcripts, combined_summary
        # )
        cleaned_transcript = re.sub(
            r"[`\u2018\u2019\u201c\u201d]", "", user_query_match_transcript
        )
        user_query_match_transcript_obj = demjson3.decode(cleaned_transcript)
        print("combined_summary_obj", user_query_match_transcript_obj)
        saved_video_paths = []
    # if all_transcripts:
    #     transript_data = transcript_service.transcript_mock_data()
    #     saved_video_paths = []

        # # Process each uploaded video file
        # for video_file in video_files:
        #     original_filename = video_file.filename
        #     temp_dir = os.path.join(os.getcwd(), "temp")
        #     os.makedirs(temp_dir, exist_ok=True)
        #     tmp_path = os.path.join(temp_dir, original_filename)

        #     with open(tmp_path, "wb") as tmp:
        #         shutil.copyfileobj(video_file.file, tmp)
        #     saved_video_paths.append(tmp_path)

        # # Pass all video paths at once
        # preview_intro_clip(
        #     saved_video_paths,  # Now passing list of paths
        #     combined_summary_obj["mapping"],
        #     video_ids,
        # )

    return JSONResponse(
        content=VideoSummaryResponse(
            results=results,
            errors=errors,
            combined_summary=user_query_match_transcript_obj,
        ).model_dump(),
        status_code=200 if results else 500,
    )
