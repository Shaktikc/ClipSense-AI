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

                You are an AI assistant designed to analyze YouTube transcripts and extract relevant information based on a user's query. 

                You must Be precise and semantically aware when matching transcript content to the user query.
                You must Select  matching segment from all the  transcript with unique video_id.
                You must not repeat same video_id in the final output .

                # Workflow:

                You are given:
                - A `user_query`.
                - A list of YouTube transcript segments. Each segment contains:
                • "text": a phrase or sentence from the video  
                • "start": when the speech begins (in seconds)  
                • "duration": how long the speech lasted (in seconds)  
                • "video_id": a unique video identifier  

                Here is the transcript data:
                {transcript_string}

                Follow These Steps

                ## 1.Understand the user query.
                -Determine what type of information the user is asking for.

               ## 2.Analyze the transcript by video_id for relevant information based on a user's query.
                For each unique video ID:
                - Search for segments that semantically relate to the user query.
                - Ensure the output includes at least one matching segment from each unique video_id.
                - Do not include duplicate video_id in the results.

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


                ## 4. Testing
                - Test each segment is semantically relate to the user query.
                - Test  the output includes at least one matching segment from each unique video_id.
                - Test  no duplicate video_id in the results.
                - Ensure all tests pass before finalizing.
                
                ## 5. Final Verification
                - verify each segment is semantically relate to the user query.
                - verify  the output includes at least one matching segment from each unique video_id.
                - verify  no duplicate video_id in the results.
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
