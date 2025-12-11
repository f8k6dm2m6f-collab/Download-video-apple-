from fastapi import FastAPI, UploadFile, File
from downloader import download_file
from compressor import compress_video
from audio import extract_audio, normalize_audio
from db import is_downloaded, add_download
from utils import ensure_storage
import os
from config import config
from queue_worker import queue, start_worker
import asyncio

app = FastAPI()

@app.on_event("startup")
async def startup():
    ensure_storage()
    await start_worker()

@app.post("/download")
async def download(url: str):
    if is_downloaded(url):
        return {"status": "duplicate", "message": "Already downloaded"}

    path = await download_file(url)
    add_download(url)
    return {"status": "ok", "path": path}

@app.post("/compress")
async def compress(file: UploadFile = File(...)):
    path = os.path.join(config.STORAGE_PATH, file.filename)

    with open(path, "wb") as f:
        f.write(await file.read())

    out = path.replace(".mp4", "_compressed.mp4")
    await queue.put({"type": "compress", "src": path, "out": out})

    return {"status": "queued", "output": out}

@app.post("/audio")
async def audio(file: UploadFile = File(...)):
    path = os.path.join(config.STORAGE_PATH, file.filename)

    with open(path, "wb") as f:
        f.write(await file.read())

    out = path.replace(".mp4", ".mp3")
    await queue.put({"type": "audio", "src": path, "out": out})

    return {"status": "queued", "output": out}

@app.post("/normalize")
async def normalize(file: UploadFile = File(...)):
    path = os.path.join(config.STORAGE_PATH, file.filename)

    with open(path, "wb") as f:
        f.write(await file.read())

    out = path.replace(".mp3", "_norm.mp3")
    await queue.put({"type": "normalize", "src": path, "out": out})

    return {"status": "queued", "output": out}
