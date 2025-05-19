from fastapi import APIRouter, HTTPException, APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from app.models.schemas import (
    VideoRequest,
    TranscriptResponse,
    TranscriptResult,
    ErrorResult,
)
from app.services.transcript_service import TranscriptService
from app.services.mergedVideo_service import preview_intro_clip
import json
import demjson3
import re
from typing import List
import tempfile
import shutil
import os

router = APIRouter()
transcript_service = TranscriptService()


@router.post("/transcripts/", response_model=TranscriptResponse)
def get_multiple_transcripts(
    video_ids: List[str] = Form(...),
    video_files: List[UploadFile] = File(...),  # Changed to List[UploadFile]
    start: int = Form(1),
    end: int = Form(11),
    fps: int = Form(20),
):
    results = []
    errors = []
    all_transcripts = []

    # Collect all transcripts
    for video_id in video_ids:
        transcript, error = transcript_service.get_transcript(video_id)
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
    # if all_transcripts:
    #     combined_text = " ".join(all_transcripts)
    #     combined_summary = transcript_service.generate_summary(combined_text)
    if all_transcripts:
        transript_data = transcript_service.transcript_mock_data()
        saved_video_paths = []

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
        preview_intro_clip(
            saved_video_paths,  # Now passing list of paths
            transript_data["combined_summary"]["mapping"],
            video_ids,
        )

    return JSONResponse(
        content=TranscriptResponse(
            results=results,
            errors=errors,
            combined_summary=transript_data,
        ).model_dump(),
        status_code=200 if results else 500,
    )
