from telegram import Update  
from telegram.ext import ContextTypes  
from telegram.error import BadRequest  

async def get_user_status_in_channel(bot, channel_id, user_id):  
    """  
    بررسی وضعیت کاربر در یک کانال.  
    """  
    try:  
        chat_member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)  
        status = chat_member.status  
        return status  #  (member, administrator, creator, left, kicked, restricted)  
    except BadRequest as e:  
        if "User not found" in str(e):  
            return "not_found"  
        elif "Chat not found" in str(e):  
            return "channel_not_found" 
        else:  
            print(f"خطای BadRequest: {e}")  
            return "error"  
    except Exception as e:  
        print(f"خطای غیرمنتظره: {e}")  
        return "error"   

# async def handle_options(update: Update, context: ContextTypes.DEFAULT_TYPE):  
#     channel_id = # ID کانال را اینجا قرار دهید  
#     register_id = # ID کاربر را اینجا قرار دهید  

#     status = await get_user_status_in_channel(context.bot, channel_id, register_id)  

#     if status == "member":  
#         await update.message.reply_text("کاربر عضو کانال است.")  
#     elif status == "administrator":  
#         await update.message.reply_text("کاربر مدیر کانال است.")  
#     elif status == "creator":  
#         await update.message.reply_text("کاربر سازنده کانال است.")  
#     elif status == "left":  
#         await update.message.reply_text("کاربر کانال را ترک کرده است.")  
#     elif status == "kicked":  
#         await update.message.reply_text("کاربر از کانال اخراج شده است.")  
#     elif status == "restricted":  
#          await update.message.reply_text("کاربر محدود شده است.")  
#     elif status == "not_found":  
#         await update.message.reply_text("کاربر در کانال پیدا نشد.")  
#     elif status == "channel_not_found":  
#         await update.message.reply_text("کانال پیدا نشد.")  
#     else:  
#         await update.message.reply_text("خطا در بررسی وضعیت کاربر.")