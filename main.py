import logging
import openai
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# Tokenlar
TOKEN = "YOUR_TELEGRAM_TOKEN"
OPENAI_API_KEY = "YOUR_OPENAI_KEY"

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

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)qn62
