import logging
import openai
from aiogram import Bot, Dispatcher, types
from aiohttp import web

# Tokenlar
TOKEN = "7429016817:AAF0dXmeSXozvNmeRJQtac8gmJcW0nMz7a4"
OPENAI_API_KEY = "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"

# Sozlamalar
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
openai.api_key = OPENAI_API_KEY

# /start komandasi
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Salom! Men sun'iy intellekt botman. Savol bering.")

# Oddiy savolga GPT orqali javob
@dp.message_handler()
async def chatgpt(message: types.Message):
    try:
        javob = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message.text}]
        )
        await message.reply(javob.choices[0].message.content)
    except Exception as e:
        await message.reply("Xatolik yuz berdi: " + str(e))

# Web server (Render uchun)
async def on_startup(app):
    from aiogram import executor
    executor.start_polling(dp)

app = web.Application()
app.on_startup.append(on_startup)

if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=10000)
