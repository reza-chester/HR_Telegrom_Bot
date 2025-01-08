from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# تعریف دستور /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "سلام! به بات تلگرام من خوش آمدید. 🌟\n"
        "برای دریافت اطلاعات بیشتر می‌توانید دستور /help را وارد کنید."
    )

# تعریف دستور /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("همینی که هست! 😉")

# اجرای برنامه
if __name__ == "__main__":
    TOKEN = "7775436060:AAEiPn2RqBbOBTtWjRIj8WJST7xlwxxcB5Q"

    # ساخت اپلیکیشن بات
    app = ApplicationBuilder().token(TOKEN).build()

    # افزودن هندلرها
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    print("robot is running..")
    app.run_polling()
