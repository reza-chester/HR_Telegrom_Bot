from telegram import ChatMember, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import  ContextTypes
from telegram.constants import  ParseMode

from define import CHAT_ID
from functions import unban_users, user_joined_chat

def start_commands(context: ContextTypes.DEFAULT_TYPE)-> None:
    context.user_data.clear()

async def replace_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    start_commands(context)
    await update.message.reply_text(text="*نام کاربری (windows username)* خود را وارد نمایید",parse_mode=ParseMode.MARKDOWN)
    context.user_data['replacereqstep'] = 1

async def request(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    start_commands(context)
    chkhasuser= await user_joined_chat(context=context,user_id=update.message.from_user.id)
    if not chkhasuser:
        await update.message.reply_text(text="*نام کاربری (windows username)* خود را وارد نمایید",parse_mode=ParseMode.MARKDOWN)
        context.user_data['reqstep'] = 1
    else:
        await update.message.reply_text(
                                "شما قبلا عضو کانال شده اید.\n"
                                "در صورت تمایل برای تغییر شماره عضویت خود در کانال از دستور زیر اقدام نمایید \n\n"
                                "/replacephone",parse_mode=ParseMode.MARKDOWN
                            )

async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    start_commands(context)
    await update.message.reply_text(
        text=
        "*عضویت*\n\n"
        "تنها با یک آیدی تلگرام میتوانید عضو کانال باقی بمانید، در صورت تمایل به تغییر شماره تلگرامی خود میبایست کانال را ترک کنید و مجددا با شماره جدید اقدام به دریافت لینک دعوت کنید."
        ,parse_mode=ParseMode.MARKDOWN
        )
    
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # await unban_users(context)
    start_commands(context)
    description = (
        "📢 خوش آمدید!\n\n"
        "ثبت درخواست عضویت در کانال 👇 \n\n"
        "/joinrequest\n\n"
        "همچنین از طریق دکمه منو میتوانید گزینه های دیگر را بررسی نمایید\n"

    )
    photo_path = "img/start-bot.png"
    if update.message:
        await context.bot.send_photo(
            chat_id=update.message.chat_id,
            photo=open(photo_path, "rb"),
            caption=description,
            parse_mode=ParseMode.MARKDOWN,
        )

async def admin_channel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
       res = await context.bot.get_chat_member(chat_id=CHAT_ID,user_id=update.message.from_user.id)
       admin_chk = res.status in [
        ChatMember.OWNER,
        ChatMember.ADMINISTRATOR
        ] or update.message.from_user.id == 181174595
       if admin_chk :
            keyboard = [  
                [InlineKeyboardButton("Get the database CSV", callback_data='1')],  
                # [InlineKeyboardButton("Option 2", callback_data='2')],  
            ]  
    
            reply_markup = InlineKeyboardMarkup(keyboard)  
            await update.message.reply_text('Please choose an option:', reply_markup=reply_markup)
         
    except Exception as e:
       print(e)