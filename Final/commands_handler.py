from telegram import Update
from telegram.ext import  ContextTypes
from telegram.constants import  ParseMode

async def start_commands(context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()

async def request(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await start_commands()
    await update.message.reply_text(text="نام کاربری* (windows username)* خود را وارد نمایید",parse_mode=ParseMode.MARKDOWN)
    context.user_data['reqstep'] = 1

async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await start_commands()
    await update.message.reply_text(text="قوانین به شرح ذیل است:\n\n")
    
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await start_commands()
    description = (
        "📢 **خوش آمدید!**\n\n"
        "برای ثبت درخواست عضویت در کانال 👇 \n\n"
        "/joinrequest\n\n"
        "همچنین از طریق دکمه منو میتوانید گزینه های دیگر را بررسی نمایید\n"

    )
    photo_path = "img/start-bot.png"
    if update.message:
        await context.bot.send_photo(
            chat_id=update.message.chat_id,
            photo=open(photo_path, "rb"),
            caption=description,
            parse_mode="Markdown",
        )
