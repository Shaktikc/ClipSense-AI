from fastapi import APIRouter, UploadFile, File, Form
from app.services.mergedVideo_service import preview_intro_clip
import tempfile
import shutil

router = APIRouter()


@router.post("/preview-intro/")
async def preview_intro(
    video_file: UploadFile = File(...),
    start: int = Form(1),
    end: int = Form(11),
    fps: int = Form(20),
):
    """
    Endpoint to preview an intro clip from a video file upload.
    """
    try:
        # Save the uploaded file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
            shutil.copyfileobj(video_file.file, tmp)
            tmp_path = tmp.name

        preview_intro_clip(tmp_path, start, end, fps)
        return {"message": "Preview played successfully."}
    except Exception as e:
        return {"error": str(e)}
