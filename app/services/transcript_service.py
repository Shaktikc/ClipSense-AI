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

    def generate_summary(self, transcript_string: str) -> str:
        prompt = f"""
        You are a helpful assistant.

        You are given a transcript of a video in JSON format. Each entry contains:
        - "text": a phrase or sentence from the video,
        - "start": the timestamp in seconds,
        - "duration": how long the speech lasted.

        Your tasks:
        1. Write a concise, coherent summary of the transcript in **paragraph form**.
        2. Then, for each **distinct idea or sentence in the summary**, identify the most relevant transcript segments that support it.
        3. For each matched segment, include:
        - the `matched_text`,
        - its `start` time,
        - its `duration`.
        -its `video_id`.

        Return your response in this exact structure and inside the structured dont include the "json" word :

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

        Here is the transcript to analyze:
        {transcript_string}
        """

        chat_response = self.client.chat.complete(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )
        # print("test", chat_response.choices[0].message.content)
        return chat_response.choices[0].message.content
