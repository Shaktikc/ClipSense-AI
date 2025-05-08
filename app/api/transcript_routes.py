from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.models.schemas import VideoRequest, TranscriptResponse, TranscriptResult, ErrorResult
from app.services.transcript_service import TranscriptService

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
            transcript_text = " ".join([entry["text"] for entry in transcript])
            all_transcripts.append(transcript_text)
            results.append(TranscriptResult(
                video_id=video_id,
                transcript=transcript,
                status="success"
            ))
        else:
            errors.append(ErrorResult(
                video_id=video_id,
                error=error,
                status="error"
            ))
    
    # Generate combined summary if we have any successful transcripts
    combined_summary = None
    if all_transcripts:
        combined_text = " ".join(all_transcripts)
        combined_summary = transcript_service.generate_summary(combined_text)
    
    return JSONResponse(
        content=TranscriptResponse(
            results=results,
            errors=errors,
            combined_summary=combined_summary
        ).dict(),
        status_code=200 if results else 500
    )