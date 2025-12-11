import aiohttp
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
import asyncio
import os

API_URL = "http://localhost:8080"   # URL твого FastAPI
BOT_TOKEN = "ВАШ_TELEGRAM_TOKEN"    # 8511917457:AAGPaOBZPcdGVB2GA4w_MgbEbJ29tIEOqME

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# -------------------------------
# 1. Прийом URL
# -------------------------------
@dp.message(F.text)
async def handle_url(msg: Message):
    url = msg.text.strip()

    if not url.startswith("http"):
        return await msg.answer("Надішли файл або URL.")

    await msg.answer("⏳ Завантажую...")

    async with aiohttp.ClientSession() as session:
        async with session.post(f"{API_URL}/download", params={"url": url}) as resp:
            data = await resp.json()

    if data.get("status") == "duplicate":
        return await msg.answer("⚠️ Це вже скачано раніше.")

    if data.get("status") != "ok":
        return await msg.answer("❌ Помилка завантаження.")

    await msg.answer(f"Файл завантажено!\nШлях: `{data['path']}`")


# -------------------------------
# 2. Прийом відео-файлів
# -------------------------------
@dp.message(F.video)
async def handle_video(msg: Message):
    await msg.answer("⏳ Обробляю...")

    file_id = msg.video.file_id
    file = await bot.get_file(file_id)
    file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file.file_path}"

    # Завантажуємо через FastAPI downloader
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{API_URL}/download", params={"url": file_url}) as resp:
            await resp.json()

    await msg.answer("🎥 Відео отримано! Хочеш:\n/compress\n/audio\n/normalize ?")


# -------------------------------
# 3. Команда /compress
# -------------------------------
@dp.message(F.text == "/compress")
async def compress_cmd(msg: Message):
    await msg.answer("📦 Надішли відео-файл для компресії.")


@dp.message(F.video, F.reply_to_message.text == "/compress")
async def compress_handler(msg: Message):
    await msg.answer("⚙️ Компресую...")

    file_id = msg.video.file_id
    file = await bot.get_file(file_id)
    file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file.file_path}"

    async with aiohttp.ClientSession() as session:
        async with session.post(f"{API_URL}/compress", data={"url": file_url}) as resp:
            data = await resp.json()

    await msg.answer(f"✔️ У черзі.\nФайл буде створено: `{data['output']}`")


# -------------------------------
# 4. Старт бота
# -------------------------------
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
