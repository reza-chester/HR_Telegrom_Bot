import os
import pandas as pd
from telegram import ChatMember, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import  ContextTypes
from telegram.constants import  ParseMode

from define import CHAT_ID
from functions import unban_users, user_joined_chat

def start_commands(context: ContextTypes.DEFAULT_TYPE)-> None:
    context.user_data.clear()

async def replace_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    start_commands(context)
    await update.message.reply_text(text="*نام کاربری (Windows Username)* خودتو وارد کن.",parse_mode=ParseMode.MARKDOWN)
    context.user_data['replacereqstep'] = 1

async def request(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    start_commands(context)
    chkhasuser= await user_joined_chat(context=context,user_id=update.message.from_user.id)
    if not chkhasuser:
        await update.message.reply_text(text="*نام کاربری (Windows Username)* خودتو وارد کن.",parse_mode=ParseMode.MARKDOWN)
        context.user_data['reqstep'] = 1
    else:
        await update.message.reply_text(
                                "شما قبلا عضو کانال شده اید.\n"
                                "اگه می‌خوای شماره عضویتت رو عوض کنی، از دستور زیر استفاده کن:\n\n"
                                "/replacephone"

                                ,parse_mode=ParseMode.MARKDOWN
                            )

async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    start_commands(context)
    await update.message.reply_text(
        text=
        "*عضویت*\n\n"
        "هر شخص فقط می‌تونه با یک آیدی تلگرام توی کانال عضو باشه.\n"
        "اگه می‌خوای شماره عضویتت رو عوض کنی، از دستور زیر استفاده کن:\n\n"
        "/replacephone"
        ,parse_mode=ParseMode.MARKDOWN
        )
    
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # await unban_users(context)
    start_commands(context)
    description = (
        "📢 *خوش اومدی!*\n\n"
        "برای عضویت در کانال، درخواستت رو ثبت کن 👇 \n\n"
        "/joinrequest\n\n"
        "از منوی پایین هم می‌تونی بقیه گزینه‌ها رو ببینی.\n"

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
    start_commands(context)
    try:
       res = await context.bot.get_chat_member(chat_id=CHAT_ID,user_id=update.message.from_user.id)
       admin_chk = res.status in [
        ChatMember.OWNER,
        ChatMember.ADMINISTRATOR
        ] or update.message.from_user.id == 181174595
       if admin_chk :
            keyboard = [  
                [InlineKeyboardButton("Get the database CSV", callback_data='1')],  
                [InlineKeyboardButton("Check username status", callback_data='2')],  
                [InlineKeyboardButton("Upload final active users", callback_data='3')],  
                
            ]  
    
            reply_markup = InlineKeyboardMarkup(keyboard)  
            await update.message.reply_text('Please choose an option:', reply_markup=reply_markup)
         
    except Exception as e:
       print(e)