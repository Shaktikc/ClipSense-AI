from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from youtube_transcript_api import YouTubeTranscriptApi
from typing import List, Dict
import os
from mistralai import Mistral
from dotenv import load_dotenv



# Load environment variables from .env file
load_dotenv()

api_key = os.environ["API_KEY"]
model = "mistral-large-latest"

client = Mistral(api_key=api_key)

chat_response = client.chat.complete(
    model= model,
    messages = [
        {
            "role": "user",
            "content": "What is the best French cheese?",
        },
    ]
)
print(chat_response.choices[0].message.content)


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