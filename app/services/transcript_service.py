from youtube_transcript_api import YouTubeTranscriptApi
from typing import List, Tuple, Dict
import os
from openai import OpenAI
from app.config.settings import API_KEY
import time

class TranscriptService:
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

    def transcript_mock_data(self) -> str:
        mock_transcript = {
            "results": [
                {
                    "video_id": "FwOTs4UxQS4",
                    "transcript": [
                        {
                            "text": "AI. AI. AI. AI. AI.",
                            "start": 3.76,
                            "duration": 6.879,
                        },
                        {
                            "text": "AI. You know, more agentic. Agentic",
                            "start": 7.96,
                            "duration": 4.92,
                        },
                        {
                            "text": "capabilities. An AI agent. Agents.",
                            "start": 10.639,
                            "duration": 4.801,
                        },
                        {
                            "text": "Agentic workflows. Agents. Agents.",
                            "start": 12.88,
                            "duration": 6.159,
                        },
                        {
                            "text": "Agent. Agent. Agent. Agent. Agentic.",
                            "start": 15.44,
                            "duration": 5.44,
                        },
                        {
                            "text": "All right. Most explanations of AI",
                            "start": 19.039,
                            "duration": 4.721,
                        },
                        {
                            "text": "agents is either too technical or too",
                            "start": 20.88,
                            "duration": 5.2,
                        },
                        {
                            "text": "basic. This video is meant for people",
                            "start": 23.76,
                            "duration": 4.64,
                        },
                        {
                            "text": "like myself. You have zero technical",
                            "start": 26.08,
                            "duration": 4.84,
                        },
                        {
                            "text": "background, but you use AI tools",
                            "start": 28.4,
                            "duration": 5.2,
                        },
                        {
                            "text": "regularly and you want to learn just",
                            "start": 30.92,
                            "duration": 5.479,
                        },
                        {
                            "text": "enough about AI agents to see how it",
                            "start": 33.6,
                            "duration": 5.279,
                        },
                        {
                            "text": "affects you. In this video, we'll follow",
                            "start": 36.399,
                            "duration": 5.201,
                        },
                        {
                            "text": "a simple one, two, three learning path",
                            "start": 38.879,
                            "duration": 5.041,
                        },
                        {
                            "text": "by building on concepts you already",
                            "start": 41.6,
                            "duration": 5.2,
                        },
                        {
                            "text": "understand like chatbt and then moving",
                            "start": 43.92,
                            "duration": 5.72,
                        },
                        {
                            "text": "on to AI workflows and then finally AI",
                            "start": 46.8,
                            "duration": 6.079,
                        },
                        {
                            "text": "agents. All the while using examples you",
                            "start": 49.64,
                            "duration": 5.8,
                        },
                        {
                            "text": "will actually encounter in real life.",
                            "start": 52.879,
                            "duration": 4.081,
                        },
                        {
                            "text": "And believe me when I tell you those",
                            "start": 55.44,
                            "duration": 3.36,
                        },
                        {
                            "text": "intimidating terms you see everywhere",
                            "start": 56.96,
                            "duration": 5.439,
                        },
                        {
                            "text": "like rag, rag, or react, they're a lot",
                            "start": 58.8,
                            "duration": 5.439,
                        },
                        {
                            "text": "simpler than you think. Let's get",
                            "start": 62.399,
                            "duration": 3.441,
                        },
                        {
                            "text": "started. Kicking things off at level",
                            "start": 64.239,
                            "duration": 4.161,
                        },
                        {
                            "text": "one, large language models. Popular AI",
                            "start": 65.84,
                            "duration": 4.959,
                        },
                        {
                            "text": "chatbots like CHBT, Google Gemini, and",
                            "start": 68.4,
                            "duration": 5.92,
                        },
                        {
                            "text": "Claude are applications built on top of",
                            "start": 70.799,
                            "duration": 6.241,
                        },
                        {
                            "text": "large language models, LLMs, and they're",
                            "start": 74.32,
                            "duration": 5.119,
                        },
                        {
                            "text": "fantastic at generating and editing",
                            "start": 77.04,
                            "duration": 4.8,
                        },
                        {
                            "text": "text. Here's a simple visualization.",
                            "start": 79.439,
                            "duration": 5.04,
                        },
                        {
                            "text": "You, the human, provides an input and",
                            "start": 81.84,
                            "duration": 5.76,
                        },
                        {
                            "text": "the LLM produces an output based on its",
                            "start": 84.479,
                            "duration": 4.881,
                        },
                        {
                            "text": "training data. For example, if I were to",
                            "start": 87.6,
                            "duration": 3.839,
                        },
                        {
                            "text": "ask Chachi BT to draft an email",
                            "start": 89.36,
                            "duration": 4.56,
                        },
                        {
                            "text": "requesting a coffee chat, my prompt is",
                            "start": 91.439,
                            "duration": 4.801,
                        },
                        {
                            "text": "the input and the resulting email that's",
                            "start": 93.92,
                            "duration": 3.68,
                        },
                        {
                            "text": "way more polite than I would ever be in",
                            "start": 96.24,
                            "duration": 4.4,
                        },
                        {
                            "text": "real life is the output. So far so good,",
                            "start": 97.6,
                            "duration": 5.839,
                        },
                        {
                            "text": "right? Simple stuff. But what if I asked",
                            "start": 100.64,
                            "duration": 6.72,
                        },
                        {
                            "text": "Chachi BT when my next coffee chat is?",
                            "start": 103.439,
                            "duration": 5.921,
                        },
                        {
                            "text": "Even without seeing the response, both",
                            "start": 107.36,
                            "duration": 4.719,
                        },
                        {
                            "text": "you and I know Chachi PT is gonna fail",
                            "start": 109.36,
                            "duration": 4.24,
                        },
                        {
                            "text": "because it doesn't know that",
                            "start": 112.079,
                            "duration": 4.161,
                        },
                        {
                            "text": "information. It doesn't have access to",
                            "start": 113.6,
                            "duration": 4.72,
                        },
                        {
                            "text": "my calendar. This highlights two key",
                            "start": 116.24,
                            "duration": 4.64,
                        },
                        {
                            "text": "traits of large language models. First,",
                            "start": 118.32,
                            "duration": 4.479,
                        },
                        {
                            "text": "despite being trained on vast amounts of",
                            "start": 120.88,
                            "duration": 4.0,
                        },
                        {
                            "text": "data, they have limited knowledge of",
                            "start": 122.799,
                            "duration": 4.241,
                        },
                        {
                            "text": "proprietary information like our",
                            "start": 124.88,
                            "duration": 4.4,
                        },
                        {
                            "text": "personal information or internal company",
                            "start": 127.04,
                            "duration": 5.68,
                        },
                        {
                            "text": "data. Second, LLMs are passive. They",
                            "start": 129.28,
                            "duration": 5.52,
                        },
                        {
                            "text": "wait for our prompt and then respond.",
                            "start": 132.72,
                            "duration": 4.32,
                        },
                        {
                            "text": "Right? Keep these two traits in mind",
                            "start": 134.8,
                            "duration": 4.4,
                        },
                        {
                            "text": "moving forward. Moving to level two, AI",
                            "start": 137.04,
                            "duration": 4.88,
                        },
                        {
                            "text": "workflows. Let's build on our example.",
                            "start": 139.2,
                            "duration": 5.92,
                        },
                        {
                            "text": 'What if I, a human, told the LM, "Every',
                            "start": 141.92,
                            "duration": 4.959,
                        },
                        {
                            "text": "time I ask about a personal event,",
                            "start": 145.12,
                            "duration": 4.08,
                        },
                        {
                            "text": "perform a search query and fetch data",
                            "start": 146.879,
                            "duration": 4.72,
                        },
                        {
                            "text": "from my Google calendar before providing",
                            "start": 149.2,
                            "duration": 4.16,
                        },
                        {
                            "text": 'a response." With this logic',
                            "start": 151.599,
                            "duration": 4.0,
                        },
                        {
                            "text": 'implemented, the next time I ask, "When',
                            "start": 153.36,
                            "duration": 4.8,
                        },
                        {
                            "text": "is my coffee chat with Elon Husky?\" I'll",
                            "start": 155.599,
                            "duration": 4.72,
                        },
                        {
                            "text": "get the correct answer because the LLM",
                            "start": 158.16,
                            "duration": 4.48,
                        },
                        {
                            "text": "will now first go into my Google",
                            "start": 160.319,
                            "duration": 5.28,
                        },
                        {
                            "text": "calendar to find that information. But",
                            "start": 162.64,
                            "duration": 5.36,
                        },
                        {
                            "text": "here's where it gets tricky. What if my",
                            "start": 165.599,
                            "duration": 4.801,
                        },
                        {
                            "text": 'next follow-up question is, "What will',
                            "start": 168.0,
                            "duration": 5.28,
                        },
                        {
                            "text": 'the weather be like that day?" The LM',
                            "start": 170.4,
                            "duration": 5.04,
                        },
                        {
                            "text": "will now fail at answering the query",
                            "start": 173.28,
                            "duration": 3.92,
                        },
                        {
                            "text": "because the path we told the LM to",
                            "start": 175.44,
                            "duration": 4.799,
                        },
                        {
                            "text": "follow is to always search my Google",
                            "start": 177.2,
                            "duration": 5.039,
                        },
                        {
                            "text": "calendar, which does not have",
                            "start": 180.239,
                            "duration": 4.561,
                        },
                        {
                            "text": "information about the weather. This is a",
                            "start": 182.239,
                            "duration": 5.201,
                        },
                        {
                            "text": "fundamental trait of AI workflows. They",
                            "start": 184.8,
                            "duration": 6.159,
                        },
                        {
                            "text": "can only follow predefined paths set by",
                            "start": 187.44,
                            "duration": 5.2,
                        },
                        {
                            "text": "humans. And if you want to get",
                            "start": 190.959,
                            "duration": 4.481,
                        },
                        {
                            "text": "technical, this path is also called the",
                            "start": 192.64,
                            "duration": 5.04,
                        },
                        {
                            "text": "control logic. Pushing my example",
                            "start": 195.44,
                            "duration": 4.64,
                        },
                        {
                            "text": "further, what if I added more steps into",
                            "start": 197.68,
                            "duration": 4.4,
                        },
                        {
                            "text": "the workflow by allowing the LM to",
                            "start": 200.08,
                            "duration": 4.32,
                        },
                        {
                            "text": "access the weather via an API and then",
                            "start": 202.08,
                            "duration": 4.879,
                        },
                        {
                            "text": "just for fun use a text to audio model",
                            "start": 204.4,
                            "duration": 4.559,
                        },
                        {
                            "text": "to speak the answer. The weather",
                            "start": 206.959,
                            "duration": 4.64,
                        },
                        {
                            "text": "forecast for seeing Elon Husky is sunny",
                            "start": 208.959,
                            "duration": 4.721,
                        },
                        {
                            "text": "with a chance of being a good boy.",
                            "start": 211.599,
                            "duration": 4.161,
                        },
                        {
                            "text": "Here's the thing. No matter how many",
                            "start": 213.68,
                            "duration": 5.52,
                        },
                        {
                            "text": "steps we add, this is still just an AI",
                            "start": 215.76,
                            "duration": 5.839,
                        },
                        {
                            "text": "workflow. Even if there were hundreds or",
                            "start": 219.2,
                            "duration": 5.679,
                        },
                        {
                            "text": "thousands of steps, if a human is the",
                            "start": 221.599,
                            "duration": 6.321,
                        },
                        {
                            "text": "decision maker, there is no AI agent",
                            "start": 224.879,
                            "duration": 5.041,
                        },
                        {
                            "text": "involvement. Pro tip: retrieval",
                            "start": 227.92,
                            "duration": 4.72,
                        },
                        {
                            "text": "augmented generation or rag is a fancy",
                            "start": 229.92,
                            "duration": 4.64,
                        },
                        {
                            "text": "term that's thrown around a lot. In",
                            "start": 232.64,
                            "duration": 3.84,
                        },
                        {
                            "text": "simple terms, rag is a process that",
                            "start": 234.56,
                            "duration": 4.239,
                        },
                        {
                            "text": "helps AI models look things up before",
                            "start": 236.48,
                            "duration": 4.16,
                        },
                        {
                            "text": "they answer, like accessing my calendar",
                            "start": 238.799,
                            "duration": 4.241,
                        },
                        {
                            "text": "or the weather service. Essentially, Rag",
                            "start": 240.64,
                            "duration": 5.44,
                        },
                        {
                            "text": "is just a type of AI workflow. By the",
                            "start": 243.04,
                            "duration": 4.72,
                        },
                        {
                            "text": "way, I have a free AI toolkit that cuts",
                            "start": 246.08,
                            "duration": 3.12,
                        },
                        {
                            "text": "through the noise and helps you master",
                            "start": 247.76,
                            "duration": 3.199,
                        },
                        {
                            "text": "essential AI tools and workflows. I'll",
                            "start": 249.2,
                            "duration": 3.679,
                        },
                        {
                            "text": "leave a link to that down below. Here's",
                            "start": 250.959,
                            "duration": 4.0,
                        },
                        {
                            "text": "a real world example. Following Helena",
                            "start": 252.879,
                            "duration": 4.241,
                        },
                        {
                            "text": "Louu's amazing tutorial, I created a",
                            "start": 254.959,
                            "duration": 4.96,
                        },
                        {
                            "text": "simple AI workflow using make.com. Here",
                            "start": 257.12,
                            "duration": 4.48,
                        },
                        {
                            "text": "you can see that first I'm using Google",
                            "start": 259.919,
                            "duration": 3.521,
                        },
                        {
                            "text": "Sheets to do something. Specifically,",
                            "start": 261.6,
                            "duration": 4.24,
                        },
                        {
                            "text": "I'm compiling links to news articles in",
                            "start": 263.44,
                            "duration": 4.56,
                        },
                        {
                            "text": "a Google sheet. And this is that Google",
                            "start": 265.84,
                            "duration": 5.2,
                        },
                        {
                            "text": "sheet. Second, I'm using Perplexity to",
                            "start": 268.0,
                            "duration": 6.479,
                        },
                        {
                            "text": "summarize those news articles. Then",
                            "start": 271.04,
                            "duration": 5.76,
                        },
                        {
                            "text": "using Claude and using a prompt that I",
                            "start": 274.479,
                            "duration": 4.16,
                        },
                        {
                            "text": "wrote, I'm asking Claude to draft a",
                            "start": 276.8,
                            "duration": 5.52,
                        },
                        {
                            "text": "LinkedIn and Instagram post. Finally, I",
                            "start": 278.639,
                            "duration": 5.921,
                        },
                        {
                            "text": "can schedule this to run automatically",
                            "start": 282.32,
                            "duration": 4.64,
                        },
                        {
                            "text": "every day at 8 a.m. As you can see, this",
                            "start": 284.56,
                            "duration": 4.8,
                        },
                        {
                            "text": "is an AI workflow because it follows a",
                            "start": 286.96,
                            "duration": 5.92,
                        },
                        {
                            "text": "predefined path set by me. Step one, you",
                            "start": 289.36,
                            "duration": 6.08,
                        },
                        {
                            "text": "do this. Step two, you do this. Step",
                            "start": 292.88,
                            "duration": 4.8,
                        },
                        {
                            "text": "three, you do this. And finally,",
                            "start": 295.44,
                            "duration": 4.4,
                        },
                        {
                            "text": "remember to run daily at 8 am. One last",
                            "start": 297.68,
                            "duration": 4.72,
                        },
                        {
                            "text": "thing, if I test this workflow and I",
                            "start": 299.84,
                            "duration": 5.68,
                        },
                        {
                            "text": "don't like the final output of the",
                            "start": 302.4,
                            "duration": 6.0,
                        },
                        {
                            "text": "LinkedIn post, for example, as you can",
                            "start": 305.52,
                            "duration": 4.48,
                        },
                        {
                            "text": "see right here, uh, it's not funny",
                            "start": 308.4,
                            "duration": 3.2,
                        },
                        {
                            "text": "enough and I'm naturally hilarious,",
                            "start": 310.0,
                            "duration": 6.12,
                        },
                        {
                            "text": "right? I'd have to manually go back and",
                            "start": 311.6,
                            "duration": 8.72,
                        },
                        {
                            "text": "rewrite the prompt for Claude. Okay? And",
                            "start": 316.12,
                            "duration": 7.0,
                        },
                        {
                            "text": "this trial and error iteration is",
                            "start": 320.32,
                            "duration": 5.439,
                        },
                        {
                            "text": "currently being done by me, a human. So",
                            "start": 323.12,
                            "duration": 4.24,
                        },
                        {
                            "text": "keep that in mind moving forward. All",
                            "start": 325.759,
                            "duration": 3.521,
                        },
                        {
                            "text": "right, level three, AI agents.",
                            "start": 327.36,
                            "duration": 4.16,
                        },
                        {
                            "text": "Continuing the make.com example, let's",
                            "start": 329.28,
                            "duration": 4.0,
                        },
                        {
                            "text": "break down what I've been doing so far",
                            "start": 331.52,
                            "duration": 4.48,
                        },
                        {
                            "text": "as the human decision maker. With the",
                            "start": 333.28,
                            "duration": 4.4,
                        },
                        {
                            "text": "goal of creating social media posts",
                            "start": 336.0,
                            "duration": 3.919,
                        },
                        {
                            "text": "based off of news articles, I need to do",
                            "start": 337.68,
                            "duration": 5.6,
                        },
                        {
                            "text": "two things. First, reason or think about",
                            "start": 339.919,
                            "duration": 4.881,
                        },
                        {
                            "text": "the best approach. I need to first",
                            "start": 343.28,
                            "duration": 3.12,
                        },
                        {
                            "text": "compile the news articles, then",
                            "start": 344.8,
                            "duration": 3.52,
                        },
                        {
                            "text": "summarize them, then write the final",
                            "start": 346.4,
                            "duration": 5.04,
                        },
                        {
                            "text": "posts. Second, take action using tools.",
                            "start": 348.32,
                            "duration": 5.28,
                        },
                        {
                            "text": "I need to find and link to those news",
                            "start": 351.44,
                            "duration": 4.319,
                        },
                        {
                            "text": "articles in Google Sheets. Use",
                            "start": 353.6,
                            "duration": 4.56,
                        },
                        {
                            "text": "Perplexity for real-time summarization",
                            "start": 355.759,
                            "duration": 4.481,
                        },
                        {
                            "text": "and then claw for copyrightiting. So,",
                            "start": 358.16,
                            "duration": 3.599,
                        },
                        {
                            "text": "and this is the most important sentence",
                            "start": 360.24,
                            "duration": 4.32,
                        },
                        {
                            "text": "in this entire video. The one massive",
                            "start": 361.759,
                            "duration": 4.961,
                        },
                        {
                            "text": "change that has to happen in order for",
                            "start": 364.56,
                            "duration": 5.12,
                        },
                        {
                            "text": "this AI workflow to become an AI agent",
                            "start": 366.72,
                            "duration": 6.319,
                        },
                        {
                            "text": "is for me, the human decision maker, to",
                            "start": 369.68,
                            "duration": 6.72,
                        },
                        {
                            "text": "be replaced by an LLM. In other words,",
                            "start": 373.039,
                            "duration": 6.081,
                        },
                        {
                            "text": "the AI agent must reason. What's the",
                            "start": 376.4,
                            "duration": 4.239,
                        },
                        {
                            "text": "most efficient way to compile these news",
                            "start": 379.12,
                            "duration": 3.44,
                        },
                        {
                            "text": "articles? Should I copy and paste each",
                            "start": 380.639,
                            "duration": 4.161,
                        },
                        {
                            "text": "article into a word document? No, it's",
                            "start": 382.56,
                            "duration": 3.84,
                        },
                        {
                            "text": "probably easier to compile links to",
                            "start": 384.8,
                            "duration": 3.519,
                        },
                        {
                            "text": "those articles and then use another tool",
                            "start": 386.4,
                            "duration": 4.56,
                        },
                        {
                            "text": "to fetch the data. Yes, that makes more",
                            "start": 388.319,
                            "duration": 5.921,
                        },
                        {
                            "text": "sense. The AI agent must act, aka do",
                            "start": 390.96,
                            "duration": 6.079,
                        },
                        {
                            "text": "things via tools. Should I use Microsoft",
                            "start": 394.24,
                            "duration": 4.88,
                        },
                        {
                            "text": "Word to compile links? No. Inserting",
                            "start": 397.039,
                            "duration": 4.0,
                        },
                        {
                            "text": "links directly into rows is way more",
                            "start": 399.12,
                            "duration": 4.96,
                        },
                        {
                            "text": "efficient. What about Excel? M. So the",
                            "start": 401.039,
                            "duration": 4.401,
                        },
                        {
                            "text": "user has already connected their Google",
                            "start": 404.08,
                            "duration": 3.36,
                        },
                        {
                            "text": "account with make.com. So Google Sheets",
                            "start": 405.44,
                            "duration": 4.319,
                        },
                        {
                            "text": "is a better option. Pro tip. Because of",
                            "start": 407.44,
                            "duration": 4.4,
                        },
                        {
                            "text": "this, the most common configuration for",
                            "start": 409.759,
                            "duration": 5.521,
                        },
                        {
                            "text": "AI agents is the react framework. All AI",
                            "start": 411.84,
                            "duration": 7.56,
                        },
                        {
                            "text": "agents must reason and act. So",
                            "start": 415.28,
                            "duration": 6.479,
                        },
                        {
                            "text": "react. Sounds simple once we break it",
                            "start": 419.4,
                            "duration": 4.519,
                        },
                        {
                            "text": "down, right? A third key trait of AI",
                            "start": 421.759,
                            "duration": 4.401,
                        },
                        {
                            "text": "agents is their ability to iterate.",
                            "start": 423.919,
                            "duration": 4.481,
                        },
                        {
                            "text": "Remember when I had to manually rewrite",
                            "start": 426.16,
                            "duration": 3.92,
                        },
                        {
                            "text": "the prompt to make the LinkedIn post",
                            "start": 428.4,
                            "duration": 4.88,
                        },
                        {
                            "text": "funnier? I, the human, probably need to",
                            "start": 430.08,
                            "duration": 5.2,
                        },
                        {
                            "text": "repeat this iterative process a few",
                            "start": 433.28,
                            "duration": 3.84,
                        },
                        {
                            "text": "times to get something I'm happy with,",
                            "start": 435.28,
                            "duration": 4.319,
                        },
                        {
                            "text": "right? An AI agent will be able to do",
                            "start": 437.12,
                            "duration": 5.44,
                        },
                        {
                            "text": "the same thing autonomously. In our",
                            "start": 439.599,
                            "duration": 5.44,
                        },
                        {
                            "text": "example, the AI agent would autonomously",
                            "start": 442.56,
                            "duration": 5.44,
                        },
                        {
                            "text": "add in another LM to critique its own",
                            "start": 445.039,
                            "duration": 5.521,
                        },
                        {
                            "text": "output. Okay, I've drafted V1 of a",
                            "start": 448.0,
                            "duration": 4.08,
                        },
                        {
                            "text": "LinkedIn post. How do I make sure it's",
                            "start": 450.56,
                            "duration": 3.68,
                        },
                        {
                            "text": "good? Oh, I know. I'll add another step",
                            "start": 452.08,
                            "duration": 4.559,
                        },
                        {
                            "text": "where an LM will critique the post based",
                            "start": 454.24,
                            "duration": 4.56,
                        },
                        {
                            "text": "on LinkedIn best practices. And let's",
                            "start": 456.639,
                            "duration": 3.601,
                        },
                        {
                            "text": "repeat this until the best practices",
                            "start": 458.8,
                            "duration": 3.76,
                        },
                        {
                            "text": "criteria are all met. And after a few",
                            "start": 460.24,
                            "duration": 5.04,
                        },
                        {
                            "text": "cycles of that, we have the final",
                            "start": 462.56,
                            "duration": 5.039,
                        },
                        {
                            "text": "output. That was a hypothetical example.",
                            "start": 465.28,
                            "duration": 4.8,
                        },
                        {
                            "text": "So let's move on to a real world AI",
                            "start": 467.599,
                            "duration": 5.681,
                        },
                        {
                            "text": "agent example. Andrew is a preeeminent",
                            "start": 470.08,
                            "duration": 5.519,
                        },
                        {
                            "text": "figure in AI and he created this demo",
                            "start": 473.28,
                            "duration": 5.359,
                        },
                        {
                            "text": "website that illustrates how an AI agent",
                            "start": 475.599,
                            "duration": 4.72,
                        },
                        {
                            "text": "works. I'll link the full video down",
                            "start": 478.639,
                            "duration": 3.921,
                        },
                        {
                            "text": "below, but when I search for a keyword",
                            "start": 480.319,
                            "duration": 7.361,
                        },
                        {
                            "text": "like skier, enter the AI vision agent in",
                            "start": 482.56,
                            "duration": 7.919,
                        },
                        {
                            "text": "the background is first reasoning what a",
                            "start": 487.68,
                            "duration": 5.04,
                        },
                        {
                            "text": "skier looks like. A person on skis going",
                            "start": 490.479,
                            "duration": 4.0,
                        },
                        {
                            "text": "really fast in snow, for example, right?",
                            "start": 492.72,
                            "duration": 5.759,
                        },
                        {
                            "text": "I'm not sure. And then it's acting by",
                            "start": 494.479,
                            "duration": 7.521,
                        },
                        {
                            "text": "looking at clips in video footage,",
                            "start": 498.479,
                            "duration": 6.241,
                        },
                        {
                            "text": "trying to identify what it thinks a",
                            "start": 502.0,
                            "duration": 7.319,
                        },
                        {
                            "text": "skier is, indexing that clip, and then",
                            "start": 504.72,
                            "duration": 7.679,
                        },
                        {
                            "text": "returning that clip to us. Although this",
                            "start": 509.319,
                            "duration": 5.08,
                        },
                        {
                            "text": "might not feel impressive, remember that",
                            "start": 512.399,
                            "duration": 4.281,
                        },
                        {
                            "text": "an AI agent did all that instead of a",
                            "start": 514.399,
                            "duration": 5.361,
                        },
                        {
                            "text": "human reviewing the footage beforehand,",
                            "start": 516.68,
                            "duration": 5.56,
                        },
                        {
                            "text": "manually identifying the skier, and",
                            "start": 519.76,
                            "duration": 5.68,
                        },
                        {
                            "text": "adding tags like skier, mountain, ski,",
                            "start": 522.24,
                            "duration": 5.599,
                        },
                        {
                            "text": "snow. The programming is obviously a lot",
                            "start": 525.44,
                            "duration": 4.079,
                        },
                        {
                            "text": "more technical and complicated than what",
                            "start": 527.839,
                            "duration": 3.841,
                        },
                        {
                            "text": "we see in the front end, but that's the",
                            "start": 529.519,
                            "duration": 4.32,
                        },
                        {
                            "text": "point of this demo, right? The average",
                            "start": 531.68,
                            "duration": 5.04,
                        },
                        {
                            "text": "user like myself wants a simple app that",
                            "start": 533.839,
                            "duration": 5.041,
                        },
                        {
                            "text": "just works without me having to",
                            "start": 536.72,
                            "duration": 3.76,
                        },
                        {
                            "text": "understand what's going on in the back",
                            "start": 538.88,
                            "duration": 3.6,
                        },
                        {
                            "text": "end. Speaking of examples, I'm also",
                            "start": 540.48,
                            "duration": 4.56,
                        },
                        {
                            "text": "building my very own basic AI agent",
                            "start": 542.48,
                            "duration": 4.72,
                        },
                        {
                            "text": "using Nan. So, let me know in the",
                            "start": 545.04,
                            "duration": 3.68,
                        },
                        {
                            "text": "comments what type of AI agent you'd",
                            "start": 547.2,
                            "duration": 4.079,
                        },
                        {
                            "text": "like me to make a tutorial on next. To",
                            "start": 548.72,
                            "duration": 4.0,
                        },
                        {
                            "text": "wrap up, here's a simplified",
                            "start": 551.279,
                            "duration": 3.441,
                        },
                        {
                            "text": "visualization of the three levels we",
                            "start": 552.72,
                            "duration": 4.4,
                        },
                        {
                            "text": "covered today. Level one, we provide an",
                            "start": 554.72,
                            "duration": 4.799,
                        },
                        {
                            "text": "input and the LM responds with an",
                            "start": 557.12,
                            "duration": 5.04,
                        },
                        {
                            "text": "output. Easy. Level two, for AI",
                            "start": 559.519,
                            "duration": 5.361,
                        },
                        {
                            "text": "workflows, we provide an input and tell",
                            "start": 562.16,
                            "duration": 5.28,
                        },
                        {
                            "text": "the LM to follow a predefined path that",
                            "start": 564.88,
                            "duration": 4.399,
                        },
                        {
                            "text": "may involve in retrieving information",
                            "start": 567.44,
                            "duration": 4.48,
                        },
                        {
                            "text": "from external tools. The key trait here",
                            "start": 569.279,
                            "duration": 5.361,
                        },
                        {
                            "text": "is that the human programs a path for LM",
                            "start": 571.92,
                            "duration": 5.76,
                        },
                        {
                            "text": "to follow. Level three, the AI agent",
                            "start": 574.64,
                            "duration": 5.28,
                        },
                        {
                            "text": "receives a goal and the LM performs",
                            "start": 577.68,
                            "duration": 4.159,
                        },
                        {
                            "text": "reasoning to determine how best to",
                            "start": 579.92,
                            "duration": 4.24,
                        },
                        {
                            "text": "achieve the goal, takes action using",
                            "start": 581.839,
                            "duration": 4.801,
                        },
                        {
                            "text": "tools to produce an interim result,",
                            "start": 584.16,
                            "duration": 4.72,
                        },
                        {
                            "text": "observes that interim result, and",
                            "start": 586.64,
                            "duration": 5.12,
                        },
                        {
                            "text": "decides whether iterations are required,",
                            "start": 588.88,
                            "duration": 4.959,
                        },
                        {
                            "text": "and produces a final output that",
                            "start": 591.76,
                            "duration": 4.72,
                        },
                        {
                            "text": "achieves the initial goal. The key trait",
                            "start": 593.839,
                            "duration": 4.801,
                        },
                        {
                            "text": "here is that the LLM is a decision maker",
                            "start": 596.48,
                            "duration": 4.08,
                        },
                        {
                            "text": "in the workflow. If you found this",
                            "start": 598.64,
                            "duration": 3.36,
                        },
                        {
                            "text": "helpful, you might want to learn how to",
                            "start": 600.56,
                            "duration": 3.76,
                        },
                        {
                            "text": "build a prompts database in Notion. See",
                            "start": 602.0,
                            "duration": 3.959,
                        },
                        {
                            "text": "you on the next video. In the",
                            "start": 604.32,
                            "duration": 5.92,
                        },
                        {
                            "text": "meantime, have a great one.",
                            "start": 605.959,
                            "duration": 4.281,
                        },
                    ],
                    "status": "success",
                },
                {
                    "video_id": "hLJTcVHW8_I",
                    "transcript": [
                        {
                            "text": "hello everyone I'm Alfie Marsh I'm the",
                            "start": 0.04,
                            "duration": 4.279,
                        },
                        {
                            "text": "co-founder and CEO of tool flow AI in",
                            "start": 1.92,
                            "duration": 3.919,
                        },
                        {
                            "text": "today's video we'll dive into the",
                            "start": 4.319,
                            "duration": 4.121,
                        },
                        {
                            "text": "fascinating world of AI agents as AI",
                            "start": 5.839,
                            "duration": 4.361,
                        },
                        {
                            "text": "agents become a more integral part of",
                            "start": 8.44,
                            "duration": 3.64,
                        },
                        {
                            "text": "our Lives it's evolving from Simply",
                            "start": 10.2,
                            "duration": 4.359,
                        },
                        {
                            "text": "responding to our commands to",
                            "start": 12.08,
                            "duration": 4.68,
                        },
                        {
                            "text": "understanding and acting autonomously so",
                            "start": 14.559,
                            "duration": 4.521,
                        },
                        {
                            "text": "let's unpack what AI agents are how they",
                            "start": 16.76,
                            "duration": 3.88,
                        },
                        {
                            "text": "work and why they might be a game",
                            "start": 19.08,
                            "duration": 4.039,
                        },
                        {
                            "text": "changer in your life and career what is",
                            "start": 20.64,
                            "duration": 5.16,
                        },
                        {
                            "text": "an AI agent an AI agent is a piece of",
                            "start": 23.119,
                            "duration": 4.601,
                        },
                        {
                            "text": "software designed to perform tasks",
                            "start": 25.8,
                            "duration": 3.92,
                        },
                        {
                            "text": "autonomously unlike traditional software",
                            "start": 27.72,
                            "duration": 4.76,
                        },
                        {
                            "text": "that follows strict rules AI agents make",
                            "start": 29.72,
                            "duration": 4.839,
                        },
                        {
                            "text": "decisions based on their understanding",
                            "start": 32.48,
                            "duration": 4.56,
                        },
                        {
                            "text": "and interactions with the world they use",
                            "start": 34.559,
                            "duration": 5.081,
                        },
                        {
                            "text": "Technologies like large language models",
                            "start": 37.04,
                            "duration": 5.359,
                        },
                        {
                            "text": "such as GPT from open AI Claude from",
                            "start": 39.64,
                            "duration": 5.28,
                        },
                        {
                            "text": "anthropic or Gemini from Google to",
                            "start": 42.399,
                            "duration": 5.16,
                        },
                        {
                            "text": "process and understand information and",
                            "start": 44.92,
                            "duration": 4.52,
                        },
                        {
                            "text": "determine the best course of action",
                            "start": 47.559,
                            "duration": 3.84,
                        },
                        {
                            "text": "imagine having like a digital assistant",
                            "start": 49.44,
                            "duration": 3.759,
                        },
                        {
                            "text": "instead of giving them an order and",
                            "start": 51.399,
                            "duration": 3.881,
                        },
                        {
                            "text": "saying ask this person if they're",
                            "start": 53.199,
                            "duration": 3.761,
                        },
                        {
                            "text": "available in this date and then send",
                            "start": 55.28,
                            "duration": 3.52,
                        },
                        {
                            "text": "them a calendar yes they would perform",
                            "start": 56.96,
                            "duration": 3.64,
                        },
                        {
                            "text": "the task but you're given a kind of",
                            "start": 58.8,
                            "duration": 3.64,
                        },
                        {
                            "text": "preset list of instructions of what they",
                            "start": 60.6,
                            "duration": 3.48,
                        },
                        {
                            "text": "need to do instead you could give",
                            "start": 62.44,
                            "duration": 3.96,
                        },
                        {
                            "text": "something a goal and more ambiguous and",
                            "start": 64.08,
                            "duration": 5.24,
                        },
                        {
                            "text": "say hey I need to book some time with",
                            "start": 66.4,
                            "duration": 5.6,
                        },
                        {
                            "text": "Joanne whenever I'm free in the next",
                            "start": 69.32,
                            "duration": 4.839,
                        },
                        {
                            "text": "month or so can you go about organizing",
                            "start": 72.0,
                            "duration": 4.4,
                        },
                        {
                            "text": "the schedules then the AI agent can go",
                            "start": 74.159,
                            "duration": 4.441,
                        },
                        {
                            "text": "and take that understand the objective",
                            "start": 76.4,
                            "duration": 3.84,
                        },
                        {
                            "text": "and then think of a list of other things",
                            "start": 78.6,
                            "duration": 3.76,
                        },
                        {
                            "text": "it needs to do step one check your",
                            "start": 80.24,
                            "duration": 4.239,
                        },
                        {
                            "text": "calendar for availability step two check",
                            "start": 82.36,
                            "duration": 4.2,
                        },
                        {
                            "text": "Joann's calendar for availability step",
                            "start": 84.479,
                            "duration": 3.761,
                        },
                        {
                            "text": "three determine the amount of time step",
                            "start": 86.56,
                            "duration": 3.559,
                        },
                        {
                            "text": "four and so on and so on and so on so",
                            "start": 88.24,
                            "duration": 4.12,
                        },
                        {
                            "text": "they act more autonomously and can",
                            "start": 90.119,
                            "duration": 3.96,
                        },
                        {
                            "text": "understand an objective rather than",
                            "start": 92.36,
                            "duration": 4.48,
                        },
                        {
                            "text": "follow a very specific set of rules AI",
                            "start": 94.079,
                            "duration": 5.201,
                        },
                        {
                            "text": "agents are different to llms large",
                            "start": 96.84,
                            "duration": 4.919,
                        },
                        {
                            "text": "language models while agents use models",
                            "start": 99.28,
                            "duration": 4.479,
                        },
                        {
                            "text": "like GPT for understanding and",
                            "start": 101.759,
                            "duration": 4.561,
                        },
                        {
                            "text": "generating language agents can do much",
                            "start": 103.759,
                            "duration": 4.72,
                        },
                        {
                            "text": "more you see traditional language models",
                            "start": 106.32,
                            "duration": 4.28,
                        },
                        {
                            "text": "predict responses Based on data that",
                            "start": 108.479,
                            "duration": 4.24,
                        },
                        {
                            "text": "they were trained on this data is static",
                            "start": 110.6,
                            "duration": 4.199,
                        },
                        {
                            "text": "they were trained on the internet and a",
                            "start": 112.719,
                            "duration": 3.961,
                        },
                        {
                            "text": "bunch of other resources but at a",
                            "start": 114.799,
                            "duration": 4.36,
                        },
                        {
                            "text": "specific Moment In Time language models",
                            "start": 116.68,
                            "duration": 4.68,
                        },
                        {
                            "text": "don't interrup act with the world beyond",
                            "start": 119.159,
                            "duration": 4.64,
                        },
                        {
                            "text": "their training data for example chat GPT",
                            "start": 121.36,
                            "duration": 5.039,
                        },
                        {
                            "text": "knows information only up until its last",
                            "start": 123.799,
                            "duration": 4.96,
                        },
                        {
                            "text": "update as of today their last update was",
                            "start": 126.399,
                            "duration": 5.281,
                        },
                        {
                            "text": "December 2023 which was more than 4",
                            "start": 128.759,
                            "duration": 5.041,
                        },
                        {
                            "text": "months ago the model itself can't fetch",
                            "start": 131.68,
                            "duration": 4.4,
                        },
                        {
                            "text": "or understand new events or data so if",
                            "start": 133.8,
                            "duration": 4.36,
                        },
                        {
                            "text": "you were to ask about the Max holay and",
                            "start": 136.08,
                            "duration": 4.879,
                        },
                        {
                            "text": "Justin gatei fight at UFC 300 that",
                            "start": 138.16,
                            "duration": 4.88,
                        },
                        {
                            "text": "happened last weekend who won and in",
                            "start": 140.959,
                            "duration": 3.961,
                        },
                        {
                            "text": "what round the language models are not",
                            "start": 143.04,
                            "duration": 3.199,
                        },
                        {
                            "text": "going to know and they're probably going",
                            "start": 144.92,
                            "duration": 3.399,
                        },
                        {
                            "text": "to try and make something up to please",
                            "start": 146.239,
                            "duration": 3.72,
                        },
                        {
                            "text": "you and that's what leads to",
                            "start": 148.319,
                            "duration": 3.801,
                        },
                        {
                            "text": "hallucinations some language models have",
                            "start": 149.959,
                            "duration": 4.761,
                        },
                        {
                            "text": "been integrating web search into their",
                            "start": 152.12,
                            "duration": 4.08,
                        },
                        {
                            "text": "applications you might see this with",
                            "start": 154.72,
                            "duration": 3.92,
                        },
                        {
                            "text": "chat pt4 that it has the ability to",
                            "start": 156.2,
                            "duration": 4.319,
                        },
                        {
                            "text": "access the internet with Bing it's",
                            "start": 158.64,
                            "duration": 3.319,
                        },
                        {
                            "text": "partnered with Microsoft and they're",
                            "start": 160.519,
                            "duration": 3.681,
                        },
                        {
                            "text": "using their Bing search but this is not",
                            "start": 161.959,
                            "duration": 4.2,
                        },
                        {
                            "text": "actually part of the language model this",
                            "start": 164.2,
                            "duration": 3.56,
                        },
                        {
                            "text": "is something they've programmed on top",
                            "start": 166.159,
                            "duration": 4.281,
                        },
                        {
                            "text": "of it which is a step towards agentic",
                            "start": 167.76,
                            "duration": 6.32,
                        },
                        {
                            "text": "Behavior so how do AI agents work AI",
                            "start": 170.44,
                            "duration": 5.84,
                        },
                        {
                            "text": "agents are essentially sophisticated",
                            "start": 174.08,
                            "duration": 4.879,
                        },
                        {
                            "text": "problem solving machines that can plan",
                            "start": 176.28,
                            "duration": 5.28,
                        },
                        {
                            "text": "execute and learn from their actions",
                            "start": 178.959,
                            "duration": 4.681,
                        },
                        {
                            "text": "they are made up of several components",
                            "start": 181.56,
                            "duration": 4.239,
                        },
                        {
                            "text": "in particular the ability to plan the",
                            "start": 183.64,
                            "duration": 4.36,
                        },
                        {
                            "text": "ability to interact with tools the",
                            "start": 185.799,
                            "duration": 4.121,
                        },
                        {
                            "text": "ability to have memory and store",
                            "start": 188.0,
                            "duration": 4.4,
                        },
                        {
                            "text": "knowledge and then lastly the ability to",
                            "start": 189.92,
                            "duration": 4.76,
                        },
                        {
                            "text": "execute actions so let's take a look at",
                            "start": 192.4,
                            "duration": 4.479,
                        },
                        {
                            "text": "each one planning everything starts with",
                            "start": 194.68,
                            "duration": 5.08,
                        },
                        {
                            "text": "a goal when it's researching a market",
                            "start": 196.879,
                            "duration": 5.521,
                        },
                        {
                            "text": "Trend or perhaps drafting an email an",
                            "start": 199.76,
                            "duration": 5.199,
                        },
                        {
                            "text": "agent Begins by defining what needs to",
                            "start": 202.4,
                            "duration": 4.839,
                        },
                        {
                            "text": "be achieved it then creates a detailed",
                            "start": 204.959,
                            "duration": 4.0,
                        },
                        {
                            "text": "plan breaking down the goal into",
                            "start": 207.239,
                            "duration": 4.041,
                        },
                        {
                            "text": "manageable tasks TKS much like the Chain",
                            "start": 208.959,
                            "duration": 3.801,
                        },
                        {
                            "text": "of Thought approach in prompt",
                            "start": 211.28,
                            "duration": 3.28,
                        },
                        {
                            "text": "engineering this means that agents not",
                            "start": 212.76,
                            "duration": 3.92,
                        },
                        {
                            "text": "only knows what to do but also how to",
                            "start": 214.56,
                            "duration": 4.72,
                        },
                        {
                            "text": "approach each task for optimal results",
                            "start": 216.68,
                            "duration": 4.88,
                        },
                        {
                            "text": "ultimately it takes the human training",
                            "start": 219.28,
                            "duration": 4.2,
                        },
                        {
                            "text": "and predefined triggers kind of out of",
                            "start": 221.56,
                            "duration": 3.759,
                        },
                        {
                            "text": "the process and comes up with them on",
                            "start": 223.48,
                            "duration": 4.16,
                        },
                        {
                            "text": "its own secondly interacting with tools",
                            "start": 225.319,
                            "duration": 4.401,
                        },
                        {
                            "text": "unlike basic language models AI agents",
                            "start": 227.64,
                            "duration": 4.48,
                        },
                        {
                            "text": "can interact with a variety of tools",
                            "start": 229.72,
                            "duration": 4.04,
                        },
                        {
                            "text": "this is part of their interacting with",
                            "start": 232.12,
                            "duration": 3.56,
                        },
                        {
                            "text": "the external world around them they can",
                            "start": 233.76,
                            "duration": 4.399,
                        },
                        {
                            "text": "browse the internet access databases and",
                            "start": 235.68,
                            "duration": 4.72,
                        },
                        {
                            "text": "use apis to gather information or",
                            "start": 238.159,
                            "duration": 4.601,
                        },
                        {
                            "text": "perform tasks this integration allows",
                            "start": 240.4,
                            "duration": 4.72,
                        },
                        {
                            "text": "them to extend their capabilities far",
                            "start": 242.76,
                            "duration": 5.0,
                        },
                        {
                            "text": "beyond just being a static data set",
                            "start": 245.12,
                            "duration": 5.56,
                        },
                        {
                            "text": "thirdly they can have memory or access",
                            "start": 247.76,
                            "duration": 5.199,
                        },
                        {
                            "text": "external knowledge agents can also be",
                            "start": 250.68,
                            "duration": 4.52,
                        },
                        {
                            "text": "equipped with specific and specialist",
                            "start": 252.959,
                            "duration": 4.4,
                        },
                        {
                            "text": "knowledge for example your company's",
                            "start": 255.2,
                            "duration": 4.52,
                        },
                        {
                            "text": "data or market research that perhaps is",
                            "start": 257.359,
                            "duration": 4.72,
                        },
                        {
                            "text": "not publicly available they use",
                            "start": 259.72,
                            "duration": 4.72,
                        },
                        {
                            "text": "techniques like retrieval augmented",
                            "start": 262.079,
                            "duration": 5.84,
                        },
                        {
                            "text": "generation I.E rag which is integrating",
                            "start": 264.44,
                            "duration": 5.68,
                        },
                        {
                            "text": "external resources and lever in the",
                            "start": 267.919,
                            "duration": 3.961,
                        },
                        {
                            "text": "ability to go and capture this",
                            "start": 270.12,
                            "duration": 3.68,
                        },
                        {
                            "text": "information and then bring it into the",
                            "start": 271.88,
                            "duration": 4.039,
                        },
                        {
                            "text": "language model's responses effectively",
                            "start": 273.8,
                            "duration": 4.08,
                        },
                        {
                            "text": "it enhances the responses with more",
                            "start": 275.919,
                            "duration": 4.241,
                        },
                        {
                            "text": "upto-date or relevant information for",
                            "start": 277.88,
                            "duration": 4.92,
                        },
                        {
                            "text": "example if you go to a startup's website",
                            "start": 280.16,
                            "duration": 4.68,
                        },
                        {
                            "text": "and type in a question instead of the",
                            "start": 282.8,
                            "duration": 3.8,
                        },
                        {
                            "text": "language model just trying to answer",
                            "start": 284.84,
                            "duration": 3.919,
                        },
                        {
                            "text": "your very specific customer question",
                            "start": 286.6,
                            "duration": 3.8,
                        },
                        {
                            "text": "with what it was trained on in this",
                            "start": 288.759,
                            "duration": 4.321,
                        },
                        {
                            "text": "generic model it's going to go and use",
                            "start": 290.4,
                            "duration": 5.0,
                        },
                        {
                            "text": "retrieval augmented generation to search",
                            "start": 293.08,
                            "duration": 4.8,
                        },
                        {
                            "text": "the database of possible questions and",
                            "start": 295.4,
                            "duration": 4.519,
                        },
                        {
                            "text": "answers from that company's help desk",
                            "start": 297.88,
                            "duration": 4.319,
                        },
                        {
                            "text": "integrate that answer into the llm",
                            "start": 299.919,
                            "duration": 4.241,
                        },
                        {
                            "text": "response for a more upto-date and",
                            "start": 302.199,
                            "duration": 4.921,
                        },
                        {
                            "text": "accurate response and lastly AI agents",
                            "start": 304.16,
                            "duration": 5.84,
                        },
                        {
                            "text": "can execute actions so they can write",
                            "start": 307.12,
                            "duration": 5.48,
                        },
                        {
                            "text": "reports or make emails and even manage",
                            "start": 310.0,
                            "duration": 4.96,
                        },
                        {
                            "text": "other software applications we are also",
                            "start": 312.6,
                            "duration": 4.439,
                        },
                        {
                            "text": "entering in a world where agents can",
                            "start": 314.96,
                            "duration": 4.239,
                        },
                        {
                            "text": "start communicating with other agents",
                            "start": 317.039,
                            "duration": 4.041,
                        },
                        {
                            "text": "who have been specifically trained to",
                            "start": 319.199,
                            "duration": 4.081,
                        },
                        {
                            "text": "perform certain things this autonomous",
                            "start": 321.08,
                            "duration": 4.2,
                        },
                        {
                            "text": "execution is what sets them apart from",
                            "start": 323.28,
                            "duration": 4.12,
                        },
                        {
                            "text": "more passive Technologies and is really",
                            "start": 325.28,
                            "duration": 3.88,
                        },
                        {
                            "text": "where people are thinking wow what can",
                            "start": 327.4,
                            "duration": 4.32,
                        },
                        {
                            "text": "we do where we can automate work to the",
                            "start": 329.16,
                            "duration": 4.92,
                        },
                        {
                            "text": "extent where we just explain what we",
                            "start": 331.72,
                            "duration": 4.68,
                        },
                        {
                            "text": "want to happen and the rest is taken",
                            "start": 334.08,
                            "duration": 5.04,
                        },
                        {
                            "text": "care of now the future of AI does pose",
                            "start": 336.4,
                            "duration": 5.44,
                        },
                        {
                            "text": "some risks now ai agents represent",
                            "start": 339.12,
                            "duration": 4.519,
                        },
                        {
                            "text": "significant advancements in how we",
                            "start": 341.84,
                            "duration": 4.04,
                        },
                        {
                            "text": "interact with technology but they can't",
                            "start": 343.639,
                            "duration": 4.201,
                        },
                        {
                            "text": "act independently the fact that they",
                            "start": 345.88,
                            "duration": 4.52,
                        },
                        {
                            "text": "come up with their own plan of tasks",
                            "start": 347.84,
                            "duration": 4.84,
                        },
                        {
                            "text": "that they must execute and then can act",
                            "start": 350.4,
                            "duration": 4.72,
                        },
                        {
                            "text": "upon those tasks autonomously could pose",
                            "start": 352.68,
                            "duration": 4.519,
                        },
                        {
                            "text": "a threat for example imagine if you",
                            "start": 355.12,
                            "duration": 4.519,
                        },
                        {
                            "text": "asked an AI agent to solve World PE",
                            "start": 357.199,
                            "duration": 5.041,
                        },
                        {
                            "text": "peace and their reasoning was such that",
                            "start": 359.639,
                            "duration": 5.041,
                        },
                        {
                            "text": "world peace was best achieved by killing",
                            "start": 362.24,
                            "duration": 4.16,
                        },
                        {
                            "text": "all humans then maybe they're going to",
                            "start": 364.68,
                            "duration": 4.4,
                        },
                        {
                            "text": "go off and kill all of humanity not the",
                            "start": 366.4,
                            "duration": 4.72,
                        },
                        {
                            "text": "ideal outcome that we would want so",
                            "start": 369.08,
                            "duration": 4.16,
                        },
                        {
                            "text": "there is an element of control and",
                            "start": 371.12,
                            "duration": 3.96,
                        },
                        {
                            "text": "interaction that humans have to maintain",
                            "start": 373.24,
                            "duration": 3.64,
                        },
                        {
                            "text": "over this process to really get good",
                            "start": 375.08,
                            "duration": 3.959,
                        },
                        {
                            "text": "quality results some people think that",
                            "start": 376.88,
                            "duration": 5.28,
                        },
                        {
                            "text": "as models go from GPT 4 to GPT 5 and so",
                            "start": 379.039,
                            "duration": 4.961,
                        },
                        {
                            "text": "on their reasoning capability is going",
                            "start": 382.16,
                            "duration": 4.08,
                        },
                        {
                            "text": "to be far more improved and help the",
                            "start": 384.0,
                            "duration": 4.52,
                        },
                        {
                            "text": "output of AI agents become more higher",
                            "start": 386.24,
                            "duration": 4.239,
                        },
                        {
                            "text": "quality that's it AI agents are",
                            "start": 388.52,
                            "duration": 4.36,
                        },
                        {
                            "text": "different from llms they can plan they",
                            "start": 390.479,
                            "duration": 4.921,
                        },
                        {
                            "text": "can interact with tools store memory and",
                            "start": 392.88,
                            "duration": 4.759,
                        },
                        {
                            "text": "access other knowledge and also execute",
                            "start": 395.4,
                            "duration": 4.519,
                        },
                        {
                            "text": "actions on your behalf so if there's",
                            "start": 397.639,
                            "duration": 3.761,
                        },
                        {
                            "text": "anything else you would like to know",
                            "start": 399.919,
                            "duration": 3.321,
                        },
                        {
                            "text": "just drop a message down in the comments",
                            "start": 401.4,
                            "duration": 3.84,
                        },
                        {
                            "text": "and I would be happy to respond with",
                            "start": 403.24,
                            "duration": 3.519,
                        },
                        {
                            "text": "that thank you very much if you haven't",
                            "start": 405.24,
                            "duration": 3.399,
                        },
                        {
                            "text": "already please subscribe and like this",
                            "start": 406.759,
                            "duration": 6.28,
                        },
                        {
                            "text": "video thanks everyone Chia chiao",
                            "start": 408.639,
                            "duration": 4.4,
                        },
                    ],
                    "status": "success",
                },
            ],
            "errors": [],
            "combined_summary": {
                "summary": "AI agents are essentially advanced software that can perform tasks autonomously, going beyond traditional AI models like large language models (LLMs) that simply respond to prompts. Unlike standard chatbots that generate text based on fixed training data and wait passively for input, AI agents actively reason, plan, and execute actions to achieve given goals. \n\nAt a basic level, LLMs like ChatGPT or Claude excel at generating and editing text based on the input they receive. However, they lack awareness of personal or up-to-date information and can only respond when prompted. For example, if you ask an LLM when your next meeting is, it will fail unless it has access to your calendar data.\n\nTo address this, AI workflows are created by connecting LLMs to external tools or data sources, such as calendars or weather APIs, enabling more dynamic responses. Still, these workflows follow predefined human-programmed sequences of steps or control logic, which limits their flexibility. They dont act independently; a human is needed to adjust and iterate on the process when something doesnt work perfectly.\n\nThe real leap happens with AI agents. These agents are designed to be decision makers themselves—they receive a goal and autonomously figure out the best sequence of actions to take. They can reason about how to approach a task, interact with multiple tools or APIs, remember information, learn from intermediate results, and improve their outputs through iteration without constant human intervention. For example, an AI agent tasked with creating social media posts from news articles can decide how to gather information, summarize content, and even critique and refine its own output automatically.\n\nTechnically, this reasoning-and-acting ability is often built using frameworks like ReAct, which combine reasoning steps with tool usage. AI agents essentially have these four key components: the ability to plan (break down a goal into tasks), interact with tools and external data in real time, store and access memory or specialized knowledge beyond their original training, and execute actions like sending emails or managing software programs.\n\nReal-world demos show AI agents identifying and indexing complex data—for instance, searching through video footage to find clips of a skier autonomously, something a human would have to do manually otherwise. This illustrates how AI agents can save time by automating decision-making and task execution.\n\nWhile AI agents offer powerful benefits and the potential for highly autonomous digital assistants, there are risks. Since agents decide how to achieve goals, if their reasoning or ethical guidelines arent carefully controlled, they might take harmful actions. This means humans still need to oversee and guide AI agent deployment and decision-making to ensure safe and beneficial outcomes.\n\nIn summary, the evolution goes from:\n1. Large Language Models that respond passively to inputs,\n2. AI workflows that follow human-created step-by-step instructions to perform tasks using LLMs plus external tools,\n3. AI agents that independently reason, plan, interact with tools, remember, learn, and iterate to achieve goals autonomously.\n\nThis progression reflects how AI is moving from simple text generation to powerful autonomous problem solving and action-taking, potentially transforming how we work and interact with technology.",
                "mapping": {
                    "AI agents are essentially advanced software that can perform tasks autonomously, going beyond traditional AI models like large language models (LLMs) that simply respond to prompts. Unlike standard chatbots that generate text based on fixed training data and wait passively for input, AI agents actively reason, plan, and execute actions to achieve given goals.": [
                        {
                            "matched_text": "an AI agent is a piece of software designed to perform tasks autonomously unlike traditional software that follows strict rules AI agents make decisions based on their understanding and interactions with the world",
                            "start": 23.119,
                            "duration": 9.041,
                            "video_id": "hLJTcVHW8_I",
                        },
                        {
                            "matched_text": "AI agents are different to llms large language models while agents use models like GPT for understanding and generating language agents can do much more",
                            "start": 96.84,
                            "duration": 11.639,
                            "video_id": "hLJTcVHW8_I",
                        },
                    ],
                    "At a basic level, LLMs like ChatGPT or Claude excel at generating and editing text based on the input they receive. However, they lack awareness of personal or up-to-date information and can only respond when prompted. For example, if you ask an LLM when your next meeting is, it will fail unless it has access to your calendar data.": [
                        {
                            "matched_text": "Popular AI chatbots like CHBT, Google Gemini, and Claude are applications built on top of large language models, LLMs, and they're fantastic at generating and editing text.",
                            "start": 65.84,
                            "duration": 15.92,
                            "video_id": "FwOTs4UxQS4",
                        },
                        {
                            "matched_text": "Chat GPT knows information only up until its last update as of today their last update was December 2023 which was more than 4 months ago the model itself can't fetch or understand new events or data",
                            "start": 121.36,
                            "duration": 18.64,
                            "video_id": "hLJTcVHW8_I",
                        },
                        {
                            "matched_text": "what if I asked Chachi BT when my next coffee chat is? Even without seeing the response, both you and I know Chachi PT is gonna fail because it doesn't know that information. It doesn't have access to my calendar.",
                            "start": 100.64,
                            "duration": 12.72,
                            "video_id": "FwOTs4UxQS4",
                        },
                    ],
                    "To address this, AI workflows are created by connecting LLMs to external tools or data sources, such as calendars or weather APIs, enabling more dynamic responses. Still, these workflows follow predefined human-programmed sequences of steps or control logic, which limits their flexibility. They dont act independently; a human is needed to adjust and iterate on the process when something doesnt work perfectly.": [
                        {
                            "matched_text": "Lets build on our example. What if I, a human, told the LM, 'Every time I ask about a personal event, perform a search query and fetch data from my Google calendar before providing a response.'",
                            "start": 139.2,
                            "duration": 13.839,
                            "video_id": "FwOTs4UxQS4",
                        },
                        {
                            "matched_text": "This is a fundamental trait of AI workflows. They can only follow predefined paths set by humans. And if you want to get technical, this path is also called the control logic.",
                            "start": 182.239,
                            "duration": 10.399,
                            "video_id": "FwOTs4UxQS4",
                        },
                        {
                            "matched_text": "but what if my next follow-up question is, 'What will the weather be like that day?' The LM will now fail at answering the query because the path we told the LM to follow is to always search my Google calendar, which does not have information about the weather.",
                            "start": 165.599,
                            "duration": 21.601,
                            "video_id": "FwOTs4UxQS4",
                        },
                        {
                            "matched_text": "step one, you do this. Step two, you do this. Step three, you do this. And finally, remember to run daily at 8 am. One last thing, if I test this workflow and I don't like the final output of the LinkedIn post ... I'd have to manually go back and rewrite the prompt for Claude ... this trial and error iteration is currently being done by me, a human.",
                            "start": 286.96,
                            "duration": 52.08,
                            "video_id": "FwOTs4UxQS4",
                        },
                    ],
                    "The real leap happens with AI agents. These agents are designed to be decision makers themselves—they receive a goal and autonomously figure out the best sequence of actions to take. They can reason about how to approach a task, interact with multiple tools or APIs, remember information, learn from intermediate results, and improve their outputs through iteration without constant human intervention. For example, an AI agent tasked with creating social media posts from news articles can decide how to gather information, summarize content, and even critique and refine its own output automatically.": [
                        {
                            "matched_text": "The one massive change that has to happen in order for this AI workflow to become an AI agent is for me, the human decision maker, to be replaced by an LLM. In other words, the AI agent must reason... The AI agent must act, aka do things via tools.",
                            "start": 360.24,
                            "duration": 40.48,
                            "video_id": "FwOTs4UxQS4",
                        },
                        {
                            "matched_text": "With the goal of creating social media posts based off of news articles, I need to do two things. First, reason or think about the best approach. I need to first compile the news articles, then summarize them, then write the final posts. Second, take action using tools.",
                            "start": 336.0,
                            "duration": 29.199,
                            "video_id": "FwOTs4UxQS4",
                        },
                        {
                            "matched_text": "An AI agent will be able to do the same thing autonomously. In our example, the AI agent would autonomously add in another LM to critique its own output.",
                            "start": 423.919,
                            "duration": 35.76,
                            "video_id": "FwOTs4UxQS4",
                        },
                    ],
                    "Technically, this reasoning-and-acting ability is often built using frameworks like ReAct, which combine reasoning steps with tool usage. AI agents essentially have these four key components: the ability to plan (break down a goal into tasks), interact with tools and external data in real time, store and access memory or specialized knowledge beyond their original training, and execute actions like sending emails or managing software programs.": [
                        {
                            "matched_text": "the most common configuration for AI agents is the react framework. All AI agents must reason and act. So react. Sounds simple once we break it down, right?",
                            "start": 409.759,
                            "duration": 19.6,
                            "video_id": "FwOTs4UxQS4",
                        },
                        {
                            "matched_text": "AI agents are essentially sophisticated problem solving machines that can plan execute and learn from their actions they are made up of several components in particular the ability to plan the ability to interact with tools the ability to have memory and store knowledge and then lastly the ability to execute actions",
                            "start": 174.08,
                            "duration": 27.039,
                            "video_id": "hLJTcVHW8_I",
                        },
                    ],
                    "Real-world demos show AI agents identifying and indexing complex data—for instance, searching through video footage to find clips of a skier autonomously, something a human would have to do manually otherwise. This illustrates how AI agents can save time by automating decision-making and task execution.": [
                        {
                            "matched_text": "Andrew is a preeeminent figure in AI and he created this demo website that illustrates how an AI agent works. ... when I search for a keyword like skier, enter the AI vision agent in the background is first reasoning what a skier looks like ... and then its acting by looking at clips in video footage, trying to identify what it thinks a skier is, indexing that clip, and then returning that clip to us.",
                            "start": 470.08,
                            "duration": 54.959,
                            "video_id": "FwOTs4UxQS4",
                        },
                        {
                            "matched_text": "An AI agent did all that instead of a human reviewing the footage beforehand, manually identifying the skier, and adding tags like skier, mountain, ski, snow.",
                            "start": 512.399,
                            "duration": 17.28,
                            "video_id": "FwOTs4UxQS4",
                        },
                    ],
                    "While AI agents offer powerful benefits and the potential for highly autonomous digital assistants, there are risks. Since agents decide how to achieve goals, if their reasoning or ethical guidelines arent carefully controlled, they might take harmful actions. This means humans still need to oversee and guide AI agent deployment and decision-making to ensure safe and beneficial outcomes.": [
                        {
                            "matched_text": "The fact that they come up with their own plan of tasks that they must execute and then can act upon those tasks autonomously could pose a threat for example imagine if you asked an AI agent to solve World PE peace and their reasoning was such that world peace was best achieved by killing all humans then maybe they're going to go off and kill all of humanity not the ideal outcome that we would want so there is an element of control and interaction that humans have to maintain over this process to really get good quality results",
                            "start": 345.88,
                            "duration": 40.04,
                            "video_id": "hLJTcVHW8_I",
                        }
                    ],
                    "In summary, the evolution goes from:\n1. Large Language Models that respond passively to inputs,\n2. AI workflows that follow human-created step-by-step instructions to perform tasks using LLMs plus external tools,\n3. AI agents that independently reason, plan, interact with tools, remember, learn, and iterate to achieve goals autonomously.": [
                        {
                            "matched_text": "a simplified visualization of the three levels we covered today. Level one, we provide an input and the LM responds with an output. Easy. Level two, for AI workflows, we provide an input and tell the LM to follow a predefined path that may involve in retrieving information from external tools. The key trait here is that the human programs a path for LM to follow. Level three, the AI agent receives a goal and the LM performs reasoning to determine how best to achieve the goal, takes action using tools to produce an interim result, observes that interim result, and decides whether iterations are required, and produces a final output that achieves the initial goal. The key trait here is that the LLM is a decision maker in the workflow.",
                            "start": 551.279,
                            "duration": 50.161,
                            "video_id": "FwOTs4UxQS4",
                        }
                    ],
                    "This progression reflects how AI is moving from simple text generation to powerful autonomous problem solving and action-taking, potentially transforming how we work and interact with technology.": [
                        {
                            "matched_text": "AI agents are different from llms they can plan they can interact with tools store memory and access other knowledge and also execute actions on your behalf",
                            "start": 390.479,
                            "duration": 9.44,
                            "video_id": "hLJTcVHW8_I",
                        }
                    ],
                },
            },
        }

        return mock_transcript
