import logging
import openai
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# Tokenlar
TOKEN = "7429016817:AAGCXxVj3J4y98mExl5CRQ9l_dOYRBY3TbI"
OPENAI_API_KEY = "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"

# Sozlamalar
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
openai.api_key = OPENAI_API_KEY

# /start komandasi
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Salom! Men ChatGPT botman. Savolingiz bo'lsa bering.")

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
    executor.start_polling(dp, skip_updates=True)
