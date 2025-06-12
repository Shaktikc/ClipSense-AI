from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import GenericProxyConfig
from typing import List, Tuple, Dict
import time
from openai import OpenAI
from app.config.settings import API_KEY
from youtube_transcript_api.proxies import WebshareProxyConfig




class VideoSummerizerService:
    def __init__(self):
        self.client = OpenAI(api_key=API_KEY)
        # self.ytt_api = YouTubeTranscriptApi(
        #     proxy_config=GenericProxyConfig(
        #         http_url="socks5h://USERNAME:PASSWORD@us.socks.nordhold.net:1080",
        #         https_url="socks5h://USERNAME:PASSWORD@us.socks.nordhold.net:1080"
        #     )
        # )
        self.ytt_api = YouTubeTranscriptApi(
            proxy_config=WebshareProxyConfig(
            proxy_username="vuuspimn",
            proxy_password="yb7utxrwqg1x",
            )
        )


    def get_transcript(self, video_id: str) -> Tuple[List[Dict], str]:
        """
        Retrieve the transcript for a given YouTube video.
        Retries up to 20 times in case of transient failures.

        :param video_id: YouTube video identifier
        :return: Tuple of (transcript list, error message or None)
        """
        for attempt in range(20):
            try:
                transcript = self.ytt_api.get_transcript(video_id)
                print(f"Transcript for video {video_id} retrieved successfully.",transcript)
                return transcript
            except Exception as e:
                if attempt == 19:
                    return None, str(e)
                time.sleep(1)

    def transcript_related_to_user_query(
        self, user_query: str, transcript_string: List[Dict]
    ) -> str:
        instructions = f"""
                # Instructions

                You are an AI assistant designed to analyze YouTube transcripts and extract relevant information based on a user's query. 

                You must Be precise and semantically aware when matching transcript content to the user query.


                # Workflow:

                You are given:
                - A `user_query`.
                - A list of YouTube transcript segments. Each segment contains:
                • "text": a phrase or sentence from the video  
                • "start": when the speech begins (in seconds)  
                • "duration": how long the speech lasted (in seconds)  

                Here is the transcript data:
                {transcript_string}

                Follow These Steps

                ## 1.Understand the user query.
                -Determine what type of information the user is asking for.

               ## 2.Analyze the transcript for relevant information based on a user's query.
                - Search for segments that semantically relate to the user query.

               ## 3. Format the final response.
                Return the result in strict JSON format as follows:

                
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
                }}  

                ## 4. Final Verification
                - verify each segment is semantically relate to the user query.
                - Iterate until you are extremely confident every step is followed.
                """

        input_text = f"User query: {user_query}"

        try:
            response = self.client.responses.create(
                model="gpt-4.1-mini",
                instructions=instructions,
                input=input_text,
            )
            print(
                "Response from OpenAI:",
                response.to_dict()["output"][0]["content"][0]["text"],
            )
            return response.to_dict()["output"][0]["content"][0]["text"]
        except Exception as e:
            return f"Error generating structured summary: {str(e)}"
