# 🤖 Telegram GPT Bot (Powered by DeepSeek + OpenRouter)

This is a Python-based Telegram bot that uses the [DeepSeek-R1-Zero](https://huggingface.co/deepseek-ai/deepseek-coder) model via [OpenRouter.ai](https://openrouter.ai/) for generating intelligent responses. Built using the `aiogram` framework.

---

## 🚀 Features

- Responds to user input using DeepSeek via OpenRouter
- Supports `/start`, `/help`, `/clear` commands
- Remembers context during a session
- Strips LaTeX-style formatting automatically from responses
- Lightweight, fast, and easy to deploy

---

## 🛠 Tech Stack

- Python 3.10+
- [Aiogram](https://docs.aiogram.dev/en/latest/) (async Telegram framework)
- OpenRouter API (wrapper for LLMs like DeepSeek)
- `httpx` for async HTTP requests
- `.env` for secure API key handling

---

## 🧪 Setup & Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/himadribh07/Telebot.git
cd telegram-gpt-bot
