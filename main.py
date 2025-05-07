from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from youtube_transcript_api import YouTubeTranscriptApi
from typing import List, Dict


app = FastAPI()

@app.get("/transcript/{video_id}")
def get_transcript(video_id: str) -> Dict:
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        
        # Format the transcript data
        formatted_transcript = {
            "status": "success",
            "video_id": video_id,
            "transcript": transcript
        }
        
        return JSONResponse(
            content=formatted_transcript,
            status_code=200
        )
    except Exception as e:
        return JSONResponse(
            content={
                "status": "error",
                "message": str(e)
            },
            status_code=500
        )