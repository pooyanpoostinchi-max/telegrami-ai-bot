from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import requests
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "meta-llama/llama-3.1-8b-instruct",
            "messages": [
                {
                    "role": "system",
                    "content": "تو یک دستیار فارسی هستی و همیشه فارسی جواب میدهی."
                },
                {
                    "role": "user",
                    "content": text
                }
            ]
        }
    )

    data = response.json()
    answer = data["choices"][0]["message"]["content"]

    await update.message.reply_text(answer)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT, handle))
app.run_polling()
