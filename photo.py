from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "7775436060:AAHeA8MFQWzCfs7Jh3r8zHH9rRYMxQjTO-A"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # توضیحات خوش‌آمدگویی
    description = (
        "📢 **خوش آمدید!**\n\n"
        "به ربات ما خوش آمدید! اینجا می‌توانید از امکانات مختلف استفاده کنید.\n"
        "لطفاً گزینه‌های زیر را بررسی کنید:"
    )
    # مسیر تصویر خوش‌آمدگویی
    photo_path = "start-bot.png"

    keyboard = [
        [InlineKeyboardButton("📥 دانلود ویدیو", callback_data="download_video")],
        [InlineKeyboardButton("ℹ️ درباره ما", url="https://example.com")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # ارسال پیام خوش‌آمدگویی شبیه پست
    if update.message:
        await context.bot.send_photo(
            chat_id=update.message.chat_id,
            photo=open(photo_path, "rb"),
            caption=description,
            parse_mode="Markdown",
            reply_markup=reply_markup,
        )
async def post_init(application) -> None:
    # تنظیم دستورات ربات
    await application.bot.set_my_commands([
        ('start', 'Starts the bot'),
        ('help', 'Show some help')
    ])
    # تنظیم دکمه منوی چت (اختیاری)
    await application.bot.set_chat_menu_button()

def main() -> None:
    application = ApplicationBuilder().token(TOKEN).post_init(post_init).build()
    application.add_handler(CommandHandler('start', start))
    # اجرای polling به صورت مستقیم
    application.run_polling()

if __name__ == '__main__':
    main()
