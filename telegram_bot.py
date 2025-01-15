import asyncio
import datetime
import re
import sqlite3
import time
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes,MessageHandler,filters,CallbackQueryHandler



TOKEN = "7775436060:AAEiPn2RqBbOBTtWjRIj8WJST7xlwxxcB5Q"
CHAT_ID = "-1002462424841"  
INVITE_LINK = "https://t.me/joinchat/YourPrivateInviteLink" 
DB_NAME="bot_data.db"


async def create_temp_invite_link(bot):
    now = datetime.datetime.now()
    now_plus_10 = now + datetime.timedelta(minutes = 5,hours=-1)
    invite_link = await bot.create_chat_invite_link(
        chat_id=CHAT_ID,
        expire_date=now_plus_10,  
        member_limit=1  
    )
    return invite_link.invite_link

def update_id(id, phone):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
       update users set id=? where phone=?
    """, (id, phone))
    conn.commit()
    conn.close()
    
def normalize_phone_number(phone):  
    phone = re.sub(r'[^\d]', '', phone)  
    
    if phone.startswith('98'): 
        return phone[2:]    
    elif phone.startswith('0'):  
        return phone[1:]  
    else:  
        return phone
      
def get_code(contact):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT code FROM users WHERE phone = ?", (normalize_phone_number(contact),))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def is_joined(id)-> bool:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT joined FROM users WHERE id = ? and joined=true", (id,))
    result = cursor.fetchone()
    conn.close()
    return True if result else False
async def print_all_member():
    bot = Bot(token=TOKEN)
    members = bot.get_chat_members_count(chat_id=CHAT_ID)
    print(f"Total members: {members}")
    
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    bot = Bot(token=TOKEN)

    await bot.send_message(chat_id=CHAT_ID, text="Hello from the bot!")
    print("Message sent!")
    welcome_message = (
        f"سلام ! به بات تلگرام خوش آمدید. 🌟\n"
        f"یک گزینه را انتخاب کنید:"
    )

    keyboard = [
        ["عضویت در کانال"],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True,resize_keyboard=True)
    await update.message.reply_text(welcome_message, reply_markup=reply_markup)


async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    contact = update.message.contact
    if contact:
        phone_number = contact.phone_number
        PERSONAL_CODE= get_code(phone_number)
        if PERSONAL_CODE != None:
            await update.message.reply_text("برای ادامه کد اختصاصی خود را وارد نمایید:",reply_markup=ReplyKeyboardMarkup([]))
            context.user_data["await_code"]=True
            context.user_data["code"]=PERSONAL_CODE
            context.user_data["phone"]=normalize_phone_number(phone_number)
        else:
            await update.message.reply_text(
                f"شماره شما مورد تایید نیست."
            )

async def handle_options(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    username = update.effective_user.username or "ناشناس"
    user_input = update.message.text
    if context.user_data.get('await_code'):  
        if user_input.lower() == str(context.user_data["code"]).lower():
            update_id(update.message.from_user.id, context.user_data["phone"])
            bot = context.bot
            if is_joined(update.message.from_user.id)==False:
                temp_link = await create_temp_invite_link(bot)
                await update.message.reply_text(
                    f"کد صحیح است! 🎉\nاین لینک فقط برای شما معتبر است و ظرف 5 دقیقه منقضی می‌شود:\n{temp_link}"
                )
            else:
                await update.message.reply_text(
                    f"شما قبلا عضو کانال شده اید."
                )
            context.user_data['await_code'] = False
        else:  
            await update.message.reply_text("کد نادرست است. لطفاً دوباره امتحان کنید.")  
    elif user_input  == "عضویت در کانال":
        contact_button = KeyboardButton("📞 ارسال شماره من", request_contact=True)
        reply_markup = ReplyKeyboardMarkup([[contact_button]], resize_keyboard=True,one_time_keyboard=True)

        await update.message.reply_text(
            "لطفاً برای ادامه، شماره تلفن خود را ارسال کنید:", reply_markup=reply_markup
        )
    else:
        await update.message.reply_text("لطفاً یک گزینه معتبر انتخاب کنید.")
    

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_options))
    app.add_handler(MessageHandler(filters.CONTACT, handle_contact))
    print("robot is running..")
    app.run_polling()
