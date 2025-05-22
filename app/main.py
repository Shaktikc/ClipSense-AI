from fastapi import FastAPI
from app.api.transcript_routes import router as transcript_router
from app.api.mergedVideo_routes import router as merged_video_router
from app.api.video_summerizer_routes import router as video_summerizer_router

app = FastAPI()
app.include_router(transcript_router)
app.include_router(merged_video_router)
app.include_router(video_summerizer_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

    print("niceeeeee Server started at http://")
