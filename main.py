from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from youtube_transcript_api import YouTubeTranscriptApi
from typing import List, Dict
import os
from mistralai import Mistral
from dotenv import load_dotenv
from pydantic import BaseModel

# Create a Pydantic model for request validation
class VideoRequest(BaseModel):
    video_ids: List[str]

# Load environment variables from .env file
load_dotenv()

api_key = os.environ["API_KEY"]
model = "mistral-large-latest"

app = FastAPI()

def generate_summary(transcript_text: str, client: Mistral) -> str:
    prompt = f"""Summarize the following combined video transcripts concisely:
    {transcript_text}
    
    Provide a clear and concise summary of the main points from all videos combined."""

    chat_response = client.chat.complete(
        model="mistral-large-latest",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ]
    )
    return chat_response.choices[0].message.content

@app.post("/transcripts/")
def get_multiple_transcripts(request: VideoRequest) -> Dict:
    results = []
    errors = []
    all_transcripts = []
    
    # Initialize Mistral client
    client = Mistral(api_key=api_key)
    
    # First, collect all transcripts
    for video_id in request.video_ids:
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            transcript_text = " ".join([entry["text"] for entry in transcript])
            all_transcripts.append(transcript_text)
      
            results.append({
                "video_id": video_id,
                "transcript": transcript,
                "status": "success"
            })
        except Exception as e:
            errors.append({
                "video_id": video_id,
                "error": str(e),
                "status": "error"
            })
    
     
    # Generate combined summary if we have any successful transcripts
    combined_summary = None
    print(all_transcripts)
    if all_transcripts:
        combined_text = " ".join(all_transcripts)
        combined_summary = generate_summary(combined_text, client)
    
    return JSONResponse(
        content={
            "results": results,
            "errors": errors,
            "combined_summary": combined_summary
        },
        status_code=200 if results else 500
    )