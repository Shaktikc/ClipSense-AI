from typing import List, Dict, Optional
from pydantic import BaseModel

class VideoRequest(BaseModel):
    video_ids: List[str]

class TranscriptResult(BaseModel):
    video_id: str
    transcript: List[Dict]
    status: str

class ErrorResult(BaseModel):
    video_id: str
    error: str
    status: str

class TranscriptResponse(BaseModel):
    results: List[TranscriptResult]
    errors: List[ErrorResult]
    combined_summary: Optional[str]