import asyncio
from compressor import compress_video
from audio import extract_audio, normalize_audio

queue = asyncio.Queue()

async def worker():
    while True:
        task = await queue.get()
        type_ = task["type"]
        src = task["src"]
        out = task["out"]

        if type_ == "compress":
            compress_video(src, out)
        elif type_ == "audio":
            extract_audio(src, out)
        elif type_ == "normalize":
            normalize_audio(src, out)

        queue.task_done()

async def start_worker():
    asyncio.create_task(worker())
import asyncio
from compressor import compress_video
from audio import extract_audio, normalize_audio

queue = asyncio.Queue()

async def worker():
    while True:
        task = await queue.get()
        type_ = task["type"]
        src = task["src"]
        out = task["out"]

        if type_ == "compress":
            compress_video(src, out)
        elif type_ == "audio":
            extract_audio(src, out)
        elif type_ == "normalize":
            normalize_audio(src, out)

        queue.task_done()

async def start_worker():
    asyncio.create_task(worker())
