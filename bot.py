import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = os.environ["BOT_TOKEN"]
ADMIN_ID = 1359403890

keyboard = ReplyKeyboardMarkup(
    [["💌 Надіслати побажання"]],
    resize_keyboard=True
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привіт!\n\n"
        "Це анонімна «Скринька побажань» Гімназії №2 💙💛\n\n"
        "Тут ти можеш залишити побажання, пропозицію або ідею.",
        reply_markup=keyboard
    )


async def wish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["waiting_for_wish"] = True

    await update.message.reply_text(
        "💌 Напиши своє побажання або пропозицію.\n\n"
        "Повідомлення буде надіслано анонімно."
    )


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("waiting_for_wish"):
        return

    text = update.message.text

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"💌 НОВЕ АНОНІМНЕ ПОБАЖАННЯ\n\n{text}"
    )

    context.user_data["waiting_for_wish"] = False

    await update.message.reply_text(
        "✅ Дякуємо!\n"
        "Твоє побажання отримано анонімно 💙💛",
        reply_markup=keyboard
    )


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(
        MessageHandler(
            filters.Regex("^💌 Надіслати побажання$"),
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
