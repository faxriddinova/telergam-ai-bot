import logging
import os
import openai

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
from dotenv import load_dotenv

# .env fayldan o'zgaruvchilarni yuklab olamiz
load_dotenv()

# Tokenlarni olish
BOT_TOKEN = os.getenv("7429016817:AAFehue5ne9fVTfHiQt7f96aeltUCdtQ-vg")        # <-- BU YERNI TO‘LDIRISHING KERAK
OPENAI_API_KEY = os.getenv("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")  # <-- BU YERNI TO‘LDIRISHING KERAK

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is missing!")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is missing!")

# OpenAI API kalitini sozlash
openai.api_key = OPENAI_API_KEY

# Botni sozlash
logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Har qanday xabarni ChatGPT orqali qaytarish
@dp.message_handler()
async def handle_message(message: types.Message):
    user_input = message.text
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}]
        )
        reply = response['choices'][0]['message']['content']
        await message.answer(reply)
    except Exception as e:
        await message.answer("Xatolik yuz berdi: " + str(e))

# Botni ishga tushirish
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
