import os
import logging
import openai
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils.executor import start_webhook
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("7429016817:AAFehue5ne9fVTfHiQt7f96aeltUCdtQ-vg")
OPENAI_API_KEY = os.getenv("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")

WEBHOOK_HOST = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}"
WEBHOOK_PATH = f"/webhook"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = int(os.environ.get("PORT", 8000))

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())
openai.api_key = OPENAI_API_KEY

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Salom! Men ChatGPT asosidagi Telegram botman.\n\n"
                        "Men quyidagilarni qila olaman:\n"
                        "- Matnga javob berish\n"
                        "- Rasm yaratish (DALL·E)\n"
                        "- Internetdan ma'lumot topish\n\n"
                        "Yozing, men yordam beraman!")

@dp.message_handler(lambda message: message.text.startswith("/image "))
async def generate_image(message: types.Message):
    prompt = message.text[7:]
    await message.reply("Rasm yaratilmoqda, iltimos kuting...")
    try:
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="512x512"
        )
        image_url = response['data'][0]['url']
        await message.reply_photo(image_url)
    except Exception as e:
        await message.reply(f"Xatolik yuz berdi:\n{e}")

@dp.message_handler()
async def chatgpt_reply(message: types.Message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": message.text}
            ]
        )
        reply = response['choices'][0]['message']['content']
        await message.reply(reply)
    except Exception as e:
        await message.reply(f"Xatolik yuz berdi:\n{e}")

async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown(dp):
    await bot.delete_webhook()

if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
