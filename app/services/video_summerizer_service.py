from youtube_transcript_api import YouTubeTranscriptApi
from typing import List, Tuple, Dict
import os
from openai import OpenAI
from app.config.settings import API_KEY
import time


class VideoSummerizerService:
    def __init__(self):
        self.client = OpenAI(api_key=API_KEY)

    def get_transcript(self, video_id: str) -> Tuple[List[Dict], str]:
        for attempt in range(10):
            try:
                transcript = YouTubeTranscriptApi.get_transcript(video_id)
                return transcript, None
            except Exception as e:
                if attempt == 3:
                    return None, str(e)
                time.sleep(1)  # Wait a bit before retrying


    def transcript_related_to_user_query(
        self,
        user_query: str,
        transcript_string: list[dict]
    ) -> str:
        # Serialize the transcript array into a compact JSON string
        prompt = f"""
                    You are given:
                    - A `user_query`: "{user_query}". 
                    - A `youtube transcript`:Each transcript contains:
                        • "text": a phrase or sentence from the video,
                        • "start":the timestamp (in seconds) when the speech begins,
                        • "duration": how long the speech lasted.

                    Your task:
                    1. Understand the user's intent from the `user_query`.
                    2. Identify the transcript segments that best answer or relate to the query (semantic relevance, not just keyword match).
                    3. Return **only** the top matching segments.
                    4.Make sure to take from every video transcript,dont repeat the same video transcript.
                    5. Format your response exactly , using this structure:

                    {{
                    "transcript": [
                        {{
                        "matched_text": "<relevant text from transcript>",
                        "start": <start time in seconds>,
                        "duration": <duration in seconds>,
                        "video_id": "<video_id>"
                        }}
                        // ... additional matches if relevant
                    ]
                    }}
                            
                    Here is the transcript to find best answer, relate to the user_query:
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
            return f"Error generating structured summary: {str(e)}"
       
