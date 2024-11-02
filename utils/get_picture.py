import aiohttp
import asyncio
from config.config import BOT_TOKEN


async def get_picture( file_id: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                file_info = await response.json()
        if file_info["ok"]:
            file_path = file_info["result"]["file_path"]
            download_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
            return download_url
    except Exception as e:
        await asyncio.sleep(3)
