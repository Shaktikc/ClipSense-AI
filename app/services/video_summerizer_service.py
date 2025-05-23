from youtube_transcript_api import YouTubeTranscriptApi
from typing import List, Tuple, Dict
import time
from openai import OpenAI
from app.config.settings import API_KEY


class VideoSummerizerService:
    def __init__(self):
        self.client = OpenAI(api_key=API_KEY)

    def get_transcript(self, video_id: str) -> Tuple[List[Dict], str]:
        """
        Retrieve the transcript for a given YouTube video.
        Retries up to 10 times in case of transient failures.

        :param video_id: YouTube video identifier
        :return: Tuple of (transcript list, error message or None)
        """
        for attempt in range(10):
            try:
                transcript = YouTubeTranscriptApi.get_transcript(video_id)
                return transcript, None
            except Exception as e:
                if attempt == 3:
                    return None, str(e)
                time.sleep(1)

    def transcript_related_to_user_query(
        self, user_query: str, transcript_string: List[Dict]
    ) -> str:
        instructions = f"""
                # Instructions

                You are an AI assistant designed to analyze YouTube transcripts and extract relevant information based on a user's query. Follow these general rules:

                - Be precise and semantically aware when matching transcript content to the user query.
                - Select at most **one matching segment per video**.
                - Ignore any video that does not contain relevant content.
                - Do not repeat video IDs in the final output.

                # 🧠 Understanding the Task

                You are given:
                - A `user_query`.
                - A list of YouTube transcript segments. Each segment contains:
                • "text": a phrase or sentence from the video  
                • "start": when the speech begins (in seconds)  
                • "duration": how long the speech lasted (in seconds)  
                • "video_id": a unique video identifier  

                Here is the transcript data:
                {transcript_string}

                # Workflow: Follow These Steps

                1. **Understand the user query.**  
                Identify what kind of response is expected: e.g., explanation, summary, how-to, opinion, etc.

                2. **Analyze the transcript by video_id.**  
                For each unique video ID:
                - Search for segments that **semantically relate** to the user query.
                - If relevant segments are found, choose **the best one** (most representative).
                - Skip the video if no segment is relevant.

                3. **Format the final response.**  
                Return the result in **strict JSON format** as follows:

                ```json
                {{
                "transcript": [
                    {{
                    "matched_text": "<relevant text from transcript>",
                    "start": <start time in seconds>,
                    "duration": <duration in seconds>,
                    "video_id": "<video_id>"
                    }}
                    // ... one entry per relevant video
                ]
                }}"""

        input_text = f"User query: {user_query}"

        try:
            response = self.client.responses.create(
                model="gpt-4.1-2025-04-14",
                instructions=instructions,
                input=input_text,
            )
            return response.text
        except Exception as e:
            return f"Error generating structured summary: {str(e)}"
