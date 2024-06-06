import asyncio
import base64
import os

import aiohttp
import requests
from aiogram import Bot, Dispatcher, F, Router, types
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()

router: Router = Router()
FASTAPI_URL = "http://main:8000/graph_agent"
FASTAPI_URL_2 = "http://main:8000/intent"

PROD_URL = "http://main:8000/api/v1/query"
VOICE_URL = "http://main:8000/api/v1/query/voice"
UPLOAD_URL = "http://main:8000/voice/sber"

headers = {
    "X-Api-Key": "568eD25b494fA9147416DfCd9Bbe71dFdC38F1c555F4c8b925f8c68C9EC17d5b",
    "Content-Type": "application/json",
}


@router.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Тестовый режим")


@router.message(F.content_type == "voice")
async def process_voice_message(message: Message, bot: Bot):
    print("====================================================")
    print("Получено голосовое сообщение!")
    print("====================================================")
    voice_file_info = await bot.get_file(message.voice.file_id)
    form_data = aiohttp.FormData()
    audio = (await bot.download_file(file_path=voice_file_info.file_path)).read()
    form_data.add_field("data", audio, content_type="audio/ogg")
    form_data.add_field("ext_id", str(message.from_user.id))
    headers = {
        "X-Api-Key": "568eD25b494fA9147416DfCd9Bbe71dFdC38F1c555F4c8b925f8c68C9EC17d5b",
        # 'Content-Type': 'application/json'
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(
            VOICE_URL, headers=headers, data=form_data, ssl=False
        ) as response:
            response = await response.json()
            await message.answer(response)


"""
    try:
        response = requests.post(
            FASTAPI_URL_2, 
            headers, 
            json={
                "user_hash": str(message.from_user.id),
                "content": voice_file_info.file_path,
                "content_type": "voice",
            },
        )
        response = response.json()
        if response["content_type"] == "text":
            await message.answer(response["content"])
        elif response["content_type"] == "voice":
            voice_bytes = base64.b64decode(response["content"])
            await bot.send_voice(
                message.chat.id,
                types.input_file.BufferedInputFile(voice_bytes, "output.ogg"),
            )
    except Exception as ex:
        print(ex)
        await message.answer("Что-то пошло не так :(")
"""


@router.message(F.content_type == "text")
async def process_message(message: Message):
    print("====================================================")
    print("Получено текстовое сообщение!")
    print("====================================================")
    user_id = message.from_user.id
    async with aiohttp.ClientSession() as session:
        async with session.post(
            PROD_URL,
            headers=headers,
            json={
                "ext_id": user_id,
                "query": message.text,
                # "content_type": "text",
            },
            ssl=False,
        ) as response:
            response = await response.json()
            await message.answer(response)


async def main():
    bot: Bot = Bot(token=os.getenv("BOT_TOKEN"), parse_mode="Markdown")
    dp: Dispatcher = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
