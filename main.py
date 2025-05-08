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

# client = Mistral(api_key=api_key)

# chat_response = client.chat.complete(
#     model= model,
#     messages = [
#         {
#             "role": "user",
#             "content": "What is the best French cheese?",
#         },
#     ]
# )
# print(chat_response.choices[0].message.content)


app = FastAPI()

# @app.get("/transcript/{video_id}")
# def get_transcript(video_id: str) -> Dict:
#     try:
#         transcript = YouTubeTranscriptApi.get_transcript(video_id)
        
#         # Format the transcript data
#         formatted_transcript = {
#             "status": "success",
#             "video_id": video_id,
#             "transcript": transcript
#         }
        
#         return JSONResponse(
#             content=formatted_transcript,
#             status_code=200
#         )
#     except Exception as e:
#         return JSONResponse(
#             content={
#                 "status": "error",
#                 "message": str(e)
#             },
#             status_code=500
#         )

@app.post("/transcripts/")
def get_multiple_transcripts(request: VideoRequest) -> Dict:
    results = []
    errors = []
    
    for video_id in request.video_ids:
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
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
    
    return JSONResponse(
        content={
            "results": results,
            "errors": errors
        },
        status_code=200 if results else 500
    )