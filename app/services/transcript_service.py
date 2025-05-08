from youtube_transcript_api import YouTubeTranscriptApi
from mistralai import Mistral
from typing import List, Tuple, Dict
from app.config.settings import API_KEY, MODEL_NAME

class TranscriptService:
    def __init__(self):
        self.client = Mistral(api_key=API_KEY)

    def get_transcript(self, video_id: str) -> Tuple[List[Dict], str]:
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            return transcript, None
        except Exception as e:
            return None, str(e)

    def generate_summary(self, transcript_text: str) -> str:
        prompt = f"""Summarize the following combined video transcripts concisely:
        {transcript_text}
        
        Provide a clear and concise summary of the main points from all videos combined."""

        chat_response = self.client.chat.complete(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ]
        )
        return chat_response.choices[0].message.content