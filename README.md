# 🎬ClipSense AI

**YouTube VidExtract AI** is an AI-powered tool that extracts and merges only the *relevant* video segments from YouTube based on the user’s request.  
Simply paste YouTube links and describe what information you need — the AI handles the rest.

---

## 🚀 Features

- 🧠 **AI-Driven Understanding:** Uses advanced LLMs (Mistral, GPT-4.1) to understand your query and locate the most relevant video segments.  
- 🎞️ **Smart Video Extraction:** Automatically identifies timestamps from transcriptions and extracts only the necessary portions.  
- ⚙️ **Fast Processing:** Built with **FastAPI** for efficient backend operations.  
- 🎬 **Video Merging:** Uses **FFmpeg** to seamlessly merge all selected clips into one concise, meaningful video.  
- 💡 **Customizable:** Specify topics, keywords, or time ranges for better precision.

---

## 🧩 Tech Stack

- **Backend:** FastAPI  
- **AI Models:** Mistral, GPT-4.1  
- **Video Processing:** FFmpeg  
- **Transcription & Analysis:** YouTube transcript extraction + LLM semantic search  

---

## 🖥️ How It Works

1. **Paste YouTube Link(s)** — Provide one or more video URLs.  
2. **Specify What You Need** — Example: “Show me the part where the speaker explains reinforcement learning.”  
3. **AI Processing** — The system uses LLMs to understand your request and locate relevant timestamps from transcriptions.  
4. **Video Extraction** — FFmpeg extracts and merges the clips.  
5. **Output** — Get a concise video containing *only* the requested content.

---

## ⚡ Example Use Case

> “Extract all parts explaining the concept of transformers from this YouTube lecture series.”

VidExtract AI will:
- Analyze the transcripts of all videos.
- Detect where “transformers” are discussed.
- Extract those clips.
- Merge them into a single summarized video.

---

## 🏗️ Setup & Installation

```bash
# Clone the repository

# Create virtual environment
python -m venv venv
source venv/bin/activate  # (Windows: venv\Scripts\activate)

# Install dependencies
pip install -r requirements.txt

# Run FastAPI server
uvicorn main:app --reload
