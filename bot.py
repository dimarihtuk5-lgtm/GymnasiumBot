```python
import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = os.environ["BOT_TOKEN"]

ADMIN_IDS = [
    1359403890,
]

keyboard = ReplyKeyboardMarkup(
    [["💌 Надіслати повідомлення"]],
    resize_keyboard=True
)


class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running!")

    def log_message(self, format, *args):
        pass


def start_web_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    server.serve_forever()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привіт!\n\n"
        "Це анонімна скринька Гімназії №2 💙💛\n\n"
        "Тут ти можеш залишити ідею, пропозицію, "
        "побажання, скаргу або зауваження.",
        reply_markup=keyboard
    )


async def wish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["waiting_for_wish"] = True

    await update.message.reply_text(
        "💌 Напиши своє повідомлення.\n\n"
        "Ідея, пропозиція, побажання, скарга чи зауваження — "
        "усе можна надіслати анонімно."
    )


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("waiting_for_wish"):
        return

    text = update.message.text

    for admin_id in ADMIN_IDS:
        await context.bot.send_message(
            chat_id=admin_id,
            text=f"💌 НОВЕ АНОНІМНЕ ПОВІДОМЛЕННЯ\n\n{text}"
        )

    context.user_data["waiting_for_wish"] = False

    await update.message.reply_text(
        "✅ Повідомлення отримано!\n"
        "Дякуємо за твою думку 💙💛",
        reply_markup=keyboard
    )


def main():
    threading.Thread(
        target=start_web_server,
        daemon=True
    ).start()

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(
        MessageHandler(
            filters.Regex("^💌 Надіслати повідомлення$"),
            wish
        )
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            message_handler
        )
    )

    print("Бот запущений!")

    app.run_polling()


if __name__ == "__main__":
    main()
```

