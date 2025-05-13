from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.models.schemas import (
    VideoRequest,
    TranscriptResponse,
    TranscriptResult,
    ErrorResult,
)
from app.services.transcript_service import TranscriptService
import json
import demjson3
import re

router = APIRouter()
transcript_service = TranscriptService()


@router.post("/transcripts/", response_model=TranscriptResponse)
def get_multiple_transcripts(request: VideoRequest):
    results = []
    errors = []
    all_transcripts = []

    # Collect all transcripts
    for video_id in request.video_ids:
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
    print("niceee", all_transcripts)
    # if all_transcripts:
    #     combined_text = " ".join(all_transcripts)
    #     combined_summary = transcript_service.generate_summary(combined_text)
    if all_transcripts:
        combined_summary = transcript_service.generate_summary(all_transcripts)
        # cleaned_transcript = re.sub(
        #     r"[`\u2018\u2019\u201c\u201d]", "", combined_summary
        # )
        # combined_summary_obj = demjson3.decode(cleaned_transcript)

    return JSONResponse(
        content=TranscriptResponse(
            results=results,
            errors=errors,
            combined_summary=combined_summary,
        ).model_dump(),
        status_code=200 if results else 500,
    )
