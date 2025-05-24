import logging 
from aiogram import Bot, Dispatcher, types , executor
from aiogram.dispatcher.filters import Command
from dotenv import load_dotenv
import os

load_dotenv()
API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
# print(API_TOKEN)


logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(Command(['start','help']))
async def command_start_handler(message: types.Message):
    """
    This handler receives messages with `/start` command
    """
    await message.reply(f"Hello, I am Echo bot!")

if __name__ == "__main__":
    executor.start_polling(dp,skip_updates=True)