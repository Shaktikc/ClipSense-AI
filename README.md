YouTube VidExtract AI

Turn long YouTube videos into short, content-only clips.
Paste a YouTube link, describe what you need, and the app finds the relevant segments, cuts them with FFmpeg, merges them, and returns a concise video focused on your request.

Tech stack: FastAPI • LLMs (Mistral, GPT-4.1) • FFmpeg

✨ Features

Natural-language search: “Show only the parts where the speaker explains transformers with code.”

Auto segmenting: LLMs scan the transcript and locate the timecodes.

Precise clipping: FFmpeg extracts the exact ranges and merges in order.

Two modes:

Auto: LLM finds segments from your prompt

Manual: you provide explicit time ranges

JSON job API: fire-and-forget with progress polling.
