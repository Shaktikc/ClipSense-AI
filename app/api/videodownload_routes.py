from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel, HttpUrl
from typing import Optional, List, Dict
import os
import asyncio
from concurrent.futures import ThreadPoolExecutor

from ..services.downloadVideo_service import download_youtube_video, extract_video_id

# Create router instance
router = APIRouter()


class BatchVideoDownloadRequest(BaseModel):
    urls: List[str]
    output_path: Optional[str] = None


@router.post("/batch-download-videos")
async def batch_download_videos(request: BatchVideoDownloadRequest):
    """
    API endpoint to download multiple YouTube videos concurrently.
    
    Args:
        request (BatchVideoDownloadRequest): Contains list of URLs and optional output path
        
    Returns:
        JSONResponse: Contains the status of each video download
    """
    try:
        # If output_path is not provided, use a default directory
        output_path = request.output_path or os.path.join(os.getcwd(), "downloads")
        
        # Create output directory if it doesn't exist
        os.makedirs(output_path, exist_ok=True)
        
        # Create tasks for each video download
        tasks = []
        for url in request.urls:
            task = asyncio.create_task(download_single_video(url, output_path))
            tasks.append(task)
        
        # Wait for all downloads to complete
        results = await asyncio.gather(*tasks)
        
        # Count successful and failed downloads
        successful = sum(1 for result in results if result["status"] == "success")
        failed = len(results) - successful
          # Extract successful video IDs
        successful_video_ids = [
            result["video_id"] 
            for result in results 
            if result["status"] == "success" and result["video_id"] is not None
        ]
        
        return JSONResponse(
            content={
                "status": "completed",
                "message": f"Completed batch download: {successful} successful, {failed} failed",
                "video_ids": successful_video_ids,  # List of successfully downloaded video IDs
                "results": results  # Detailed results including video IDs for each attempt
            },
            status_code=200
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Batch download failed: {str(e)}"
        )
    


    
async def download_single_video(url: str, output_path: str) -> Dict:
    """
    Helper function to download a single video and return its status
    """
    try:
        video_id = extract_video_id(url)
        video_path = download_youtube_video(url=url, output_path=output_path)
        return {
            "url": url,
            "video_id": video_id,
            "status": "success",
            "video_path": video_path,
            "error": None
        }
    except Exception as e:
        video_id = None
        try:
            video_id = extract_video_id(url)
        except:
            pass
        return {
            "url": url,
            "video_id": video_id,
            "status": "failed",
            "video_path": None,
            "error": str(e)
        }
