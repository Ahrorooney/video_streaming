from pathlib import Path
from fastapi import FastAPI
from fastapi import Request, Response
from fastapi import Header
from fastapi.templating import Jinja2Templates
import asyncpg


app = FastAPI()
templates = Jinja2Templates(directory="templates")
CHUNK_SIZE = 1024*1024
video_path_1920 = Path("video_1920.mp4")
video_path_1280 = Path("video_1280.mp4")
video_path_640 = Path("video_640.mp4")
video_path_320 = Path("video_320.mp4")


@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.htm", context={"request": request})


@app.get("/video/{quality}")
async def video_endpoint(quality, range: str = Header(None)):
    start, end = range.replace("bytes=", "").split("-")
    start = int(start)
    end = int(end) if end else start + CHUNK_SIZE
    if quality == "1920":
        video_path = video_path_1920
    elif quality == "1280":
        video_path = video_path_1280
    elif quality == "640":
        video_path = video_path_640
    elif quality == "320":
        video_path = video_path_320
    else:
        video_path = video_path_1920
    with open(video_path, "rb") as video:
        video.seek(start)
        data = video.read(end - start)
        filesize = str(video_path.stat().st_size)
        headers = {
            'Content-Length': str(len(data)),
            'Content-Range': f'bytes {str(start)}-{str(end)}/{filesize}',
            'Accept-Ranges': 'bytes'
        }
        return Response(data, status_code=206, headers=headers, media_type="video/mp4")

