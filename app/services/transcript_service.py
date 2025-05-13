from youtube_transcript_api import YouTubeTranscriptApi
from typing import List, Tuple, Dict
import os
from openai import OpenAI
from app.config.settings import API_KEY


class TranscriptService:
    def __init__(self):
        self.client = OpenAI(api_key=API_KEY)

    def get_transcript(self, video_id: str) -> Tuple[List[Dict], str]:
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            return transcript, None
        except Exception as e:
            return None, str(e)

    def generate_summary(self, transcript_string: str) -> str:
        prompt = f"""
                  Summarize the following YouTube transcript as if you are a person directly sharing 
                  the knowledge. Do not say that you watched the video. Present the information as 
                  your own, clearly and confidently. Use a natural, human-like tone that’s conversational
                  yet informative. Focus on the core ideas, key points, and main takeaways. Avoid 
                  robotic language, repetition, or filler words from the transcript.

                  Here is the transcript to analyze:
                  {transcript_string}
                """

        try:
            response = self.client.chat.completions.create(
                model="gpt-4.1-mini",  # or "gpt-4", "gpt-3.5-turbo", etc.
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating summary: {str(e)}"
