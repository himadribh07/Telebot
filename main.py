import os
import re
import httpx
import openai
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import Command
from aiogram.utils import executor
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Constants
MODEL_NAME = "deepseek/deepseek-r1-zero:free"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Initialize bot
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dispatcher = Dispatcher(bot)

# Reference object to hold conversation context
class Reference:
    def __init__(self):
        self.response = ""

reference = Reference()

def clear_past():
    """Clear previous session data."""
    reference.response = ""

# Start command handler
@dispatcher.message_handler(Command("start"))
async def command_start_handler(message: types.Message):
    await message.reply("👋 Hello!\nI'm Tele bot, created by Immortal Dragon!\nHow can I assist you today?")

# Clear command handler
@dispatcher.message_handler(Command("clear"))
async def cmd_clear(message: types.Message):
    clear_past()
    await message.reply("✅ Your previous session data has been cleared.")

# Help command handler
@dispatcher.message_handler(Command("help"))
async def help_command(message: types.Message):
    help_text = (
        "📘 *Bot Commands*\n\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/clear - Clear previous conversation\n"
        "Just send any message and I'll respond!"
    )
    await message.reply(help_text, parse_mode="Markdown")

# Chat handler using OpenRouter DeepSeek model
@dispatcher.message_handler()
async def chatgpt(message: types.Message):
    user_input = message.text.strip()
    print("User Input:", user_input)  # DEBUG

    if not user_input:
        await message.reply("⚠️ Please enter a valid message.")
        return

    headers = {
        "Authorization": f"Bearer {openai.api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful and friendly assistant. Respond in plain language. Avoid LaTeX or special formatting unless asked."
            },
            {
                "role": "user",
                "content": user_input
            }
        ]
    }

    try:
        print("Sending request to OpenRouter...")  # DEBUG
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(API_URL, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            print("API Response:", data)  # DEBUG

            if "choices" not in data or not data["choices"]:
                await message.reply("⚠️ No response received from the model.")
                return

            if "message" not in data["choices"][0] or "content" not in data["choices"][0]["message"]:
                await message.reply("⚠️ Message text is empty or improperly formatted.")
                return

            reply = data["choices"][0]["message"]["content"]

            # Clean LaTeX formatting properly
            clean_reply = re.sub(r"\\[a-zA-Z]+\{(.*?)\}", r"\1", reply)
            clean_reply = re.sub(r"[{}\\]", "", clean_reply)

            await message.reply(clean_reply.strip())


    except httpx.HTTPStatusError as e:
        print("HTTP error:", e.response.text)  # DEBUG
        await message.reply(f"❌ API error: {e.response.status_code}")
    except Exception as e:
        print("Unhandled error:", e)  # DEBUG
        await message.reply(f"⚠️ Unexpected error: {str(e)}")

# Start polling
if __name__ == "__main__":
    executor.start_polling(dispatcher, skip_updates=True)
