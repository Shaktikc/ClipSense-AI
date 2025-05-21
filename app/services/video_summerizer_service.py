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

    def summary_to_transcript_mapping(
        self, transcript_string: str, summary: str
    ) -> str:
        prompt = f"""
      
        You are given a summary and youtube transcript. Each transcript contains:
        - "text": a phrase or sentence from the video,
        - "start": the timestamp (in seconds) when the speech begins,
        - "duration": how long the speech lasted.

        Your tasks:
        1. For each **sentence in the summary**, identify the most relevant transcript segments that support it.
        2. For each matched segment, include:
        - the matched_text: the matching phrase from the transcript,
        - its start time:its starting time in seconds,
        - its duration:how long it lasted in seconds.
        - its video_id.
        

        Return your response in this exact structure :

        "
        {{
            "summary": "Your paragraph summary here.",
            "mapping": {{
                "summary sentence or idea 1": [
                    {{"matched_text": "...", "start": ..., "duration": ...}}
                ],
                "summary sentence or idea 2": [
                    ...
                ]
            }}
        }}
        "

        Here is the summary  and  transcript to map:
        {summary} {transcript_string}
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
