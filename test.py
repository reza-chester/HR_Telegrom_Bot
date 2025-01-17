import sqlite3
DB_NAME = "bot_data.db"


conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()
cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (  
    emporusername TEXT PRIMARY KEY UNIQUE,  
    phone TEXT,  
    code TEXT,  
    id INT,
    joined BIT,  
    dateCreated DATETIME  
) 
    """)
conn.commit()
conn.close()



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    # keyboard = [
    #     [InlineKeyboardButton("📥 دانلود ویدیو", callback_data="download_video")],
    #     [InlineKeyboardButton("ℹ️ درباره ما", url="https://example.com")],
    # ]
    # reply_markup = InlineKeyboardMarkup(keyboard)

    description = (
        "📢 **خوش آمدید!**\n\n"
        "به ربات ما خوش آمدید! از طریق دکمه منو درخواست های خود را بررسی نمایید.\n"
    )
    photo_path = "img/start-bot.png"
    if update.message:
        await context.bot.send_photo(
            chat_id=update.message.chat_id,
            photo=open(photo_path, "rb"),
            caption=description,
            parse_mode="Markdown",
        )

# async def check_group_members(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     try:
        
#         async for member in context.bot.get_chat_members(CHAT_ID):  
#         chat_members = await context.bot.get_chat_administrators(chat_id=CHAT_ID)
#         unauthorized_users = []
#         now = datetime.datetime.now()
#         until_date = now + datetime.timedelta(days=1,hours=-1)  
#         until_timestamp = int(until_date.timestamp())
#         for member in chat_members:
#             print(member.user.first_name)
#             print(member.user.last_name)
#             print(member.user.id)
#             if member.status not in ["administrator", "creator"]:
#                 user_id = member.user.id
#                 # if user_id not in AUTHORIZED_USERS:
#                 unauthorized_users.append(user_id)
#                 print(member.user.first_name)
#                 print(member.user.last_name)
#                 print(member.user.id)
#                 await context.bot.ban_chat_member(chat_id=CHAT_ID, user_id=user_id, until_date=until_timestamp)
#                     # await context.bot.unban_chat_member(chat_id=CHAT_ID, user_id=user_id) 
#                 print(f"User {user_id} has been removed.")

#         if unauthorized_users:
#             await update.message.reply_text(f"{len(unauthorized_users)} کاربران غیرمجاز حذف شدند.")
#         else:
#             await update.message.reply_text("همه کاربران مجاز هستند.")
#     except Exception as e:
#         print(f"Error: {e}")
#         await update.message.reply_text("خطایی رخ داد.")

            # await update.effective_chat.send_message(
            #     f"{member_name} was added by {cause_name}. Welcome!",
            #     parse_mode=ParseMode.HTML,
            # )
    
    # await update.effective_chat.send_message(
        #     f"{member_name} is no longer with us. Thanks a lot, {cause_name} ...",
        #     parse_mode=ParseMode.HTML,
        # )