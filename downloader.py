import aiohttp
import aiofiles
import os
from config import config
from utils import ensure_storage

async def download_file(url: str) -> str:
    ensure_storage()
    filename = url.split("/")[-1]
    path = os.path.join(config.STORAGE_PATH, filename)

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                raise Exception("Failed to download file")

            async with aiofiles.open(path, "wb") as f:
                await f.write(await resp.read())

    return path
